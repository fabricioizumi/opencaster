import string
from struct import *

from dvbobjects.utils import *
from dvbobjects.MPEG.Section import Section

class event_relation_section(Section):
    table_id = 0xd1

    section_max_size = 1024

    event_relation_id = 0x1

    information_provider_id = 0x1

    relation_type = 0x1

    reserved_future_use = 0xf

    def pack_section_body(self):
        self.table_id_extension = self.event_relation_id

        event_bytes = string.join(
                map(lambda x:x.pack(), self.event_loop)
                , "")

        #descriptor_bytes = string.join(
        #        map(lambda x:x.pack(), self.event_descriptor_loop)
        #        , "")

        fmt = "!III%ds" % (len(event_bytes))

        return pack(fmt,
                    self.information_provider_id
                    ,
                    self.relation_type
                    ,
                    self.reserved_future_use
                    ,
                    event_bytes
                    )


class event_loop_item(DVBobject):
    reserved_future_use0 = 0xf

    reserved_future_use1 = 0xf

    parent_node_id = 0xffff

    reference_number = 0x1

    def pack(self):
        # pack event_descriptor_loop
        edl_bytes = string.join(
                map(lambda x: x.pack(),
                    self.event_descriptor_loop),
             "")

        fmt = "!IBBIHBI%ds" % len(edl_bytes)
        return pack(fmt,
                    self.node_id,
                    self.collection_mode,
                    self.reserved_future_use0,
                    self.parent_node_id,
                    self.reference_number,
                    self.reserved_future_use1,
                    len(edl_bytes),
                    edl_bytes,
)

"""
Description: class without sanity check
"""
class event_relation_section2(Section):
    table_id = 0xd1

    section_max_size = 1024

    event_relation_id = 0x1

    information_provider_id = 0x1

    relation_type = 0x1

    reserved_future_use = 0xf

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
        self.table_id_extension = self.event_relation_id

        event_bytes = string.join(
                map(lambda x:x.pack(), self.event_loop)
                , "")

        #descriptor_bytes = string.join(
        #        map(lambda x:x.pack(), self.event_descriptor_loop)
        #        , "")

        fmt = "!III%ds" % (len(event_bytes))

        return pack(fmt,
                    self.information_provider_id
                    ,
                    self.relation_type
                    ,
                    self.reserved_future_use
                    ,
                    event_bytes
                    )


