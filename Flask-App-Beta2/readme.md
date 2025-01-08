# Chess Game with AI

A web-based chess game implementation where you can play against an AI opponent. The game is built using Flask for the backend and vanilla JavaScript for the frontend.

Live Demo: [Chess Game](https://chess-app-aditya-9fe69273beb5.herokuapp.com/)

## ⚠️ Important Notice About Live Demo

**Session Management Notice**: Due to the current deployment setup, multiple users accessing the game simultaneously might experience session conflicts, where you might see moves from other players' games. This is a known issue in the live demo only.

**Quick Fix**: If you notice moves you didn't make or irregular behavior, simply refresh your browser page to get back your old session.

**Note**: This issue only affects the live demo. The application runs normally when deployed locally.

## Features


- AI opponent using the Minimax algorithm with Alpha-Beta pruning
- Interactive UI with move highlighting
- Valid move indication for selected pieces
- New game functionality
- Turn indicator
- Visual representation of the chess board with piece images

## Technical Highlights

### Strengths
1. **Robust Chess Engine**
   - Full implementation of chess rules (working on some rules)
   - AI using Minimax algorithm with Alpha-Beta pruning
   - Efficient move calculation system

2. **Clean Architecture**
   - Separation of concerns between frontend and backend
   - Modular code structure
   - RESTful API endpoints

3. **User Interface**
   - Intuitive move highlighting
   - Clear turn indication
   - Visual feedback for valid moves
   - Responsive design

4. **Performance**
   - Efficient board state management
   - Quick AI response times
   - Minimal server requests

### Known Issues and Future Improvements

1. **Session Management**
   - Current limitation: Shared game state between users 
   - Planned fix: Implementation of user sessions and game rooms -Not sure about this

2. **AI Improvements**
   - Current depth limitation for performance depth = 2 to reduce computation cost
   - Potential for implementing opening books
   - Opportunity for difficulty levels

3. **Features to Add**
   - Move history
   - Game save/load functionality
   - Multiplayer support
   - Timer/Clock implementation
   - Undo move option

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/adityaanilraut/Chess-engine.git
cd chess-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Access the game at `http://localhost:5000`

## Project Structure
```
chess-app/
├── main.py              # Flask application
├── chess_engine.py      # Chess logic and AI
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku configuration
├── runtime.txt         # Python runtime specification
├── static/
│   ├── css/
│   │   └── style.css   # Game styling
│   ├── js/
│   │   └── chess.js    # Frontend logic
│   └── images/         # Chess piece images
└── templates/
    └── index.html      # Game interface
```

## API Endpoints

- `GET /` - Main game interface
- `GET /api/get_board` - Get current board state
- `POST /api/make_move` - Make a move
- `GET /api/valid_moves/<row>/<col>` - Get valid moves for a piece
- `POST /api/new_game` - Start a new game

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by Aditya Anil Raut
Chess piece images sourced from Chess.com

## Contact

For any queries or issues, please open an issue on GitHub or contact adityaanilraut@gmail.com

