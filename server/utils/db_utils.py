import sqlite3

__CONN = None
__CURSOR = None
__COLUMNS = None

def set_conn(path: str):
    global __CONN
    __CONN = None
    __CONN = sqlite3.connect(path)

def get_conn() -> sqlite3.Connection:
    global __CONN
    if __CONN:
        return __CONN
    else:
        return None

def set_cursor():
    global __CURSOR
    __CURSOR = None
    __CURSOR = get_conn().cursor()

def get_cursor() -> sqlite3.Cursor:
    global __CURSOR
    if __CURSOR:
        return __CURSOR
    else:
        return None

def conn_commit():
    get_conn().commit()

def conn_close():
    get_conn().close()

def cursor_execute(query: str, values=None):
    if values != None:
        get_cursor().execute(query, tuple(values))
    else:
        get_cursor().execute(query)

def cursor_fetch() -> list:
    return get_cursor().fetchall()

def set_cols(table_name: str):
    global __COLUMNS
    __COLUMNS = None
    cursor_execute("PRAGMA table_info({table_name})".format(table_name=table_name))
    __COLUMNS = [(col[1], col[2]) for col in cursor_fetch()]

def get_cols() -> list:
    global __COLUMNS
    if __COLUMNS:
        return __COLUMNS[1:]
    else:
        return None

def make_insert_query(form: dict) -> (str, list):
    col_names = [i[0] for i in get_cols()]

    fields = ",".join(['?' for i in range(len(col_names))])
    query = "INSERT INTO predictions{cols} VALUES ({fields})".format(
        cols=tuple(col_names), fields=fields
        )
    values = [form[value[0]] for value in get_cols()]

    print(query, values)
    return query, values

def insert_pred(path: str, form: dict):
    set_conn(path)
    set_cursor()
    set_cols('predictions')

    query, values = make_insert_query(form)

    cursor_execute(query, values)

    conn_commit()
    conn_close()

def fetch_top_n(path:str, n: str, rows: str) -> list:
    set_conn(path)
    set_cursor()
    set_cols('predictions')
    col_names = ",".join([i[0] for i in get_cols()])

    # Select query to return the top nth sample
    cursor_execute("""SELECT {col_names} FROM predictions ORDER BY 
        rating DESC LIMIT {rows} OFFSET {offset}""".format(
            col_names=col_names, rows=rows, offset=(int(n)-1)
            ))
    row_data = cursor_fetch()

    conn_commit()
    conn_close()

    return row_data

# main func for testing functions
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
    print(fetch_top_n("server/database/mal_regression.db", 1, 1))