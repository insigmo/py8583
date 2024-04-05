#!/usr/bin/env python
import logging
import struct

from py8583.py8583spec import IsoSpec1987ASCII

from py8583.py8583 import Iso8583, mem_dump


logging.basicConfig(level=logging.DEBUG)
data = (b"F0F1F0F0723C440188E18008F1F6F5F5F3F1F5F75C5C5C5C5CF1F6F5F5F4F0F0F0F0F0F0F0F0F0F0F0F0F0F0F2F5F0F0F0F8F3F0F0F9"
        b"F0F6F1F5F2F2F4F4F0F0F1F2F0F6F1F4F0F8F3F0F2F2F1F2F4F1F1F1F0F1F2F0F6F0F0F5F0F3F7F0F6F2F0F0F1F5F4F1F2F4F2F1F2F4"
        b"F4F8F0F1F6F2F0F1F5F6F0F6F7F1F0F1F0F0F0F0F1F5F6F4F6404040E3E2E340D7C1D9D2C94040404040404040404040404040C28191"
        b"929695A499404040404040D9E4E2F0F1F8E7F6F1F0F5F0F0F0F0F1F6F4F0F4F0F7F0F0F6F4F3F0F2F2F2F0F3F1F0F0F0F0F0F0F6F0F0"
        b"F6F4F3F4F6F8F3F2")

mem_dump("Received:", data)
IsoPacket = Iso8583(data, iso_spec=IsoSpec1987ASCII())

IsoPacket.print_message()

IsoPacket.mti("0210")

IsoPacket.field(39, 1)
IsoPacket.field_data(39, "00")
IsoPacket.field(2, 0)
IsoPacket.field(35, 0)
IsoPacket.field(52, 0)
IsoPacket.field(60, 0)

print("\n\n\n")
IsoPacket.print_message()
data = IsoPacket.build_iso()
data = struct.pack("!H", len(data)) + data

mem_dump("Sending:", data)
