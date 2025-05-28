from flask import Flask, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)
database = Path(__file__).parent / "database.json"

# Load or initialize data
def load_data():
    try:
        with open(database, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(database, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/command", methods=["POST"])
def command():
    body = request.json
    cmd = body.get("cmd")
    args = body.get("args", [])
    data = load_data()

    if cmd == "greet":
        return jsonify({"output": "📀 Welcome to Vault OS 1.0 — Your Personal Password Commander\n1. Show\n2. Add\n3. Edit\n4. Delete\n5. Exit"})

    elif cmd == "show":
        if not data:
            return jsonify({"output": "⚠️ Vault is empty."})
        out = ""
        for key, value in data.items():
            website, username = key.split("_")
            out += f"{username}'s {website} -> {value}\n"
        return jsonify({"output": out})

    elif cmd == "add":
        if len(args) != 3:
            return jsonify({"output": "❌ Missing arguments. Format: add website username password"})
        w, u, p = args
        data[f"{w}_{u}"] = p
        save_data(data)
        return jsonify({"output": "✅ Saved."})

    elif cmd == "edit":
        if len(args) != 3:
            return jsonify({"output": "❌ Missing arguments. Format: edit website username newpassword"})
        w, u, p = args
        key = f"{w}_{u}"
        if key in data:
            data[key] = p
            save_data(data)
            return jsonify({"output": "🔁 Updated successfully."})
        else:
            return jsonify({"output": "❌ Credential not found."})

    elif cmd == "delete":
        if len(args) != 2:
            return jsonify({"output": "❌ Missing arguments. Format: delete website username"})
        key = f"{args[0]}_{args[1]}"
        if key in data:
            data.pop(key)
            save_data(data)
            return jsonify({"output": "🗑️ Deleted."})
        else:
            return jsonify({"output": "❌ Entry not found."})

    else:
        return jsonify({"output": "❓ Unknown command."})

if __name__ == "__main__":
    app.run()
