from dvbobjects.PSI.SDT import *

class service_description_section2(service_description_section):
    no_sanity_check = False

    section_syntax_indicator = 0x1

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

        self.private_indicator = 0

        self.section_length = (
            5                           # section header rest
            + len(body)                 # section body
            + 4                         # CRC32
            )
        length_info_16 = (
            0x0000 # changed reserved and reserved for future use to 0
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
