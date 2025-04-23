"""
Text generator for typing exercises.
"""

import random
from config.settings import MIN_TEXT_LEN

class TextGenerator:
    def __init__(self):
        self.word_list = self.load_english_words()
        
    def load_english_words(self):
        """Load a list of English words from a file or use a predefined list."""
        try:
            with open('/usr/share/dict/words', 'r') as f:
                return [word.strip().lower() for word in f if word.strip().isalpha()]
        except:
            # Fallback to a basic word list
            basic_words = ["the", "be", "to", "of", "and", "a", "in", "that", "have", 
                "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", 
                "this", "but", "his", "by", "from", "they", "we", "say", "her", 
                "she", "or", "an", "will", "my", "one", "all", "would", "there"]
            return basic_words
    
    def find_english_words(self, keys_to_use):
        """Find English words that can be formed using the given letters."""
        valid_words = []
        keys_to_use = ''.join(keys_to_use).lower()
        
        for word in self.word_list:
            # Skip words that are too long
            if len(word) > len(keys_to_use):
                continue
                
            # Check if the word can be formed using the available letters
            letter_counts = {}
            
            # Count available letters
            for letter in keys_to_use:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
            
            # Check if word can be formed
            can_form = True
            for letter in word:
                if letter not in letter_counts or letter_counts[letter] <= 0:
                    can_form = False
                    break
                letter_counts[letter] -= 1
            
            if can_form and len(word) >= 3:  # Only include words with 3+ letters
                valid_words.append(word)
        
        return valid_words
    
    def create_english_sentence(self, keys_to_use, max_length=180):
        """Create a sentence from English words that can be formed using the given letters."""
        valid_words = self.find_english_words(keys_to_use)
        
        if not valid_words:
            # If no valid words found, return a simple message
            return "No valid English words found with these letters"
        
        sentence = ""
        current_length = 0
        
        while current_length < max_length and valid_words:
            word = random.choice(valid_words)
            if current_length + len(word) + 1 <= max_length:  # +1 for space
                if sentence:
                    sentence += " " + word
                    current_length += len(word) + 1
                else:
                    sentence = word
                    current_length += len(word)
            else:
                break
        sentence += " "
        
        return sentence