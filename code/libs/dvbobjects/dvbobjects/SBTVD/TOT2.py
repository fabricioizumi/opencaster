from dvbobjects.PSI.TOT import *
from Converter import *
import pdb

class local_time_offset_loop_item2(DVBobject):

	def pack(self):

		FMT = "!%dsBBBHBBBBB" % len(self.ISO_639_language_code)
		return pack(FMT,
			self.ISO_639_language_code,
			((self.country_region_id & 0x3F) << 2) | 0x2 | (self.local_time_offset_polarity & 0x1),
			self.local_time_offset_hour,
			self.local_time_offset_minute,
			int(MJD_convert(self.year_of_change-1900, self.month_of_change, self.day_of_change)) & 0x00FFFF,
			convert_to_bcd(self.hour_of_change),
			convert_to_bcd(self.minute_of_change),
			convert_to_bcd(self.second_of_change),
			convert_to_bcd(self.next_time_offset_hour),
			convert_to_bcd(self.next_time_offset_minute),
                )


class time_offset_section2(DVBobject):

        table_id = 0x73

        section_syntax_indicator = 0x0

        def pack(self):
            self.table_id_extension = int( str(self.year) + str(self.month) + \
                                        str(self.day) )

            date = int(MJD_convert(self.year-1900, self.month, self.day)) & 0x00FFFF
            # pack service_stream_loop
            tl_bytes = string.join(
            map(lambda x: x.pack(),
        		self.descriptor_loop),
        		"")

            fmt = "!BHHBBBH%ds" % len(tl_bytes)

            data = pack(fmt,
        		self.table_id,
        		0x7000 | (self.section_syntax_indicator << 15) | ((len(tl_bytes) + 11) & 0xFFF),
        		date,
        		convert_to_bcd(self.hour),
        		convert_to_bcd(self.minute),
        		convert_to_bcd(self.second),
        		0xF000 | (len(tl_bytes) & 0xFFF),
        		tl_bytes
                    )

            return data + self.crc_32(data)

        def crc_32(self, data):
	    crc = crc32.CRC_32(data)
            return pack("!L", crc)
