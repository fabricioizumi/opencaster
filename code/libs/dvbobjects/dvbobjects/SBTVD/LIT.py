import string
from struct import *

from dvbobjects.utils import *
from dvbobjects.MPEG.Section import Section

class local_event_information_section(Section):
    table_id = 0xd0

    section_max_size = 1024

    service_id = 0x0

    transport_stream_id = 0x0

    original_network_id = 0x0

    event_id = 0x0

    def pack_section_body(self):
        self.table_id_extension = self.service_id

        local_event_bytes = string.join(
                map(lambda x:x.pack(), self.local_event_loop)
                , "")


        fmt = "!III%ds" % (len(local_event_bytes))

        return pack(fmt,
                    self.service_id
                    ,
                    self.transport_stream_id
                    ,
                    self.original_network_id
                    ,
                    local_event_bytes
                    )


class local_event_loop_item(DVBobject):

    def pack(self):
        # pack event_descriptor_loop
        ldl_bytes = string.join(
                map(lambda x: x.pack(),
                    self.local_event_descriptor_loop),
             "")

        fmt = "!IBH%ds" % len(ldl_bytes)
        return pack(fmt,
                    self.local_event_id,
                    self.reserved_future_use,
                    len(ldl_bytes),
                    ldl_bytes,
)

"""
Description: class without sanity check
"""
class local_event_information_section2(Section):

    table_id = 0xd0

    section_max_size = 1024

    service_id = 0x0

    transport_stream_id = 0x0

    original_network_id = 0x0

    event_id = 0x0


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
        self.table_id_extension = self.service_id

        local_event_bytes = string.join(
                map(lambda x:x.pack(), self.local_event_loop)
                , "")

        fmt = "!III%ds" % (len(local_event_bytes))

        return pack(fmt,
                    self.service_id
                    ,
                    self.transport_stream_id
                    ,
                    self.original_network_id
                    ,
                    local_event_bytes
                    )

