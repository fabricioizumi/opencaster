import string

from struct import *
from dvbobjects.utils import *
from dvbobjects.MPEG.Descriptor import Descriptor
import pdb

class AAC_Descriptor2(Descriptor):
    descriptor_tag = 0x7c

    profile_and_level = 0x2c
    AAC_type_flag = 0x0

    AAC_type = 0x0

    def bytes(self):

        ai_l = string.join(
                    pack("!%ds" % len(self.additional_info), self.additional_info)
            , "")

        if (self.AAC_type_flag == 1):
           fmt = "!BBB%ds" % (len(self.additional_info))

           return pack(fmt,
                    self.profile_and_level
                    ,
                    0xFF & (self.AAC_type_flag << 8)
                    ,
                    self.AAC_type
                    ,
                    ai_l

                )
        else:
            fmt = "!BB%ds" % (len(ai_l))

            return pack(fmt,
                    self.profile_and_level
                    ,
                    0xFF & (self.AAC_type_flag << 8)
                    ,
                    ai_l

                )



class CA_Identifier_descriptor(Descriptor):
    descriptor_tag = 0x53

    def bytes(self):

        ca_l = string.join(
               map(lambda x: pack("!H", x), self.CA_system_id_loop)
            , "")

        fmt = '!%ds' % (len(ca_l))

        return pack(fmt,
                ca_l
            )


class private_data_item(DVBobject):
    def pack(self):
        fmt = "!B"

        return pack(fmt,
                    self.private_data_byte
                )

class association_tag_descriptor2(Descriptor):

    descriptor_tag = 0x14

    association_tag = 256

    use = 0x1000

    at_selector_byte_length = 0x0

    at_selector_byte = 0x0

    def bytes(self):
        pd_l = string.join(
                    map(lambda x:x.pack(), self.private_data_loop)
                ,"")

        fmt = "!HHBB%ds" % len(pd_l)

        return pack(fmt,
                    self.association_tag
                    ,
                    self.use
                    ,
                    self.at_selector_byte_length
                    ,
                    self.at_selector_byte
                    ,
                    pd_l
                )

class hierarchical_transmission_descriptor(Descriptor):
    descriptor_tag = 0xc0

    quality_level = 0x01

    reference_PID = 0x0000

    def bytes(self):
        fmt = "!BH"

        return pack(fmt,
                0x01 & self.quality_level,
                0x1FFF & self.reference_PID
            )

class extended_broadcast_descriptor(Descriptor):
    descriptor_tag = 0xce

    terrestrial_brodcaster_id = 0x10

    number_of_afiliation_id_loop = 0

    original_network_id =0x0

    broadcaster_id = 0x0

    def bytes(self):
        fmt = "!BHBHB"

        return pack(fmt,
                    self.broadcaster_type << 4 | 0x0F
                    ,
                    self.terrestrial_brodcaster_id
                    ,
                    (self.number_of_afiliation_id_loop & 0x0F) << 4
                        | (self.number_of_broadcaster_id_loop & 0x0F)
                    ,
                    self.original_network_id
                    ,
                    self.broadcaster_id

                )

class table_description_loop_item(DVBobject):

    def pack(self):
        fmt = "!B"

        return pack(fmt,
                self.table_description
            )

class CA_descriptor(Descriptor):
    descriptor_tag = 0x09

    CA_system_id = 0x0

    CA_PID = 0x00

    def bytes(self):

        pdb_l = string.join(
                    map(lambda x:pack("!B", x), self.private_data_byte_loop)
                , "")

        fmt = "!HH%ds" % (len(pdb_l))

        return pack(fmt,
                    self.CA_system_id,
                    (0x0000 | self.CA_PID) & 0x1fff,
                    pdb_l
                )
class table_loop_item(DVBobject):

    def pack(self):

        td_l = string.join(
                map(lambda x:x.pack(), self.table_description_loop)
            )
        fmt = "!BB%ds" % (len(td_l))

        return pack(fmt,
                    self.table_id,
                    len(td_l),
                    td_l
                )

class SI_parameter_descriptor(Descriptor):
    descriptor_tag = 0xd7

    parameter_version = 0x1

    update_time = 0x20

    def bytes(self):

        tb_l = string.join(
                map(lambda x:x.pack(), self.table_loop)
            , "")

        fmt = "!BH%ds" % len(tb_l)

        return pack(fmt,
                    self.parameter_version
                    ,
                    self.update_time
                    ,
                    tb_l
                )

class component_control_item(DVBobject):

    component_tag = 0x0

    digital_recording_control_data = 0x0

    maximum_bitrate_flag = 0x1

    copy_control_type = 0x0

    def pack(self):
        fmt = "!BB"

        self.APS_control_data = 0x3

        if (copy_control_type != 00):
            self.APS_control_data = 0x0

        if (maximum_bitrate_flag == 1):
            maximum_bitrate = 130

            fmt += "B"

            return pack(fmt,
                    self.component_tag
                    ,
                     0x10
                     | (self.digital_recording_control_data << 6)
                     | (maximum_bitrate_flag << 5)
                     | (copy_control_type << 2)
                     | self.APS_control_data
                    ,
                    self.maximum_bitrate
                )

        else:
            return pack(fmt,
                    self.component_tag
                    ,
                     0x10
                     | (self.digital_recording_control_data << 6)
                     | (maximum_bitrate_flag << 5)
                     | (copy_control_type << 2)
                     | self.APS_control_data
                )



