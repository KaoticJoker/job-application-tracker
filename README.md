# Job Application Tracker — COP4751 Course Project

**Repository:** https://github.com/KaoticJoker/job-application-tracker  
**Stack:** Python 3, Flask, MySQL 8+, HTML/CSS, Bootstrap, Git/GitHub

A local full-stack application for tracking companies, job postings, applications, and contacts. It includes a dashboard and a Job Match feature that ranks job postings against skills entered by a user.

## Features

- **Companies, Jobs, Applications, Contacts:** Create, view, edit, and delete records through web forms and list/detail pages.
- **Dashboard:** Live record totals, application-status breakdown, and recent applications.
- **Job Match:** Enter comma-separated skills; results show match percentage, matched skills, and missing skills, sorted by match score.
- **MySQL relationships:** Foreign keys connect jobs to companies, applications to jobs, and contacts to companies. Related parent records are protected against accidental deletion.
- **JSON fields:** `jobs.requirements` stores job skill requirements; `applications.interview_data` stores flexible interview information.
- **Validation:** Required fields, dates, salary bounds, and JSON syntax are validated by the Flask application.

## Project files

| File/folder | Purpose |
| --- | --- |
| `app.py` | Flask routes, CRUD logic, dashboard, skill-matching algorithm |
| `database.py` | MySQL connection configured using environment variables |
| `schema.sql` | **Destructive reset:** recreates the `job_tracker` database and four tables |
| `seed_assignments_1_to_7.sql` | Optional sample records for an **empty** project database (include this file if using the seed data) |
| `templates/` | HTML pages for dashboard, lists, details, forms, Job Match |
| `static/` | CSS styling |
| `tests/test_matching.py` | Skill-matching unit tests |
| `requirements.txt` | Python dependencies |
| `.env.example` | Placeholder environment configuration; **never put secrets here** |
| `AI_USAGE.md` | GenAI assistance and student testing record |

## Setup on Windows (Command Prompt)

1. Install **Python 3** and **MySQL Server 8+**. MySQL Workbench is recommended.
2. Clone the repository using **Windows Command Prompt**:

   ```cmd
   git clone https://github.com/KaoticJoker/job-application-tracker.git
   cd job-application-tracker
   ```

   Alternatively, download the GitHub ZIP and open CMD in the extracted folder containing `app.py` and `requirements.txt`.
3. Install dependencies:

   ```cmd
   python -m pip install -r requirements.txt
   ```

4. **Back up any existing `job_tracker` database before proceeding.** Open `schema.sql` in a connected MySQL Workbench session and execute the entire script. **It begins with `DROP DATABASE IF EXISTS job_tracker` and permanently deletes existing data.** If you already have a compatible populated database, skip this step.
5. **Load the demonstration data (recommended for grading):** Verify that `seed_assignments_1_to_7.sql` is in the repository root alongside `schema.sql`. After running `schema.sql` on a fresh/empty project database, open `seed_assignments_1_to_7.sql` in MySQL Workbench, connect to the same MySQL server, and execute the entire script **once**. The seed inserts five companies, 17 jobs, five applications, and five contacts, and sets up JSON demonstration values. **Do not run it on an already populated database:** it uses fixed IDs and may fail with duplicate-key errors. If the seed file is missing from the clone, the repository is incomplete; obtain/commit it before testing.
6. Copy `.env.example` to `.env` in the project folder. Edit `.env` with your own MySQL credentials and a new random Flask secret key:

   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=YOUR_MYSQL_PASSWORD
   DB_NAME=job_tracker
   FLASK_SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET
   ```

   Do not commit `.env` to GitHub. The included `.gitignore` should exclude it. Do not reuse the example values as real secrets.
7. Start Flask:

   ```cmd
   python app.py
   ```

8. Visit **http://127.0.0.1:5000**. Keep the CMD window running while using the application; press `Ctrl+C` to stop it.

### Optional: verify MySQL tables

```sql
USE job_tracker;
SHOW TABLES;
SELECT COUNT(*) FROM companies;
SELECT COUNT(*) FROM jobs;
SELECT COUNT(*) FROM applications;
SELECT COUNT(*) FROM contacts;
```

When the included sample data is loaded into an otherwise empty database, the initial counts should be **5 companies, 17 jobs, 5 applications, and 5 contacts**. These are demonstration counts, not required minimums.

## Job Match example

On **Job Match**, enter:

```text
Python, SQL, Git
```

With the provided sample data, the **Software Developer** role at **Tech Solutions Inc** returns **100%** (3 of 3 required skills). The **Data Analyst** role at **Data Analytics Corp** returns **33%** (1 of 3), with **Excel** and **Tableau** shown as missing.

When adding a job, enter a JSON object—not plain `Python`—in the Requirements JSON field, for example:

```json
{"required_skills":["Python","SQL","Git"]}
```

The algorithm compares skills case-insensitively, calculates `matched required skills / total required skills × 100`, and skips jobs without a usable `required_skills` list.

## Testing and observed results

The project was tested locally on Windows with Flask connected to MySQL:

| Test | Observed result |
| --- | --- |
| Flask startup and database connection | Dashboard loaded successfully |
| Sample dashboard | 5 companies, 17 jobs, 5 applications, 5 contacts |
| Company CRUD | Created, viewed, edited, deleted a temporary company; count returned to 5 |
| Job CRUD | Created, viewed, edited, deleted a temporary job; count returned to 17 |
| Application CRUD | Created with Applied status, updated to Interview, deleted; count returned to 5 |
| Contact CRUD | User confirmed create/read/update/delete passed |
| Job Match | 100% and 33% results with matched/missing skills displayed |
| Unit tests | 2 tests passed (`OK`) |

Run the automated tests from the project root:

```cmd
python -m unittest discover -s tests -v
```

The two unit tests check job ranking/missing skills and ignoring empty requirements. These tests are **not** a complete automated integration-test suite; CRUD and database connectivity were verified manually.

## Troubleshooting

- **`Access denied ... (using password: NO)`**: Check that `.env` exists (not `.env.example` or `.env.txt`), contains the actual MySQL password, and that `database.py` loads environment variables. Restart Flask after editing.
- **Dashboard shows zeros**: The tables may be empty. Add records in the UI or optionally run the seed script once on empty tables.
- **`Requirements JSON must be valid JSON`**: Use an object such as `{"required_skills":["Python","SQL"]}` rather than plain text.
- **`py` not recognized**: Use `python` commands instead if Python is available through PATH.
- **Delete blocked**: Foreign-key relationships may prevent deletion of a company/job with dependent records.

## Limitations and security

This is a local academic demonstration, **not** a production deployment. It does not provide user accounts or CSRF protection. Do not expose the Flask development server publicly. Keep `.env` private and use placeholder values in `.env.example`.

The final project schema differs from earlier assignment schemas (for example `job_url` vs. `posting_url`, and `contact_name` vs. separate first/last names). Do not apply the reset script to earlier coursework data without a backup.

## Course submission

- **GitHub:** https://github.com/KaoticJoker/job-application-tracker
- **Required source:** Flask code, templates, styling, `schema.sql`, `requirements.txt`, `README.md`, and `AI_USAGE.md`
- **Video:** Record and submit a **3–7 minute** demonstration showing the browser/client, Flask server, and MySQL database. The video is a separate submission deliverable.

Suggested demo: show the database and JSON fields; demonstrate dashboard statistics; perform representative CRUD operations; show Job Match results and missing skills; show the Flask CMD window; show the repository and documentation.
