from db import get_connection

def clear():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE Page_Content RESTART IDENTITY")

    conn.commit()
    cursor.close()
    conn.close()