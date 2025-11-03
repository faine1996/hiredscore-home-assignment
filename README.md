#hiredScore home assignment

Python 3.11. Minimal third-party:`pymongo` for Section 2.  
Data source: https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json

##setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt

## Examples
Dry-run everything:
python -m section2.main --explain --dry-run

Industry:
python -m section2.main --industry "real estate" --dry-run

Skills (any-of):
python -m section2.main --skills "quickbooks,payroll" --dry-run

Combined with years and insert:
python -m section2.main --industry "real estate" --skills "quickbooks,payroll" --min-years 2 --mongo "mongodb://localhost:27017"
