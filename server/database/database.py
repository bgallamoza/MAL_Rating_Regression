import sqlite3

__CONN = None
__CURSOR = None

def set_conn(path):
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

def cursor_execute(query):
    get_cursor().execute(query)

def cursor_fetch(n):
    return get_cursor().fetchone(n)

def make_insert_query(form, features):
    query = "INSERT INTO predictions VALUES ("
    for feature in features:
        query = query + "'" + form[feature] + "',"
    return query + ")"

def insert_pred(form, features):
    set_conn('mal_regression.db')
    set_cursor()

    cursor_execute(make_insert_query(form, features))

    conn_commit()
    conn_close()

def fetch_top_n(n):
    set_conn('mal_regression.db')
    set_cursor()
    cursor_execute("SELECT * FROM predictions ORDER BY rating DESC")

    row_data = cursor_fetch(n)

    conn_commit()
    conn_close()

    return row_data