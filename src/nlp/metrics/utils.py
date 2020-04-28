import re
import six
import collections

def tokenize(text):
    """Tokenize input text into a list of tokens.
    Args:
        text: A text blob to tokenize.
    Returns:
        A list of string tokens extracted from input text.
    """

    # Convert everything to lowercase.
    text = text.lower()
    # Replace any non-alpha-numeric characters with spaces.
    text = re.sub(r"[^a-z0-9]+", " ", six.ensure_str(text))

    tokens = re.split(r"\s+", text)

    # drop any empty or invalid tokens.
    tokens = [x for x in tokens if re.match(r"^[a-z0-9]+$", six.ensure_str(x))]

    return tokens

def n_grams(sequence, n):
    """
    Args:
        sequence: the source data (list of tokens) to be converted into ngrams
    Returns: 
        ngrams generated from a sequence of items, as an dictionary where each key is an ngram and the values correspond to the number of time that this ngram appear in the input sequence.
    
    """
    ngrams = collections.Counter()
    for ngram in (tuple(sequence[i:i + n]) for i in range(len(sequence) - n + 1)):
        ngrams[ngram] += 1
    return ngrams
        
if __name__ == '__main__':

    sequence = 'my name is mariama'
    tokens  = tokenize(sequence)
    ngrams = n_grams(tokens, 3)
    print(ngrams)
    matches_by_order = [0] * 4
    print(matches_by_order)
    
