from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *


import string

class broadcaster_information_section(Section):

    table_id = 0xc4

    original_network_id = 0x0

    broadcast_view_propriety = 0x1

    table_id_extension = original_network_id


    # override parent pack method
    def pack(self):

        body = self.pack_section_body()

        self.section_length = (
                5                           # section header
                + len(body)                 # section body
                + 4                         # CRC32
                )
        length_info_16 = (
                0xF000 | (self.section_length)
            )

        version_info_8 = (
            (0x03 << 6)
            | (self.version_number << 1)
            | (self.current_next_indicator)
            )

        self._Section__sanity_check()

        data = pack("!BHHBBB",
                    self.table_id,
                    length_info_16,
                    self.original_network_id,
                    version_info_8,
                    self.section_number,
                    self.last_section_number,
                    ) + body

        return data + self.crc_32(data)

    def pack_section_body(self):

        fdl = string.join(
            map(lambda x:x.pack(),
                self.first_descriptor_loop
            )
        ,"")

        reserved_future_use = 0x7

        bl = string.join(
                map(lambda x:x.pack(), self.broadcaster_loop)
            ,"")
        fmt = "!BB%ds%ds" % (len(fdl), len(bl))

        reserved_future_use2 = 0xf

        return pack(fmt,
                    (self.broadcast_view_propriety << 4) | (reserved_future_use << 5)
                        |
                        (0xF00 & len(fdl) >> 8)
                    ,
                    0xFF & len(fdl)
                    ,
                    fdl
                    ,
                    bl
                )


class broadcaster_loop_item(DVBobject):

    def pack(self):

        dl = string.join(
            map(lambda x:x.pack(),
                self.descriptor_loop)
        ,"")

        fmt = "!BH%ds" % (len(dl))

        return pack(fmt,
                self.broadcaster_id,
                (0xF << 12) | (0x0FFF & len(dl)),
                dl
            )

