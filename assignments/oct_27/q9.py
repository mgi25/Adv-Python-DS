# Q9. Using NLTK, create a Python program that:
# • Tokenizes a paragraph into sentences and words.
# • Removes stopwords.
# • Prints the top 5 most frequent words and their counts.


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import string

# --- Download NLTK Data (only runs the first time) ---
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# --- Step 1: Paragraph Input ---
paragraph = """Natural Language Processing (NLP) is a fascinating field of Artificial Intelligence.
It allows computers to understand, interpret, and generate human language.
Python provides excellent libraries such as NLTK and spaCy for NLP tasks."""

# --- Step 2: Tokenize into sentences and words ---
sentences = sent_tokenize(paragraph)
words = word_tokenize(paragraph)

print("🧩 Sentences:")
for s in sentences:
    print("-", s)

print("\n🧩 Words:")
print(words)

# --- Step 3: Remove punctuation and stopwords ---
stop_words = set(stopwords.words("english"))
words_cleaned = [
    word.lower()
    for word in words
    if word.lower() not in stop_words and word not in string.punctuation
]

print("\n🧹 Cleaned Words (after removing stopwords):")
print(words_cleaned)

# --- Step 4: Find top 5 most frequent words ---
word_counts = Counter(words_cleaned)
top5 = word_counts.most_common(5)

print("\n🏆 Top 5 Most Frequent Words:")
for word, count in top5:
    print(f"{word} → {count}")
