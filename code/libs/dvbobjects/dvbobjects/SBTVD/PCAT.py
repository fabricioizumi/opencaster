from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *

from dvbobjects.utils import *

class content_loop_item(DVBobject):
    content_version = 0x0
    content_minor_version = 0x0
    version_indicator = 0x0
    reserved_future_use = 0x3
    reserved_future_use2 = 0xf

    def pack(self):

        sl_bytes = string.join(
                    map(lambda x:x.pack(), schedule_loop)
                , "")

        dl_bytes = string.join(
                    map(lambda x:x.pack(), descriptors_loop)
                ,"")

        fmt = "!HHHH%ds%ds" % (len(sl_bytes), len(dl_bytes))

        cl_length = len(sl_bytes) + len(dl_bytes)

        return pack(fmt,
                    self.content_version
                    ,
                    self.content_minor_version
                    ,
                      0x0000
                      | (self.version_indicator << 14)
                      | (self.reserved_future_use << 12)
                      | cl_length
                    ,
                      0xF000
                      | len(dl_bytes)


                )


class schedule_loop_item(DVBobject):

    start_time = 0x0
    duration = 0x0

    def pack(self):
        fmt = "!Q"

        return pack(fmt,
                0x0000000000000000
                | self.start_time << 40
                | self.duration
        )

class partial_content_announcement_section(Section):

    table_id = 0xc2

    transport_stream_id = 0x0
    original_network_id = 0x0
    content_id = 0x0
    num_of_content_version = 0x0
    
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

    
    def pack_section_body(self):

        self.table_id_extension = self.transport_stream_id

        cl_bytes = string.join(
                    map(lambda x:x.pack(), self.content_loop)
                , "")

        fmt = "!IB%ds" % (len(cl_bytes))

        return pack(fmt,
            self.content_id
            ,
            self.num_of_content_version
            ,
            cl_bytes
        )