class digital_copy_control_descriptor(Descriptor):

    descriptor_tag = 0xc1

    digital_recording_control_data = 0x0

    maximum_bitrate_flag = 0x1

    component_control_flag = 0x1

    copy_control_type = 0x0

    no_maximum_bitrate = False

    def bytes(self):
        self.APS_control_data = 0x0

        fmt = "!B"

        if (self.copy_control_type == 0):
            self.APS_control_data == 0x3

        if (self.maximum_bitrate_flag == 1 and not self.no_maximum_bitrate):
            #self.maximum_bitrate = 130
            fmt += "B"

            if (self.component_control_flag == 1):

               cl_bytes = string.join(
                        map(lambda x:x.pack(), self.component_control_loop)
                    ,"")

               fmt += "B%ds" % (len(cl_bytes))

               return pack(fmt,
                         0x00
                         | (self.digital_recording_control_data << 6)
                         | (self.maximum_bitrate_flag << 5)
                         | (self.component_control_flag << 4)
                         | (self.copy_control_type << 2)
                         | self.APS_control_data
                       ,
                       self.maximum_bitrate
                       ,
                       len(cl_bytes)
                       ,
                       cl_bytes
                   )


            else:
                return pack(fmt,
                        0x00
                          | (self.digital_recording_control_data << 6)
                          | (self.maximum_bitrate_flag << 5)
                          | (self.component_control_flag << 4)
                          | (self.copy_control_type << 2)
                          | self.APS_control_data
                        ,
                        self.maximum_bitrate

                    )
        else:

            if (self.component_control_flag == 1):

                cl_bytes = string.join(
                        map(lambda x:x.pack(), self.component_control_loop)
                    ,"")

                fmt += "B%ds" % (len(cl_bytes))

                return pack(fmt,
                          0x00
                          | (self.digital_recording_control_data << 6)
                          | (self.maximum_bitrate_flag << 5)
                          | (self.component_control_flag << 4)
                          | (self.copy_control_type << 2)
                          | self.APS_control_data
                        ,
                        len(cl_bytes)
                        ,
                        cl_bytes
                    )
            else:
                return pack(fmt,
                        0x00
                          | (self.digital_recording_control_data << 6)
                          | (self.maximum_bitrate_flag << 5)
                          | (self.component_control_flag << 4)
                          | (self.copy_control_type << 2)
                          | self.APS_control_data
                        ,

                    )

class conditional_playback_descriptor(Descriptor):

    descriptor_tag = 0xf8

    CA_system_id = 0x01

    CA_PID = 0x01

    def bytes(self):

        pdb_l = string.join(
            map(lambda x:pack("!B", x), self.private_data_byte)
        )

        fmt = "!HH%ds" % (len(pdb_l))

        return pack(fmt,
            self.CA_system_id,
            0x1FFF & self.CA_PID,
            pdb_l
        )
class content_availability_descriptor(Descriptor):

    descriptor_tag = 0x71

    retention_mode = 0x01

    retention_state = 0x1

    encryption_mode = 0x1

    def bytes(self):

        rfu_l = string.join(
            map(lambda x:pack("!B", x), self.reserved_future_use)
        )

        fmt = "!B%ds" % (len(rfu_l))

        return pack(fmt,
            (((0x1 & self.retention_mode) << 4 ) |
             ( 0x0F & ((self.retention_state << 1) | self.encryption_mode))
            )
            ,
            rfu_l
        )

class audio_component_descriptor(Descriptor):
    descriptor_tag = 0xc4

    stream_content = 0x6

    component_type = 0x9 # HE-AAC MPEG4 audio, modo 3/2 + LFE

    component_tag = 0x0

    stream_type = 0x11

    simulcast_group_tag = 0xff

    ES_multi_lingual_flag = 0x0

    main_component_flag = 0x1

    quality_indicator = 0x1

    sampling_rate = 0x7

    ISO_639_language_code = "por"

    def bytes(self):

        tc_l = string.join(
                map(lambda x:pack("!B", x), self.text_char)
            ,"")

        fmt = "!BBBBBB3s"

        if (self.ES_multi_lingual_flag == 1):

            fmt += "3s%ds" % (len(tc_l))

            self.ISO_639_language_code_2 = "eng"

            return pack(fmt,
                    0xf0 | self.stream_content
                    ,
                    self.component_type
                    ,
                    self.component_tag
                    ,
                    self.stream_type
                    ,
                    self.simulcast_group_tag
                    ,
                     0x01
                     | (self.ES_multi_lingual_flag << 7)
                     | (self.main_component_flag << 6)
                     | (self.quality_indicator << 4)
                     | (self.sampling_rate << 1)
                    ,
                    self.ISO_639_language_code
                    ,
                    self.ISO_639_language_code_2
                    ,
                    tc_l

                )
        else:

            fmt += "%ds" % (len(tc_l))

            return pack(fmt,
                    0xf0 | self.stream_content
                    ,
                    self.component_type
                    ,
                    self.component_tag
                    ,
                    self.stream_type
                    ,
                    self.simulcast_group_tag
                    ,
                     0x01
                     | (self.ES_multi_lingual_flag << 7)
                     | (self.main_component_flag << 6)
                     | (self.quality_indicator << 4)
                     | (self.sampling_rate << 1)
                    ,
                    self.ISO_639_language_code
                    ,
                    tc_l

                )

class copyright_descriptor(Descriptor):
    descriptor_tag = 0x44

    def bytes(self):

        aci_l = string.join(
                map(lambda x:pack("!B", x), self.additional_copyright_info)
            ,"")

        fmt = "!L%ds" % (len(aci_l))

        return pack(fmt,
                self.copyright_identifier
                ,
                aci_l
            )

class partial_transport_stream_descriptor(Descriptor):
    descriptor_tag = 0x63

    peak_rate = 0x02

    minimum_overall_smoothing_rate = 0x01

    maximum_overall_smoothing_rate = 0x02

    def bytes(self):
        fmt = "!Q"

        return pack(fmt,
         (
          ((0x0000000000000000 | self.peak_rate) << 40)
          |
          ((0x0000000000000000 | self.minimum_overall_smoothing_rate) << 16)
          |
          (0x0000000000000000 | self.maximum_overall_smoothing_rate)
         )
        )
