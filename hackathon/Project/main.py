
print("RUNNING UPDATED FILE ✅")
import pandas as pd
# GLOBAL STOPWORDS
STOPWORDS = {
    "the", "and", "a", "of", "to", "in", "his", "her", "with",
    "was", "as", "by", "for", "that", "it", "is", "on", "at"
}


# Load train.csv
train_path = r"C:\Users\admin\Desktop\hackathon\dataset\train.csv"
df = pd.read_csv(train_path)

# Take first row as example
row = df.iloc[0]

book_name = row["book_name"]

# Map book name to file path
if book_name == "In Search of the Castaways":
    book_path = r"C:\Users\admin\Desktop\hackathon\dataset\books\In search of the castaways.txt"
elif book_name == "The Count of Monte Cristo":
    book_path = r"C:\Users\admin\Desktop\hackathon\dataset\books\The Count of Monte Cristo.txt"
else:
    raise ValueError("Unknown book name")

# Read the novel text
with open(book_path, "r", encoding="utf-8") as f:
    novel_text = f.read()

#  NEW PART STARTS HERE 

# Extract claim text
caption = row["caption"]
content = row["content"]

if pd.isna(caption):
    claim_text = content
    source = "content"
else:
    claim_text = caption
    source = "caption"

# BACKSTORY CLAIM EXTRACTION 

backstory_claim = claim_text.strip()

print("\n[BACKSTORY CLAIM]")
print("Source:", source)
print("Claim:")
print(backstory_claim)

#  CHUNKING THE NOVEL 
def chunk_text(text, chunk_size=800):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


chunks = chunk_text(novel_text)

print("\nTotal number of chunks:", len(chunks))
print("\nFirst chunk preview:\n")
print(chunks[0][:500])  # print first 500 characters only

# MOCK PATHWAY STORAGE 

chunk_table = [{"chunk_id": i, "text": chunks[i]} for i in range(len(chunks))]

print("\n[MOCK PATHWAY] Table created successfully!")
print("Number of rows in table:", len(chunk_table))

# RETRIEVE RELEVANT CHUNKS 
def get_relevant_chunks(claim_text, chunk_table, top_k=3):
    claim_words = {
        w for w in claim_text.lower().split()
        if w not in STOPWORDS
    }

    scored_chunks = []

    for row in chunk_table:
        chunk_words = {
            w for w in row["text"].lower().split()
            if w not in STOPWORDS
        }

        score = len(claim_words.intersection(chunk_words))
        scored_chunks.append((score, row["text"]))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    return scored_chunks[:top_k]
relevant_chunks = get_relevant_chunks(backstory_claim, chunk_table)

#  LLM-STYLE REASONING (SIMULATED) 
def compute_consistency_score(backstory_claim, relevant_chunks):
    claim_words = {
        w for w in backstory_claim.lower().split()
        if w not in STOPWORDS}


    supported_words = set()
    total_words_checked = 0

    for score, chunk in relevant_chunks:
        chunk_words = set(chunk.lower().split())
        overlap = claim_words.intersection(chunk_words)

        supported_words.update(overlap)
        total_words_checked += len(chunk_words)

    # Strength: how much of the claim is supported
    support_ratio = len(supported_words) / max(len(claim_words), 1)

    # Weak evidence penalty: if chunks are large but overlap is tiny
    evidence_density = len(supported_words) / max(total_words_checked, 1)

    # Final bounded score (0–1)
    final_score = (
    0.6 * support_ratio +
    0.4 * min(len(supported_words) / 10, 1.0))


    return min(final_score, 1.0)

# COMPUTE CONSISTENCY SCORE (TOP-LEVEL) 

consistency_score = compute_consistency_score(backstory_claim, relevant_chunks)


#  FINAL LABEL DECISION 

THRESHOLD = 0.25

final_label = 1 if consistency_score >= THRESHOLD else 0

print("\n[FINAL DECISION]")
print("Predicted label:", final_label)


#  WRAP PIPELINE INTO A FUNCTION

def predict_label(row):
    # Extract claim
    caption = row["caption"]
    content = row["content"]

    if pd.isna(caption):
        backstory_claim = content
    else:
        backstory_claim = caption

    # Load correct book
    book_name = row["book_name"]
    if book_name == "In Search of the Castaways":
        book_path = r"C:\Users\admin\Desktop\hackathon\dataset\books\In search of the castaways.txt"
    elif book_name == "The Count of Monte Cristo":
        book_path = r"C:\Users\admin\Desktop\hackathon\dataset\books\The Count of Monte Cristo.txt"
    else:
        return 0

    with open(book_path, "r", encoding="utf-8") as f:
        novel_text = f.read()

    # Chunk
    chunks = chunk_text(novel_text)
    chunk_table = [{"chunk_id": i, "text": chunks[i]} for i in range(len(chunks))]

    # Retrieve
    relevant_chunks = get_relevant_chunks(backstory_claim, chunk_table)

    # Reason
    score = compute_consistency_score(backstory_claim, relevant_chunks)

    # Final label
    return 1 if score >= 0.25 else 0



print("\n[FUNCTION TEST]")
print("Predicted label from function:", predict_label(df.iloc[0]))

#  RUN ON TEST DATA (DRY RUN) 

test_path = r"C:\Users\admin\Desktop\hackathon\dataset\test.csv"
test_df = pd.read_csv(test_path)

print("\n[TEST DATA PREDICTIONS - PREVIEW]")

test_predictions = []

for i, row in test_df.iterrows():
    label = predict_label(row)
    test_predictions.append(label)

    if i < 5:  # preview only first 5
        print(f"Row {i} → Predicted label:", label)

print("\nTotal test samples processed:", len(test_predictions))

# CREATE SUBMISSION FILE

submission = pd.DataFrame({
    "id": test_df["id"],
    "label": test_predictions
})

submission_path = r"C:\Users\admin\Desktop\hackathon\submission_v1.csv"
submission.to_csv(submission_path, index=False)

print("\n[SUCCESS]")
print("Submission file created at:", submission_path)
