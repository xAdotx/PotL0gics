# Pot Logic - Advanced Poker Bot

A comprehensive poker bot application that calculates pot odds, hand probabilities, and provides real-time analysis for online poker games.

## Features

### Current Features
- **Pot Odds Calculator**: Real-time calculation of pot odds and implied odds
- **Hand Evaluator**: Advanced poker hand ranking and evaluation
- **Probability Engine**: Calculate winning probabilities for different scenarios
- **Game History**: Track and analyze your poker sessions
- **Statistics Dashboard**: View your performance metrics
- **Responsive UI**: Modern web interface built with React

### Future Features
- **Screen Capture**: Real-time screen sharing for live poker games
- **OCR Integration**: Automatic card and pot detection
- **AI Recommendations**: Machine learning-based playing suggestions
- **Multi-table Support**: Handle multiple poker tables simultaneously
- **Tournament Mode**: Specialized features for tournament play

## Architecture

### Backend (Python/FastAPI)
- **API Server**: FastAPI with WebSocket support
- **Poker Engine**: Custom hand evaluation and odds calculation
- **Database**: SQLite with SQLAlchemy ORM
- **Screen Capture**: OpenCV for future screen sharing

### Frontend (React/TypeScript)
- **Modern UI**: React with TypeScript and Tailwind CSS
- **Real-time Updates**: WebSocket connection for live data
- **Responsive Design**: Works on desktop and mobile
- **Interactive Charts**: Visual representation of statistics

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
alembic upgrade head

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. **Start the Backend**: Run the FastAPI server
2. **Start the Frontend**: Run the React development server
3. **Access the Application**: Open http://localhost:3000
4. **Enter Game Details**: Input your cards, pot size, and bet amounts
5. **Get Real-time Analysis**: View pot odds, probabilities, and recommendations

## API Endpoints

### Core Poker Endpoints
- `POST /api/calculate-pot-odds`: Calculate pot odds for current situation
- `POST /api/evaluate-hand`: Evaluate poker hand strength
- `POST /api/calculate-probabilities`: Calculate winning probabilities
- `GET /api/game-history`: Retrieve game history
- `POST /api/save-game`: Save game data

### WebSocket Endpoints
- `WS /ws/poker-analysis`: Real-time poker analysis updates

## Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./poker_bot.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Development

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend && npm test
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This application is for educational and entertainment purposes only. Please ensure you comply with all local laws and poker site terms of service regarding the use of poker assistance tools. 