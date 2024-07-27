import pandas as pd
import sqlite3

class Leaderboards:

    def __init__(self, db_path="/home/jasmine/tayLyrics_v2/tayLyrics/leaderboard.db"):

        self.db_path = db_path
        self.table_names = [f"leaderboard_{diff}" for diff in ["easy", "medium", "hard"]]
        self.difficulty_mapping = {"Easy (an entire section, e.g. chorus)": "easy", 
                                   "Medium (2 lines)": "medium", 
                                   "Hard (1 line)": "hard"}

    def __enter__(self):

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):

        self.connection.close()

    def create_tables(self):
        
        for table_name in self.table_names:
            create_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                rounds INTEGER NOT NULL,
                                points_of_possible TEXT NOT NULL,
                                datetime TEXT NOT NULL,
                                points_of_possible_pct REAL NOT NULL)"""
            self.cursor.execute(create_query)
            self.connection.commit()
    
    def add_to_leaderboard(self, difficulty, results):
        
        db_difficulty = self.difficulty_mapping[difficulty]
        add_query = f"""INSERT INTO leaderboard_{db_difficulty} (name, rounds, points_of_possible, datetime, points_of_possible_pct)
                        VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(add_query, results)
        self.connection.commit()

    def get_leaderboards(self):

        all_leaderboards = {}
        columns = ["ID", "Name", "Rounds", "Points of possible", "Datetime", "Points of Possible pct."]
        final_cols = ["Rank", "Name", "Rounds", "Points of possible", "Datetime"]

        for table_name, long_name in zip(self.table_names, list(self.difficulty_mapping.keys())): 
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()

            df = pd.DataFrame(rows, columns=columns)
            df["Datetime"] = pd.to_datetime(df["Datetime"])
            df = df.sort_values(by=["Rounds", 'Points of Possible pct.', "Datetime"], ascending=[False, False, True])
            df["Rank"] = df[["Rounds"]].rank(method="first", ascending=False).astype(int)
            final_df = df[final_cols].set_index("Rank")
            all_leaderboards[long_name] = final_df
        
        return all_leaderboards