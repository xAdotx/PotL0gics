from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Position(str, Enum):
    """Poker positions"""
    EARLY = "early"
    MIDDLE = "middle"
    CUTOFF = "cutoff"
    BUTTON = "button"
    SMALL_BLIND = "small_blind"
    BIG_BLIND = "big_blind"
    UNKNOWN = "unknown"

class PotOddsRequest(BaseModel):
    """Request model for pot odds calculation"""
    pot_size: float = Field(..., gt=0, description="Current pot size")
    bet_to_call: float = Field(..., ge=0, description="Amount needed to call")
    player_cards: Optional[List[str]] = Field(default=None, description="Player's hole cards")
    community_cards: Optional[List[str]] = Field(default=None, description="Community cards on board")
    position: Position = Field(default=Position.UNKNOWN, description="Player's position")
    num_players: int = Field(default=2, ge=2, le=10, description="Number of players in hand")

class PotOddsResponse(BaseModel):
    """Response model for pot odds calculation"""
    pot_odds_ratio: float = Field(..., description="Pot odds as a ratio")
    pot_odds_percentage: float = Field(..., description="Pot odds as a percentage")
    implied_odds: float = Field(..., description="Implied odds value")
    equity: float = Field(..., description="Hand equity percentage")
    expected_value: float = Field(..., description="Expected value of calling")
    is_profitable: bool = Field(..., description="Whether calling is profitable")
    recommendation: str = Field(..., description="Playing recommendation")
    break_even_equity: float = Field(..., description="Equity needed to break even")

class HandEvaluationRequest(BaseModel):
    """Request model for hand evaluation"""
    player_cards: List[str] = Field(..., min_items=2, max_items=2, description="Player's hole cards")
    community_cards: Optional[List[str]] = Field(default=None, description="Community cards on board")

class HandEvaluationResponse(BaseModel):
    """Response model for hand evaluation"""
    hand_rank: str = Field(..., description="Poker hand rank")
    hand_value: int = Field(..., description="Numerical value of the hand")
    strength_percentage: float = Field(..., description="Hand strength as percentage")
    hand_description: str = Field(..., description="Human-readable hand description")
    outs: Dict[str, int] = Field(..., description="Number of outs for different draws")
    hole_cards: List[str] = Field(..., description="Player's hole cards")
    board_cards: List[str] = Field(..., description="Community cards on board")

class ProbabilityRequest(BaseModel):
    """Request model for probability calculation"""
    player_cards: List[str] = Field(..., min_items=2, max_items=2, description="Player's hole cards")
    community_cards: Optional[List[str]] = Field(default=None, description="Community cards on board")
    num_players: int = Field(default=2, ge=2, le=10, description="Number of players")
    num_simulations: int = Field(default=10000, ge=1000, le=100000, description="Number of Monte Carlo simulations")

class ProbabilityResponse(BaseModel):
    """Response model for probability calculation"""
    win_probability: float = Field(..., description="Probability of winning")
    tie_probability: float = Field(..., description="Probability of tying")
    lose_probability: float = Field(..., description="Probability of losing")
    simulations: int = Field(..., description="Number of simulations run")

class GameData(BaseModel):
    """Model for saving game data"""
    pot_size: float = Field(..., description="Final pot size")
    bet_amount: float = Field(..., description="Amount bet in the hand")
    player_cards: List[str] = Field(..., description="Player's hole cards")
    community_cards: List[str] = Field(..., description="Community cards")
    position: Position = Field(..., description="Player's position")
    num_players: int = Field(..., description="Number of players")
    action_taken: str = Field(..., description="Action taken (fold/call/raise)")
    result: str = Field(..., description="Result of the hand (win/lose/tie)")
    profit_loss: float = Field(..., description="Profit or loss from the hand")
    pot_odds_calculated: float = Field(..., description="Pot odds that were calculated")
    equity_calculated: float = Field(..., description="Equity that was calculated")
    recommendation_given: str = Field(..., description="Recommendation that was given")

class GameHistory(BaseModel):
    """Model for game history"""
    id: Optional[int] = Field(None, description="Game ID")
    timestamp: datetime = Field(..., description="When the game was played")
    pot_size: float = Field(..., description="Final pot size")
    bet_amount: float = Field(..., description="Amount bet")
    player_cards: List[str] = Field(..., description="Player's hole cards")
    community_cards: List[str] = Field(..., description="Community cards")
    position: str = Field(..., description="Player's position")
    num_players: int = Field(..., description="Number of players")
    action_taken: str = Field(..., description="Action taken")
    result: str = Field(..., description="Result")
    profit_loss: float = Field(..., description="Profit or loss")
    pot_odds_calculated: float = Field(..., description="Pot odds calculated")
    equity_calculated: float = Field(..., description="Equity calculated")
    recommendation_given: str = Field(..., description="Recommendation given")

class Statistics(BaseModel):
    """Model for poker statistics"""
    total_games: int = Field(..., description="Total number of games played")
    win_rate: float = Field(..., description="Win rate percentage")
    average_pot_odds: float = Field(..., description="Average pot odds encountered")
    best_hands: List[str] = Field(..., description="Best hands played")
    session_profit: float = Field(..., description="Total session profit/loss")
    total_hands: int = Field(..., description="Total hands played")
    profitable_hands: int = Field(..., description="Number of profitable hands")
    average_equity: float = Field(..., description="Average equity calculated")
    recommendation_accuracy: float = Field(..., description="Accuracy of recommendations")

class ScreenCaptureRequest(BaseModel):
    """Request model for screen capture"""
    enabled: bool = Field(..., description="Whether to enable screen capture")
    capture_region: Optional[Dict[str, int]] = Field(default=None, description="Screen region to capture")
    update_frequency: int = Field(default=1000, ge=100, le=5000, description="Update frequency in milliseconds")

class ScreenCaptureResponse(BaseModel):
    """Response model for screen capture"""
    status: str = Field(..., description="Capture status")
    message: str = Field(..., description="Status message")
    detected_cards: Optional[List[str]] = Field(default=None, description="Detected cards")
    detected_pot: Optional[float] = Field(default=None, description="Detected pot size")
    confidence: float = Field(..., description="Detection confidence")

class WebSocketMessage(BaseModel):
    """Model for WebSocket messages"""
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")

class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp") 