import traceback
import sys

# Redirect everything to a log file
log = open("test_db_output.txt", "w")
sys.stdout = log
sys.stderr = log

try:
    from database import get_db, create_tables
    print("Imported OK")
    create_tables()
    print("create_tables() OK")
    conn = get_db()
    print("get_db() OK — server:", conn.get_server_info())
    conn.close()
    print("ALL GOOD — MySQL connection works!")
except Exception as e:
    traceback.print_exc()
finally:
    log.flush()
    log.close()
