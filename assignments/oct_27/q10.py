# Q10. Implement text similarity using FastText:
# • Train a FastText model on a small text file.
# • Compare the similarity score between two words (e.g., ‘python’ and ‘programming’).
# • Display the vector representation of one word.

from gensim.models import FastText
from gensim.utils import simple_preprocess

# -----------------------------------------------------------
# Step 1: Load and prepare text data
# -----------------------------------------------------------
file_name = "sample_text.txt"  # your training text file

try:
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()
        print("✅ File loaded successfully!")
except FileNotFoundError:
    print("❌ File not found! Please make sure 'sample_text.txt' exists.")
    exit()

# Preprocess text — split into list of word lists (sentences)
sentences = [simple_preprocess(line) for line in text.split('\n') if line.strip()]

# -----------------------------------------------------------
# Step 2: Train FastText model
# -----------------------------------------------------------
print("⏳ Training FastText model... (this may take a few seconds)")

model = FastText(
    sentences=sentences,
    vector_size=100,    # length of each word vector
    window=5,           # context window size
    min_count=1,        # include even rare words
    epochs=10,          # training passes
)

print("✅ FastText model trained successfully!\n")

# -----------------------------------------------------------
# Step 3: Compare similarity between two words
# -----------------------------------------------------------
word1 = "python"
word2 = "programming"

if word1 in model.wv and word2 in model.wv:
    similarity = model.wv.similarity(word1, word2)
    print(f"🔹 Similarity between '{word1}' and '{word2}': {similarity:.4f}")
else:
    print("⚠️ One or both words not found in vocabulary.")

# -----------------------------------------------------------
# Step 4: Display word vector for one word
# -----------------------------------------------------------
if word1 in model.wv:
    vector = model.wv[word1]
    print(f"\n🔸 Vector representation of '{word1}':\n{vector}\n")
else:
    print(f"⚠️ Word '{word1}' not found in the model vocabulary.")

# -----------------------------------------------------------
# Step 5: Save model (optional)
# -----------------------------------------------------------
model.save("fasttext_model_q10.model")
print("💾 Model saved as fasttext_model_q10.model")
