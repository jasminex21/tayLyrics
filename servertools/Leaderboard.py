import pandas as pd
import sqlite3

class Leaderboards:
    """
    A class that manages leaderboards via a SQLite database. 

    Args: 
        db_path: The path to the database.
    """

    def __init__(self, db_path="leaderboard.db"):

        """
        Constructor
        """

        self.db_path = db_path
        self.table_names = [f"leaderboard_{diff}" for diff in ["easy", "medium", "hard"]]
        self.difficulty_mapping = {"Easy (an entire section, e.g. chorus)": "easy", 
                                   "Medium (2 lines)": "medium", 
                                   "Hard (1 line)": "hard"}

    def __enter__(self):
        """
        Connects the database and creates the leaderboards for each
        difficulty if they do not already exist.
        """

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically closes the database connection.
        """

        self.connection.close()

    def create_tables(self):
        """
        Method that creates the three leaderboards (one for each difficulty) if
        they do not already exist.
        """
        
        for table_name in self.table_names:
            create_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                points INTEGER NOT NULL,
                                rounds INTEGER NOT NULL,
                                datetime TEXT NOT NULL)"""
            self.cursor.execute(create_query)
            self.connection.commit()
    
    def add_to_leaderboard(self, difficulty, results):
        """
        Method that adds a user's results to the corresponding leaderboard.

        Args: 
            difficulty: A string specifying the game difficulty; this 
                        determines which leaderboard the results are added to.

            results: A tuple (name, points, rounds, points, datetime) containing the user's 
            game results.
        """
        
        db_difficulty = self.difficulty_mapping[difficulty]
        add_query = f"""INSERT INTO leaderboard_{db_difficulty} (name, points, rounds, datetime)
                        VALUES (?, ?, ?, ?)"""
        self.cursor.execute(add_query, results)
        self.connection.commit()

    def get_leaderboards(self):
        """
        Method that returns the most updated leaderboards, each ranked by the
        number of points the users have earned.

        Returns: 
            A dictionary containing the leaderboards (as pandas dataframes) 
            for each difficulty.
        """

        all_leaderboards = {}
        columns = ["ID", "Name", "Points", "Rounds", "Datetime (EST)"]
        final_cols = ["Rank", "Name", "Points", "Rounds", "Datetime (EST)"]

        for table_name, long_name in zip(self.table_names, list(self.difficulty_mapping.keys())): 
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()

            df = pd.DataFrame(rows, columns=columns)
            df["Datetime (EST)"] = pd.to_datetime(df["Datetime (EST)"])
            # the primary determinator of rank is the number of points earned
            df = df.sort_values(by=["Points", "Rounds", "Datetime (EST)"], ascending=[False, False, True])
            df["Rank"] = df[["Points"]].rank(method="first", ascending=False).astype(int)
            final_df = df[final_cols].set_index("Rank")
            all_leaderboards[long_name] = final_df
        
        return all_leaderboards