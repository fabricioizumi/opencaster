from struct import *
from dvbobjects.PSI.BAT import *
from dvbobjects.utils.DVBobject import *


class bouquet_association_section2(bouquet_association_section):

    no_sanity_check = False

    def __sanity_check(self):
            assert self.section_syntax_indicator == 1
            assert self.current_next_indicator in (0, 1)
            assert 0 <= self.table_id <= 0xff
            assert 0 <= self.table_id_extension <= 0xffff
            assert 0 <= self.section_length <= self.section_max_size - 3
            assert 0 <= self.section_number <= 0xFF
            assert 0 <= self.last_section_number <= 0xFF

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

        if not self.no_sanity_check:
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

    def crc_32(self, data):
        crc = crc32.CRC_32(data)
        return pack("!L", crc)

