import joblib
import pandas as pd
import mne
import re
import util.feature_extraction as fe
import lightgbm

class ModelHandler:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)
        self.sampling = 256  
        self.low_freq = 0
        self.high_freq = 60
        self.use_channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7','T8','P7','P8','P9','P10', 'Fz', 'Cz', 'Pz','F9','F10','T9','T10']          
        self.wavelet_family = "db4"
        self.window_size = 256
        self.decomp_level = 5

    def load_model(self, model_path):
        return joblib.load(model_path)

    def clean_rename_channel(self, Rawdata):
        replace_dict = {}
        drop_list = []
        for channel_name in Rawdata.info['ch_names']:
            if channel_name in self.use_channels:
                continue
            name_change=None
            if re.findall('\w+',channel_name)[0] in ['E','P']:
                if not re.findall('ROC|LOC|EKG|26|27|28|29|30',channel_name):
                    name_change = re.findall('\w+',channel_name)[1].title()
                else:
                    drop_list.append(channel_name)
            else:
                drop_list.append(channel_name)        
            if name_change:
                if name_change in list(replace_dict.values()):
                    drop_list.append(channel_name)
                else:
                    replace_dict[channel_name] = name_change    
        Rawdata.drop_channels(drop_list)
        Rawdata.rename_channels(replace_dict)
        return Rawdata

    def clean_data(self, raw):
        raw.filter(l_freq=self.low_freq, h_freq=self.high_freq, skip_by_annotation='edge', filter_length=len(raw)-1, verbose=False)
        raw.resample(self.sampling, npad='auto', verbose=0)
        return self.clean_rename_channel(raw)

    def segment_annotated(self, times, onset_in_seconds, df):
        df["time"] = times
        df["index"] = df.index

        decimal_places = 3
        onset_trunc = int(onset_in_seconds * 10**decimal_places) / 10**decimal_places
        
        onset_index = int(df[df["time"] >= onset_trunc].iloc[0]["index"])
        df["label"] = 0
        start_label = onset_index - int(self.window_size/2)
        end_label = onset_index + int(self.window_size/2)
        df.loc[(df["index"] >= start_label) & (df["index"] <= end_label), "label"] = 1

        crop_duration = 1 * self.sampling #1 second crops
        start_index = onset_index -  crop_duration // 2

        # Calculate the end index for cropping
        end_index = min(len(df), start_index + crop_duration)
        cropped_df = df.loc[(df["index"] >= start_index) & (df["index"] <= end_index)].drop(columns = ["time", "index", "label"])
        return cropped_df

    def extract_feature(self, df):
            power_measure = fe.power_measure_channels(df, self.sampling)
            wavelets = fe.wavelet_decompose_channels(df, level=self.decomp_level)
            absolute_sums_log = fe.log_sum_channels(wavelets)
            wavelet_mean = fe.ave_channels(wavelets)
            mean_abs = fe.mean_abs_channels(wavelets)
            std = fe.coeff_std_channels(wavelets)
            ratio_data = wavelets.mean().unstack('channel').apply(fe.ratio_channels)
            ratio_data = fe.reformat(ratio_data, 'Ratio_Mean_')
            res = pd.concat([power_measure, absolute_sums_log, wavelet_mean, mean_abs, std, ratio_data], axis=1) 
            
            return res[sorted(list(res.columns))]

    def preprocess_data(self, raw):
        #TODO: standardize raw
        cleaned_data = self.clean_data(raw)
        #TODO: convert to dataframe
        df = pd.DataFrame(cleaned_data.get_data().T, columns=cleaned_data.ch_names)
        times = cleaned_data.times
        onset_in_seconds = cleaned_data.annotations[-1]["onset"]    
        #TODO: segment dataframe
        segment = self.segment_annotated(times, onset_in_seconds, df)
        #TODO: extract feature
        return self.extract_feature(segment)

    def predict(self, raw):
        processed_data = self.preprocess_data(raw)
        prediction = (self.model.predict(processed_data)).tolist()[0]
        if prediction == 0:
            return 'Non-Epileptic';
        else:
            return 'Epileptic';