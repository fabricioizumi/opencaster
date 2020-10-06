import string
from struct import *

from dvbobjects.MPEG.Section import Section

class index_transmission_section(Section):
    table_id = 0xd2

    section_max_size = 1024

    def pack_section_body(self):
        self.table_id_extension = self.program_id

        descriptors_bytes = string.join(
                map(lambda x: x.pack(), self.index_descriptor_loop)
                ,"")

        fmt = "!s"

        return pack(fmt, descriptors_bytes)

"""
Description: class without sanity check
"""
class index_transmission_section2(Section):
    table_id = 0xd2

    section_max_size = 1024

    def _Section__sanity_check(self):
        pass

    def pack(self):

        body = self.pack_section_body()

        self.section_length = (
            5                           # section header rest
            + len(body)                 # section body
            + 4                         # CRC32
            )
        length_info_16 = (
            0x3000
            | (self.section_syntax_indicator<<15)
            | (self.private_indicator << 14)
            | (self.section_length)
            )
        version_info_8 = (
            0xC0
            | ((self.version_number & 0x01f) << 1)
            | (self.current_next_indicator)
            )

        #self.__sanity_check()

        data = pack("!BHHBBB",
                    self.table_id,
                    length_info_16,
                    self.table_id_extension,
                    version_info_8,
                    self.section_number,
                    self.last_section_number,
                ) + body

        return data + self.crc_32(data)

    def pack_section_body(self):
        self.table_id_extension = self.program_id

        descriptors_bytes = string.join(
                map(lambda x: x.pack(), self.index_descriptor_loop)
                ,"")

        fmt = "!%ds" % len(descriptors_bytes)

        return pack(fmt, descriptors_bytes)
