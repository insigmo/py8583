
import binascii
import logging
import unittest

from py8583 import py8583
from py8583 import py8583spec

logging.basicConfig(level=logging.DEBUG)

data = (b"F0F1F0F0723C440188E18008F1F6F5F5F3F1F5F75C5C5C5C5CF1F6F5F5F4F0F0F0F0F0F0F0F0F0F0F0F0F0F0F2F5F0F0F0F8F3F0F0F9"
        b"F0F6F1F5F2F2F4F4F0F0F1F2F0F6F1F4F0F8F3F0F2F2F1F2F4F1F1F1F0F1F2F0F6F0F0F5F0F3F7F0F6F2F0F0F1F5F4F1F2F4F2F1F2F4"
        b"F4F8F0F1F6F2F0F1F5F6F0F6F7F1F0F1F0F0F0F0F1F5F6F4F6404040E3E2E340D7C1D9D2C94040404040404040404040404040C28191"
        b"929695A499404040404040D9E4E2F0F1F8E7F6F1F0F5F0F0F0F0F1F6F4F0F4F0F7F0F0F6F4F3F0F2F2F2F0F3F1F0F0F0F0F0F0F6F0F0"
        b"F6F4F3F4F6F8F3F2")


class AsciiParse1987(unittest.TestCase):

    def setUp(self):
        self.IsoPacket = py8583.Iso8583(data[2:], iso_spec=py8583spec.IsoSpec1987ASCII())
        self.IsoPacket.strict = True

    def tearDown(self):
        pass

    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0, 9):
                    for b4 in range(0, 5):
                        mti = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.set_iso_content((mti + "0000000000000000").encode('latin'))
                        self.assertEqual(self.IsoPacket.mti(), mti)

        # negative test
        with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
            self.IsoPacket.set_iso_content("000A".encode('latin'))

        with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
            self.IsoPacket.set_iso_content("0000".encode('latin'))

        for b4 in range(6, 9):
            with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
                mti = "010" + str(b4)
                self.IsoPacket.set_iso_content(mti.encode('latin'))

    def test_Bitmap(self):

        # primary bitmap
        for shift in range(0, 63):
            bitmap = '{:0>16X}'.format(1 << shift)
            content = '0200' + bitmap + ''.zfill(256)

            self.IsoPacket.set_iso_content(content.encode('latin'))
            self.assertEqual(self.IsoPacket.bitmap()[64 - shift], 1)
            self.assertEqual(self.IsoPacket.field(64 - shift), 1)

        # secondary bitmap
        for shift in range(0, 64):
            bitmap = '8{:0>31X}'.format(1 << shift)
            content = '0200' + bitmap + ''.zfill(256)

            self.IsoPacket.set_iso_content(content.encode('latin'))
            self.assertEqual(self.IsoPacket.bitmap()[128 - shift], 1)
            self.assertEqual(self.IsoPacket.field(128 - shift), 1)


class BCDParse1987(unittest.TestCase):

    def setUp(self):
        self.IsoPacket = py8583.Iso8583(iso_spec=py8583spec.IsoSpec1987BCD())
        self.IsoPacket.strict(True)

    def tearDown(self):
        pass

    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0, 9):
                    for b4 in range(0, 5):
                        mti = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.set_iso_content(binascii.unhexlify(mti + "0000000000000000"))
                        self.assertEqual(self.IsoPacket.mti(), mti)

        # negative test
        with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
            self.IsoPacket.set_iso_content(binascii.unhexlify("000A"))

        with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
            self.IsoPacket.set_iso_content(binascii.unhexlify("0000"))

        for b4 in range(6, 9):
            with self.assertRaisesRegex(py8583.ParseError, "Invalid mti"):
                mti = binascii.unhexlify("010" + str(b4))
                self.IsoPacket.set_iso_content(mti)

    def test_Bitmap(self):
        pass


if __name__ == '__main__':
    unittest.main()
