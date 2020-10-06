# -*- coding: ISO-8859-1 -*-

import string
from dvbobjects.utils import *
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils.MJD import *

class time_date_section2(DVBobject):

    table_id = 0x70

    section_length = 0x5

    section_syntax_indicator = 0x0

    def pack(self):

        date = MJD_convert(self.year, self.month, self.day)

        fmt = "!BHHBBB"
        return pack(fmt,
            self.table_id,
            0x7000 | (self.section_syntax_indicator << 15) | self.section_length,
            date,
            self.hour,
            self.minute,
            self.second,
        )
