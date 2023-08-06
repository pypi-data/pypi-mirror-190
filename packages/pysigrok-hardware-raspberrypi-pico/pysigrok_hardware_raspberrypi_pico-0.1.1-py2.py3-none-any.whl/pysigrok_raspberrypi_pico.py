"""PySigrok driver for rp2040 logic capture"""

__version__ = "0.1.1"

import serial

from sigrokdecode import SR_KHZ, SR_MHZ, cond_matches

class PicoDriver:
    name = "raspberrypi-pico"
    longname = "RaspberryPI PICO"

    samplerates = [
        SR_KHZ(5),
        SR_KHZ(6),
        SR_KHZ(8),
        SR_KHZ(10),
        SR_KHZ(20),
        SR_KHZ(30),
        SR_KHZ(40),
        SR_KHZ(50),
        SR_KHZ(60),
        SR_KHZ(80),
        SR_KHZ(100),
        SR_KHZ(125),
        SR_KHZ(150),
        SR_KHZ(160), # max rate of 3 ADC channels that has integer divisor/dividend
        SR_KHZ(200),
        SR_KHZ(250), # max rate of 2 ADC channels
        SR_KHZ(300),
        SR_KHZ(400),
        SR_KHZ(500),
        SR_KHZ(600),
        SR_KHZ(800),
        # Give finer granularity near the thresholds of RLE effectiveness ~1-4Msps
        # Also use 1.2 and 2.4 as likely max values for ADC overclocking
        SR_MHZ(1),
        SR_MHZ(1.2),
        SR_MHZ(1.5),
        SR_MHZ(2),
        SR_MHZ(2.4),
        SR_MHZ(3),
        SR_MHZ(4),
        SR_MHZ(5),
        SR_MHZ(6),
        SR_MHZ(8),
        SR_MHZ(10),
        SR_MHZ(15),
        SR_MHZ(20),
        SR_MHZ(30),
        SR_MHZ(40),
        SR_MHZ(60),
        # The baseline 120Mhz PICO clock won't support an 80 or 100
        # with non fractional divisor, but an overclocked version or one
        # that modified sysclk could
        SR_MHZ(80),
        SR_MHZ(100),
        SR_MHZ(120),
        # These may not be practically useful, but someone might want to
        # try to make it work with overclocking
        SR_MHZ(150),
        SR_MHZ(200),
        SR_MHZ(240)
    ]

    def __init__(self, channellist=None, conn="", samplerate="5000"):
        self.serial = serial.Serial(conn)
        self._samplerate = int(samplerate)
        self.data = []

        self.serial.reset_input_buffer()
        self.serial.write(b"*")
        self.serial.reset_input_buffer()

        self.serial.write(b"i\n")
        info = self.serial.read(17)
        if not info.startswith(b"SRPICO,A"):
            raise RuntimeError()
        _, channelinfo, self.version = info.split(b",")
        self.version = int(self.version)

        if self.version >= 3:
            # For the future. In 3, it's empty.
            remaining_info = self.serial.readline()
            self.serial.write(b"b\n")
            board_name = self.serial.readline()
            pin_names = self.serial.readline()
        else:
            board_name = "Pico"
            pin_names = ""

        self.pin_names = pin_names.decode("utf-8").strip().split(",")
        if len(self.pin_names) != 30:
            raise RuntimeError("Board doesn't name all 30 pins")

        self.num_a_channels = int(channelinfo[1:3])
        self.analog_bytes = int(channelinfo[3:4])
        self.num_d_channels = int(channelinfo[-2:])
        # print(self.num_a_channels, self.analog_bytes, self.num_d_channels)

        if channellist is None:
            self.enabled_channels = [z for z in self.pin_names if z]
        else:
            self.enabled_channels = channellist.split(",")
            for channel in self.enabled_channels:
                if channel not in self.pin_names:
                    raise ValueError(f"Unknown pin: {channel}")

        self.last_sample = None
        self.next_sample = None
        self.samplenum = 0
        self.rle_remaining = 0
        self.data_index = 0
        self.chunk_index = 0
        self.overall_index = 0
        self.analog_values = []

    def __del__(self):
        self.serial.close()

    @property
    def samplerate(self):
        return self._samplerate

    @samplerate.setter
    def samplerate(self, value):
        if value not in self.samplerates:
            raise ValueError()
        self._samplerate = value

    def send_w_ack(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.serial.write(data)
        response = self.serial.read(1)
        if response != b"*":
            raise RuntimeError()

    def acquire(self, sample_count):
        self.serial.reset_input_buffer()
        self.serial.write(b"*")
        self.serial.reset_input_buffer()

        self.analog_channel_count = 0
        self.analog_channels = []
        for i in range(4):
            pin_name = self.pin_names[26 + i]
            enabled = 1 if pin_name in self.enabled_channels else 0
            self.send_w_ack(f"A{enabled:d}{i:d}\n")
            self.analog_channel_count += enabled
            if enabled:
                self.analog_channels.append(pin_name)
        digital_enables = ["D"] * 26
        first_enabled = None
        for i in range(26):
            enabled = 1 if self.pin_names[i] in self.enabled_channels else 0
            if enabled == 1 and first_enabled is None:
                first_enabled = i
            self.send_w_ack(f"D{enabled:d}{i:d}\n")
            if enabled:
                digital_enables[i] = "E"
        # TODO: Remove this check. We're ok skipping channels, it'll just slow things down.
        digital_enables = "".join(digital_enables)
        digital_enables = digital_enables.strip("D")
        if "D" in digital_enables:
            raise RuntimeError("Digital pins must be continuous")

        self.logic_channel_count = len(digital_enables)
        self.logic_channels = self.pin_names[first_enabled:first_enabled+len(digital_enables)]

        self.send_w_ack(f"L{sample_count:d}\n")

        self.serial.write(f"R{self.samplerate:d}\n".encode("utf-8"))
        response = self.serial.read(1)
        if response == b"*":
            warning = self.serial.read(self.serial.in_waiting)
            if warning:
                print(warning)
        else:
            raise RuntimeError()

        self.serial.write(b"F\n")

        samples_read = 0
        last_value = 0
        byte_count = 0
        trailer = None
        while trailer is None:
            while self.serial.in_waiting == 0:
                pass
            data = self.serial.read(self.serial.in_waiting)
            if b"!" in data:
                self.serial.write(b"+")
                continue
            if b"$" in data:
                trailer = data
                break
            if trailer is None:
                self.data.append(data)
        if not trailer.startswith(b"$"):
            raise RuntimeError()
        while b"+" not in trailer:
            trailer += self.serial.read(self.serial.in_waiting)
        total_bytes = int(trailer[1:trailer.index(b"+")])
        if sum((len(x) for x in self.data)) != total_bytes:
            raise RuntimeError()

    def _next_byte(self):
        if self.data_index >= len(self.data):
            self.samplenum += self.rle_remaining
            raise EOFError()
        chunk = self.data[self.data_index]
        b = chunk[self.chunk_index]
        self.chunk_index += 1
        self.overall_index += 1
        if self.chunk_index >= len(chunk):
            self.chunk_index = 0
            self.data_index += 1
        return b


    def wait(self, conds=None):
        self.matched = [False]

        next_sample = None

        while not any(self.matched):
            # Check for a skip shorter than our RLE or a condition that still matches
            if self.rle_remaining > 0:
                self.matched = [False] * len(conds)
                for i, cond in enumerate(conds):
                    if cond_matches(cond, self.last_sample, self.last_sample):
                        self.matched[i] = True
                        sample = self.last_sample
                
                if any(self.matched):
                    self.rle_remaining -= 1
                else:
                    for i, cond in enumerate(conds):
                        if "skip" in cond and cond["skip"] <= self.rle_remaining:
                            self.matched[i] = True
                            self.rle_remaining -= cond["skip"]
                            self.samplenum += cond["skip"]
                            sample = self.last_sample
                            # Only one skip is possible
                            break

            if any(self.matched):
                break

            self.samplenum += self.rle_remaining
            self.rle_remaining = 0

            if self.next_sample is not None:
                sample = self.next_sample
                self.next_sample = None
            else:
                b = self._next_byte()
                # No RLE when analog is active.
                if self.analog_channel_count > 0:
                    sample = b & 0x7f
                    for _ in range(1, self.logic_channel_count // 7 + 1):
                        b = self._next_byte()
                        sample |= (b & 0x7f) << 7
                    # throw away analog in this function
                    values = []
                    for _ in range(self.analog_channel_count):
                        b = self._next_byte()
                        values.append((b & 0x7f) / 0x7f * 3.3)
                    self.analog_values.append(values)
                elif self.logic_channel_count <= 4:
                    # RLE byte
                    if b & 0x80 != 0:
                        sample = b & 0x0f
                        previous_length = (b >> 4) & 0x7
                        if previous_length > 0:
                            # We have more rle remaining and might match a skip.
                            self.rle_remaining = previous_length
                            self.next_sample = sample
                            sample = self.last_sample
                            continue
                    elif 0x30 <= b < 0x80:
                        previous_length = (b - 0x30 + 1) * 8
                        self.rle_remaining += previous_length
                        continue
                else:
                    # Start of a new sample
                    if b & 0x80 != 0:
                        sample = b & 0x7f
                        for i in range(self.logic_channel_count // 7):
                            b = self._next_byte()
                            if b & 0x80 == 0:
                                raise RuntimeError(f"Expected more sample {b:02x}")
                            sample |= (b & 0x7f) << (7 * (i + 1))
                    else:
                        # RLE byte
                        if 48 <= b <= 79:
                            self.rle_remaining += b - 47
                        elif 80 <= b <= 127:
                            self.rle_remaining += (b - 78) * 32
                        else:
                            raise RuntimeError(f"Unexpected byte value {b:02x}")
                        continue


            if self.last_sample is None:
                self.last_sample = sample
                break
            self.samplenum += 1
            self.matched = [True] * len(conds)
            for i, cond in enumerate(conds):
                if cond_matches(cond, self.last_sample, sample):
                    self.matched[i] = True
            self.last_sample = sample

        bits = []
        for b in range(len(self.logic_channels)):
            bits.append((sample >> b) & 0x1)

        return tuple(bits)

    def get_analog_values(self, samplenum):
        return self.analog_values[samplenum]
