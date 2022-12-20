import sqlite3
import pickle
import numpy as np
from typing import List

class PickleSQLiteHelper:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name: str):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, image BLOB, location BLOB, pickle BLOB)")
        self.conn.commit()

    def insert_pickle(self, table_name, id: int, image: np.ndarray, location: List[int], pickle_obj: bytes):
        # Convert the image and location to binary strings
        image_str = image.tobytes()
        location_str = pickle.dumps(location)
        # Convert the pickle object to a binary string
        pickle_str = pickle.dumps(pickle_obj)
        # Insert the binary strings into the table as blobs
        self.cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", (id, image_str, location_str, pickle_str))
        self.conn.commit()
        return self.cursor.lastrowid

    def retrieve_pickle(self, table_name: str, id: int):
        self.cursor.execute(f"SELECT image, location, pickle FROM {table_name} WHERE id=?", (id,))
        # Retrieve the image, location, and pickle object from the binary strings
        row = self.cursor.fetchone()
        image = np.frombuffer(row[0], dtype=np.uint8).reshape((1, -1))
        location = pickle.loads(row[1])
        pickle_obj = pickle.loads(row[2])
        return image, location, pickle_obj



    def retrieve_pickles_in_range(self, table_name: str, min_location: int, max_location: int):
        self.cursor.execute(f"SELECT image, location, pickle FROM {table_name} WHERE location BETWEEN ? AND ?", (min_location, max_location))
        rows = self.cursor.fetchall()
        # Retrieve the image, location, and pickle object for each row
        results = []
        for row in rows:
            image = np.frombuffer(row[0], dtype=np.uint8).reshape((1, -1))
            location = pickle.loads(row[1])
            pickle_obj = pickle.loads(row[2])
            results.append((image, location, pickle_obj))
        return results

if __name__ == '__main__':
    databasehelper = PickleSQLiteHelper('databases/test.db')
    databasehelper.create_table('test')
    last_row = databasehelper.insert_pickle('test', 1, np.zeros(shape= (3,480,640)), [1, 2, 3], pickle.dumps({'a': 1, 'b': 2, 'c': 3}))
    print(last_row)
    print(databasehelper.retrieve_pickle('test', 1))

