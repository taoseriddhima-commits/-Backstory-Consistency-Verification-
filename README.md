# Backstory-Consistency-Verification

**Evidence-aware consistency classification of backstory claims against long-form literary narratives using lightweight retrieval and reasoning.**

This project verifies whether backstory claims are consistent with long-form literary texts by retrieving relevant evidence from novels and performing bounded reasoning to generate a binary consistency label.


## Project Overview

The pipeline performs the following steps:

1. Extracts backstory claims from the dataset
2. Chunks long-form literary narratives into fixed-size segments
3. Retrieves the top-K relevant chunks for each claim
4. Computes a bounded consistency score
5. Converts the score into a binary label
6. Generates a submission-ready CSV file


## Environment Setup

### Step 1: Create Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```


## Dataset Placement

Ensure the following files are present and correctly named (case-sensitive):

```text
dataset/train.csv
dataset/test.csv
dataset/books/In search of the castaways.txt
dataset/books/The Count of Monte Cristo.txt
```


## Project Structure

```text
hackathon-project/
│
├── project/
│   └── main.py
│
├── dataset/
│   ├── train.csv
│   ├── test.csv
│   └── books/
│       ├── In search of the castaways.txt
│       └── The Count of Monte Cristo.txt
│
├── output/
│   └── submission_v1.csv
│
├── KHARAGPUR DATA SCIENCE HACKATHON Report
├── requirements.txt
└── README.md
```


## Running the Pipeline

### Step 3: Navigate to Project Directory

```bash
cd project
```

### Run the Script

```bash
python main.py
```


## Expected Output

The program will:

* Extract backstory claims
* Chunk the novels into fixed-size segments
* Retrieve top-K relevant chunks
* Compute a bounded consistency score
* Convert the score to a binary label
* Generate a submission file

### Example Console Output

```text
[BACKSTORY CLAIM] [MOCK PATHWAY]
Table created successfully
[FINAL DECISION] Predicted label: 1
[SUCCESS] Submission file created at: output/submission_v1.csv
```


## Submission File

**Output Path**

```text
output/submission_v1.csv
```

**Format**

```csv
id,label
121,1
129,0
...
```


## Team Members

* **Mrunali Kamerikar**
* **Riddhima Taose**
