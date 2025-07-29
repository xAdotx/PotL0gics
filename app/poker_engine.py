import random
import math
from typing import List, Dict, Any, Tuple, Optional
from enum import Enum

class Card:
    """Represents a playing card"""
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def get_value(self) -> int:
        """Get numerical value of card for comparison"""
        values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return values.get(self.rank, 0)

class HandRank(Enum):
    """Poker hand rankings"""
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class PokerEngine:
    """Advanced poker engine with pot odds calculation and hand evaluation"""
    
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['h', 'd', 'c', 's']  # hearts, diamonds, clubs, spades
        
    def parse_cards(self, card_strings: List[str]) -> List[Card]:
        """Convert card strings to Card objects"""
        cards = []
        for card_str in card_strings:
            if len(card_str) >= 2:
                rank = card_str[:-1]
                suit = card_str[-1].lower()
                if rank in self.ranks and suit in self.suits:
                    cards.append(Card(rank, suit))
        return cards
    
    def calculate_pot_odds(
        self,
        pot_size: float,
        bet_to_call: float,
        player_cards: List[str] = None,
        community_cards: List[str] = None,
        position: str = "unknown",
        num_players: int = 2
    ) -> Dict[str, Any]:
        """Calculate pot odds and implied odds for the current situation"""
        
        # Basic pot odds calculation
        pot_odds_ratio = bet_to_call / (pot_size + bet_to_call)
        pot_odds_percentage = pot_odds_ratio * 100
        
        # Calculate implied odds (future betting potential)
        implied_odds = self._calculate_implied_odds(
            pot_size, bet_to_call, position, num_players
        )
        
        # Calculate equity if cards are provided
        equity = 0.0
        if player_cards and community_cards:
            equity = self._calculate_equity(player_cards, community_cards, num_players)
        
        # Determine if call is profitable
        is_profitable = equity > pot_odds_percentage if equity > 0 else False
        
        # Calculate expected value
        ev = self._calculate_expected_value(
            pot_size, bet_to_call, equity, implied_odds
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            pot_odds_percentage, equity, ev, position, num_players
        )
        
        return {
            "pot_odds_ratio": round(pot_odds_ratio, 4),
            "pot_odds_percentage": round(pot_odds_percentage, 2),
            "implied_odds": round(implied_odds, 2),
            "equity": round(equity, 2),
            "expected_value": round(ev, 2),
            "is_profitable": is_profitable,
            "recommendation": recommendation,
            "break_even_equity": round(pot_odds_percentage, 2)
        }
    
    def evaluate_hand(
        self,
        player_cards: List[str],
        community_cards: List[str] = None
    ) -> Dict[str, Any]:
        """Evaluate the strength of a poker hand"""
        
        if not player_cards or len(player_cards) < 2:
            raise ValueError("Player must have at least 2 cards")
        
        # Parse cards
        hole_cards = self.parse_cards(player_cards)
        board_cards = self.parse_cards(community_cards) if community_cards else []
        
        # Get all available cards
        all_cards = hole_cards + board_cards
        
        # Evaluate hand strength
        hand_rank, hand_value, kickers = self._evaluate_hand_strength(all_cards)
        
        # Calculate hand strength percentage
        strength_percentage = self._calculate_hand_strength_percentage(hand_rank, hand_value)
        
        # Get hand description
        hand_description = self._get_hand_description(hand_rank, hand_value, kickers)
        
        # Calculate outs (cards that improve the hand)
        outs = self._calculate_outs(hole_cards, board_cards)
        
        return {
            "hand_rank": hand_rank.name,
            "hand_value": hand_value,
            "strength_percentage": round(strength_percentage, 2),
            "hand_description": hand_description,
            "outs": outs,
            "hole_cards": [str(card) for card in hole_cards],
            "board_cards": [str(card) for card in board_cards]
        }
    
    def calculate_probabilities(
        self,
        player_cards: List[str],
        community_cards: List[str] = None,
        num_players: int = 2,
        num_simulations: int = 10000
    ) -> Dict[str, Any]:
        """Calculate winning probabilities through Monte Carlo simulation"""
        
        if not player_cards or len(player_cards) < 2:
            raise ValueError("Player must have at least 2 cards")
        
        # Parse known cards
        known_cards = self.parse_cards(player_cards + (community_cards or []))
        
        # Run Monte Carlo simulation
        wins = 0
        ties = 0
        
        for _ in range(num_simulations):
            # Create deck without known cards
            deck = self._create_deck(known_cards)
            
            # Deal remaining community cards
            remaining_community = 5 - len(community_cards) if community_cards else 5
            simulated_board = board_cards + random.sample(deck, remaining_community)
            
            # Deal opponent hands
            opponent_hands = []
            for _ in range(num_players - 1):
                if len(deck) >= 2:
                    opponent_hand = random.sample(deck, 2)
                    opponent_hands.append(opponent_hand)
                    deck = [card for card in deck if card not in opponent_hand]
            
            # Evaluate all hands
            player_hand = self._evaluate_hand_strength(hole_cards + simulated_board)
            player_score = (player_hand[0].value, player_hand[1], player_hand[2])
            
            best_opponent_score = (0, 0, [])
            for opponent_hand in opponent_hands:
                opponent_eval = self._evaluate_hand_strength(opponent_hand + simulated_board)
                opponent_score = (opponent_eval[0].value, opponent_eval[1], opponent_eval[2])
                if opponent_score > best_opponent_score:
                    best_opponent_score = opponent_score
            
            # Determine winner
            if player_score > best_opponent_score:
                wins += 1
            elif player_score == best_opponent_score:
                ties += 1
        
        win_probability = wins / num_simulations * 100
        tie_probability = ties / num_simulations * 100
        lose_probability = 100 - win_probability - tie_probability
        
        return {
            "win_probability": round(win_probability, 2),
            "tie_probability": round(tie_probability, 2),
            "lose_probability": round(lose_probability, 2),
            "simulations": num_simulations
        }
    
    def _calculate_implied_odds(
        self,
        pot_size: float,
        bet_to_call: float,
        position: str,
        num_players: int
    ) -> float:
        """Calculate implied odds based on position and number of players"""
        
        # Base implied odds multiplier
        base_multiplier = 1.0
        
        # Position adjustments
        position_multipliers = {
            "button": 1.2,
            "cutoff": 1.1,
            "middle": 1.0,
            "early": 0.9,
            "blinds": 1.0
        }
        
        position_mult = position_multipliers.get(position.lower(), 1.0)
        
        # Number of players adjustment
        player_multiplier = max(0.8, 1.0 - (num_players - 2) * 0.1)
        
        # Calculate implied odds
        implied_odds = pot_size * base_multiplier * position_mult * player_multiplier
        
        return implied_odds
    
    def _calculate_equity(
        self,
        player_cards: List[str],
        community_cards: List[str],
        num_players: int
    ) -> float:
        """Calculate hand equity (winning probability)"""
        
        # This is a simplified equity calculation
        # In a real implementation, you'd use more sophisticated methods
        
        hole_cards = self.parse_cards(player_cards)
        board_cards = self.parse_cards(community_cards)
        
        # Basic equity based on hand strength
        hand_rank, hand_value, _ = self._evaluate_hand_strength(hole_cards + board_cards)
        
        # Convert hand rank to equity percentage
        rank_equity = {
            HandRank.ROYAL_FLUSH: 95.0,
            HandRank.STRAIGHT_FLUSH: 90.0,
            HandRank.FOUR_OF_A_KIND: 85.0,
            HandRank.FULL_HOUSE: 80.0,
            HandRank.FLUSH: 75.0,
            HandRank.STRAIGHT: 70.0,
            HandRank.THREE_OF_A_KIND: 65.0,
            HandRank.TWO_PAIR: 60.0,
            HandRank.PAIR: 55.0,
            HandRank.HIGH_CARD: 50.0
        }
        
        base_equity = rank_equity.get(hand_rank, 50.0)
        
        # Adjust for number of players
        player_adjustment = max(0.5, 1.0 - (num_players - 2) * 0.1)
        
        return base_equity * player_adjustment
    
    def _calculate_expected_value(
        self,
        pot_size: float,
        bet_to_call: float,
        equity: float,
        implied_odds: float
    ) -> float:
        """Calculate expected value of calling"""
        
        # EV = (equity * (pot_size + implied_odds)) - bet_to_call
        ev = (equity / 100) * (pot_size + implied_odds) - bet_to_call
        
        return ev
    
    def _generate_recommendation(
        self,
        pot_odds: float,
        equity: float,
        ev: float,
        position: str,
        num_players: int
    ) -> str:
        """Generate playing recommendation based on analysis"""
        
        if equity == 0:
            return "Insufficient information to make recommendation"
        
        if ev > 0:
            if ev > bet_to_call * 0.5:
                return "Strong call - high expected value"
            else:
                return "Call - marginally profitable"
        elif equity > pot_odds:
            return "Call - equity exceeds pot odds"
        else:
            return "Fold - equity below pot odds"
    
    def _evaluate_hand_strength(self, cards: List[Card]) -> Tuple[HandRank, int, List[int]]:
        """Evaluate the strength of a poker hand"""
        
        if len(cards) < 5:
            return HandRank.HIGH_CARD, 0, []
        
        # Sort cards by value
        sorted_cards = sorted(cards, key=lambda x: x.get_value(), reverse=True)
        
        # Check for flush
        suits = [card.suit for card in cards]
        flush_suit = None
        for suit in set(suits):
            if suits.count(suit) >= 5:
                flush_suit = suit
                break
        
        # Check for straight
        values = [card.get_value() for card in sorted_cards]
        straight_high = self._find_straight_high(values)
        
        # Check for straight flush
        if flush_suit and straight_high:
            if straight_high == 14:  # Ace high
                return HandRank.ROYAL_FLUSH, 14, []
            else:
                return HandRank.STRAIGHT_FLUSH, straight_high, []
        
        # Check for four of a kind
        four_kind = self._find_four_of_a_kind(values)
        if four_kind:
            return HandRank.FOUR_OF_A_KIND, four_kind, []
        
        # Check for full house
        full_house = self._find_full_house(values)
        if full_house:
            return HandRank.FULL_HOUSE, full_house[0], [full_house[1]]
        
        # Check for flush
        if flush_suit:
            flush_cards = [card for card in sorted_cards if card.suit == flush_suit][:5]
            return HandRank.FLUSH, flush_cards[0].get_value(), [card.get_value() for card in flush_cards[1:]]
        
        # Check for straight
        if straight_high:
            return HandRank.STRAIGHT, straight_high, []
        
        # Check for three of a kind
        three_kind = self._find_three_of_a_kind(values)
        if three_kind:
            return HandRank.THREE_OF_A_KIND, three_kind, []
        
        # Check for two pair
        two_pair = self._find_two_pair(values)
        if two_pair:
            return HandRank.TWO_PAIR, two_pair[0], [two_pair[1]]
        
        # Check for pair
        pair = self._find_pair(values)
        if pair:
            return HandRank.PAIR, pair, []
        
        # High card
        return HandRank.HIGH_CARD, sorted_cards[0].get_value(), [card.get_value() for card in sorted_cards[1:5]]
    
    def _find_straight_high(self, values: List[int]) -> Optional[int]:
        """Find the highest straight possible"""
        unique_values = sorted(set(values), reverse=True)
        
        # Check for Ace-low straight (A,2,3,4,5)
        if 14 in unique_values and 2 in unique_values and 3 in unique_values and 4 in unique_values and 5 in unique_values:
            return 5  # 5-high straight
        
        # Check for regular straights
        for i in range(len(unique_values) - 4):
            if unique_values[i] - unique_values[i + 4] == 4:
                return unique_values[i]
        
        return None
    
    def _find_four_of_a_kind(self, values: List[int]) -> Optional[int]:
        """Find four of a kind"""
        for value in set(values):
            if values.count(value) == 4:
                return value
        return None
    
    def _find_full_house(self, values: List[int]) -> Optional[Tuple[int, int]]:
        """Find full house (three of a kind + pair)"""
        value_counts = {}
        for value in values:
            value_counts[value] = value_counts.get(value, 0) + 1
        
        three_kind = None
        pair = None
        
        for value, count in value_counts.items():
            if count >= 3:
                if three_kind is None or value > three_kind:
                    three_kind = value
            elif count >= 2:
                if pair is None or value > pair:
                    pair = value
        
        if three_kind and pair:
            return (three_kind, pair)
        return None
    
    def _find_three_of_a_kind(self, values: List[int]) -> Optional[int]:
        """Find three of a kind"""
        for value in set(values):
            if values.count(value) == 3:
                return value
        return None
    
    def _find_two_pair(self, values: List[int]) -> Optional[Tuple[int, int]]:
        """Find two pair"""
        pairs = []
        for value in set(values):
            if values.count(value) == 2:
                pairs.append(value)
        
        if len(pairs) >= 2:
            pairs.sort(reverse=True)
            return (pairs[0], pairs[1])
        return None
    
    def _find_pair(self, values: List[int]) -> Optional[int]:
        """Find a pair"""
        for value in set(values):
            if values.count(value) == 2:
                return value
        return None
    
    def _calculate_hand_strength_percentage(self, hand_rank: HandRank, hand_value: int) -> float:
        """Calculate hand strength as a percentage"""
        base_percentages = {
            HandRank.ROYAL_FLUSH: 100.0,
            HandRank.STRAIGHT_FLUSH: 95.0,
            HandRank.FOUR_OF_A_KIND: 90.0,
            HandRank.FULL_HOUSE: 85.0,
            HandRank.FLUSH: 80.0,
            HandRank.STRAIGHT: 75.0,
            HandRank.THREE_OF_A_KIND: 70.0,
            HandRank.TWO_PAIR: 65.0,
            HandRank.PAIR: 60.0,
            HandRank.HIGH_CARD: 50.0
        }
        
        base = base_percentages.get(hand_rank, 50.0)
        
        # Adjust based on hand value
        value_adjustment = (hand_value - 2) * 0.5  # 2 is lowest card value
        
        return min(100.0, base + value_adjustment)
    
    def _get_hand_description(self, hand_rank: HandRank, hand_value: int, kickers: List[int]) -> str:
        """Get human-readable hand description"""
        rank_names = {
            2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
            10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"
        }
        
        value_name = rank_names.get(hand_value, str(hand_value))
        
        descriptions = {
            HandRank.ROYAL_FLUSH: "Royal Flush",
            HandRank.STRAIGHT_FLUSH: f"{value_name}-high Straight Flush",
            HandRank.FOUR_OF_A_KIND: f"Four {value_name}s",
            HandRank.FULL_HOUSE: f"Full House, {value_name}s over {rank_names.get(kickers[0], str(kickers[0]))}s",
            HandRank.FLUSH: f"{value_name}-high Flush",
            HandRank.STRAIGHT: f"{value_name}-high Straight",
            HandRank.THREE_OF_A_KIND: f"Three {value_name}s",
            HandRank.TWO_PAIR: f"Two Pair, {value_name}s and {rank_names.get(kickers[0], str(kickers[0]))}s",
            HandRank.PAIR: f"Pair of {value_name}s",
            HandRank.HIGH_CARD: f"{value_name} High"
        }
        
        return descriptions.get(hand_rank, "Unknown Hand")
    
    def _calculate_outs(self, hole_cards: List[Card], board_cards: List[Card]) -> Dict[str, int]:
        """Calculate outs (cards that improve the hand)"""
        outs = {
            "straight_draw": 0,
            "flush_draw": 0,
            "overcards": 0,
            "gutshot": 0,
            "open_ended": 0
        }
        
        # This is a simplified outs calculation
        # In a real implementation, you'd calculate actual outs
        
        return outs
    
    def _create_deck(self, excluded_cards: List[Card] = None) -> List[Card]:
        """Create a deck of cards excluding specified cards"""
        deck = []
        for rank in self.ranks:
            for suit in self.suits:
                card = Card(rank, suit)
                if not excluded_cards or card not in excluded_cards:
                    deck.append(card)
        return deck 