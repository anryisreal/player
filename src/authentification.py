import psycopg2
def connection():
    try:
        # Пытаемся подключиться к базе данных
        conn = psycopg2.connect(
            dbname='test',
            user='postgres',
            password='15sore9292noo',
            host='localhost'
        )
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"Server version {cursor.fetchone()}")

        return conn
    except:
        print('Can`t establish connection to database')
        return -1

def register(conn, login, password):
    with conn.cursor() as cursor:
        # Проверка на существование логина
        cursor.execute(f"SELECT user_login FROM auth_menu WHERE user_login = '{login}'")
        if cursor.fetchone() is None:
            cursor.execute(
                f"""INSERT INTO auth_menu (user_login, user_password) VALUES 
                ('{login}', '{password}');"""
            )
            print("Your account was succesfully added")
        else:
            print("User already exist")

    if conn:
        conn.close()
        print("DB was closed")

def login(conn, login, password):
    with conn.cursor() as cursor:
        # Проверка на существование логина
        cursor.execute(f"SELECT user_password FROM auth_menu WHERE user_login = '{login}'")
        t_password = cursor.fetchone()
        if t_password is None:
            print("Wrong Login!!!")
        else:
            if t_password[0] != password:
                print("Wrong password, try again :>")
            else:
                return login

    if conn:
        conn.close()
        print("DB was closed")