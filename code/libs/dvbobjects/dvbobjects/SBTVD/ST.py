from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils import *


class stuffing_section(DVBobject):

    table_id = 0x72

    section_syntax_indicator = 0x0

    reserved_future_use = 0x1

    reserved = 0x3

    def pack(self):

        dl_bytes = string.join(
                map(lambda x:pack("!B", x), self.data_byte_loop)
            , "")

        fmt = "!BH%ds" % (len(dl_bytes))

        data = pack(fmt,
                self.table_id
                ,
                0x0000
                | (self.section_syntax_indicator << 15)
                | (self.reserved_future_use << 14)
                | (self.reserved << 12)
                | len(dl_bytes)
                ,
                dl_bytes

            )

        return data + self.crc_32(data)

    def crc_32(self, data):
        crc = crc32.CRC_32(data)
        return pack("!L", crc)

