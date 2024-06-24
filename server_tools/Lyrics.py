import pandas as pd
import random
import time

data = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")

class Lyrics(): 

    def __init__(self, data):
        self.data = data
        self.rand_num = None
        self.track_name = None

    def generate(self, mode):
        self.rand_num = random.randint(0, self.data.shape[0])
        if mode == "Hard (1 line)": 
            return self.data["lyric"][self.rand_num]
        if mode == "Medium (2 lines)": 
            track_name = self.data["track_name"][self.rand_num]
            # check if next line is from same song
            if self.data["track_name"][self.rand_num + 1] == track_name: 
                start = self.rand_num
                end = self.rand_num + 1
            else: 
                start = self.rand_num - 1
                end = self.rand_num
            return "<br>".join(self.data["lyric"][start:end + 1].tolist())
        else: 
            rand_section = self.data["element"][self.rand_num]

            start = self.rand_num
            while self.data["element"][start - 1] == rand_section: 
                start -= 1
            end = self.rand_num
            while self.data["element"][end + 1] == rand_section: 
                end += 1
            return "<br>".join(self.data["lyric"][start:end + 1].tolist())
    
    def get_track_name(self): 
        return self.data["track_name"][self.rand_num]
    
lyrics = Lyrics(data)
print(lyrics.generate("Medium (2 lines)"))
print(lyrics.get_track_name())