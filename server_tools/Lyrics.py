import pandas as pd
import random
import time
import math
import re
import stringdist

data = pd.read_csv("/home/jasmine/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")

class Lyrics(): 

    def __init__(self, data):
        self.data = data
        self.rand_num = None
        self.start_line = None
        self.end_line = None
    
    def set_random_seed(seed):
        try: 
            random.seed(int(seed))
        except ValueError: 
            return "Seed must be a valid integer, such as 21 or 2003."

    def generate(self, mode):
        self.rand_num = random.randint(0, self.data.shape[0])
        if mode == "Hard (1 line)": 
            self.start_line = self.rand_num
            self.end_line = self.rand_num
            return self.data["lyric"][self.rand_num]
        if mode == "Medium (2 lines)": 
            track_name = self.data["track_name"][self.rand_num]
            # check if next line is from same song
            if self.data["track_name"][self.rand_num + 1] == track_name: 
                self.start_line = self.rand_num
                self.end_line = self.rand_num + 1
            else: 
                self.start_line = self.rand_num - 1
                self.end_line = self.rand_num
            return "<br>".join(self.data["lyric"][self.start_line:self.end_line + 1].tolist())
        else: 
            rand_section = self.data["element"][self.rand_num]

            self.start_line = self.rand_num
            while self.data["element"][self.start_line - 1] == rand_section: 
                self.start_line -= 1
            self.end_line = self.rand_num
            while self.data["element"][self.end_line + 1] == rand_section: 
                self.end_line += 1
            return "<br>".join(self.data["lyric"][self.start_line:self.end_line + 1].tolist())
    
    def get_track_name(self): 
        return self.data["track_name"][self.rand_num]
    
    def get_album_name(self): 
        return self.data["album_name"][self.rand_num]
    
    def get_previous_line(self):
        if self.data["track_name"][self.start_line - 1] == self.get_track_name():
            return self.data["lyric"][self.start_line - 1]
        return "N/A"

    def get_next_line(self):
        if self.data["track_name"][self.end_line + 1] == self.get_track_name():
            return self.data["lyric"][self.end_line + 1]
        return "N/A"
    
    def get_section(self):
        return self.data["element"][self.rand_num]
    
    def get_guess_feedback(self, guess): 
        # remove parentheses (e.g. Taylor's Version) from track name
        correct_song = self.get_track_name()
        if correct_song not in ["Mary's Song (Oh My My My)", 
                                "I Can Fix Him (No Really I Can)"]:
            correct_song = re.sub(r"\([^)]*\)", "", correct_song).strip()
        # remove whitespace from guess
        guess = guess.strip()
        # allowing for minor typos
        track_name_length = len(correct_song)
        allowed_diff = math.ceil(track_name_length * 0.33)
        if stringdist.levenshtein(guess.lower(), correct_song.lower()) <= allowed_diff: 
            return True
        return False