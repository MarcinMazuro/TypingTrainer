"""
Core text utilities for generating words and sentences.
"""

import random
from config.settings import MIN_WORD_SIZE, MAX_WORD_SIZE, MIN_TEXT_LEN

def create_word(keys):
    """Create a random word using the provided keys."""
    word_len = random.randint(MIN_WORD_SIZE, MAX_WORD_SIZE)
    word = ''.join(random.choice(keys) for _ in range(word_len))
    return word


def create_sentence(keys: str):
    """Create a random sentence using the provided keys."""
    text = ''
    text_len = 0
    
    while text_len < MIN_TEXT_LEN:
        word = create_word(keys)
        text += (word + ' ')
        text_len += len(word)

    return text