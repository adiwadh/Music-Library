from flask import Flask, render_template, request, jsonify
from database import get_db, create_tables

app = Flask(__name__)
create_tables()

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _sql_literal(value):
    return "'" + str(value).replace("'", "''") + "'"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_song", methods=["POST"])
def add_song():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    sql = "INSERT INTO songs (title, artist, url) VALUES (%s, %s, %s)"
    params = (data["title"], data["artist"], data["url"])
    cursor.execute(sql, params)
    new_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()

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


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM songs WHERE title LIKE %s OR artist LIKE %s",
        (f"%{q}%", f"%{q}%")
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {"id": r[0], "title": r[1], "artist": r[2], "url": r[3], "fav": r[4]}
        for r in rows
    ])


@app.route("/favorite/<int:id>")
def favorite(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT is_favorite FROM songs WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "Song not found"}), 404

    new_value = 0 if row[0] else 1
    cursor.execute("UPDATE songs SET is_favorite = %s WHERE id = %s", (new_value, id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Added to favourites" if new_value else "Removed from favourites",
        "fav": new_value
    })


@app.route("/favorites")
def favorites():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM songs WHERE is_favorite = 1 ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {"id": r[0], "title": r[1], "artist": r[2], "url": r[3], "fav": r[4]}
        for r in rows
    ])


@app.route("/library")
def library():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM songs ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {"id": r[0], "title": r[1], "artist": r[2], "url": r[3], "fav": r[4]}
        for r in rows
    ])


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_song(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Song deleted successfully"})


@app.route("/update/<int:id>", methods=["PUT"])
def update_song(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE songs SET title = %s, artist = %s, url = %s WHERE id = %s",
        (data["title"], data["artist"], data["url"], id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Song updated successfully"})


if __name__ == "__main__":
    app.run(debug=True)
