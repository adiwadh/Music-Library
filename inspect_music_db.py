import sqlite3

conn = sqlite3.connect('instance/music.db')
cur = conn.cursor()

print('--- SQLite Schema ---')
for row in cur.execute("SELECT type, name, tbl_name, sql FROM sqlite_master WHERE type IN ('table','index','trigger','view') ORDER BY type,name"):
    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

print('\n--- songs table rows ---')
print('ID | Title | Artist | URL | Favorite')
print('-' * 120)
for row in cur.execute('SELECT * FROM songs ORDER BY id'):
    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

conn.close()
