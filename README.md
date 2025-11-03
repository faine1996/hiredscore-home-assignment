This project implements a candidate data processing system that fetches, parses, and filters candidate resumes from a JSON API.

## Quick Start

You can run this project either by cloning from GitHub or from the provided ZIP.

---

### option a — run from gitHub

```bash
# 1) clone
git clone https://github.com/faine1996/hiredscore-home-assignment.git
cd hiredscore-home-assignment

# 2) (recommended) create & activate a virtualenv
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .\.venv\Scripts\Activate.ps1

# 3) install dependencies (needed for Section 2)
pip install -r requirements.txt

# 4) run Section 1 (prints candidates + gap lines)
python -m section1.main --limit 3

# 5) run Section 2 (dry-run: no DB writes)
python -m section2.main --explain --dry-run

# 6) (optional) insert into mongoDB (make sure Mongo is running)
# Example filter that should match at least one candidate:
python -m section2.main --industry "real estate" --skills "quickbooks,payroll" --min-years 2

### option b — run from zip

# 1) unzip the archive (submission.zip) and cd into the folder
cd hiredscore-home-assignment  # folder must contain common/, section1/, section2/

# 2) (recommended) create & activate a virtualenv
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .\.venv\Scripts\Activate.ps1

# 3) install dependencies (needed for Section 2)
pip install -r requirements.txt

# 4) run Section 1 (prints candidates + gap lines)
python -m section1.main --limit 3

# 5) run Section 2 (dry-run: no DB writes)
python -m section2.main --explain --dry-run

# 6) (optional) insert into mongoDB (make sure Mongo is running)
python -m section2.main --industry "real estate" --skills "quickbooks,payroll" --min-years 2

# requirements

- **Python 3.11** or higher
- **MongoDB** (for Section 2 only)

# installation

### python and virtual environment

create and activate a virtual environment before installing dependencies.

```bash
# macos/linux
python3 -m venv .venv
source .venv/bin/activate

# windows (powershell)
# py -3.11 -m venv .venv
# .\.venv\Scripts\Activate.ps1
```

### install dependencies

the project primarily uses the standard library. the only external dependency is `pymongo` (required for section 2). install via:

```bash
pip install -r requirements.txt
# or
pip install pymongo
```

### mongodb (section 2 only)

#### option a: docker (quickest)

```bash
docker run -d --name mongo -p 27017:27017 mongo:7
```

#### option b: local install

- macos (homebrew):
  ```bash
  brew tap mongodb/brew
  brew install mongodb-community
  brew services start mongodb-community
  ```

- ubuntu/debian:
  ```bash
  sudo apt-get update
  sudo apt-get install -y mongodb
  sudo systemctl start mongodb
  sudo systemctl enable mongodb
  ```

- windows:
  - download and install mongodb community server from mongodb.com
  - start the mongodb service

## project structure

```
assignment/
├── common/
│   ├── __init__.py
│   ├── http.py           # HTTP utilities for fetching JSON
│   └── types.py          # Type definitions
├── section1/
│   ├── dates.py          # Date parsing and gap calculation
│   ├── formatting.py     # Output formatting
│   ├── main.py           # Section 1 entry point
│   └── parsing.py        # Candidate data extraction
├── section2/
│   ├── filters.py        # Candidate filtering logic
│   ├── main.py           # Section 2 entry point
│   ├── mongo_io.py       # MongoDB operations
│   └── transform.py      # Data transformation utilities
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## usage

### section 1: display candidates with employment gaps

This section fetches candidate data and displays their work experience, including gaps between jobs.

#### basic usage

```bash
python -m section1.main
```

This will print all candidates in the format:
```
Hello Clark L Kent,
Worked as: Staff Accountant, From Jan/01/2008 To Dec/31/2008 in Agrabah, GM, US
Worked as: C.O.A.'s, From Jan/01/2007 To Dec/31/2007 in Agrabah, GM, US
Worked as: Wax Preparer, From Jan/01/2006 To Dec/31/2006 in Agrabah, GM, US
Gap in CV for 364 days
Worked as: Staff Accountant, From Jan/01/2004 To Dec/31/2004 in New York, NY, US
...
```

#### command line options

```bash
# limit output to first 3 candidates
python -m section1.main --limit 3

# use a custom data URL
python -m section1.main --url "https://your-custom-url.com/data.json"
```

**available flags:**
- `--url <URL>` - Custom data source URL (default: provided test URL)
- `--limit <N>` - Limit output to first N candidates

---

### section 2: filter candidates and insert to mongoDB

This section filters candidates based on industry, skills, and experience, then inserts them into MongoDB.

#### basic usage

```bash
# insert all candidates (no filters)
python -m section2.main
```

#### filtering examples

**filter by industry:**
```bash
python -m section2.main --industry "real estate"
python -m section2.main --industry "education"
```

**filter by skills:**
```bash
# single skill
python -m section2.main --skills "quickbooks"

# multiple skills (comma or semicolon separated)
python -m section2.main --skills "quickbooks,payroll,smashing"
python -m section2.main --skills "python;java;sql"
```

**filter by minimum years of experience:**
```bash
# candidates with at least 5 years total experience
python -m section2.main --min-years 5

# candidates with at least 10 years
python -m section2.main --min-years 10
```

**combine multiple filters:**
```bash
python -m section2.main \
  --industry "real estate" \
  --skills "quickbooks,excel" \
  --min-years 3
```

#### mongoDB connection

**default (local mongoDB):**
```bash
python -m section2.main --industry "education"
```
Uses `mongodb://localhost:27017` by default.

#### utility options

**dry dun (see what would be inserted without actually inserting):**
```bash
python -m section2.main --industry "education" --dry-run
```

**explain mode (see dataset statistics and match count):**
```bash
python -m section2.main --explain
python -m section2.main --industry "real estate" --explain
```

**preview matched candidates:**
```bash
# show first 5 matched candidate names
python -m section2.main --industry "education" --show-n 5
```

**export to jSON file:**
```bash
python -m section2.main --industry "real estate" --export-json output.json
```

#### command line options summary

| Flag | Description | Example |
|------|-------------|---------|
| `--url <URL>` | Custom data source URL | `--url "https://..."` |
| `--industry <TEXT>` | Filter by industry (substring match) | `--industry "real estate"` |
| `--skills <CSV>` | Filter by skills (comma/semicolon separated) | `--skills "python,sql"` |
| `--min-years <FLOAT>` | Minimum total years of experience | `--min-years 5.5` |
| `--mongo <URI>` | MongoDB connection string | `--mongo "mongodb://localhost:27017"` |
| `--dry-run` | Show what would be inserted without inserting | `--dry-run` |
| `--explain` | Show dataset statistics and filter results | `--explain` |
| `--show-n <N>` | Preview first N matched candidate names | `--show-n 10` |
| `--export-json <FILE>` | Export matched candidates to JSON file | `--export-json results.json` |

---

## mongoDB database structure

**Database:** `assignment`  
**Collection:** `filtered_candidates`

### document schema

```json
{
  "name": "Clark L Kent",
  "skills": ["quickbooks", "smashing", "wax", "general ledger"],
  "industries": ["real estate industry", "primary/secondary education industry"],
  "total_years": 31.08,
  "experiences": [
    {
      "title": "Staff Accountant",
      "start_date": "Jan/01/2008",
      "end_date": "Dec/31/2008",
      "location": "Agrabah, GM, US",
      "current": false
    }
  ]
}
```

### querying mongoDB

After running Section 2, you can query the data:

```bash
mongosh

use assignment
db.filtered_candidates.find().pretty()
db.filtered_candidates.countDocuments()
db.filtered_candidates.find({ "total_years": { $gte: 10 } })
db.filtered_candidates.find({ "skills": "quickbooks" })
```

---

## example workflows

### workflow 1: basic data exploration

```bash
# 1.see a few candidates with their employment history
python -m section1.main --limit 5

# 2.understand the dataset
python -m section2.main --explain

# 3.preview education industry candidates
python -m section2.main --industry "education" --show-n 10 --dry-run
```

### workflow 2: filter and insert to database

```bash
# 1.find experienced real estate accountants
python -m section2.main \
  --industry "real estate" \
  --skills "quickbooks,smashing" \
  --min-years 5

# 2.verify insertion
mongosh
> use assignment
> db.filtered_candidates.find().pretty()
```

### workflow 3: export filtered data

```bash
# export to JSON without using MongoDB
python -m section2.main \
  --industry "education" \
  --skills "teaching,administration" \
  --min-years 3 \
  --export-json education_candidates.json \
  --dry-run
```

---

## features

### s 1
- Fetches candidate data from remote JSON API
- Extracts name, job roles, dates, and locations
- Calculates employment gaps between jobs
- Handles various date formats (MMM/DD/YYYY, MMM/YYYY, YYYY)
- Sorts jobs chronologically (most recent first)
- Pretty-prints formatted output

### s 2
- Filters by industry (substring matching, case-insensitive)
- Filters by skills (matches any skill in list, case-insensitive)
- Filters by minimum years of experience (handles overlapping jobs)
- Calculates total experience accounting for job overlaps
- Inserts filtered candidates into MongoDB
- Creates index on name field for performance
- Supports dry-run mode for testing
- Dataset statistics and explanation mode
- JSON export capability
- Flexible MongoDB connection options

---

## troubleshooting

### mongoDB connection issues

**Error: "Connection refused"**
```bash
# check if mongoDB is running
# macOS
brew services list | grep mongodb

# Linux
sudo systemctl status mongodb

# start mongoDB if not running
brew services start mongodb-community  # macOS
sudo systemctl start mongodb           # Linux
```

**Error: "Authentication failed"**
- Verify your connection string has correct username/password
- Ensure user has read/write permissions on the database

### python version issues

**Error: "SyntaxError" or type hint issues**
- verify you're using Python 3.11+:
```bash
python --version
# should show Python 3.11.x or higher
```

### import errors

**Error: "No module named 'pymongo'"**
```bash
pip install pymongo
```

**Error: "No module named 'section1'" or "No module named 'section2'"**
- Ensure you're running from the project root directory
- Use the module syntax: `python -m section1.main` (not `python section1/main.py`)

---

## notes

- **date handling**: The system handles various date formats and calculates inclusive gaps (end date of previous job to start date of next job, minus 1 day)
- **skill matching**: Skills are matched case-insensitively and support both comma and semicolon separators
- **industry matching**: Uses substring matching (e.g., "education" matches "Primary/Secondary Education industry")
- **experience calculation**: Properly handles overlapping job periods by merging intervals
- **data source**: Default URL points to the provided test dataset

---