# -Backstory-Consistency-Verification-
Evidence-aware consistency classification of backstory claims against long-form literary narratives using lightweight retrieval and reasoning.

Step 1: Environment Setup
```
python -m venv venv

```
Activate:

Windows
```
venv\Scripts\activate

```
Linux / macOS
```
source venv/bin/activate

```

Install dependencies:

```
pip install -r requirements.txt

```

Step 2: Dataset Placement

Ensure the following files are present:

dataset/train.csv

dataset/test.csv

dataset/books/In search of the castaways.txt

dataset/books/The Count of Monte Cristo.txt

Filenames are case-sensitive.

Project directory
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
├──KHARAGPUR DATA SCIENCE HACKATHON Report
│   
│
├── requirements.txt
│
└── README.md

Step 3: Run the Pipeline

Navigate to the project folder:

```
cd project

```

Run:

```
python main.py

```

Step 4: Expected Output

The program will:

Extract the claim (caption or content)

Chunk the novel into fixed-size segments

Retrieve top-K relevant chunks

Compute a bounded consistency score

Convert score → binary label

Generate submission file

Console output example:

[BACKSTORY CLAIM]
[MOCK PATHWAY] Table created successfully
[FINAL DECISION]
Predicted label: 1
[SUCCESS]
Submission file created at: output/submission_v1.csv

Step 5: Submission File


The final output file:

```
output/submission_v1.csv

```
Format:

```
id,label
121,1
129,0
...
```
##Team members

Mrunali Kamerikar
Riddhima Taose
