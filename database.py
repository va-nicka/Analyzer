import sqlite3
import uuid
from typing import Optional, List, Any

from image_analysis import ImageAnalysisState


class Image:
    def __init__(
            self,
            image_id: str,
            path: str,
            state: ImageAnalysisState,
            marker_id: str,
            marker_lane: int,
            number_of_lanes: int
    ):
        self.image_id = image_id
        self.path = path
        self.state = state
        self.marker_id = marker_id
        self.marker_lane = marker_lane
        self.number_of_lanes = number_of_lanes


def insert_image(
        database: str,
        image_path: str,
        image_state: ImageAnalysisState,
        marker_id: str,
        marker_lane: int,
        number_of_lanes: int
) -> str:
    image_id = uuid.uuid4().hex

    execute_query(
        database,
        """INSERT INTO images (id, path, state, marker_id, marker_lane, number_of_lanes) values (?, ?, ?, ?, ?, ?)""",
        parameters=[image_id, image_path, image_state.value, marker_id, marker_lane, number_of_lanes]
    )

    return image_id


def fetch_image(database: str, image_id: str) -> Optional[Image]:
    result = execute_query(
        database,
        """SELECT * FROM images WHERE id = ?""",
        parameters=[image_id]
    )

    if len(result) > 0:
        return Image(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

    return None


def fetch_images_by_state(database: str, state: ImageAnalysisState) -> list[Image]:
    result = execute_query(
        database,
        """SELECT * FROM images WHERE state = ?""",
        parameters=[state.value]
    )
    images = []

    for index, image in enumerate(result):
        images.append(
            Image(
                result[index][0],
                result[index][1],
                result[index][2],
                result[index][3],
                result[index][4],
                result[index][5]
            )
        )

    return images


def update_analysis_state(database: str, image_id: str, status: ImageAnalysisState):
    execute_query(
        database,
        """UPDATE images SET state = ? WHERE id = ?""",
        parameters=[status.value, image_id]
    )


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def init_database(database):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS images (
                                    id text,
                                    path text NOT NULL,
                                    state text NOT NULL,
                                    marker_id text NOT NULL,
                                    marker_lane int NOT NULL,
                                    number_of_lanes int NOT NULL
                                ); """

    conn = create_connection(database)

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def execute_query(database: str, query: str, parameters: []) -> list[Any]:
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute(query, parameters)

        result = cur.fetchall()

    return result
