from flask import Flask, render_template, request, jsonify
import chess

app = Flask(__name__)

board = chess.Board()

players = {
    "white": False,
    "black": False
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/join")
def join():

    role = "spectator"

    if not players["white"]:
        players["white"] = True
        role = "white"

    elif not players["black"]:
        players["black"] = True
        role = "black"

    print("Jugador conectado:", role)

    return jsonify({
        "role": role,
        "fen": board.fen()
    })


@app.route("/board")
def get_board():

    return jsonify({
        "fen": board.fen(),
        "turn": "white" if board.turn else "black",
        "checkmate": board.is_checkmate(),
        "stalemate": board.is_stalemate()
    })


@app.route("/move", methods=["POST"])
def move():

    data = request.json

    role = data["role"]
    move_text = data["move"]

    move = chess.Move.from_uci(move_text)

    if move not in board.legal_moves:

        return jsonify({
            "success": False,
            "message": "Movimiento ilegal"
        })

    turn = "white" if board.turn else "black"

    if role != turn:

        return jsonify({
            "success": False,
            "message": "No es tu turno"
        })

    board.push(move)

    print("Movimiento:", move_text)

    result = {
        "success": True,
        "fen": board.fen()
    }

    if board.is_checkmate():

        winner = "Blancas" if board.turn == chess.BLACK else "Negras"

        result["game_over"] = f"Jaque mate. Ganaron las {winner}"

    elif board.is_stalemate():

        result["game_over"] = "Empate"

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )