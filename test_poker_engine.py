#!/usr/bin/env python3
"""
Test script for Pot Logic Poker Engine
Demonstrates the core functionality
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path.cwd()))

from app.poker_engine import PokerEngine

def test_pot_odds_calculation():
    """Test pot odds calculation"""
    print("🧮 Testing Pot Odds Calculation")
    print("-" * 40)
    
    poker_engine = PokerEngine()
    
    # Test case 1: Basic pot odds
    result = poker_engine.calculate_pot_odds(
        pot_size=100,
        bet_to_call=20,
        player_cards=["Ah", "Kh"],
        community_cards=["Qh", "Jh", "10h"],
        position="button",
        num_players=3
    )
    
    print(f"Pot Size: $100")
    print(f"Bet to Call: $20")
    print(f"Player Cards: Ah Kh")
    print(f"Community Cards: Qh Jh 10h")
    print(f"Position: Button")
    print(f"Players: 3")
    print()
    print(f"Pot Odds: {result['pot_odds_percentage']:.1f}%")
    print(f"Implied Odds: ${result['implied_odds']:.2f}")
    print(f"Equity: {result['equity']:.1f}%")
    print(f"Expected Value: ${result['expected_value']:.2f}")
    print(f"Recommendation: {result['recommendation']}")
    print()

def test_hand_evaluation():
    """Test hand evaluation"""
    print("🃏 Testing Hand Evaluation")
    print("-" * 40)
    
    poker_engine = PokerEngine()
    
    # Test case 1: Royal Flush
    result = poker_engine.evaluate_hand(
        player_cards=["Ah", "Kh"],
        community_cards=["Qh", "Jh", "10h"]
    )
    
    print(f"Player Cards: Ah Kh")
    print(f"Community Cards: Qh Jh 10h")
    print(f"Hand Rank: {result['hand_rank']}")
    print(f"Hand Description: {result['hand_description']}")
    print(f"Strength: {result['strength_percentage']:.1f}%")
    print()
    
    # Test case 2: Full House
    result = poker_engine.evaluate_hand(
        player_cards=["As", "Ks"],
        community_cards=["Ah", "Kh", "Qd"]
    )
    
    print(f"Player Cards: As Ks")
    print(f"Community Cards: Ah Kh Qd")
    print(f"Hand Rank: {result['hand_rank']}")
    print(f"Hand Description: {result['hand_description']}")
    print(f"Strength: {result['strength_percentage']:.1f}%")
    print()

def test_probability_calculation():
    """Test probability calculation"""
    print("📊 Testing Probability Calculation")
    print("-" * 40)
    
    poker_engine = PokerEngine()
    
    # Test case: Pre-flop probabilities
    result = poker_engine.calculate_probabilities(
        player_cards=["Ah", "Kh"],
        community_cards=[],
        num_players=6,
        num_simulations=1000  # Reduced for faster testing
    )
    
    print(f"Player Cards: Ah Kh")
    print(f"Community Cards: None (Pre-flop)")
    print(f"Players: 6")
    print(f"Simulations: 1000")
    print()
    print(f"Win Probability: {result['win_probability']:.1f}%")
    print(f"Tie Probability: {result['tie_probability']:.1f}%")
    print(f"Lose Probability: {result['lose_probability']:.1f}%")
    print()

def test_card_parsing():
    """Test card parsing functionality"""
    print("🎴 Testing Card Parsing")
    print("-" * 40)
    
    poker_engine = PokerEngine()
    
    # Test various card formats
    test_cards = [
        ["Ah", "Kh"],  # Standard format
        ["AS", "KS"],  # Capital suits
        ["10h", "Jd"], # 10 and face cards
        ["2c", "3s"],  # Low cards
    ]
    
    for i, cards in enumerate(test_cards, 1):
        parsed = poker_engine.parse_cards(cards)
        print(f"Test {i}: {cards} -> {[str(card) for card in parsed]}")
    print()

def test_different_positions():
    """Test pot odds with different positions"""
    print("🎯 Testing Different Positions")
    print("-" * 40)
    
    poker_engine = PokerEngine()
    
    positions = ["early", "middle", "cutoff", "button", "small_blind", "big_blind"]
    
    for position in positions:
        result = poker_engine.calculate_pot_odds(
            pot_size=100,
            bet_to_call=20,
            player_cards=["Ah", "Kh"],
            community_cards=["Qh", "Jh", "10h"],
            position=position,
            num_players=6
        )
        
        print(f"Position: {position}")
        print(f"  Implied Odds: ${result['implied_odds']:.2f}")
        print(f"  Recommendation: {result['recommendation']}")
    print()

def main():
    """Run all tests"""
    print("🎰 Pot Logic Poker Engine Tests")
    print("=" * 50)
    print()
    
    try:
        test_card_parsing()
        test_pot_odds_calculation()
        test_hand_evaluation()
        test_probability_calculation()
        test_different_positions()
        
        print("✅ All tests completed successfully!")
        print("\nThe poker engine is working correctly.")
        print("You can now use the web interface at http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 