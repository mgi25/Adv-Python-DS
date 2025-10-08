# ------------------------------------------------------------
# (1) Real-World Examples of Text Data Generated Daily
# ------------------------------------------------------------
# 1. Tweets on Twitter/X
# 2. Comments on YouTube videos
# 3. Emails sent and received
# 4. News articles published online
# 5. Customer reviews on Amazon
# 6. Chat messages in WhatsApp or Slack
# 7. Search queries typed into Google
# 8. Captions and posts on Instagram
# 9. Call transcripts in customer support systems
# 10. Survey responses collected by organizations


# ------------------------------------------------------------
# (2) Python Libraries for Text Data Processing
# ------------------------------------------------------------
# | Library | Key Function | Example Use Case |
# |----------|--------------|-----------------|
# | NLTK (Natural Language Toolkit) | word_tokenize() | Tokenize sentences into words for sentiment analysis |
# | spaCy | nlp() | Named Entity Recognition (NER) for extracting names or organizations |
# | re (Regular Expressions) | findall() | Extract patterns like emails, hashtags, or numbers |
# | TextBlob | sentiment | Analyze sentiment polarity and subjectivity of reviews |
# | gensim | Word2Vec() | Build word embeddings for semantic similarity |
# | scikit-learn | CountVectorizer() | Convert text into numerical vectors for ML models |
# | BeautifulSoup | get_text() | Extract visible text from HTML web pages |
# | pandas | str.replace() | Clean and preprocess large text datasets |
# | regex | sub() | Replace unwanted characters or digits in strings |
# | transformers | pipeline() | Use pre-trained BERT or GPT models for NLP tasks |


# ------------------------------------------------------------
# Simple Example: Cleaning and Processing Text Data
# ------------------------------------------------------------

import re  # Regular expression module

# Sample text
text = "Hey!!! My Email is john_doe123@gmail.com 😄. I scored 98% in exam!!! #Success #AIrocks"

# 1. Make all letters small (lowercase)
text = text.lower()

# 2. Remove numbers and punctuation marks
clean_text = re.sub(r'[^a-z\s#]', '', text)

# 3. Find all hashtags
hashtags = re.findall(r'#\w+', text)

# 4. Find the email address
email = re.findall(r'\S+@\S+', text)

# 5. Show the results
print("Cleaned Text:", clean_text)
print("Hashtags:", hashtags)
print("Email:", email)
