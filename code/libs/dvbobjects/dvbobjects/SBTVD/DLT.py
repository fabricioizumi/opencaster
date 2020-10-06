from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils import *

class download_table_section(DVBobject):

    table_id = 0xc1

    section_syntax_indicator = 0x0

    private_indicator = 0x1

    section_length = 0x89c # defined by standard

    maker_id = 0x0

    model_id = 0x0

    version_id = 0x0

    section_number = 0x0

    last_section_number = 0x0

    def pack(self):
        ml_bytes = string.join(
                map(lambda x:pack("!B", x), self.model_info_loop)
            , "")

        cdb_bytes =  string.join(
                map(lambda x:pack("!B", x), self.code_data_bytes_loop)
            , "")


        fmt = "!BHBBBHH%ds%ds" % (len(ml_bytes), len(cdb_bytes))

        data = pack(fmt,
                self.table_id
                ,
                 0x7000 | self.section_length
                ,
                self.maker_id
                ,
                self.model_id
                ,
                self.version_id
                ,
                self.section_number
                ,
                self.last_section_number
                ,
                ml_bytes
                ,
                cdb_bytes
            )

        return data + self.crc_32(data)

    def crc_32(self, data):
        crc = crc32.CRC_32(data)
        return pack("!L", crc)
