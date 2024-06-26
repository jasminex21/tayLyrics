import pandas as pd
import random
import time
import math
import re
import stringdist

data = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")

class Lyrics(): 

    def __init__(self, data):
        self.data = data
        self.rand_num = None

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
    
    def get_album_name(self): 
        return self.data["album_name"][self.rand_num]
    
    def get_guess_feedback(self, guess): 
        # remove parentheses (e.g. Taylor's Version) from track name
        correct_song = re.sub(r"\([^)]*\)", "", self.get_track_name()).strip()
        # remove whitespace from guess
        guess = guess.strip()
        # allowing for minor typos
        track_name_length = len(correct_song)
        allowed_diff = math.ceil(track_name_length * 0.33)
        if stringdist.levenshtein(guess.lower(), correct_song.lower()) <= allowed_diff: 
            return True
        return False