from flask import Flask, render_template, request, jsonify
from database import get_db, create_tables

app = Flask(__name__)
create_tables()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_song", methods=["POST"])
def add_song():
    data = request.json
    db = get_db()
    sql = "INSERT INTO songs (title, artist, url) VALUES (?, ?, ?)"
    params = (data["title"], data["artist"], data["url"])
    cursor = db.execute(sql, params)
    new_id = cursor.lastrowid
    db.commit()
    db.close()
    return jsonify({
        "message": "Song added successfully",
        "id": new_id,
        "sql": sql,
        "params": params,
        "display_sql": (
            "INSERT INTO songs (title, artist, url) VALUES "
            f"({_sql_literal(data['title'])}, {_sql_literal(data['artist'])}, {_sql_literal(data['url'])})"
        )
    })

def _sql_literal(value):
    return "'" + str(value).replace("'", "''") + "'"

@app.route("/search")
def search():
    q = request.args.get("q")
    db = get_db()
    rows = db.execute(
        "SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ?",
        (f"%{q}%", f"%{q}%")
    ).fetchall()
    db.close()

    return jsonify([
        {
            "id": r[0],
            "title": r[1],
            "artist": r[2],
            "url": r[3],
            "fav": r[4]
        }
        for r in rows
    ])

@app.route("/favorite/<int:id>")
def favorite(id):
    db = get_db()
    row = db.execute("SELECT is_favorite FROM songs WHERE id = ?", (id,)).fetchone()
    if row is None:
        db.close()
        return jsonify({"message": "Song not found"}), 404

    new_value = 0 if row[0] else 1
    db.execute("UPDATE songs SET is_favorite = ? WHERE id = ?", (new_value, id))
    db.commit()
    db.close()
    return jsonify({
        "message": "Added to favourites" if new_value else "Removed from favourites",
        "fav": new_value
    })

@app.route("/favorites")
def favorites():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM songs WHERE is_favorite = 1 ORDER BY id DESC"
    ).fetchall()
    db.close()

    return jsonify([
        {"id": r[0], "title": r[1], "artist": r[2], "url": r[3], "fav": r[4]}
        for r in rows
    ])

@app.route("/library")
def library():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM songs ORDER BY id DESC"
    ).fetchall()
    db.close()

    return jsonify([
        {"id": r[0], "title": r[1], "artist": r[2], "url": r[3], "fav": r[4]}
        for r in rows
    ])

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_song(id):
    db = get_db()
    db.execute("DELETE FROM songs WHERE id = ?", (id,))
    db.commit()
    db.close()
    return jsonify({"message": "Song deleted successfully"})

@app.route("/update/<int:id>", methods=["PUT"])
def update_song(id):
    data = request.json
    db = get_db()
    db.execute(
        "UPDATE songs SET title = ?, artist = ?, url = ? WHERE id = ?",
        (data["title"], data["artist"], data["url"], id)
    )
    db.commit()
    db.close()
    return jsonify({"message": "Song updated successfully"})

if __name__ == "__main__":
    app.run(debug=True)
