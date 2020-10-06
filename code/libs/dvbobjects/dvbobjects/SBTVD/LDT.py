# -*- coding: ISO-8859-1 -*-

from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *

import string

class description_item(DVBobject):
    description_id = 0x0

    def pack(self):
        d_l = string.join(
                map(lambda x:x.pack, self.descriptor_loop)
            , "")

        fmt = "!HL%ds" % len(d_l)

        return pack(fmt,
                self.description_id
                ,
                 0x00000000
                 | (0xfff << 20)
                 | (len(d_l) << 8)
                ,
                d_l
            )


class linked_description_section(Section):

    table_id = 0xc7

    table_id_extension = 0xc71

    transport_stream_id = 0x0

    original_network_id = 0x0

    section_syntax_indicator = 0x1

    no_sanity_check = False

    def pack_section_body(self):

        d_l = string.join(
                map(lambda x:x.pack(), self.description_loop)
            , "")


        fmt = "!HH%ds" % len(d_l)

        return pack(fmt,
                self.transport_stream_id
                ,
                self.original_network_id
                ,
                d_l
            )

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
