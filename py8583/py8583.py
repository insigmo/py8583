import binascii
import struct
import logging

from py8583.enums import DT, LT, MsgVersion, MsgClass, MsgFunction, MsgOrigin
from py8583.errors import ParseError, SpecError, BuildError
from py8583.py8583spec import IsoSpec1987ASCII


log = logging.getLogger('py8583')
secondary, primary, length = None, None, None


def mem_dump(Title, data, size=16):
    from string import printable as PrintableString
    printable = bytes(PrintableString, 'ascii').replace(b'\r', b'').replace(b'\n', b'') \
        .replace(b'\t', b'').replace(b'\x0b', b'') \
        .replace(b'\x0c', b'')

    if not isinstance(data, bytes):
        raise TypeError("Expected bytes for data")

    log.info("{} [{}]:".format(Title, len(data)))
    dump = "\n"

    for line in [data[i:i + size] for i in range(0, len(data), size)]:

        for c in line:
            dump += "{:02x} ".format(c)

        dump += "   " * (size - len(line))

        dump += ' | '
        for c in line:
            if c in printable:
                dump += "{:1c}".format(c)
            else:
                dump += '.'

        dump += "\n"

    log.info(dump)


def bcd_to_str(bcd):
    return binascii.hexlify(bcd).decode('latin')


def str_to_bcd(string):
    if len(string) % 2 == 1:
        string = string.zfill(len(string) + 1)
    return binascii.unhexlify(string)


def bcd_to_int(bcd):
    return int(bcd_to_str(bcd))


def int_to_bcd(integer):
    string = str(integer)
    if len(string) % 2 == 1:
        string = string.zfill(len(string) + 1)

    return binascii.unhexlify(string)