class AVC_video_descriptor(Descriptor):
    descriptor_tag = 0x28

    profile_idc = 0x0

    constraint_set0_flag = 0x0

    constraint_set1_flag = 0x0

    constraint_set2_flag = 0x0

    AVC_compatible_flags = 0x0

    level_idc = 0x0

    AVC_still_present = 0x0

    AVC_24_hour_picture_flag = 0x0

    def bytes(self):

        fmt = "!BBBB"

        return pack(fmt,
                self.profile_idc
                ,
                 0x00
                 | (self.constraint_set0_flag << 7)
                 | (self.constraint_set1_flag << 6)
                 | (self.constraint_set2_flag << 5)
                 | self.AVC_compatible_flags
                ,
                self.level_idc
                ,
                 0x00
                 | (self.AVC_still_present << 7)
                 | (self.AVC_24_hour_picture_flag << 6)
                 | 0x3f
            )

class AVC_timing_and_descriptor(Descriptor):
    descriptor_tag = 0x2a

    hdr_management_valid_flag = 0x0

    picture_and_timing_info_present = 0x0

    def bytes(self):
        fmt = "!B"

        if (self.picture_and_timing_info_present == 1):
            fmt += "B"

            if (self.a90kHz_flag == 0):
                fmt += "LLLB"

                return pack(fmt,
                         0x00
                         | (self.hdr_management_valid_flag << 7)
                         | 0x7e
                         | self.picture_and_timing_info_present
                        ,
                         0x00
                         | (self.a90kHz_flag << 7)
                         | 0x7f
                        ,
                        self.n
                        ,
                        self.k
                        ,
                        self.num_units_in_tick
                        ,
                         0x00
                         | (self.fixed_frame_rate_flag << 7)
                         | (self.temporal_poc_flag << 6 )
                         | (self.picture_to_display_conversion_flag << 5)
                         | 0x1f
                    )
            else:
                fmt += "LB"
                return pack(fmt,
                         0x00
                         | (self.hdr_management_valid_flag << 7)
                         | 0x7e
                         | self.picture_and_timing_info_present
                        ,
                         0x00
                         | (self.a90kHz_flag << 7)
                         | 0x7f
                        ,
                        self.num_units_in_tick
                        ,
                         0x00
                         | (self.fixed_frame_rate_flag << 7)
                         | (self.temporal_poc_flag << 6 )
                         | (self.picture_to_display_conversion_flag << 5)
                         | 0x1f
                    )
        else:
            fmt += "B"

            return pack(fmt,
                         0x00
                         | (self.hdr_management_valid_flag << 7)
                         | 0x7e
                         | self.picture_and_timing_info_present
                        ,
                         0x00
                         | (self.fixed_frame_rate_flag << 7)
                         | (self.temporal_poc_flag << 6 )
                         | (self.picture_to_display_conversion_flag << 5)
                         | 0x1f
                    )


class elementary_cell_id_item(DVBobject):
    elementary_cell_id = 0x0

    def pack(self):
        return pack("!B", 0x00 | (0x3 << 6) | self.elementary_cell_id)


class logical_cell_id_item(DVBobject):
    logical_cell_id = 0x0

    logical_cell_presentation_info = 0x1


    def pack(self):
        eci_l = string.join(
                map(lambda x:x.pack(), self.elementary_cell_id_loop)
            , "")


        fmt = "!HB%dsB" % (len(eci_l))


        if (self.cell_linkage_info == 0x01):
            fmt += "H"

            return pack(fmt,
                     0x0000
                     | (self.logical_cell_id << 10)
                     | (0x7F << 3)
                     | self.logical_cell_presentation_info
                    ,
                    len(eci_l)
                    ,
                    eci_l
                    ,
                    self.cell_linkage_info
                    ,
                    self.bouquet_id
                )

        if (self.cell_linkage_info == 0x02 or self.cell_linkage_info == 0x03):
            fmt += "HHH"

            return pack(fmt,
                     0x0000
                     | (self.logical_cell_id << 10)
                     | (0x7F << 3)
                     | self.logical_cell_presentation_info
                    ,
                    len(eci_l)
                    ,
                    eci_l
                    ,
                    self.cell_linkage_info
                    ,
                    self.original_network_id
                    ,
                    self.transport_stream_id
                    ,
                    self.service_id
                )

        if (self.cell_linkage_info == 0x4):
            fmt += "HHHH"

            return pack(fmt,
                     0x0000
                     | (self.logical_cell_id << 10)
                     | (0x7F << 3)
                     | self.logical_cell_presentation_info
                    ,
                    len(eci_l)
                    ,
                    eci_l
                    ,
                    self.cell_linkage_info
                    ,
                    self.original_network_id
                    ,
                    self.transport_stream_id
                    ,
                    self.service_id
                    ,
                    self.event_id
                )

        else:

            return pack(fmt,
                     0x0000
                     | (self.logical_cell_id << 10)
                     | (0x7F << 3)
                     | self.logical_cell_presentation_info
                    ,
                    len(eci_l)
                    ,
                    eci_l
                    ,
                    self.cell_linkage_info

            )


class mosaic_descriptor(Descriptor):
    descriptor_tag = 0x51

    mosaic_entry_point = 0x1

    number_of_horizontal_elementary_cells = 0x00

    number_of_vertical_elementary_cells = 0x00

    wrong_length = False

    def pack(self):
        if not self.wrong_length:
            return Descriptor.pack(self)
        else:
            bytes = self.bytes()

            return pack("!BB%ds" % 100,
                         self.descriptor_tag,
                         100,
                         bytes,
            )

    def bytes(self):

        lci_l = string.join(
                map(lambda x:x.pack(), self.logical_cell_id_loop)
            , "")

        fmt = "!B%ds" % (len(lci_l))

        return pack(fmt,
                 0x00
                 | (self.mosaic_entry_point << 7)
                 | (self.number_of_horizontal_elementary_cells << 4)
                 | (0x1 << 3)
                 | self.number_of_vertical_elementary_cells
                ,
                lci_l
            )


