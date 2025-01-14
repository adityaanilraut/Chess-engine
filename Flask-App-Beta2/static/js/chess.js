
/* JavaScript file: static/js/chess.js */
let selectedSquare = null;
let validMoves = [];
let currentTurn = 'white';

function createBoard() {
    const board = document.getElementById('chessboard');
    for (let row = 7; row >= 0; row--) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
            square.dataset.row = row;
            square.dataset.col = col;
            square.addEventListener('click', () => handleSquareClick(row, col));
            board.appendChild(square);
        }
    }
    updateBoard();
}

async function updateBoard() {
    const response = await fetch('/api/get_board');
    const data = await response.json();
    const board = data.board;

    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        const row = parseInt(square.dataset.row);
        const col = parseInt(square.dataset.col);
        const piece = board[row][col];
        
        // Clear existing content
        square.innerHTML = '';
        
        if (piece) {
            const img = document.createElement('img');
            img.src = `/static/Images/${piece.color[0]}${piece.type[0]}.png`;
            img.alt = `${piece.color} ${piece.type}`;
            square.appendChild(img);
        }
    });
}

async function handleSquareClick(row, col) {
    if (currentTurn !== 'white') return;

    if (selectedSquare === null) {
        const response = await fetch(`/api/valid_moves/${row}/${col}`);
        const data = await response.json();
        validMoves = data.moves;
        
        if (validMoves.length > 0) {
            selectedSquare = [row, col];
            highlightSquares();
        }
    } else {
        const moveIsValid = validMoves.some(move => move[0] === row && move[1] === col);
        
        if (moveIsValid) {
            const response = await fetch('/api/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start: selectedSquare,
                    end: [row, col]
                })
            });
            
            const data = await response.json();
            if (data.success) {
                currentTurn = 'black';
                updateTurnIndicator();
                await updateBoard();
                
                // Handle AI move
                if (data.ai_move) {
                    setTimeout(async () => {
                        currentTurn = 'white';
                        updateTurnIndicator();
                        await updateBoard();
                    }, 500);
                }
            }
        }
        
        selectedSquare = null;
        validMoves = [];
        clearHighlights();
    }
}

function highlightSquares() {
    clearHighlights();
    
    if (selectedSquare) {
        const selectedElement = document.querySelector(
            `[data-row="${selectedSquare[0]}"][data-col="${selectedSquare[1]}"]`
        );
        selectedElement.classList.add('selected');
        
        validMoves.forEach(([row, col]) => {
            const square = document.querySelector(
                `[data-row="${row}"][data-col="${col}"]`
            );
            square.classList.add('valid-move');
        });
    }
}

function clearHighlights() {
    document.querySelectorAll('.square').forEach(square => {
        square.classList.remove('selected', 'valid-move');
    });
}

function updateTurnIndicator() {
    document.getElementById('turnIndicator').textContent = `Turn: ${
        currentTurn.charAt(0).toUpperCase() + currentTurn.slice(1)
    }`;
}

async function newGame() {
    await fetch('/api/new_game', { method: 'POST' });
    selectedSquare = null;
    validMoves = [];
    currentTurn = 'white';
    updateTurnIndicator();
    clearHighlights();
    await updateBoard();
}


// Initialize the board when the page loads
document.addEventListener('DOMContentLoaded', createBoard);
