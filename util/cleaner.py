import re

def clean_rename_channel(Rawdata,use_ch):
    replace_dict = {}
    drop_list = []
    # for the channel names in the data...
    for channel_name in Rawdata.info['ch_names']:
        if channel_name in use_ch:
            continue
        name_change=None
        if re.findall('\w+',channel_name)[0] in ['E','P']:
            # print(channel_name)
            # if not re.findall('ROC|LOC|EKG|26|27|28|29|30|T1|T2',channel_name):
            if not re.findall('ROC|LOC|EKG|26|27|28|29|30',channel_name):
                name_change = re.findall('\w+',channel_name)[1].title()
            else:
                drop_list.append(channel_name)
        else:
            drop_list.append(channel_name)        
        if name_change:
            # check if it is already in the change list
            if name_change in list(replace_dict.values()):
                drop_list.append(channel_name)
            else:
                # if its not already there get the origional name and what we want to 
                # change it to
                replace_dict[channel_name] = name_change    
    # drop the ones that would be repeats
    Rawdata.drop_channels(drop_list)
    # rename the channels
    Rawdata.rename_channels(replace_dict)

    return Rawdata