class hierarchical_transmission_descriptor2(Descriptor):
    descriptor_tag = 0xc0

    quality_level = 0x1

    reference_PID = 0x111

    def bytes(self):
        fmt = "!BH"

        return pack(fmt,
                 0x00
                 | 0xfe
                 | self.quality_level
                ,
                 0x0000
                 | (0x7 << 13)
                 | self.reference_PID
            )

class target_area_descriptor(Descriptor):
    descriptor_tag = 0xc6

    region_spec_type = 0x1

    prefecture_bitmap = 0x0

    def bytes(self):
        # arib b10 not definy field target region spec (last field in this descriptor), so we get the same specification
        # found in tektonix script and put here
        fmt ="!BQ"

        return pack(fmt,
                self.region_spec_type
                ,
                 0x0000000000000000
                 | (self.prefecture_bitmap << 8)
            )

class video_decode_control_descriptor(Descriptor):
    descriptor_tag = 0xc8

    still_picture_flag = 0x0

    sequence_end_code_flag = 0x0

    video_encode_format = 0x0

    def bytes(self):

        fmt ="!B"

        return pack(fmt,
                0x00
                | (self.still_picture_flag << 7)
                | (self.sequence_end_code_flag << 6)
                | (self.video_encode_format << 2)
                | 0x3
            )

class area_code_loop_item(DVBobject):
    area_code = 0x34d # Local commom code

    def pack(self):
        fmt = "!H"

        return struct.pack(fmt,
                    0x0000
                    | (self.area_code << 4)
                    | 0xf
                )

class service_id_loop_item(DVBobject):
    service_id = 0x0

    start_end_flag = 0x0

    signal_level = 0x0

    def pack(self):

        ac_l = string.join(
                map(lambda x:x.pack(), self.area_code_loop)
            , "")

        fmt = "!HBB%ds" % (len(ac_l))

        return pack(fmt,
                self.service_id
                ,
                 0x00
                 | (self.start_end_flag << 7)
                 | (self.signal_level << 6)
                 | 0x3f
                ,
                len(ac_l)
                ,
                ac_l
            )

class emergency_information_descriptor(Descriptor):
    descriptor_tag = 0xfc

    def bytes(self):

        si_l = string.join(
                map(lambda x:x.pack(), self.service_id_loop)
            , "")

        fmt = "!%ds" % (len(si_l))

        return pack(fmt,
                si_l
            )

class unknown_subdescriptor(DVBobject):
    descriptor_tag = 0x0

    def pack(self):

        fmt = "!B"

        return pack(fmt,
                self.descriptor_tag
            )

class carousel_identification_descriptor(Descriptor):
    descriptor_tag = 0x13

    carousel_id = 0x01

    FormatID = 0x00

    ModuleVersion = 0x01

    ModuleId = 0x01

    BlockSize = 0x01

    ModuleSize = 0x01

    CompressionMethod = 0x01

    OriginalSize = 0x01

    Timeout = 0x01

    ObjectKeyLength = 0x01

    def bytes(self):
        if (self.FormatID == 0):
            pdb_l = string.join(
                map(lambda x:pack("!B", x), self.private_data_byte)
            )

            fmt = "!%ds" % (len(pdb_l))

            return pack(fmt,
                pdb_l
            )

        if (self.FormatID == 0x01):
            okd_l = string.join(
                map(lambda x:pack("!B", x), self.ObjectKeyData)
            )

            self.ObjectKeyLength = len(okd_l)

            pdb_l = string.join(
                map(lambda x:pack("!B", x), self.private_data_byte)
            )

            fmt = "!BHHLBLBB%ds%ds" % (len(okd_l), len(pdb_l))

            return pack(fmt,
                self.ModuleVersion,
                self.ModuleId,
                self.BlockSize,
                self.ModuleSize,
                self.CompressionMethod,
                self.OriginalSize,
                self.Timeout,
                self.ObjectKeyLength,
                okd_l,
                pdb_l
            )

class carousel_compatible_composite_descriptor(Descriptor):
   descriptor_tag = 0xf7

   def bytes(self):

       sd_l = string.join(
               map(lambda x:x.pack(), self.subdescriptor_loop)
            ,"")
       fmt = "!%ds" % (len(sd_l))

       return pack(fmt,
               sd_l
            )

class stuffing_descriptor(Descriptor):
    descriptor_tag = 0x43

    wrong_descriptor_length = False

    def bytes(self):

        sd_l = string.join(
                map(lambda x:pack("!B", x), self.stuffing_byte)

            , "")

        fmt = "!%ds" % (len(sd_l))

        return pack(fmt,
                sd_l
            )

    def pack(self):
        bytes = self.bytes()

        if not self.wrong_descriptor_length:
            return pack("!BB%ds" % len(bytes),
                        self.descriptor_tag,
                        len(bytes),
                        bytes,

            )

        else:
            return pack("!BB%ds" % len(bytes),
                        self.descriptor_tag,
                        50,
                        bytes,

            )

class transmission_type_info_item(DVBobject):
    transmission_type_info = 0x0

    def pack(self):

        si_l = string.join(
                map(lambda x:pack("!H", x), self.service_ids)
            , "")

        fmt = "!BB%ds" % (len(si_l))

        return pack(fmt,
                self.transmission_type_info
                ,
                len(self.service_ids)
                ,
                si_l
            )


class TS_information_descriptor(Descriptor):
    descriptor_tag = 0xcd

    remote_control_key_id = 0x1


    def bytes(self):

        tsn_l = string.join(
                map(lambda x:pack("!1s", x), self.ts_name)
            ,"")

        tti_l = string.join(
                map(lambda x:x.pack(), self.transmission_type_info_loop)
            , "")

        tff_l = string.join(
                map(lambda x:pack("!B", x), self.reserved_future_use_loop)
            , "")

        fmt = "!BB%ds%ds%ds" % (len(tsn_l), len(tti_l), len(tff_l))


        return pack(fmt,
                self.remote_control_key_id
                ,
                 0x00
                 | (len(tsn_l) << 2)
                 | len(self.transmission_type_info_loop)
                ,
                tsn_l
                ,
                tti_l
                ,
                tff_l
            )


