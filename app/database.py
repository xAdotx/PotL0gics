from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from datetime import datetime
import os
from typing import List, Optional
import json

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./poker_bot.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class GameRecord(Base):
    """Database model for storing game records"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    pot_size = Column(Float, nullable=False)
    bet_amount = Column(Float, nullable=False)
    player_cards = Column(Text, nullable=False)  # JSON string
    community_cards = Column(Text, nullable=False)  # JSON string
    position = Column(String(20), nullable=False)
    num_players = Column(Integer, nullable=False)
    action_taken = Column(String(20), nullable=False)
    result = Column(String(20), nullable=False)
    profit_loss = Column(Float, nullable=False)
    pot_odds_calculated = Column(Float, nullable=False)
    equity_calculated = Column(Float, nullable=False)
    recommendation_given = Column(Text, nullable=False)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "pot_size": self.pot_size,
            "bet_amount": self.bet_amount,
            "player_cards": json.loads(self.player_cards),
            "community_cards": json.loads(self.community_cards),
            "position": self.position,
            "num_players": self.num_players,
            "action_taken": self.action_taken,
            "result": self.result,
            "profit_loss": self.profit_loss,
            "pot_odds_calculated": self.pot_odds_calculated,
            "equity_calculated": self.equity_calculated,
            "recommendation_given": self.recommendation_given
        }

class StatisticsRecord(Base):
    """Database model for storing statistics"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_games = Column(Integer, default=0, nullable=False)
    win_rate = Column(Float, default=0.0, nullable=False)
    average_pot_odds = Column(Float, default=0.0, nullable=False)
    session_profit = Column(Float, default=0.0, nullable=False)
    total_hands = Column(Integer, default=0, nullable=False)
    profitable_hands = Column(Integer, default=0, nullable=False)
    average_equity = Column(Float, default=0.0, nullable=False)
    recommendation_accuracy = Column(Float, default=0.0, nullable=False)

class SettingsRecord(Base):
    """Database model for storing application settings"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database dependency
def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")

class DatabaseManager:
    """Manager class for database operations"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def save_game(self, game_data: dict) -> int:
        """Save a game record to the database"""
        try:
            game_record = GameRecord(
                pot_size=game_data["pot_size"],
                bet_amount=game_data["bet_amount"],
                player_cards=json.dumps(game_data["player_cards"]),
                community_cards=json.dumps(game_data["community_cards"]),
                position=game_data["position"],
                num_players=game_data["num_players"],
                action_taken=game_data["action_taken"],
                result=game_data["result"],
                profit_loss=game_data["profit_loss"],
                pot_odds_calculated=game_data["pot_odds_calculated"],
                equity_calculated=game_data["equity_calculated"],
                recommendation_given=game_data["recommendation_given"]
            )
            
            self.db.add(game_record)
            self.db.commit()
            self.db.refresh(game_record)
            
            return game_record.id
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_game_history(self, limit: int = 100) -> List[dict]:
        """Get game history from database"""
        try:
            games = self.db.query(GameRecord).order_by(GameRecord.timestamp.desc()).limit(limit).all()
            return [game.to_dict() for game in games]
        except Exception as e:
            raise e
    
    def get_statistics(self) -> dict:
        """Calculate and return statistics"""
        try:
            # Get total games
            total_games = self.db.query(GameRecord).count()
            
            if total_games == 0:
                return {
                    "total_games": 0,
                    "win_rate": 0.0,
                    "average_pot_odds": 0.0,
                    "session_profit": 0.0,
                    "total_hands": 0,
                    "profitable_hands": 0,
                    "average_equity": 0.0,
                    "recommendation_accuracy": 0.0
                }
            
            # Calculate win rate
            wins = self.db.query(GameRecord).filter(GameRecord.result == "win").count()
            win_rate = (wins / total_games) * 100
            
            # Calculate average pot odds
            avg_pot_odds = self.db.query(GameRecord.pot_odds_calculated).all()
            avg_pot_odds = sum([row[0] for row in avg_pot_odds]) / len(avg_pot_odds)
            
            # Calculate session profit
            total_profit = self.db.query(GameRecord.profit_loss).all()
            session_profit = sum([row[0] for row in total_profit])
            
            # Calculate profitable hands
            profitable_hands = self.db.query(GameRecord).filter(GameRecord.profit_loss > 0).count()
            
            # Calculate average equity
            avg_equity = self.db.query(GameRecord.equity_calculated).all()
            avg_equity = sum([row[0] for row in avg_equity]) / len(avg_equity)
            
            # Calculate recommendation accuracy (simplified)
            # This would need more sophisticated logic in a real implementation
            recommendation_accuracy = 75.0  # Placeholder
            
            return {
                "total_games": total_games,
                "win_rate": round(win_rate, 2),
                "average_pot_odds": round(avg_pot_odds, 2),
                "session_profit": round(session_profit, 2),
                "total_hands": total_games,
                "profitable_hands": profitable_hands,
                "average_equity": round(avg_equity, 2),
                "recommendation_accuracy": round(recommendation_accuracy, 2)
            }
        except Exception as e:
            raise e
    
    def get_best_hands(self, limit: int = 10) -> List[str]:
        """Get the best hands played"""
        try:
            # Get hands with highest equity
            best_games = self.db.query(GameRecord).order_by(GameRecord.equity_calculated.desc()).limit(limit).all()
            return [game.player_cards for game in best_games]
        except Exception as e:
            raise e
    
    def save_setting(self, key: str, value: str, description: Optional[str] = None):
        """Save a setting to the database"""
        try:
            setting = self.db.query(SettingsRecord).filter(SettingsRecord.key == key).first()
            if setting:
                setting.value = value
                if description:
                    setting.description = description
            else:
                setting = SettingsRecord(
                    key=key,
                    value=value,
                    description=description
                )
                self.db.add(setting)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting from the database"""
        try:
            setting = self.db.query(SettingsRecord).filter(SettingsRecord.key == key).first()
            return setting.value if setting else None
        except Exception as e:
            raise e 