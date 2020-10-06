from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *

class model_info_loop_item(DVBobject):

    maker_id = 0x0

    model_id = 0x0

    version_id = 0x0

    DLT_size = 0x0

    def pack(self):
        fmt = "!BBBB"

        return pack(fmt,
                self.maker_id
                ,
                self.model_id
                ,
                self.version_id
                ,
                self.DLT_size
            )

class transport_st_loop_item(DVBobject):

    transport_stream_id = 0x0

    DL_pid = 0x0

    ECM_pid = 0x0

    def pack(self):

        ml_bytes = stream.join(
                map(lambda x:x.pack(), self.model_info_loop)
            , "")

        fmt = "!HHHH%ds" % (len(ml_bytes))

        return pack(fmt,
                self.transport_stream_id
                ,
                 0xE000 | self.DL_pid
                ,
                 0xE000 | self.ECM_pid
                ,
                 0xF000 | len(ml_bytes)
                ,
                ml_bytes

            )

class download_control_section(Section):

    table_id = 0xc0

    table_id_extension = 0xc00

    transmission_rate = 0x0

    def pack_section_body(self):

        tl_bytes = string.join(
                map(lambda x:x.pack(), self.transport_loop)
            ,"")

        fmt = "!B%ds" % (len(self.transport_loop))

        return pack(fmt,
                self.transmission_rate
                ,
                tl_bytes
            )