class connected_transmission_descriptor(Descriptor):
    descriptor_tag = 0xdd

    connected_transmission_group_id = 0x0

    segment_type = 0x0

    modulation_type_A = 0x1

    modulation_type_B = 0x1


    def bytes(self):

        acti_l = string.join(
                map(lambda x:pack("!B", x), self.additional_connected_transmission_info_loop)
            , "")


        fmt = "!HB%ds" % (len(acti_l))

        return pack(fmt,
                self.connected_transmission_group_id
                ,
                 0x00
                 | (self.segment_type << 6)
                 | (self.modulation_type_A << 4)
                 | (self.modulation_type_B << 2)
                 | 0x3
                ,
                acti_l
            )

class service_loop_item(DVBobject):
    primary_service_id = 0x0

    secondary_service_id = 0x0

    def pack(self):

        fmt = "!HH"

        return pack(fmt,
                self.primary_service_id
                ,
                self.secondary_service_id
            )

class service_group_descriptor(Descriptor):
    descriptor_tag = 0xe0

    service_group_type = 0x1

    def bytes(self):

        fmt = "!B"

        if (self.service_group_type == 0x1):

            si_l = string.join(
                    map(lambda x:x.pack(), self.service_loop)
                , "")


            fmt += "%ds" % (len(si_l))

            return pack(fmt,
                     0x00
                     | (self.service_group_type << 4)
                     | 0xf
                    ,
                    si_l
                )

        else:
            pdb_l = string.join(
                    map(lambda x:pack("!B", x), self.private_data_byte_loop)
                , "")

            fmt += "%ds" % (len(pdb_l))

            return pack(fmt,
                     0x00
                     | (self.service_group_type << 4)
                     | 0xf
                    ,
                    pdb_l
                 )

class country_availability_descriptor(Descriptor):
    descriptor_tag = 0x49

    country_availability_flag = 0x1

    def bytes(self):

        cc_l = string.join(
                map(lambda x:pack("%ds" % len(x), x ), self.country_code_loop)
            , "")

        fmt = "!B%ds" % (len(cc_l))

        return pack(fmt,
                 0x00
                 | (self.country_availability_flag << 7)
                 | 0x7f
                ,
                cc_l
            )


class logo_transmission_descriptor(Descriptor):
    descriptor_tag = 0xcf

    logo_transmission_type = 0x3

    def bytes(self):

        fmt = "!B"

        if (self.logo_transmission_type == 0x01):
            fmt += "HHH"

            return pack(fmt,
                    self.logo_transmission_type
                    ,
                     0x0000
                     | (0x7f << 9)
                     | self.logo_id
                    ,
                     0x0000
                     | (0xf << 12)
                     | self.logo_version
                    ,
                    self.download_data_id
                )

        elif (self.logo_transmission_type == 0x02):
            fmt += "H"

            return pack(fmt,
                    self.logo_transmission_type
                    ,
                     0x0000
                     | (0x7f << 9)
                     | self.logo_id
                )

        elif (self.logo_transmission_type == 0x03):
            lc_l = string.join(
                    map(lambda x:pack("!B", x), self.logo_char)
                , "")

            fmt += "%ds" % (len(lc_l))

            return pack(fmt,
                    self.logo_transmission_type
                    ,
                    lc_l
                )

        else:
            rfu_l = string.join(
                    map(lambda x:pack("!B", x), self.reserved_future_use_loop)
                , "")

            fmt += "%ds" % (len(rfu_l))

            return pack(fmt,
                    self.logo_transmission_type
                    ,
                    rfu_l
                )

class link_service_info(DVBobject):
    original_network_id = 0x0

    transport_stream_id = 0x0

    service_id = 0x0

    def pack(self):

        fmt = "!HHH"

        return pack(fmt,
                self.original_network_id
                ,
                self.transport_stream_id
                ,
                self.service_id
            )

class nvod_reference_item(DVBobject):
    transport_stream_id = 0x01

    original_network_id = 0x01

    service_id = 0x01

    def pack(self):
        fmt = "!HHH"

        return pack(fmt,
            self.transport_stream_id,
            self.original_network_id,
            self.service_id
        )

class nvod_reference_descriptor(Descriptor):
    descriptor_tag = 0x70

    def bytes(self):

        nri = string.join(
            map(lambda x:x.pack(), self.nvod_reference_items)
        )

        fmt = "!%ds" % len(nri)

        return pack(fmt,
            nri
        )

class time_shifted_service_descriptor(Descriptor):
    descriptor_tag = 0x4c

    reference_service_id = 0x01

    def bytes(self):
        fmt = "!H"

        return pack(fmt,
            self.reference_service_id
        )


class time_shifted_event_descriptor(Descriptor):
    descriptor_tag = 0x4f

    reference_service_id = 0x01

    reference_event_id = 0x01

    def bytes(self):
        fmt = "!HH"

        return pack(fmt,
            self.reference_service_id,
            self.reference_event_id
        )


class network_identifier_descriptor(Descriptor):
    descriptor_tag = 0xc2

    country_code = "BRA"

    media_type = "TB"

    network_id = 0x01

    def bytes(self):

        assert(len(self.country_code) == 3)

        assert(len(self.media_type) == 2)

        pdb_l = string.join(
            map(lambda x:pack("!B"), self.private_data)
        )
        fmt = "!BBBBBH%ds" % len(pdb_l)

        return pack(fmt,
            ord(self.country_code[0]),
            ord(self.country_code[1]),
            ord(self.country_code[2]),
            ord(self.media_type[0]),
            ord(self.media_type[1]),
            self.network_id,
            pdb_l
        )
