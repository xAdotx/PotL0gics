from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Dict, Any
import json
import asyncio

from app.poker_engine import PokerEngine
from app.models import (
    PotOddsRequest, 
    PotOddsResponse, 
    HandEvaluationRequest, 
    HandEvaluationResponse,
    GameHistory,
    GameData
)
from app.database import get_db, init_db
from app.screen_capture import ScreenCapture

# Global variables
poker_engine = PokerEngine()
active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("🚀 Pot Logic Poker Bot started!")
    yield
    # Shutdown
    print("👋 Pot Logic Poker Bot shutting down...")

app = FastAPI(
    title="Pot Logic - Advanced Poker Bot",
    description="A comprehensive poker bot with pot odds calculation and real-time analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Pot Logic - Advanced Poker Bot",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "poker_engine": "active"}

@app.post("/api/calculate-pot-odds", response_model=PotOddsResponse)
async def calculate_pot_odds(request: PotOddsRequest):
    """Calculate pot odds for the current poker situation"""
    try:
        result = poker_engine.calculate_pot_odds(
            pot_size=request.pot_size,
            bet_to_call=request.bet_to_call,
            player_cards=request.player_cards,
            community_cards=request.community_cards,
            position=request.position,
            num_players=request.num_players
        )
        return PotOddsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/evaluate-hand", response_model=HandEvaluationResponse)
async def evaluate_hand(request: HandEvaluationRequest):
    """Evaluate the strength of a poker hand"""
    try:
        result = poker_engine.evaluate_hand(
            player_cards=request.player_cards,
            community_cards=request.community_cards
        )
        return HandEvaluationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/calculate-probabilities")
async def calculate_probabilities(request: Dict[str, Any]):
    """Calculate winning probabilities for different scenarios"""
    try:
        result = poker_engine.calculate_probabilities(
            player_cards=request.get("player_cards", []),
            community_cards=request.get("community_cards", []),
            num_players=request.get("num_players", 2),
            num_simulations=request.get("num_simulations", 10000)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/game-history")
async def get_game_history():
    """Retrieve game history from database"""
    db = get_db()
    try:
        # This would be implemented with actual database queries
        return {"games": [], "total_games": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-game")
async def save_game(game_data: GameData):
    """Save game data to database"""
    db = get_db()
    try:
        # This would be implemented with actual database operations
        return {"message": "Game saved successfully", "game_id": "123"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/poker-analysis")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time poker analysis"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process the message based on type
            if message.get("type") == "pot_odds_request":
                result = poker_engine.calculate_pot_odds(
                    pot_size=message["pot_size"],
                    bet_to_call=message["bet_to_call"],
                    player_cards=message.get("player_cards", []),
                    community_cards=message.get("community_cards", []),
                    position=message.get("position", "unknown"),
                    num_players=message.get("num_players", 2)
                )
                
                # Send response back to client
                await websocket.send_text(json.dumps({
                    "type": "pot_odds_response",
                    "data": result
                }))
            
            elif message.get("type") == "hand_evaluation_request":
                result = poker_engine.evaluate_hand(
                    player_cards=message["player_cards"],
                    community_cards=message.get("community_cards", [])
                )
                
                await websocket.send_text(json.dumps({
                    "type": "hand_evaluation_response",
                    "data": result
                }))
            
            elif message.get("type") == "start_screen_capture":
                # Future implementation for screen capture
                await websocket.send_text(json.dumps({
                    "type": "screen_capture_status",
                    "status": "not_implemented_yet"
                }))
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))

@app.get("/api/statistics")
async def get_statistics():
    """Get poker statistics and performance metrics"""
    try:
        # This would calculate actual statistics from database
        stats = {
            "total_games": 0,
            "win_rate": 0.0,
            "average_pot_odds": 0.0,
            "best_hands": [],
            "session_profit": 0.0
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 