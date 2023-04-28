import pathlib
import sqlite3


class SQLiteCursor:

    def __init__(self, db_path=pathlib.Path().resolve() / "keys_db"):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, _type, value, traceback):
        self.conn.commit()
        self.conn.close()


def create_tables():
    with SQLiteCursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS k (
                key_type TEXT NOT NULL PRIMARY KEY,
                key TEXT NOT NULL
            )
        """)


def add_keys(key_type, key):
    with SQLiteCursor() as cur:
        cur.execute("""
            INSERT OR REPLACE INTO k (key_type, key) VALUES (?, ?)
        """, (key_type, key))


def remove_key(key_type):
    with SQLiteCursor() as cur:
        cur.execute("""
            DELETE FROM k where key_type = ?
        """, (key_type,))


def get_all_keys():
    with SQLiteCursor() as cur:
        cur.execute("SELECT * FROM k")

        if r := cur.fetchall():
            return {
                "status": True,
                "payload": [(i["key_type"], i["key"]) for i in r]
            }

        return {
            "status": False,
            "payload": None
        }


def main():
    create_tables()
    add_keys("a", "b")
    add_keys("c", "b")

    print(get_all_keys())


if __name__ == '__main__':
    main()