class network_name_descriptor(Descriptor):
    descriptor_tag = 0x40

    def bytes(self):
        cfd = string.join(
            map(lambda x:pack("!B"), self.char_delivery_system)
        )

        fmt = "%ds" % (len(cfd))

        return pack(fmt,
            cfd
        )

class reference_descriptor_item(DVBobject):
    reference_node_id = 0x01

    reference_number = 0x01

    last_reference_number = 0x01

    def pack(self):

        fmt = "!HBB"

        return pack(fmt,
            self.reference_node_id,
            self.reference_number,
            self.last_reference_number
        )

class reference_descriptor(Descriptor):
    descriptor_tag = 0xd1

    information_provider_id = 0x01

    event_relation_id = 0x01

    def bytes(self):

        rdi_l = string.join(
            map(lambda x:x.pack(), self.reference_descriptor_items)
        )

        fmt = "!HH%ds" % len(rdi_l)

        return pack(fmt,
            self.information_provider_id,
            self.event_relation_id,
            rdi_l
        )

class short_node_information_descriptor(Descriptor):
    descriptor_tag = 0xd3

    ISO_639_language_code = "BRA"

    node_name_length = 0x1

    text_length = 0x01

    def bytes(self):

        assert (len(self.ISO_639_language_code) == 3)

        nnc_l = string.join(
            map(lambda x:pack("!B", x), self.node_name_chars)
        )

        self.node_name_length = len(nnc_l)

        tc_l = string.join(
            map(lambda x:pack("!B", x), self.text_chars)
        )

        self.text_length = len(tc_l)

        assert (self.node_name_length == len(nnc_l))

        assert (self.text_length == len(tc_l))

        fmt = "!BBBB%dsB%ds" % (len(nnc_l), len(tc_l))

        return pack(fmt,
            ord(self.ISO_639_language_code[0]),
            ord(self.ISO_639_language_code[1]),
            ord(self.ISO_639_language_code[2]),
            self.node_name_length,
            nnc_l,
            self.text_length,
            tc_l
        )

class board_information_descriptor(Descriptor):
    descriptor_tag = 0xdb

    title_length = 0x0

    text_length = 0x00

    def bytes(self):
        tc = string.join(
            map(lambda x:pack("!B", ord(x)), self.title_chars)
        )

        txc = string.join(
            map(lambda x:pack("!B", ord(x)), self.text_chars)
        )

        self.title_length = len(tc)

        self.text_length = len(txc)

        fmt = "!B%dsB%ds" % (len(tc), len(txc))

        return pack(fmt,
            self.title_length,
            tc,
            self.text_length,
            txc
        )
class broadcaster_name_descriptor(Descriptor):

    descriptor_tag = 0xd8

    def bytes(self):
        c_l = string.join(
            map(lambda x:pack("!B",x), self.chars)
        )

        fmt = "!%ds" % len(c_l)

        return pack(fmt,
            c_l
        )

class hyperlink_descriptor(Descriptor):
    descriptor_tag = 0xc5

    hyper_linkage_type = 0x1

    link_destination_type = 0x1

    def bytes(self):

        sb_l = string.join(
                map(lambda x:x.pack(), self.selector_byte_loop)
            , "")

        pd_l = string.join(
                map(lambda x:pack("!B", x), self.private_data_loop)
            , "")

        fmt = "!BBB%ds%ds" % (len(sb_l), len(pd_l))

        return pack(fmt,
                self.hyper_linkage_type
                ,
                self.link_destination_type
                ,
                len(sb_l)
                ,
                sb_l
                ,
                pd_l
            )

class series_descriptor(Descriptor):
    descriptor_tag = 0xd5

    series_id = 0x0

    repeat_label = 0x0

    program_pattern = 0x0

    expire_date_valid_flag = 0x0

    def bytes(self):
        snc_l = string.join(
                map(lambda x: pack("!B", x ), self.series_name_char)
            , "")

        fmt = "!HBHHH%ds" % (len(snc_l))

        return pack(fmt,
                self.series_id
                ,
                 0x00
                 | (self.repeat_label << 4)
                 | (self.program_pattern << 1)
                 | self.expire_date_valid_flag
                ,
                self.expire_date
                ,
                 0x0000
                 | (self.episode_number << 4)
                ,
                 0x0000
                 | (self.last_episode_number << 4)
                ,
                snc_l
            )

class service_event_loop_item(DVBobject):
    service_id = 0x0

    event_id = 0x0

    def pack(self):
        fmt = "!HH"

        return pack(fmt,
                self.service_id
                ,
                self.event_id
            )

class network_events_item(DVBobject):
    original_network_id = 0x0

    transport_stream_id = 0x0

    service_id = 0x0

    event_id = 0x0

    def pack(self):

        fmt = "!HHHH"

        return pack(fmt,
                self.original_network_id
                ,
                self.transport_stream_id
                ,
                self.service_id
                ,
                slef.event_id
            )

class event_group_descriptor(Descriptor):
    descriptor_tag = 0xd6

    group_type = 0x1

    def bytes(self):

        se_l = string.join(
                map(lambda x:x.pack(), self.service_event_loop)
            , "")

        fmt = "!B%ds" % (len(se_l))

        if (self.group_type == 4 or self.group_type == 5):

            nei_l = string.join(
                    map(lambda x:x.pack(), self.network_event_loop)
                , "")

            fmt += "%ds" % (len(nei_l))

            return pack(fmt,
                     0x00
                     | (self.group_type << 4)
                     | len(se_l)
                    ,
                    se_l
                    ,
                    nei_l
                )
        else:
            pdb_l = string.join(
                    map(lambda x:pack("!B", x), self.private_data_byte_loop)
                , "")

            fmt += "%ds" % (len(pdb_l))

            return pack(fmt,
                     0x00
                     | (self.group_type << 4)
                     | len(self.service_event_loop)
                    ,
                    se_l
                    ,
                    pdb_l

                )

