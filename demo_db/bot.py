import uuid
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
import sqlite3

from faker import Faker

logging.basicConfig(level=logging.INFO, format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d-%b-%y %H:%M:%S')

BASE_PATH = Path(__file__).parent.parent.absolute()
DB_FILE = Path(f'{BASE_PATH}/sqlite3.db')


load_dotenv(BASE_PATH / '.env')

NUMBER_OF_USERS = os.getenv('NUMBER_OF_USERS')
MAX_POSTS_PER_USER = os.getenv('MAX_POSTS_PER_USER')
MAX_LIKES_PER_USER = os.getenv('MAX_LIKES_PER_USER')


def clear_tables() -> None:
    with create_connection(DB_FILE) as connection:
        try:
            connection.execute('DELETE FROM users;', )
            connection.execute('DELETE FROM posts;', )
            connection.execute('DELETE FROM likes;', )

        except sqlite3.Error as e:
            logging.error(f"clear_tables(): {e}")


def create_connection(db_file: Path) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        logging.error(e)


def sign_up_users(faker: Faker) -> None:
    with create_connection(DB_FILE) as connection:
        try:
            sqlite_insert_query = """INSERT INTO users
                              (id, email, password, verification_token, date_created, date_updated, date_deleted, 
                              date_logged) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

            record_list: list[tuple] = []
            if NUMBER_OF_USERS is None:
                logging.error("NUMBER_OF_USERS in config file is empty")
                return

            for _ in range(int(NUMBER_OF_USERS)):
                record_list.append(
                    (str(uuid.uuid4()), faker.email(), faker.password(), faker.word(), faker.date(), faker.date(), None,
                     faker.date())
                )

            connection.executemany(sqlite_insert_query, record_list)
        except sqlite3.Error as e:
            logging.error(f"sign_up_users(): {e}")


def create_posts() -> None:
    ...


def like_activity() -> None:
    ...


def get_users_statistics() -> None:
    with create_connection(DB_FILE) as connection:
        try:
            sqlite_query = """SELECT * from Users"""
            users = connection.execute(sqlite_query)

            for user in users:
                print(user)
        except sqlite3.Error as e:
            logging.error(f"get_users_statistics(): {e}")


def get_posts_statistics() -> None:
    ...


def get_like_activity_statistics() -> None:
    ...


def main() -> None:
    clear_tables()

    fake = Faker()
    sign_up_users(fake)
    # create_posts()
    # like_activity()
    #
    get_users_statistics()
    # get_posts_statistics()
    # get_like_activity_statistics()


if __name__ == "__main__":
    main()
