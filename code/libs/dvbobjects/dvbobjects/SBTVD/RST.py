# -*- coding: ISO-8859-1 -*-

from struct import *

from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils import *


class ts_running_status_item(DVBobject):

    transport_stream_id = 0x0

    original_network_id = 0x0

    service_id = 0x0

    event_id = 0x0

    running_status = 0x4

    def pack(self):
        fmt = "!HHHHB"

        return pack(fmt,
                self.transport_stream_id
                ,
                self.original_network_id
                ,
                self.service_id
                ,
                self.event_id
                ,
                 0x00
                 | (0x1f << 3)
                 | (self.running_status)
            )

class running_status_section(DVBobject):
    table_id = 0x71

    section_max_size = 4096

    no_sanity_check = False

    section_syntax_indicator = 0x1

    private_indicator = 0x1

    def pack_section_body(self):
        tss_l = string.join(
                map(lambda x:x.pack(), self.ts_running_status_loop)
            , "")

        fmt = "!%ds" % (len(tss_l))

        return pack(fmt,
                tss_l
            )

    def pack(self):

        body = self.pack_section_body()

        self.section_length = (
            3                           # section header rest
            + len(body)                 # section body
            + 4                         # CRC32
            )

        length_info_16 = (
            0x3000
            | (self.section_syntax_indicator<<15)
            | (self.private_indicator << 14)
            | (self.section_length)
            )

        if not self.no_sanity_check:
           self. __sanity_check()

        data = pack("!BH",
                    self.table_id,
                    length_info_16
                    ) + body

        return data + self.crc_32(data)

    def crc_32(self, data):
        crc = crc32.CRC_32(data)
        return pack("!L", crc)

    def __sanity_check(self):
        assert self.section_syntax_indicator == 1
        assert 0 <= self.table_id <= 0xff
        assert 0 <= self.section_length <= self.section_max_size - 3
