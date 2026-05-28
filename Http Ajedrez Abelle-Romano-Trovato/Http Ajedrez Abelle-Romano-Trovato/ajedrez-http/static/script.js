let playerRole = "spectator";

const game = new Chess();

const board = Chessboard("board", {

    draggable: true,

    position: "start",

    pieceTheme:
        "https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png",

    onDrop: onDrop
});


async function connectPlayer() {

    const response = await fetch("/join");

    const data = await response.json();

    playerRole = data.role;

    game.load(data.fen);

    board.position(data.fen);

    document.getElementById("role").innerText =
        "Sos: " + playerRole.toUpperCase();

    console.log("Rol:", playerRole);
}


async function updateBoard() {

    const response = await fetch("/board");

    const data = await response.json();

    game.load(data.fen);

    board.position(data.fen);

    if (data.checkmate) {

        alert("Jaque mate");

    } else if (data.stalemate) {

        alert("Empate");
    }
}


async function onDrop(source, target) {

    const move = {

        from: source,
        to: target,
        promotion: "q"
    };

    const legalMove = game.move(move);

    if (legalMove === null) {

        return "snapback";
    }

    game.undo();

    const turn = game.turn();

    if (
        (playerRole === "white" && turn !== "w") ||
        (playerRole === "black" && turn !== "b")
    ) {

        return "snapback";
    }

    const response = await fetch("/move", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            role: playerRole,
            move: source + target
        })
    });

    const data = await response.json();

    if (!data.success) {

        return "snapback";
    }

    game.load(data.fen);

    board.position(data.fen);

    if (data.game_over) {

        alert(data.game_over);
    }
}


connectPlayer();

setInterval(updateBoard, 1000);