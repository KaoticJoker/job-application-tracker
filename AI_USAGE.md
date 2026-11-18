# AI Usage Documentation — COP4751 Job Application Tracker

## Tools used

**ChatGPT (GPT-6)** was used to assist with planning, generating initial source code, designing the MySQL schema, writing Flask routes and HTML templates, preparing sample data, troubleshooting errors, and drafting documentation. MySQL Workbench, Windows CMD, Python, Git, and GitHub were used to set up and verify the project.

## Key prompts and requests

The following are representative prompts and follow-up requests from the development process:

1. **“Build the complete project”** based on the supplied COP4751 Job Application Tracker specification.
2. **“Can you make the schema sql replace everything in the db”** — requested a fresh database schema, including a destructive reset.
3. **“How do I open the project folder in cmd to install dependencies”** — requested Windows setup help.
4. **“Yes populate all four tables with sample data from assignments 1–7 final expected outcome”** — requested compatible demonstration data.
5. **“Is the project expecting there to be data? Also can you verify we've done every requirement from the project”** — requested a requirements review.
6. Follow-up questions and screenshots to troubleshoot **MySQL authentication**, **invalid JSON**, **Git setup**, **credential protection**, and **GitHub merge conflicts**.

## What AI assistance helped accomplish

- Drafted the four-table MySQL project schema with primary keys, foreign keys, and JSON fields.
- Generated the Flask backend for Companies, Jobs, Applications, and Contacts, including CRUD pages and dashboard queries.
- Generated the Job Match algorithm, which compares entered skills with `required_skills` JSON and ranks jobs by percentage.
- Produced reusable HTML templates, styling, and two automated matching tests.
- Helped adapt sample records from earlier database assignments to the final project schema.
- Provided troubleshooting steps and commands for Windows CMD, MySQL Workbench, Python dependencies, Git, and GitHub.

## What I changed or configured during development

The following actions were completed during the local setup and testing process:

- Switched from the original database setup to a resettable project schema, then imported sample records into the new tables.
- Configured the local `.env` file with MySQL connection settings. Fixed an authentication failure caused by the application initially attempting to connect without a password.
- Used `python app.py` after `py` was not recognized in CMD.
- Corrected an invalid Job Requirements JSON input: entering plain `Python` caused a validation error; using a JSON object with `required_skills` allowed the job to be saved.
- Tested creating, viewing, editing, and deleting temporary records in all four sections, confirming that the original sample counts were restored afterward.
- Corrected the test discovery command to point to `tests` rather than `test`.
- Installed Git, initialized the repository, configured the main branch, and uploaded the project to GitHub.
- Ensured `.env` was excluded by `.gitignore`, corrected the example environment file to use placeholder credentials, and resolved merge conflicts in `.gitignore` and `README.md` before pushing.

These are setup, configuration, testing, and version-control actions. They do not imply that every line of the AI-generated application code was manually rewritten.

## Verification and testing

| Area | Evidence observed during local testing |
| --- | --- |
| Flask + MySQL | Flask server started and dashboard loaded after configuring the `.env` file |
| Database | Dashboard showed 5 companies, 17 jobs, 5 applications, 5 contacts after sample import |
| Dashboard | Application status breakdown and recent applications displayed |
| Companies CRUD | Temporary company added and edited, then deleted; count returned to 5 |
| Jobs CRUD | Temporary job added and edited, then deleted; count returned to 17 |
| Applications CRUD | Temporary application added (Applied), updated (Interview), then deleted; count returned to 5 |
| Contacts CRUD | Create, read, update, and delete manually confirmed successful |
| Job Match | `Python, SQL, Git` returned 100% for Software Developer and 33% for Data Analyst, with missing skills displayed |
| Automated tests | `python -m unittest discover -s tests -v` completed with **2 tests, OK** |
| GitHub | Local `main` branch pushed successfully to `origin/main` |

**GitHub repository:** https://github.com/KaoticJoker/job-application-tracker

## Lessons learned

- **AI-generated code must be tested:** The initial server startup did not guarantee a successful database connection. The MySQL error message helped identify missing credentials.
- **JSON requires a specific structure:** Plain text such as `Python` is not a valid JSON value in the required format. A JSON object containing `required_skills` is needed for the matching feature.
- **Database relationships matter:** Foreign keys connect related records and can prevent accidental deletion of referenced parent records.
- **Testing should cover both behavior and code:** Manual CRUD tests confirmed the database operations, while automated tests checked key parts of the matching algorithm.
- **Version control requires care:** Git staging, commits, remote synchronization, merge conflicts, and ignoring secrets are important parts of sharing a working application.
- **AI is a development aid, not proof of correctness:** The final behavior was checked by running the application, reviewing screenshots/results, and performing local tests.

## Limitations and next steps

The automated suite currently contains two matching tests, not comprehensive database integration tests. The application is intended for a local academic demonstration, not public production hosting. A **3–7 minute demonstration video** showing the browser, Flask server, and MySQL database is still required as a separate submission item.

This document records AI assistance and the tests actually reported during development; it does not claim unperformed code changes or testing.
