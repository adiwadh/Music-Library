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
    cursor = db.execute(
        "INSERT INTO songs (title, artist, url) VALUES (?, ?, ?)",
        (data["title"], data["artist"], data["url"])
    )
    new_id = cursor.lastrowid
    db.commit()
    db.close()
    return jsonify({"message": "Song added successfully", "id": new_id})

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
    db.execute("UPDATE songs SET is_favorite = 1 WHERE id = ?", (id,))
    db.commit()
    db.close()
    return jsonify({"message": "Added to Library"})

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

