import pandas as pd
import random
import math
import re
import stringdist
class Lyrics(): 
    """
    Class to manage lyric generation.

    Args:
        data: A pandas dataframe containing artist lyrics
    """
    def __init__(self, data):
        """Constructor"""

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
        """
        Method that returns the generated lyrics, given a game difficulty.

        Args:
            mode: A string specifying the game difficulty (i.e., whether to 
                  generate a whole section, 2 lines, or 1 line)
        
        Returns: 
            An HTML-formatted string containing the generated lyrics.
        """

        self.rand_num = random.randint(0, self.data.shape[0] - 1)

        if mode == "Hard (1 line)": 
            self.start_line = self.rand_num
            self.end_line = self.rand_num
            return self.data["lyric"][self.rand_num]
        
        if mode == "Medium (2 lines)": 
            track_name = self.data["track_name"][self.rand_num]
            # check if next line is from same song; it not, give previous line
            if (self.rand_num <= self.data.shape[0] - 1) and (self.data["track_name"][self.rand_num + 1] == track_name): 
                self.start_line = self.rand_num
                self.end_line = self.rand_num + 1
            else: 
                self.start_line = self.rand_num - 1
                self.end_line = self.rand_num

            return "<br>".join(self.data["lyric"][self.start_line:self.end_line + 1].tolist())
        
        else: 
            rand_section = self.data["element"][self.rand_num]
            # continue adding lines until section differs
            self.start_line = self.rand_num
            while (self.start_line > 0) and (self.data["element"][self.start_line - 1] == rand_section): 
                self.start_line -= 1

            self.end_line = self.rand_num
            while (self.end_line < self.data.shape[0] - 1) and (self.data["element"][self.end_line + 1] == rand_section): 
                self.end_line += 1

            return "<br>".join(self.data["lyric"][self.start_line:self.end_line + 1].tolist())
    
    def get_track_name(self): 
        """
        Method that returns the name of the track whose lyrics were returned.

        Returns: 
            The correct track name.
        """
        return self.data["track_name"][self.rand_num]
    
    def get_album_name(self): 
        """
        Method that returns the album of the track whose lyrics were returned.

        Returns: 
            The correct album name.
        """
        return self.data["album_name"][self.rand_num]
    
    def get_previous_line(self):
        """
        Method that returns the line prior to the generated lyrics.

        Returns:
            The line prior to the generated lyrics; if there is nothing prior (
            i.e., the generated lyrics was the very beginning of the song),
            "N/A" is returned.
        """
        if (self.start_line > 0) and (self.data["track_name"][self.start_line - 1] == self.get_track_name()):
            return self.data["lyric"][self.start_line - 1]
        return "N/A"

    def get_next_line(self):
        """
        Method that returns the line following the generated lyrics.

        Returns:
            The line following the generated lyrics; if there is nothing 
            following (i.e., the generated lyrics was the end of the song),
            "N/A" is returned.
        """
        if (self.end_line < self.data.shape[0] - 1) and (self.data["track_name"][self.end_line + 1] == self.get_track_name()):
            return self.data["lyric"][self.end_line + 1]
        return "N/A"
    
    def get_section(self):
        """
        Returns the section of the generated lyrics.

        Returns:
            The section (e.g. Chorus, Verse 1, etc.) of the generated lyrics.
        """
        return self.data["element"][self.rand_num]
    
    def get_guess_feedback(self, guess): 
        """
        Returns a boolean indicating whether a user guess was correct or
        incorrect. Capitalization is waived, as are minor (within 1/3 of the
        track name's length) spelling mistakes.

        Returns:
            A boolean; True if the guess is "correct," False otherwise.
        """
        correct_song = self.get_track_name()
        # exceptions where the parentheses should be included in the guess
        if correct_song not in ["Mary's Song (Oh My My My)", 
                                "I Can Fix Him (No Really I Can)"]:
            # remove parentheses (e.g. Taylor's Version) from track name
            correct_song = re.sub(r"\([^)]*\)", "", correct_song).strip()
        guess = guess.strip()
        # allowing for minor typos
        track_name_length = len(correct_song)
        allowed_diff = math.ceil(track_name_length * 0.33)
        if stringdist.levenshtein(guess.lower(), correct_song.lower()) <= allowed_diff: 
            return True
        return False