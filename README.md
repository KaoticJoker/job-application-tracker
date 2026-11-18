# Job Application Tracker — COP4751 Course Project

A full-stack Flask/MySQL application with four related tables, full CRUD, a dashboard, and a skill-based Job Match page.

## Requirements
- Python 3.10+
- MySQL 8+
- Internet access for the optional Bootstrap CDN styling

## Setup (Windows PowerShell)
1. Clone/download the repository and open the `job_tracker_project` folder.
2. Create a virtual environment: `py -m venv .venv`
3. Activate it: `.venv\Scripts\Activate.ps1` (if PowerShell blocks activation, use `.venv\Scripts\python.exe` directly).
4. Install dependencies: `pip install -r requirements.txt`
5. In MySQL Workbench, open `schema.sql` and execute it, or run `mysql -u root -p < schema.sql` in a terminal with MySQL on PATH.
6. Copy `.env.example` to `.env` and set your MySQL password and a random `FLASK_SECRET_KEY`.
7. Start: `python app.py`
8. Open `http://127.0.0.1:5000`.

## Suggested demonstration sequence (3–7 minutes)
1. Show the four MySQL tables and JSON columns in Workbench.
2. Open dashboard; create a company and job, with `requirements` JSON such as `{"required_skills":["Python","SQL","Flask"]}`.
3. Create an application and contact linked to the new records.
4. View and edit each record, show dashboard stats.
5. Open Job Match; enter `Python, SQL` and show 67% (2/3), missing Flask.
6. Delete a contact and show confirmation; demonstrate safe foreign-key delete protection.
7. Show repository, README and AI_USAGE.md.

## Features
- Company, job, application and contact create/read/update/delete, with confirmation on deletes
- Required-field, date, numeric and JSON validation
- Parameterized SQL values and MySQL foreign keys
- Dashboard counts, status distribution, recent applications
- Job Match ranks jobs by matched / total required skills (case-insensitive)
- `requirements` and `interview_data` JSON columns

## Notes
- This project uses the **course project specification schema**, which differs from some earlier assignment versions (e.g. `job_url` instead of `posting_url`, and `contact_name` instead of separate first/last names). Import into a fresh database or migrate your old schema carefully.
- No example records are preloaded. Add them through the UI.
- Run locally for the course demo; it has no user accounts or CSRF protection and is not production-ready.
- Deleting a parent company/job with related records is blocked by foreign keys.
- Never commit `.env` or passwords to GitHub.

## Testing
Run `python -m unittest discover -s tests -v` for standalone skill-match unit tests. Also manually verify each CRUD operation against a local MySQL server.

## Submission checklist
- [ ] Push this project to GitHub and share the repository URL
- [ ] Record a 3–7 minute demonstration showing browser, Flask server, and MySQL
- [ ] Test all CRUD pages and Job Match on your machine
- [ ] Complete AI_USAGE.md with your own testing, changes, and lessons
