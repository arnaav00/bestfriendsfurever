import sqlite3

def clear_database():
    conn = sqlite3.connect('user_credentials.db')
    cursor = conn.cursor()
    delete_query = "DELETE FROM users"

    try:
        cursor.execute(delete_query)
        conn.commit()
        print("All data deleted from the users table.")
    except sqlite3.Error as e:
        print("Error deleting data:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
