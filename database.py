import sqlite3
import os

class HighScores:
    def __init__(self):
        self.conn = sqlite3.connect("scores.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='high_scores' ''')
        if self.cursor.fetchone()[0]==1:
            print("Table exists")
        else:
            self.cursor.execute("""CREATE TABLE high_scores (
                            user_name text,
                            score INTEGER
                    )""")

    def __del__(self):
        self.conn.close()
        print("Database Closed")

    def update(self, username, score):
        self.cursor.execute("SELECT user_name,score FROM high_scores WHERE user_name = ?",(username,))
        row = [(username, score)]
        player = self.cursor.fetchall()
        if not player:
            self.cursor.executemany("INSERT INTO high_scores (user_name, score) VALUES (?, ?)",row )
        elif player[0][1]<score:
            self.cursor.execute("UPDATE high_scores SET score = ? WHERE user_name = ?", row[0][::-1])

        self.conn.commit()
        self.cursor.execute("SELECT * FROM high_scores")
        items = self.cursor.fetchall()
        for item in items:
            print(item)

        self.conn.commit()

    # def del_rows(self):
    #     self.cursor.executemany("DELETE FROM high_scores WHERE rowid = ?", [1,2,3,4,5,6])
    #     self.conn.commit()