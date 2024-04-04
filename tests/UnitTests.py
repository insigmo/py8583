import os
import time
import sys
import binascii
import unittest

sys.path.insert(0, os.path.abspath('..'))

from py8583 import *



class AsciiParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = py8583.Iso8583(IsoSpec = py8583spec.IsoSpec1987ASCII())
        self.IsoPacket.strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
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
            content = '0200' +  bitmap + ''.zfill(256)

            self.IsoPacket.set_iso_content(content.encode('latin'))
            self.assertEqual(self.IsoPacket.bitmap()[64 - shift], 1)
            self.assertEqual(self.IsoPacket.field(64 - shift), 1)
            
        # secondary bitmap
        for shift in range(0, 64):
            bitmap = '8{:0>31X}'.format(1 << shift)
            content = '0200' +  bitmap + ''.zfill(256)
            
            self.IsoPacket.set_iso_content(content.encode('latin'))
            self.assertEqual(self.IsoPacket.bitmap()[128 - shift], 1)
            self.assertEqual(self.IsoPacket.field(128 - shift), 1)
                
class BCDParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = py8583.Iso8583(IsoSpec = py8583spec.IsoSpec1987BCD())
        self.IsoPacket.strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
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
