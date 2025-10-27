import re

# -------------------------------------------------------------
# Q1. From a multiline string, extract all 10-digit Indian mobile
#     numbers (starting with 6–9)
# -------------------------------------------------------------
print("\nQ1. Extract 10-digit Indian mobile numbers")

text = """Here are some contacts:
9876543210, 8123456789, 4567891234, 9999999999
Call me at 7000000000 or 81234-56789 when free.
"""

# find all 10-digit numbers starting with 6-9
numbers = re.findall(r'\b[6-9]\d{9}\b', text)
print("Mobile numbers found:", numbers)



# -------------------------------------------------------------
# Q2. Remove all stopwords (like 'is', 'the', 'a', 'an', 'in')
#     from a given text and print the cleaned output
# -------------------------------------------------------------
print("\nQ2. Remove stopwords from text")

text2 = input("Enter a sentence: ")

stopwords = ['is', 'the', 'a', 'an', 'in', 'of', 'on', 'and', 'to', 'for']
words = text2.split()

# keep only words that are not stopwords
cleaned_words = [w for w in words if w.lower() not in stopwords]

cleaned_text = ' '.join(cleaned_words)
print("Cleaned text:", cleaned_text)



# -------------------------------------------------------------
# Q3. From a Twitter post, extract both hashtags (#) and mentions (@),
#     and display the count for each
# -------------------------------------------------------------
print("\nQ3. Extract hashtags and mentions from a Twitter post")

tweet = input("Enter your Twitter post: ")

hashtags = re.findall(r'#\w+', tweet)
mentions = re.findall(r'@\w+', tweet)

print("Hashtags:", hashtags)
print("Mentions:", mentions)
print("Number of hashtags:", len(hashtags))
print("Number of mentions:", len(mentions))



# -------------------------------------------------------------
# Q4. From a list of URLs, extract only the domain names
#     (e.g., 'python.org', 'github.com')
# -------------------------------------------------------------
print("\nQ4. Extract domain names from URLs")

urls = [
    "https://www.python.org",
    "http://github.com/user",
    "https://docs.google.com/forms",
    "https://openai.com/research"
]

# extract domain using regex
domains = []
for u in urls:
    match = re.findall(r'https?://(?:www\.)?([^/]+)', u)
    if match:
        domains.append(match[0])

print("Extracted domain names:", domains)



# -------------------------------------------------------------
# Q5. Remove words shorter than 4 characters and
#     extract all capitalized words (proper nouns)
# -------------------------------------------------------------
print("\nQ5. Remove short words and extract capitalized words")

paragraph = input("Enter a paragraph: ")

# remove words shorter than 4 letters
long_words = [w for w in paragraph.split() if len(w) >= 4]

# extract all capitalized words (Proper Nouns)
proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', paragraph)

print("Paragraph without short words:", ' '.join(long_words))
print("Proper nouns found:", proper_nouns)
