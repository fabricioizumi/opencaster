from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils import *

class discontinuity_information_section(DVBobject):

    table_id = 0x7e

    transaction_flag = 0x0

    section_syntax_indicator = 0x0

    section_length = 0x1

    def pack(self):

        fmt = "!BHH"
        data = pack(fmt,
                self.table_id
                ,
                 0x7000
                 | (self.section_syntax_indicator << 15)
                 | self.section_length
                ,
                 0x007F | (self.transaction_flag << 14)
            )

        return data + self.crc_32(data)

    def crc_32(self, data):
        crc = crc32.CRC_32(data)
        return pack("!L", crc)
