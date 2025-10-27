import re

# -----------------------------
# Q1. Convert text to lowercase, remove punctuation and numbers,
#     extract all hashtags and email addresses using regex
# -----------------------------
print("\nQ1. Convert text to lowercase, remove punctuation and numbers, extract hashtags and emails")
text = input("Enter your text: ")

# convert to lowercase
text_lower = text.lower()

# remove punctuation and numbers
cleaned = re.sub(r'[^a-z\s#@.]', '', text_lower)

# find hashtags and emails
hashtags = re.findall(r'#\w+', text)
emails = re.findall(r'\S+@\S+\.\S+', text)

print("Cleaned text:", cleaned)
print("Hashtags found:", hashtags)
print("Emails found:", emails)



# -----------------------------
# Q2. Extract all @mentions and URLs from a social media post
# -----------------------------
print("\nQ2. Extract all @mentions and URLs from a post")
post = input("Enter your social media post: ")

# find mentions and URLs
mentions = re.findall(r'@\w+', post)
urls = re.findall(r'https?://[^\s]+', post)

print("Mentions found:", mentions)
print("URLs found:", urls)



# -----------------------------
# Q3. Remove punctuation and numbers from a paragraph,
#     split it into words, and count frequency of each unique word
# -----------------------------
print("\nQ3. Remove punctuation & numbers, then count word frequency")
text2 = input("Enter a paragraph: ")

# remove punctuation and numbers
cleaned2 = re.sub(r'[^a-zA-Z\s]', '', text2)

# convert to lowercase and split into words
words = cleaned2.lower().split()

# count frequency
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

print("\nWord frequencies:")
for w, c in freq.items():
    print(w, ":", c)



# -----------------------------
# Q4. Extract all valid dates using regex
#     Example formats: 12/10/2025 or 2025-10-12
# -----------------------------
print("\nQ4. Extract all valid dates from text")
text3 = input("Enter text containing dates: ")

# find both formats
dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b', text3)

print("Dates found:", dates)



# -----------------------------
# Q5. Check whether each string in a list is a valid email address
# -----------------------------
print("\nQ5. Check if given emails are valid")
n = int(input("How many emails do you want to check? "))

emails_list = []
for i in range(n):
    email = input(f"Enter email {i+1}: ")
    emails_list.append(email)

# check if each email is valid
for email in emails_list:
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        print(email, "→ Valid email")
    else:
        print(email, "→ Not valid")


#Hey!!! My Email is john_doe123@gmail.com and I love #Python3!!!
#Hey @john! Check out https://example.com and also follow @python_dev.
#Python is great! Python 3.12 is even better, isn't it?
#Some dates are 12/10/2025, 2025-10-12, and 13-05-2023 in this text.