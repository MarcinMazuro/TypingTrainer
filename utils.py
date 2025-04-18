import random

MIN_TEXT_LEN = 170
LINE_SIZE = 40  # Maximum characters per line
MIN_WORD_SIZE = 2
MAX_WORD_SIZE = 8

def create_word(keys):
    word_len = random.randint(MIN_WORD_SIZE, MAX_WORD_SIZE)
    word = ''.join(random.choice(keys) for _ in range(word_len))
    return word


def create_sentence(keys: str):
    text = ''
    text_len = 0
    
    while text_len < MIN_TEXT_LEN:
        word = create_word(keys)
        text += (word + ' ')
        text_len += len(word)

    return text