class CA_unit_item(DVBobject):
    CA_unit_id = 0x0

    def pack(self):

        ct_l = string.join(
                map(lambda x:pack("!B", x), self.component_tag_loop)
            )

        fmt = "!B%ds" % (len(ct_l))

        return pack(fmt,
                 0x00
                 | (self.CA_unit_id << 4)
                 | len(self.component_tag_loop)
                ,
                ct_l
            )

class component_group_loop_item(DVBobject):
    component_group_id = 0x0

    def pack(self):

        cau_l = string.join(
                map(lambda x:x.pack(), self.ca_unit_loop)
            , "")

        fmt = "!B%ds" % (len(cau_l))

        if (self.total_bit_rate_flag == 1):
            tc_l = string.join(
                    map(lambda x:pack("!B", x), self.text_char)
                , "")

            fmt += "BB%ds" % (len(tc_l))

            return pack(fmt,
                     0x00
                     | (self.component_group_id << 4)
                     | len(ca_unit_loop)
                    ,
                    cau_l
                    ,
                    self.total_bit_rate
                    ,
                    len(self.text_char)
                    ,
                    tc_l
                )
        else:
            tc_l = string.join(
                    map(lambda x:pack("!B", x), self.text_char)
                , "")

            fmt += "B%ds" % (len(tc_l))

            return pack(fmt,
                     0x00
                     | (self.component_group_id << 4)
                     | len(ca_unit_loop)
                    ,
                    cau_l
                    ,
                    len(self.text_char)
                    ,
                    tc_l
                )

class component_group_descriptor(Descriptor):
    descriptor_tag = 0xd9

    component_group_type = 0x0

    total_bit_rate_flag = 0x0

    def bytes(self):
        cgi_l = string.join(
                map(lambda x:x.pack(), self.component_group_loop)
            ,"")

        fmt ="!B%ds" % (len(cgi_l))

        return pack(fmt,
                 0x00
                 | (self.component_group_type << 5)
                 | (self.total_bit_rate_flag << 4)
                 | len(self.component_group_loop)
                ,
                cgi_l
            )

class linkage_description_item(DVBobject):
    description_id = 0x0

    description_type = 0x1 # short event descriptor

    def pack(self):
        fmt = "!HBB"

        return pack(fmt,
                self.description_id
                ,
                 0x00
                 | (0xf << 4)
                 | self.description_type
                ,
                0x0
            )

class LDT_linkage_descriptor(Descriptor):
    descriptor_tag = 0xdc

    original_service_id = 0x0

    transport_stream_id = 0x0

    original_network_id = 0x0

    def bytes(self):
        ld_l = string.join(
                map(lambda x:x.pack(), self.linkage_description_loop)
            , "")

        fmt = "!HHH%ds" % (len(ld_l))

        return pack(fmt,
                self.original_service_id
                ,
                self.transport_stream_id
                ,
                self.original_network_id
                ,
                ld_l
            )

class deferred_service_location_item(DVBobject):
    org_network_id =0x0

    def pack(self):
        pdb_l = string.join(
                map(lambda x:pack("!B", x), self.private_data_byte_loop)
            , "")
        fmt ="!H%ds" % (len(pdb_l))

        return pack(fmt,
                self.org_network_id
                ,
                pdb_l
            )

class deferred_association_tags_descriptor(Descriptor):

    descriptor_tag = 0x15

    transport_stream_id = 0x0

    program_number = 0x0

    def bytes(self):

        at_l = string.join(
                map(lambda x:pack("!H", x), self.association_tag_loop)
            , "")

        dsl_l = string.join(
                map(lambda x:x.pack(), self.deferred_service_location_loop)
            , "")
        fmt = "!B%dsHH%ds" % (len(at_l), len(dsl_l))

        return pack(fmt,
                len(at_l)
                ,
                at_l
                ,
                self.transport_stream_id
                ,
                self.program_number
                ,
                dsl_l
            )

class basic_local_event_descriptor(Descriptor):
    descriptor_tag = 0xd0

    segmentation_mode = 0x2

    segmentation_info_length = 0x0

    def bytes(self):

        fmt = "!BB"

        if (self.segmentation_mode == 0x0):
            ct_l = string.join(
                    map(lambda x:pack("!B", x), self.component_tag_loop)
                , "")

            fmt += "%ds" % len(ct_l)

            return pack(fmt,
                     0x00
                     | (0xf << 4)
                     | self.segmentation_mode
                    ,
                    self.segmentation_info_length
                    ,
                    ct_l
                )

        elif self.segmentation_mode == 0x1:

            ct_l = string.join(
                    map(lambda x:pack("!B", x), self.component_tag_loop)
                , "")

            fmt += "BQBQ%ds" % len(ct_l)

            self.segmentation_info_length = 80 + len(ct_l)

            return pack(fmt,
                     0x00
                     | (0xf << 4)
                     | self.segmentation_mode
                    ,
                    self.segmentation_info_length
                    ,
                     0x00
                     | (0x7f << 1)
                    ,
                     0x0000000000000000
                     | (self.start_time_NPT << 31)
                    ,
                     0x00
                     | (0x7f << 1)
                    ,
                     0x0000000000000000
                     | (self.end_time_NPT << 31)
                    ,
                    ct_l
                )

        elif (self.segmentation_mode < 6 ):
            fmt += "LL"

            if (self.segmentation_info_length == 10):
                ct_l = string.join(
                    map(lambda x:pack("!B", x), self.component_tag_loop)
                , "")

                fmt += "HH%ds" % len(ct_l)

                return pack(fmt,
                     0x00
                      | (0xf << 4)
                      | self.segmentation_mode
                   ,
                   self.segmentation_info_length
                   ,
                    0x00000000
                    | (self.start_time << 8)
                   ,
                    0x00000000
                    | (self.duration << 8)
                   ,
                    0x0000
                    | (self.start_time_extension << 4)
                    | 0xf
                   ,
                    0x0000
                    | (self.duration_extension << 4)
                    | 0xf

                )

            else:
                ct_l = string.join(
                      map(lambda x:pack("!B", x), self.component_tag_loop)
                  , "")

                fmt += "%ds" % len(ct_l)

                self.segmentation_info_length = 48

                return pack(fmt,
                     0x00
                      | (0xf << 4)
                      | self.segmentation_mode
                   ,
                   self.segmentation_info_length
                   ,
                    0x00000000
                    | (self.start_time << 8)
                   ,
                    0x00000000
                    | (self.duration << 8)
                   ,
                   ct_l
                )

        else:
            r_l = string.join(
                map(lambda x:pack("!B",x), self.reserved_loop)
            , "")

            ct_l = string.join(
                      map(lambda x:pack("!B", x), self.component_tag_loop)
                  , "")

            segmentation_info_length = len(r_l) + len(ct_l)

            fmt += "%ds%ds" % (len(r_l), len(ct_l))

            return pack(fmt,
                  0x00
                  | (0xf << 4)
                  | self.segmentation_mode
                 ,
                 self.segmentation_info_length
                 ,
                 r_l
                 ,
                 ct_l
            )

