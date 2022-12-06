import random
import uuid
from pathlib import Path
import os
from random import randrange

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
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        logging.error(e)
    finally:
        if conn is None:
            exit()
        return conn


def sign_up_users(faker: Faker) -> None:
    with create_connection(DB_FILE) as connection:
        try:
            record_list: list[tuple] = []
            sqlite_insert_query = """
                    INSERT INTO users 
                    (id, email, password, verification_token, date_created, date_updated, date_deleted, date_logged) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """

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
        finally:
            logging.info("Users created successfully")


def create_posts(faker: Faker) -> None:
    with create_connection(DB_FILE) as connection:
        try:
            record_list: list[tuple] = []
            users = connection.execute("""SELECT * FROM users""")

            for user in users:
                sqlite_insert_query = """INSERT INTO posts
                                  (id, author_id, title, description, date_created, date_updated, date_deleted) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?);"""

                if MAX_POSTS_PER_USER is None:
                    logging.error("MAX_POSTS_PER_USER in config file is empty")
                    return

                for _ in range(randrange(int(MAX_POSTS_PER_USER))):
                    record_list.append(
                        (str(uuid.uuid4()), user[0], str(uuid.uuid4()), faker.word(), faker.date(), faker.date(), None)
                    )
            connection.executemany(sqlite_insert_query, record_list)
        except sqlite3.Error as e:
            logging.error(f"create_posts(): {e}")
        finally:
            logging.info("Posts created successfully")


def like_activity(faker: Faker) -> None:
    with create_connection(DB_FILE) as connection:
        try:
            record_list: list[tuple] = []
            users = connection.execute("""SELECT * FROM users""")
            posts = connection.execute("""SELECT * FROM posts""").fetchall()

            for user in users:
                sqlite_insert_query = """INSERT INTO likes (id, user_id, post_id, date_created) VALUES (?, ?, ?, ?);"""

                if MAX_LIKES_PER_USER is None:
                    logging.error("MAX_LIKES_PER_USER in config file is empty")
                    return

                for _ in range(randrange(int(MAX_LIKES_PER_USER))):
                    post_id = random.choice(posts)[0]

                    record_list.append(
                        (str(uuid.uuid4()), user[0], post_id, faker.date())
                    )

            connection.executemany(sqlite_insert_query, record_list)
        except sqlite3.Error as e:
            logging.error(f"like_activity(): {e}")
        finally:
            logging.info("Likes created successfully")


def get_posts_statistics() -> None:
    with create_connection(DB_FILE) as connection:
        try:
            sqlite_query = """SELECT email AS name, count(posts.id) AS qty FROM users 
                            INNER JOIN posts ON posts.author_id == users.id
                            GROUP BY author_id 
                            ORDER BY qty 
                            DESC LIMIT 5
                            """
            posts = connection.execute(sqlite_query)
            logging.info("TOP 5 AUTHORS BY POST QUANTITY")
            for post in posts:
                logging.info(post)
        except sqlite3.Error as e:
            logging.error(f"get_posts_statistics(): {e}")


def get_like_activity_statistics() -> None:
    with create_connection(DB_FILE) as connection:
        try:
            sqlite_query = """SELECT title, count(likes.id) AS liked FROM posts
                                INNER JOIN likes ON likes.post_id == posts.id
                                GROUP BY posts.id
                                ORDER BY liked
                                DESC LIMIT 5
                            """
            posts = connection.execute(sqlite_query)
            logging.info("TOP 5 MOST LIKED POSTS")
            for post in posts:
                logging.info(post)
        except sqlite3.Error as e:
            logging.error(f"get_posts_statistics(): {e}")


def get_users_statistics() -> None:
    with create_connection(DB_FILE) as connection:
        try:
            sqlite_query = """SELECT users.id, users.email, COUNT(likes.id) AS liked FROM users
                                INNER JOIN posts ON posts.author_id == users.id
                                INNER JOIN likes ON likes.post_id == posts.id
                                GROUP BY posts.author_id
                                ORDER BY liked
                                DESC LIMIT 5
                            """
            users = connection.execute(sqlite_query)
            logging.info("TOP 5 AUTHORS BY MOST LIKED POSTS")
            for user in users:
                logging.info(user)
        except sqlite3.Error as e:
            logging.error(f"get_users_statistics(): {e}")


def main() -> None:
    clear_tables()
    fake = Faker()
    sign_up_users(fake)
    create_posts(fake)
    like_activity(fake)

    get_users_statistics()
    get_posts_statistics()
    get_like_activity_statistics()


if __name__ == "__main__":
    main()
