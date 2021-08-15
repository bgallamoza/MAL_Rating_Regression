import sqlite3

__CONN = None
__CURSOR = None
__COLUMNS = None

def set_conn(path: str):
    global __CONN
    __CONN = None
    __CONN = sqlite3.connect(path)

def get_conn():
    global __CONN
    if __CONN:
        return __CONN
    else:
        return None

def set_cursor():
    global __CURSOR
    __CURSOR = None
    __CURSOR = get_conn().cursor()

def get_cursor():
    global __CURSOR
    if __CURSOR:
        return __CURSOR
    else:
        return None

def conn_commit():
    get_conn().commit()

def conn_close():
    get_conn().close()

def cursor_execute(query: str):
    get_cursor().execute(query)

def cursor_fetch():
    return get_cursor().fetchall()

def set_cols(table_name: str):
    global __COLUMNS
    __COLUMNS = None
    cursor_execute("PRAGMA table_info({table_name})".format(table_name=table_name))
    __COLUMNS = [(col[1], col[2]) for col in cursor_fetch()]

def get_cols() -> list:
    global __COLUMNS
    if __COLUMNS:
        return __COLUMNS
    else:
        return None

def make_insert_query(form: dict) -> str:
    col_names = [i[0] for i in get_cols()]
    col_names.remove('id')

    query = "INSERT INTO predictions{cols} VALUES (".format(cols=tuple(col_names))
    for feature in get_cols():
        if feature[0] == 'id':
            continue
        elif feature[1] == 'TEXT':
            query += ("'" + form[feature[0]] + "',")
        else:
            query += (str(form[feature[0]]) + ",")
    return query[:-1] + ")"

def insert_pred(path: str, form: dict):
    set_conn(path)
    set_cursor()

    cursor_execute(make_insert_query(form))

    conn_commit()
    conn_close()

def fetch_top_n(path:str, n: int, rows: int) -> list:
    set_conn(path)
    set_cursor()
    cursor_execute("SELECT * FROM predictions ORDER BY rating DESC LIMIT {rows} OFFSET {offset}".format(rows=rows, offset=n-1))

    row_data = cursor_fetch()

    conn_commit()
    conn_close()

    return row_data

if __name__ == "__main__":
    set_conn('mal_regression.db')
    print(get_conn())
    set_cursor()
    print(get_cursor())
    set_cols('predictions')
    print(get_cols())

    form = {
        "en_title": "Dogman",
        "synopsis": "This is the synopsis of the legendary dogman.",
        "genres": '["Drama", "Action"]',
        "studios": '["Shaft"]',
        "extra_studios": 1,
        "source": "manga",
        "num_related_anime":2,
        "num_episodes": 24,
        "average_episode_duration": 1320,
        "rating":7.20
    }

    # query = make_insert_query(form)
    # print(query)
    conn_close()

    # insert_pred('mal_regression.db', form)
    print(fetch_top_n("database/mal_regression.db", 1, 5))