import mariadb
import sys

# Connect to MariaDB Platform
try:
    connection = mariadb.connect(
        user = "root",
        password = "root",
        host = "127.0.0.1",
        port = 3306,
        database = "environ"
    )
    
    # Get Cursor
    cursor = connection.cursor()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

print(connection)
print(cursor)