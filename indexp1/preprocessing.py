import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()


def clean_text(text: str):
    
    
    # 1. Lowercase
    text = text.lower()

    # 2. Keeping  only alphanumeric + whitespace
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. Removing extra whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    # 4. Tokenize by whitespace 
    tokens = text.split()

    # 5. Removing stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]

    # 6. Porter stemmer
    tokens = [STEMMER.stem(t) for t in tokens]

    return tokens
