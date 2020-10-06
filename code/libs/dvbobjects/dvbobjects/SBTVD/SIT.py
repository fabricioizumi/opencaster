from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *

class service_loop_item(DVBobject):

    service_id = 0x0
    running_status = 0x0

    def pack(self):

        dl_bytes = string.join(
                map(lambda x:x.pack(), self.descriptor_loop)
            , "")

        fmt = "!HH%ds" % (len(dl_bytes))

        return pack(fmt,
                self.service_id
                ,
                0x8000 | self.running_status < 12
            )

class selection_information_section(Section):

    table_id = 0x7f
    table_id_extension = 0x1
    def pack_section_body(self):

        dl_bytes = string.join(
                map(lambda x:x.pack(), self.descriptor_loop)
            , "")

        sl_bytes = string.join(
                map(lambda c:x.pack(), self.service_loop)
            ,"")
        fmt = "!H%ds%ds" % (len(dl_bytes), len(sl_bytes))

        return pack(fmt,
                0xF000 | len(dl_bytes)
                ,
                dl_bytes
                ,
                sl_bytes
            )

