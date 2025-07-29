import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from typing import List, Dict, Any, Optional, Tuple
import time
import threading
import asyncio
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class DetectedCard:
    """Represents a detected playing card"""
    rank: str
    suit: str
    confidence: float
    position: Tuple[int, int, int, int]  # x, y, width, height

@dataclass
class DetectedPot:
    """Represents detected pot information"""
    amount: float
    confidence: float
    position: Tuple[int, int, int, int]

@dataclass
class OrganizedCards:
    """Represents cards organized by suits in columns"""
    hearts: List[DetectedCard]
    diamonds: List[DetectedCard]
    clubs: List[DetectedCard]
    spades: List[DetectedCard]
    total_cards: int

class ScreenCapture:
    """Screen capture and analysis for poker tables"""
    
    def __init__(self):
        self.is_capturing = False
        self.capture_thread = None
        self.capture_region = None
        self.update_frequency = 1000  # milliseconds
        self.card_templates = {}
        self.pot_detection_enabled = True
        self.card_detection_enabled = True
        
        # Initialize OCR
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            print("⚠️  Tesseract not found. OCR features will be disabled.")
            self.ocr_enabled = False
        else:
            self.ocr_enabled = True
    
    def start_capture(self, region: Optional[Tuple[int, int, int, int]] = None, frequency: int = 1000):
        """Start screen capture in a separate thread"""
        if self.is_capturing:
            return {"status": "error", "message": "Capture already running"}
        
        self.capture_region = region
        self.update_frequency = frequency
        self.is_capturing = True
        
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        return {"status": "success", "message": "Screen capture started"}
    
    def stop_capture(self):
        """Stop screen capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=1)
        
        return {"status": "success", "message": "Screen capture stopped"}
    
    def _capture_loop(self):
        """Main capture loop"""
        while self.is_capturing:
            try:
                # Capture screen
                screenshot = self._capture_screen()
                if screenshot is None:
                    continue
                
                # Analyze the screenshot
                analysis = self._analyze_screenshot(screenshot)
                
                # Store results for retrieval
                self.last_analysis = analysis
                
                # Wait for next capture
                time.sleep(self.update_frequency / 1000.0)
                
            except Exception as e:
                print(f"Error in capture loop: {e}")
                time.sleep(1)
    
    def _capture_screen(self) -> Optional[np.ndarray]:
        """Capture screen or region"""
        try:
            if self.capture_region:
                screenshot = pyautogui.screenshot(region=self.capture_region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
            
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
    
    def _analyze_screenshot(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze screenshot for poker elements"""
        analysis = {
            "timestamp": time.time(),
            "detected_cards": [],
            "organized_cards": None,
            "detected_pot": None,
            "confidence": 0.0,
            "error": None
        }
        
        try:
            # Detect cards
            if self.card_detection_enabled:
                cards = self._detect_cards(image)
                analysis["detected_cards"] = cards
                
                # Organize cards by suits
                if cards:
                    analysis["organized_cards"] = self._organize_cards_by_suits(cards)
            
            # Detect pot
            if self.pot_detection_enabled:
                pot = self._detect_pot(image)
                analysis["detected_pot"] = pot
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(analysis)
            analysis["confidence"] = confidence
            
        except Exception as e:
            analysis["error"] = str(e)
        
        return analysis
    
    def _detect_cards(self, image: np.ndarray) -> List[DetectedCard]:
        """Detect playing cards in the image"""
        cards = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Filter by area (cards should be reasonably sized)
                area = cv2.contourArea(contour)
                if area < 1000 or area > 50000:  # Adjust thresholds as needed
                    continue
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Check aspect ratio (cards are typically 2.5:1)
                aspect_ratio = w / h
                if aspect_ratio < 1.5 or aspect_ratio > 3.5:
                    continue
                
                # Extract card region
                card_region = image[y:y+h, x:x+w]
                
                # Try to recognize the card
                card_info = self._recognize_card(card_region)
                if card_info:
                    cards.append(DetectedCard(
                        rank=card_info["rank"],
                        suit=card_info["suit"],
                        confidence=card_info["confidence"],
                        position=(x, y, w, h)
                    ))
        
        except Exception as e:
            print(f"Error detecting cards: {e}")
        
        return cards
    
    def _recognize_card(self, card_image: np.ndarray) -> Optional[Dict[str, Any]]:
        """Recognize a single card using OCR and template matching"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
            
            # Use OCR to read text
            if self.ocr_enabled:
                text = pytesseract.image_to_string(gray, config='--psm 7')
                text = text.strip().upper()
                
                # Parse card from text
                card_info = self._parse_card_text(text)
                if card_info:
                    return {
                        "rank": card_info["rank"],
                        "suit": card_info["suit"],
                        "confidence": 0.8  # Placeholder confidence
                    }
            
            # Fallback to template matching
            return self._template_match_card(card_image)
            
        except Exception as e:
            print(f"Error recognizing card: {e}")
            return None
    
    def _parse_card_text(self, text: str) -> Optional[Dict[str, str]]:
        """Parse card information from OCR text"""
        # Common card patterns
        patterns = [
            (r'(\d{1,2}|[JQKA])([HDCS])', 'rank', 'suit'),  # 10H, AS, etc.
            (r'([HDCS])(\d{1,2}|[JQKA])', 'suit', 'rank'),  # H10, SA, etc.
        ]
        
        for pattern, rank_group, suit_group in patterns:
            import re
            match = re.search(pattern, text)
            if match:
                rank = match.group(1) if rank_group == 'rank' else match.group(2)
                suit = match.group(2) if suit_group == 'suit' else match.group(1)
                
                # Validate rank and suit
                valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                valid_suits = ['H', 'D', 'C', 'S']
                
                if rank in valid_ranks and suit in valid_suits:
                    return {
                        "rank": rank,
                        "suit": suit.lower()
                    }
        
        return None
    
    def _template_match_card(self, card_image: np.ndarray) -> Optional[Dict[str, Any]]:
        """Template matching for card recognition"""
        # This would require pre-built templates for each card
        # For now, return None to indicate no template matching
        return None
    
    def _detect_pot(self, image: np.ndarray) -> Optional[DetectedPot]:
        """Detect pot amount in the image"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Use OCR to find numbers (pot amounts)
            if self.ocr_enabled:
                text = pytesseract.image_to_string(gray, config='--psm 6')
                
                # Look for currency patterns
                import re
                currency_patterns = [
                    r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
                    r'(\d+(?:,\d{3})*(?:\.\d{2})?)',   # 1,234.56
                    r'(\d+\.\d{2})',                    # 123.45
                ]
                
                for pattern in currency_patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        # Convert to float
                        amount_str = matches[0].replace(',', '')
                        try:
                            amount = float(amount_str)
                            return DetectedPot(
                                amount=amount,
                                confidence=0.7,  # Placeholder confidence
                                position=(0, 0, image.shape[1], image.shape[0])
                            )
                        except ValueError:
                            continue
            
            return None
            
        except Exception as e:
            print(f"Error detecting pot: {e}")
            return None
    
    def _organize_cards_by_suits(self, cards: List[DetectedCard]) -> OrganizedCards:
        """Organize detected cards into columns by suits"""
        # Initialize suit collections
        hearts = []
        diamonds = []
        clubs = []
        spades = []
        
        # Sort cards by suit
        for card in cards:
            suit = card.suit.lower()
            if suit == 'h':
                hearts.append(card)
            elif suit == 'd':
                diamonds.append(card)
            elif suit == 'c':
                clubs.append(card)
            elif suit == 's':
                spades.append(card)
        
        # Sort each suit by rank (A, K, Q, J, 10, 9, ..., 2)
        rank_order = {
            'A': 14, 'K': 13, 'Q': 12, 'J': 11,
            '10': 10, '9': 9, '8': 8, '7': 7,
            '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
        }
        
        def sort_by_rank(card_list):
            return sorted(card_list, key=lambda card: rank_order.get(card.rank, 0), reverse=True)
        
        hearts = sort_by_rank(hearts)
        diamonds = sort_by_rank(diamonds)
        clubs = sort_by_rank(clubs)
        spades = sort_by_rank(spades)
        
        return OrganizedCards(
            hearts=hearts,
            diamonds=diamonds,
            clubs=clubs,
            spades=spades,
            total_cards=len(cards)
        )
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence of the analysis"""
        confidence = 0.0
        total_weight = 0
        
        # Card detection confidence
        if analysis["detected_cards"]:
            card_confidences = [card.confidence for card in analysis["detected_cards"]]
            avg_card_confidence = sum(card_confidences) / len(card_confidences)
            confidence += avg_card_confidence * 0.6
            total_weight += 0.6
        
        # Pot detection confidence
        if analysis["detected_pot"]:
            confidence += analysis["detected_pot"].confidence * 0.4
            total_weight += 0.4
        
        # Normalize confidence
        if total_weight > 0:
            confidence /= total_weight
        
        return min(1.0, max(0.0, confidence))
    
    def get_last_analysis(self) -> Optional[Dict[str, Any]]:
        """Get the most recent analysis results"""
        if hasattr(self, 'last_analysis'):
            return self.last_analysis
        return None
    
    def get_organized_cards_display(self) -> Optional[str]:
        """Get organized cards as a formatted string for display"""
        if not hasattr(self, 'last_analysis') or not self.last_analysis:
            return None
        
        organized_cards = self.last_analysis.get("organized_cards")
        if not organized_cards:
            return "No cards detected"
        
        # Create formatted display with columns
        display_lines = []
        display_lines.append("Cards Organized by Suits:")
        display_lines.append("=" * 80)
        
        # Get all cards for each suit
        hearts_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.hearts]
        diamonds_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.diamonds]
        clubs_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.clubs]
        spades_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.spades]
        
        # Find the maximum number of cards in any suit
        max_cards = max(len(hearts_cards), len(diamonds_cards), len(clubs_cards), len(spades_cards))
        
        # Create header row
        header = f"{'♥ Hearts':<20}|{'♦ Diamonds':<20}|{'♣ Clubs':<20}|{'♠ Spades':<20}"
        display_lines.append(header)
        display_lines.append("-" * 80)
        
        # Create card rows
        for i in range(max_cards):
            hearts_card = hearts_cards[i] if i < len(hearts_cards) else ""
            diamonds_card = diamonds_cards[i] if i < len(diamonds_cards) else ""
            clubs_card = clubs_cards[i] if i < len(clubs_cards) else ""
            spades_card = spades_cards[i] if i < len(spades_cards) else ""
            
            row = f"{hearts_card:<20}|{diamonds_card:<20}|{clubs_card:<20}|{spades_card:<20}"
            display_lines.append(row)
        
        display_lines.append("-" * 80)
        display_lines.append(f"Total cards: {organized_cards.total_cards}")
        
        return "\n".join(display_lines)
    
    def get_organized_cards_colored_display(self) -> Optional[str]:
        """Get organized cards as a colored formatted string for terminal display"""
        if not hasattr(self, 'last_analysis') or not self.last_analysis:
            return None
        
        organized_cards = self.last_analysis.get("organized_cards")
        if not organized_cards:
            return "No cards detected"
        
        # ANSI color codes
        RED = '\033[91m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        BLACK = '\033[30m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        
        # Create formatted display with colored columns
        display_lines = []
        display_lines.append(f"{BOLD}Cards Organized by Suits:{RESET}")
        display_lines.append("=" * 80)
        
        # Get all cards for each suit
        hearts_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.hearts]
        diamonds_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.diamonds]
        clubs_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.clubs]
        spades_cards = [f"{card.rank}{card.suit.upper()}" for card in organized_cards.spades]
        
        # Find the maximum number of cards in any suit
        max_cards = max(len(hearts_cards), len(diamonds_cards), len(clubs_cards), len(spades_cards))
        
        # Create header row with colors
        header = f"{RED}{'♥ Hearts':<20}{RESET}|{BLUE}{'♦ Diamonds':<20}{RESET}|{GREEN}{'♣ Clubs':<20}{RESET}|{BLACK}{'♠ Spades':<20}{RESET}"
        display_lines.append(header)
        display_lines.append("-" * 80)
        
        # Create card rows with colors
        for i in range(max_cards):
            hearts_card = hearts_cards[i] if i < len(hearts_cards) else ""
            diamonds_card = diamonds_cards[i] if i < len(diamonds_cards) else ""
            clubs_card = clubs_cards[i] if i < len(clubs_cards) else ""
            spades_card = spades_cards[i] if i < len(spades_cards) else ""
            
            row = f"{RED}{hearts_card:<20}{RESET}|{BLUE}{diamonds_card:<20}{RESET}|{GREEN}{clubs_card:<20}{RESET}|{BLACK}{spades_card:<20}{RESET}"
            display_lines.append(row)
        
        display_lines.append("-" * 80)
        display_lines.append(f"{BOLD}Total cards: {organized_cards.total_cards}{RESET}")
        
        return "\n".join(display_lines)
    
    def get_organized_cards_dict(self) -> Optional[Dict[str, List[str]]]:
        """Get organized cards as a dictionary for programmatic access"""
        if not hasattr(self, 'last_analysis') or not self.last_analysis:
            return None
        
        organized_cards = self.last_analysis.get("organized_cards")
        if not organized_cards:
            return None
        
        return {
            "hearts": [f"{card.rank}{card.suit.upper()}" for card in organized_cards.hearts],
            "diamonds": [f"{card.rank}{card.suit.upper()}" for card in organized_cards.diamonds],
            "clubs": [f"{card.rank}{card.suit.upper()}" for card in organized_cards.clubs],
            "spades": [f"{card.rank}{card.suit.upper()}" for card in organized_cards.spades],
            "total_cards": organized_cards.total_cards
        }
    
    def set_capture_region(self, region: Tuple[int, int, int, int]):
        """Set the screen region to capture"""
        self.capture_region = region
    
    def enable_card_detection(self, enabled: bool):
        """Enable or disable card detection"""
        self.card_detection_enabled = enabled
    
    def enable_pot_detection(self, enabled: bool):
        """Enable or disable pot detection"""
        self.pot_detection_enabled = enabled
    
    def get_status(self) -> Dict[str, Any]:
        """Get current capture status"""
        return {
            "is_capturing": self.is_capturing,
            "capture_region": self.capture_region,
            "update_frequency": self.update_frequency,
            "card_detection_enabled": self.card_detection_enabled,
            "pot_detection_enabled": self.pot_detection_enabled,
            "ocr_enabled": self.ocr_enabled
        }
    
    def calibrate(self, sample_image: np.ndarray) -> Dict[str, Any]:
        """Calibrate detection parameters using a sample image"""
        # This would involve analyzing a sample image to adjust detection parameters
        # For now, return basic calibration info
        return {
            "status": "calibration_complete",
            "message": "Basic calibration completed",
            "parameters": {
                "card_detection_threshold": 0.7,
                "pot_detection_threshold": 0.6,
                "ocr_confidence_threshold": 0.8
            }
        } 