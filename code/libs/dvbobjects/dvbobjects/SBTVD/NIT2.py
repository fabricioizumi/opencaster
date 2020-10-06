# -*- coding: ISO-8859-1 -*-

from dvbobjects.DVB.Descriptors import *
from dvbobjects.PSI.NIT import *

class network_information_section2(network_information_section):
    no_sanity_check = False

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

        if (not self.no_sanity_check):
            self.__sanity_check()

        data = pack("!BHHBBB",
                    self.table_id,
                    length_info_16,
                    self.table_id_extension,
                    version_info_8,
                    self.section_number,
                    self.last_section_number,
                    ) + body

        return data + self.crc_32(data) 
