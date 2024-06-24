import random
import pandas as pd
import numpy as np
import time

data = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
mode_options = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]

def generate_lyric(data, mode): 
    rand_num = random.randint(0, data.shape[0])

    if mode == "Hard (1 line)": 
        return data["lyric"][rand_num]
    if mode == "Medium (2 lines)": 
        track_name = data["track_name"][rand_num]
        # check if next line is from same song
        if data["track_name"][rand_num + 1] == track_name: 
            start = rand_num
            end = rand_num + 1
        else: 
            start = rand_num - 1
            end = rand_num
        return "<br>".join(data["lyric"][start:end + 1].tolist())
    else: 
        rand_section = data["element"][rand_num]

        start = rand_num
        while data["element"][start - 1] == rand_section: 
            start -= 1
        end = rand_num
        while data["element"][end + 1] == rand_section: 
            end += 1
        return "<br>".join(data["lyric"][start:end + 1].tolist())