class application_icons_descriptor(Descriptor):
    descriptor_tag = 0x0b
    
    icon_locator_byte = []

    reserved_future_use = [] 
    
    icon_flags = 1

    def bytes(self):
    
        
        ilb = string.join(
            map(lambda x:pack("!B", x), self.icon_locator_byte)
        )

        rfu_l = string.join(
            map(lambda x:pack("!B", x), self.reserved_future_use)
        )

        fmt = "!B%dsH%ds" % (len(ilb), len(rfu_l))

        return pack(fmt,
                    len(ilb),
                    ilb,
                    self.icon_flags,
                    rfu_l
        )

class node_relation_descriptor(Descriptor):
    descriptor_tag = 0xd2

    reference_type = 0x0

    external_reference_flag = 0x0

    reference_node_id = 0x1

    reference_number = 0xff

    def bytes(self):

        fmt = "!B"

        if (self.external_reference_flag == 1):

            fmt += "HHHB"

            return pack(fmt,
                     0x00
                     | (self.reference_type << 4)
                     | (self.external_reference_flag << 3)
                     | 0x7
                    ,
                    self.information_provider_id
                    ,
                    self.event_relation_id
                    ,
                    self.reference_node_id
                    ,
                    self.reference_number
                )
        else:

            fmt += "HB"

            return pack(fmt,
                    0x00
                     | (self.reference_type << 4)
                     | (self.external_reference_flag << 3)
                     | 0x7
                    ,
                    self.reference_node_id
                    ,
                    self.reference_number

                )

           
class STC_reference_descriptor(Descriptor):
    descriptor_tag = 0xd4

    external_event_flag = 0x0

    STC_reference_mode = 0x1

    def bytes(self):

        fmt = "!B"

        if (self.external_event_flag == 0x1):

            fmt += "HHH"

            if (self.STC_reference_mode == 0):
                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                        self.external_event_id
                        ,
                        self.external_service_id
                        ,
                        self.external_network_id

                    )

            elif (self.STC_reference_mode == 1):

                fmt += "BQBQ"

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                        self.external_event_id
                        ,
                        self.external_service_id
                        ,
                        self.external_network_id
                        ,
                         0x00
                         | 0x7f
                        ,
                         0x0000000000000000
                         | (NPT_reference << 31)
                        ,
                         0x00
                         | 0x7f
                        ,
                         0x0000000000000000
                         | (STC_reference << 31)

                    )

            elif (self.STC_reference_mode == 3 or self.STC_reference_mode == 5):
                fmt += "LHHQ"

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                        self.external_event_id
                        ,
                        self.external_service_id
                        ,
                        self.external_network_id
                        ,
                         0x00000000
                         | (self.time_reference << 8)
                        ,
                         0x0000
                         | (self.time_reference_extention << 4)
                        ,
                         0x0000
                         | (0x7ff)
                        ,
                         0x0000000000000000
                         | (self.STC_reference << 31)

                    )
            else:
                r_l = string.join(
                        map(lambda x:pack("!B", x), self.reserved_loop)
                    ,"")

                fmt += "%ds" % len(r_l)

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                        self.external_event_id
                        ,
                        self.external_service_id
                        ,
                        self.external_network_id
                        ,
                        r_l
                    )
        else:
            if (self.STC_reference_mode == 0):
                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)

                    )

            elif (self.STC_reference_mode == 1):

                fmt += "BQBQ"

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                         0x00
                         | 0x7f
                        ,
                         0x0000000000000000
                         | (NPT_reference << 31)
                        ,
                         0x00
                         | 0x7f
                        ,
                         0x0000000000000000
                         | (STC_reference << 31)

                    )

            elif (self.STC_reference_mode == 3 or self.STC_reference_mode == 5):
                fmt += "LHHQ"

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                         0x00000000
                         | (self.time_reference << 8)
                        ,
                         0x0000
                         | (self.time_reference_extention << 4)
                        ,
                         0x0000
                         | (0x7ff)
                        ,
                         0x0000000000000000
                         | (self.STC_reference << 31)

                    )
            else:
                r_l = string.join(
                        map(lambda x:pack("!B", x), self.reserved_loop)
                    ,"")

                fmt += "%ds" % len(r_l)

                return pack(fmt,
                         0x00
                         | (0x7 << 5)
                         | (self.external_event_flag << 4)
                         | (self.STC_reference_mode)
                        ,
                        r_l
                    )



# TODO - finish
class additional_ginga_info(DVBobject):
    transmission_format = 0xa
    application_identifier_flag = 0x1
