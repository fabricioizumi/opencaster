from struct import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.DVBobject import *


class common_data_section(Section):

    table_id = 0xc8
    
    original_network_id = 0x0

    table_id_extension = original_network_id

    data_type = 0x1

    def pack_section_body(self):

        dl_bytes = string.join(
                map(lambda x:x.pack(), self.descriptor_loop)
            , "")

        dml_bytes = string.join(
                map(lambda x:pack("!B", x), self.data_module_loop)
            , "")

        fmt = "!HBH%ds%ds" % (len(dl_bytes), len(dml_bytes))

        return pack(fmt,
                    self.original_network_id
                    ,
                    self.data_type
                    ,
                    0xF000 | (len(dl_bytes))
                    ,
                    dl_bytes
                    ,
                    dml_bytes
                )
