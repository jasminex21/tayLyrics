import random
import math
import re
import stringdist
import pandas as pd
from typing import Optional, List

class Lyrics(): 
    """
    Class to manage lyric generation.

    Args:
        data: 
            A pandas dataframe containing artist lyrics
    """
    def __init__(self, data: pd.DataFrame):
        """Constructor"""

        self.data = data
        self.rand_num = None
        self.start_line = None
        self.end_line = None

    def generate(self, mode: str) -> str:
        """
        Method that returns the generated lyrics, given a game difficulty.

        Args:
            mode: 
                A string specifying the game difficulty (i.e., whether to 
                generate a whole section, 2 lines, or 1 line)
        
        Returns: 
            An HTML-formatted string containing the generated lyrics.
        """

        self.rand_num = random.randint(0, self.data.shape[0] - 1)
        track_name = self.data["track_name"][self.rand_num]

        if mode == "Hard (1 line)": 
            self.start_line = self.rand_num
            self.end_line = self.rand_num
            return self.data["lyric"][self.rand_num]
        
        if mode == "Medium (2 lines)": 
            # check if next line is from same song; it not, give previous line
            if ((self.rand_num <= self.data.shape[0] - 1) 
                and (self.data["track_name"][self.rand_num + 1] == track_name)): 
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
            while ((self.start_line > 0) 
                   and (self.data["element"][self.start_line - 1] == rand_section) 
                   and (self.data["track_name"][self.start_line - 1] == track_name)): 
                self.start_line -= 1

            self.end_line = self.rand_num
            while ((self.end_line < self.data.shape[0] - 1) 
                   and (self.data["element"][self.end_line + 1] == rand_section)
                   and (self.data["track_name"][self.end_line + 1] == track_name)): 
                self.end_line += 1

            return "<br>".join(self.data["lyric"][self.start_line:self.end_line + 1].tolist())
    
    def get_track_name(self) -> str: 
        """
        Method that returns the name of the track whose lyrics were returned.

        Returns: 
            The correct track name.
        """
        return self.data["track_name"][self.rand_num]
    
    def get_album_name(self) -> str: 
        """
        Method that returns the album of the track whose lyrics were returned.

        Returns: 
            The correct album name.
        """
        return self.data["album_name"][self.rand_num]
    
    def get_previous_line(self) -> str:
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

    def get_next_line(self) -> str:
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
    
    def get_section(self) -> str:
        """
        Returns the section of the generated lyrics.

        Returns:
            The section (e.g. Chorus, Verse 1, etc.) of the generated lyrics.
        """
        return self.data["element"][self.rand_num]
    
    def get_guess_feedback(self, guess: str, 
                           acceptable_answers: Optional[dict]=None,
                           remove_parentheses: Optional[bool]=False, 
                           keep_parentheses: Optional[List]=None) -> bool: 
        """
        Returns a boolean indicating whether a user guess was correct or
        incorrect. Capitalization is waived, as are minor (within 1/3 of the
        track name's length) spelling mistakes.

        Args: 
            guess: 
                The user's guess as a string
            
            acceptable_answers: 
                Optional parameter, formatted as a dict where the correct song is
                the key and the value is a list of acceptable answers, used to 
                specify acceptable answers for given songs

            remove_parentheses: 
                Optional parameter used to specify whether to remove parentheses
                within song titles. Useful if the artist's discography has 
                features, or if the artist is Taylor Swift
            
            keep_parentheses: 
                When remove_parentheses is True, this is an optional parameter 
                used to specify songs where the parentheses should not be removed. 
                Useful if you want to remove incidences of (feat. x) but not
                parentheses such as (Lobotomy) in Peach (Lobotomy) by Waterparks.
                Ignored when remove_parentheses is False.

        Returns:
            A boolean; True if the guess is "correct," False otherwise.
        """
        correct_song = self.get_track_name()
        # other accepted answers - e.g. just "Gladiator" is accepted for Gladiator (Interlude)
        accepted_songs = acceptable_answers[correct_song] if correct_song in acceptable_answers else []
        # exceptions where the parentheses should be included in the guess
        if remove_parentheses:
            if correct_song not in keep_parentheses:
                # remove parentheses (e.g. Taylor's Version) from track name
                correct_song = re.sub(r"\([^)]*\)", "", correct_song).strip()
        guess = guess.strip()
        # allowing for minor typos
        for accepted in [correct_song] + accepted_songs: 
            track_name_length = len(accepted)
            allowed_diff = math.ceil(track_name_length * 0.33)
            if stringdist.levenshtein(guess.lower(), accepted.lower()) <= allowed_diff: 
                return True
        return False