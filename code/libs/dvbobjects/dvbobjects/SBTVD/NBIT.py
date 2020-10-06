import string
import pdb
from struct import *

from dvbobjects.utils import *
from dvbobjects.MPEG.Section import Section

class network_board_information_section(Section):
    table_id = 0xc6

    section_max_size = 1024

    original_network_id = 0x0

    def pack_section_body(self):
        self.table_id_extension = self.original_network_id

        network_board_bytes = string.join(
                map(lambda x:x.pack(), self.network_board_loop)
                , "")

        fmt = "!%ds" % (len(network_board_bytes))

        return pack(fmt,
                    network_board_bytes
                    )

class key_loop_item(DVBobject):

    #key_id = 0x0

    def pack(self):
        fmt = "!H"

        return pack(fmt,
                    self.key_id
                )

class network_board_loop_item(DVBobject):

    def pack(self):
        self.information_id = 0x0

        self.information_type = 0x1

        self.description_body_location = 0x1

        self.reserved_future_use = 0x3

        self.user_defined = 0x1

        kl_bytes =  string.join(
                map(lambda x: x.pack(),
                    self.keys_loop),
             "")


        self.reserved_future_use2 = 0xf

        ndl_bytes = string.join(
                map(lambda x: x.pack(),
                    self.network_board_descriptor_loop),
             "")

        body_info = (
            self.reserved_future_use
                | (self.information_type<<4)
                | (self.description_body_location << 2)
        )

        length_descriptors = (
            self.reserved_future_use2 << 12
            | (len(ndl_bytes))

        )
        #fmt = "!HBBBBB%dsBI%ds" % (len(kl_bytes), len(ndl_bytes))
        fmt = "!HBBB%dsH%ds" % (len(kl_bytes), len(ndl_bytes))


        return pack(fmt,
                    self.information_id,
                    body_info,
                    self.user_defined,
                    len(self.keys_loop),
                    kl_bytes,
                    length_descriptors,
                    ndl_bytes
                )

"""
Description: class without sanity check
"""
class local_event_information_section2(Section):

    table_id = 0xc6

    section_max_size = 1024

    original_network_id = 0x0

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
        self.table_id_extension = self.original_network_id

        network_board_bytes = string.join(
                map(lambda x:x.pack(), self.network_board_loop)
                , "")


        fmt = "!%ds" % (len(network_board_bytes))

        return pack(fmt,
                    network_board_bytes
                    )

