import socket
import json
import chess
import webbrowser
import os

board = chess.Board()

players = {
    "white": False,
    "black": False
}

HOST = "0.0.0.0"
PORT = 5000

ip = socket.gethostbyname(socket.gethostname())

print(f"http://{ip}:{PORT}")

webbrowser.open(f"http://{ip}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(5)

base = os.path.dirname(os.path.abspath(__file__))

while True:

    client, address = server.accept()

    request = client.recv(4096).decode()

    if not request:
        client.close()
        continue

    line = request.split("\n")[0]

    method = line.split(" ")[0]

    path = line.split(" ")[1]

    if path == "/":
        path = "/templates/index.html"

    try:

        if path.endswith(".html"):

            file = open(
                os.path.join(base, path[1:]),
                "r",
                encoding="utf-8"
            )

            body = file.read()

            file.close()

            content_type = "text/html"

        elif path.endswith(".css"):

            file = open(
                os.path.join(base, path[1:]),
                "r",
                encoding="utf-8"
            )

            body = file.read()

            file.close()

            content_type = "text/css"

        elif path.endswith(".js"):

            file = open(
                os.path.join(base, path[1:]),
                "r",
                encoding="utf-8"
            )

            body = file.read()

            file.close()

            content_type = "application/javascript"

        elif method == "GET" and path == "/join":

            role = "spectator"

            if not players["white"]:
                players["white"] = True
                role = "white"

            elif not players["black"]:
                players["black"] = True
                role = "black"

            body = json.dumps({
                "role": role,
                "fen": board.fen()
            })

            content_type = "application/json"

        elif method == "GET" and path == "/board":

            body = json.dumps({
                "fen": board.fen(),
                "turn": "white" if board.turn else "black",
                "checkmate": board.is_checkmate(),
                "stalemate": board.is_stalemate()
            })

            content_type = "application/json"

        elif method == "POST" and path == "/move":

            data = json.loads(
                request.split("\r\n\r\n")[1]
            )

            role = data["role"]

            move_text = data["move"]

            move = chess.Move.from_uci(move_text)

            if move not in board.legal_moves:

                response_data = {
                    "success": False,
                    "message": "Movimiento ilegal"
                }

            else:

                turn = (
                    "white"
                    if board.turn
                    else "black"
                )

                if role != turn:

                    response_data = {
                        "success": False,
                        "message": "No es tu turno"
                    }

                else:

                    board.push(move)

                    response_data = {
                        "success": True,
                        "fen": board.fen()
                    }

                    if board.is_checkmate():

                        winner = (
                            "Blancas"
                            if board.turn == chess.BLACK
                            else "Negras"
                        )

                        response_data["game_over"] = (
                            f"Jaque mate. Ganaron las {winner}"
                        )

                    elif board.is_stalemate():

                        response_data["game_over"] = "Empate"

            body = json.dumps(response_data)

            content_type = "application/json"

        else:

            body = "404"

            content_type = "text/plain"

        response = "HTTP/1.1 200 OK\r\n"

        response += f"Content-Type: {content_type}\r\n"

        response += "Access-Control-Allow-Origin: *\r\n"

        response += "\r\n"

        response += body

        client.send(response.encode())

    except Exception as e:

        response = "HTTP/1.1 500 Internal Server Error\r\n"

        response += "Content-Type: text/plain\r\n"

        response += "\r\n"

        response += str(e)

        client.send(response.encode())

    client.close()