class Iso8583:
    ValidContentTypes = ('a', 'n', 's', 'an', 'as', 'ns', 'ans', 'b', 'z')

    def __init__(self, IsoMsg=None, IsoSpec=None):

        self._mti = None
        self.strict = False

        self._bitmap = {}
        self._field_data = {}
        self._iso = b''
        self._iso_spec = None

        if IsoSpec is not None:
            self._iso_spec = IsoSpec
        else:
            self._iso_spec = IsoSpec1987ASCII()

        if IsoMsg is not None:
            if not isinstance(IsoMsg, bytes):
                raise TypeError("Expected bytes for iso message")

            self._iso = IsoMsg
            self.parse_iso()

    def strict(self, Value):
        if Value is not True and Value is not False:
            raise ValueError
        self.strict = Value

    def set_iso_content(self, IsoMsg):
        if not isinstance(IsoMsg, bytes):
            raise TypeError("Expected bytes for iso message")
        self._iso = IsoMsg
        self.parse_iso()

    def parse_mti(self, p):
        data_type = self._iso_spec.data_type('mti')

        if data_type == DT.BCD:
            self._mti = bcd_to_str(self._iso[p:p + 2])
            p += 2
        elif data_type == DT.ASCII:
            self._mti = self._iso[p:p + 4].decode('latin')
            p += 4

        try:  # mti should only contain numbers
            int(self._mti, 16)
        except Exception:
            raise ParseError("Invalid mti: [{0}]".format(self._mti))

        if self.strict:
            if self._mti[1] == '0':
                raise ParseError("Invalid mti: Invalid Message type [{0}]".format(self._mti))

            if int(self._mti[3]) > 5:
                raise ParseError("Invalid mti: Invalid Message origin [{0}]".format(self._mti))

        return p

    def parse_bitmap(self, p):
        global secondary, primary
        data_type = self._iso_spec.data_type(1)

        if data_type == DT.BIN:
            primary = self._iso[p:p + 8]
            p += 8
        elif data_type == DT.ASCII:
            primary = binascii.unhexlify(self._iso[p:p + 16])
            p += 16

        int_primary = struct.unpack_from("!Q", primary)[0]

        for i in range(1, 65):
            self._bitmap[i] = (int_primary >> (64 - i)) & 0x1

        if self._bitmap[1] == 1:
            if data_type == DT.BIN:
                secondary = self._iso[p:p + 8]
                p += 8
            elif data_type == DT.ASCII:
                secondary = binascii.unhexlify(self._iso[p:p + 16])
                p += 16

            int_secondary = struct.unpack_from("!Q", secondary)[0]

            for i in range(1, 65):
                self._bitmap[i + 64] = (int_secondary >> (64 - i)) & 0x1

        return p

    def parse_field(self, field, p):

        global length
        try:
            data_type = self._iso_spec.data_type(field)
            len_type = self._iso_spec.length_type(field)
            content_type = self._iso_spec.content_type(field)
            max_length = self._iso_spec.max_length(field)
        except Exception:
            raise SpecError("Cannot parse F{0}: Incomplete field specification".format(field))

        try:
            if data_type == DT.ASCII and content_type == 'b':
                max_length *= 2

            if len_type == LT.FIXED:
                length = max_length
            elif len_type == LT.LVAR:
                pass
            elif len_type == LT.LLVAR:
                length_data_type = self._iso_spec.length_data_type(field)
                if length_data_type == DT.ASCII:
                    length = int(self._iso[p:p + 2])
                    p += 2
                elif length_data_type == DT.BCD:
                    length = bcd_to_int(self._iso[p:p + 1])
                    p += 1
                else:
                    raise ParseError('Unsupported length data type')
            elif len_type == LT.LLLVAR:
                length_data_type = self._iso_spec.length_data_type(field)
                if length_data_type == DT.ASCII:
                    length = int(self._iso[p:p + 3])
                    p += 3
                elif length_data_type == DT.BCD:
                    length = bcd_to_int(self._iso[p:p + 2])
                    p += 2
                else:
                    raise ParseError('Unsupported length data type')
        except ValueError as ex:
            raise ParseError("Cannot parse F{0} - Invalid length: {1}".format(field, ex))

        if length > max_length:
            raise ParseError("F{0} is larger than maximum length ({1}>{2})".format(field, length, max_length))

        # In case of zero length, don't try to parse the field itself, just continue
        if length == 0:
            if content_type == 'n':
                self._field_data[field] = None
            else:
                self._field_data[field] = ''
            return p

        try:
            if data_type == DT.ASCII:
                if content_type == 'n':
                    self._field_data[field] = int(self._iso[p:p + length])
                else:
                    self._field_data[field] = self._iso[p:p + length].decode('latin')
                p += length
            elif data_type == DT.BCD:
                if length % 2 == 1:
                    length += 1
                if content_type == 'n':
                    self._field_data[field] = bcd_to_int(self._iso[p:p + (length // 2)])
                elif content_type == 'z':
                    self._field_data[field] = binascii.hexlify(self._iso[p:p + (length // 2)]).decode('latin').upper()
                p += length // 2
            elif data_type == DT.BIN:
                self._field_data[field] = binascii.hexlify(self._iso[p:p + length]).decode('latin').upper()
                p += length
        except Exception as ex:
            raise ParseError("Cannot parse F{}: {}".format(field, str(ex))) from None

        if content_type == 'z':
            self._field_data[field] = self._field_data[field].replace("D", "=")  # in track2, replace d with =
            self._field_data[field] = self._field_data[field].replace("F", "")  # in track2, remove trailing f

        return p

    def parse_iso(self):
        p = 0
        p = self.parse_mti(p)
        p = self.parse_bitmap(p)

        for field in sorted(self._bitmap):
            # field 1 is parsed by the bitmap function
            if field != 1 and self.field(field) == 1:
                p = self.parse_field(field, p)

    def build_mti(self):
        if self._iso_spec.data_type('mti') == DT.BCD:
            self._iso += str_to_bcd(self._mti)
        elif self._iso_spec.data_type('mti') == DT.ASCII:
            self._iso += self._mti.encode('latin')

    def build_bitmap(self):
        data_type = self._iso_spec.data_type(1)

        # check if we need a secondary bitmap
        for i in self._bitmap.keys():
            if i > 64:
                self._bitmap[1] = 1
                break

        int_primary = 0
        for i in range(1, 65):
            if i in self._bitmap.keys():
                int_primary |= (self._bitmap[i] & 0x1) << (64 - i)
        global primary, secondary
        primary = struct.pack("!Q", int_primary)

        if data_type == DT.BIN:
            self._iso += primary
        elif data_type == DT.ASCII:
            self._iso += binascii.hexlify(primary).upper()

        # Add secondary bitmap if applicable
        if 1 in self._bitmap.keys() and self._bitmap[1] == 1:

            int_secondary = 0
            for i in range(65, 129):
                if i in self._bitmap.keys():
                    int_secondary |= (self._bitmap[i] & 0x1) << (128 - i)

            secondary = struct.pack("!Q", int_secondary)

            if data_type == DT.BIN:
                self._iso += secondary
            elif data_type == DT.ASCII:
                self._iso += binascii.hexlify(secondary)

    def build_field(self, field):
        try:
            data_type = self._iso_spec.data_type(field)
            len_type = self._iso_spec.length_type(field)
            content_type = self._iso_spec.content_type(field)
            max_length = self._iso_spec.max_length(field)
        except Exception:
            raise SpecError("Cannot parse F{0}: Incomplete field specification".format(field))

        global length
        if len_type == LT.FIXED:
            length = max_length

            if content_type == 'n':
                formatter = "{{0:0{0}d}}".format(length)
            elif 'a' in content_type or 'n' in content_type or 's' in content_type:
                formatter = "{{0: >{0}}}".format(length)
            else:
                formatter = "{0}"

            data = formatter.format(self._field_data[field])

        else:
            length_data_type = self._iso_spec.length_data_type(field)

            data = "{0}".format(self._field_data[field])

            if content_type == 'z' and data_type == DT.BIN:
                if len(data) % 2 == 1:
                    data = data + 'F'

                data = data.replace("=", "D")

            length = len(data)
            if data_type == DT.BIN:
                length //= 2

            if length > max_length:
                raise BuildError("Cannot Build F{0}: field Length larger than specification".format(field))
            length_data = ''
            if len_type == LT.LVAR:
                length_data = "{0:01d}".format(length)

            elif len_type == LT.LLVAR:
                length_data = "{0:02d}".format(length)

            elif len_type == LT.LLLVAR:
                length_data = "{0:03d}".format(length)

            if length_data_type == DT.ASCII:
                self._iso += length_data.encode('latin')
            elif length_data_type == DT.BCD:
                self._iso += str_to_bcd(length_data)
            elif length_data_type == DT.BIN:
                self._iso += binascii.unhexlify(length_data)

        if data_type == DT.ASCII:
            self._iso += data.encode('latin')
        elif data_type == DT.BCD:
            self._iso += str_to_bcd(data)
        elif data_type == DT.BIN:
            self._iso += binascii.unhexlify(self._field_data[field])

    def build_iso(self):
        self._iso = b''
        self.build_mti()
        self.build_bitmap()

        for field in sorted(self._bitmap):
            if field != 1 and self.field(field) == 1:
                try:
                    self.build_field(field)
                except Exception as ex:
                    raise type(ex)('Error building F{}: '.format(field) + repr(ex)) from None

        return self._iso

    def field(self, field, Value=None):
        if Value is None:
            try:
                return self._bitmap[field]
            except KeyError:
                return None
        elif Value in (1, 0):
            self._bitmap[field] = Value
        else:
            raise ValueError

    def field_data(self, field, Value=None):
        if Value is None:
            try:
                return self._field_data[field]
            except KeyError:
                return None
        else:
            if len(str(Value)) > self._iso_spec.max_length(field):
                raise ValueError('Value length larger than field maximum ({0})'.format(self._iso_spec.max_length(field))
                                 )

            self._field_data[field] = Value

    def fields(self):
        return self._field_data

    def bitmap(self):
        return self._bitmap

    def mti(self, mti=None):
        if mti is None:
            return self._mti
        else:
            mti = mti.zfill(4)

            if int(mti[0]) not in list(map(int, MsgVersion)):
                raise ValueError("Invalid mti [{0}]: Invalid message version".format(mti))

            if int(mti[1]) not in list(map(int, MsgClass)):
                raise ValueError("Invalid mti [{0}]: Invalid message class".format(mti))

            if int(mti[2]) not in list(map(int, MsgFunction)):
                raise ValueError("Invalid mti [{0}]: Invalid message class".format(mti))

            if int(mti[3]) not in list(map(int, MsgOrigin)):
                raise ValueError("Invalid mti [{0}]: Invalid message class".format(mti))

            self._mti = mti

    def version(self):
        for i in MsgVersion:
            if int(self._mti[0]) == i.value:
                return i

    def msg_class(self):
        for i in MsgClass:
            if int(self._mti[1]) == i.value:
                return i

    def function(self):
        for i in MsgFunction:
            if int(self._mti[2]) == i.value:
                return i

    def origin(self):
        for i in MsgOrigin:
            if int(self._mti[3]) == i.value:
                return i

    def description(self, field, description=None):
        return self._iso_spec.description(field, description)

    def data_type(self, field, data_type=None):
        return self._iso_spec.data_type(field, data_type)

    def content_type(self, field, content_type=None):
        return self._iso_spec.content_type(field, content_type)

    # Due to legacy...
    def print_message(self, level=logging.DEBUG):
        self.debug_message(level)

    def debug_message(self, level=logging.DEBUG):
        log.log(level, "mti:    [{0}]".format(self._mti))

        bitmap_line = "fields: [ "
        for i in sorted(self._bitmap.keys()):
            if i == 1:
                continue
            if self._bitmap[i] == 1:
                bitmap_line += str(i) + " "
        bitmap_line += "]"
        log.log(level, bitmap_line)

        for i in sorted(self._bitmap.keys()):
            if i == 1:
                continue
            if self._bitmap[i] == 1:

                try:
                    field_data = self._field_data[i]
                except KeyError:
                    field_data = ''

                if self.content_type(i) == 'n' and self._iso_spec.length_type(i) == LT.FIXED:
                    field_data = str(field_data).zfill(self._iso_spec.max_length(i))

                log.log(level, "\t{0:>3d} - {1: <41} : [{2}]".format(i, self._iso_spec.description(i), field_data))
