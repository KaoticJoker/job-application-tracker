-- COP4751 Job Tracker: sample records from Assignments 2, 3, and 7.
-- Compatible with the FINAL PROJECT schema.sql (not the older assignment schema).
-- RUN ONCE against the EMPTY project tables. Does NOT DROP or DELETE anything.
-- If you have existing rows, back up first and do not run this file unchanged.
-- Assignment 1 is setup; Assignments 4-6 emphasize transactions, Python and analytics,
-- rather than defining a single additional fixed final dataset.
USE job_tracker;
START TRANSACTION;

-- Assignment 2: five original companies (names, industries, cities, websites).
INSERT INTO companies (company_id,company_name,industry,website,city,state) VALUES
(1,'Tech Solutions Inc','Technology','www.techsolutions.com','Miami','Florida'),
(2,'Data Analytics Corp','Data Science','www.dataanalytics.com','Austin','Texas'),
(3,'Cloud Systems LLC','Cloud Computing','www.cloudsystems.com','Seattle','Washington'),
(4,'Digital Innovations','Software','www.digitalinnovations.com','San Francisco','California'),
(5,'Smart Tech Group','AI/ML','www.smarttech.com','Boston','Massachusetts');

-- Assignment 2: seven jobs; Assignment 3: ten additional jobs (17 total).
INSERT INTO jobs (job_id,company_id,job_title,salary_min,salary_max,job_type,date_posted) VALUES
(1,1,'Software Developer',70000,90000,'Full-time','2025-01-15'),
(2,1,'Database Administrator',75000,95000,'Full-time','2025-01-10'),
(3,2,'Data Analyst',65000,85000,'Full-time','2025-01-12'),
(4,3,'Cloud Engineer',80000,100000,'Full-time','2025-01-08'),
(5,4,'Junior Developer',55000,70000,'Full-time','2025-01-14'),
(6,4,'Senior Developer',95000,120000,'Full-time','2025-01-14'),
(7,5,'ML Engineer',90000,115000,'Full-time','2025-01-11'),
(8,1,'QA Engineer',60000,80000,'Full-time','2025-01-05'),
(9,2,'Business Analyst',65000,85000,'Full-time','2025-01-06'),
(10,2,'Data Scientist',85000,110000,'Full-time','2025-01-07'),
(11,3,'DevOps Engineer',80000,105000,'Full-time','2025-01-08'),
(12,3,'Security Analyst',75000,95000,'Full-time','2025-01-09'),
(13,4,'UI/UX Designer',60000,80000,'Full-time','2025-01-10'),
(14,5,'Product Manager',90000,120000,'Full-time','2025-01-11'),
(15,1,'Technical Writer',55000,75000,'Contract','2025-01-12'),
(16,2,'Intern - Data',30000,40000,'Internship','2025-01-13'),
(17,4,'Intern - Development',32000,42000,'Internship','2025-01-14');

-- Assignment 2: five applications. Map older status labels to final project ENUM:
-- 'Interview Scheduled' -> 'Interview'; 'Phone Screen' -> 'Screening'.
-- Assignment 2's later 'Interview Completed' update for application 3 cannot be
-- represented verbatim in the final project ENUM; final status remains Rejected.
INSERT INTO applications (application_id,job_id,application_date,status,resume_version,cover_letter_sent) VALUES
(1,1,'2025-01-16','Applied','v2.1',TRUE),
(2,3,'2025-01-13','Interview','v2.1',TRUE),
(3,4,'2025-01-09','Rejected','v2.0',FALSE),
(4,5,'2025-01-15','Applied','v2.1',TRUE),
(5,7,'2025-01-12','Screening','v2.1',TRUE);

-- Assignment 2: five contacts, combining first_name and last_name into contact_name.
INSERT INTO contacts (contact_id,company_id,contact_name,title,email) VALUES
(1,1,'Sarah Johnson','HR Manager','sjohnson@techsolutions.com'),
(2,2,'Michael Chen','Technical Recruiter','mchen@dataanalytics.com'),
(3,3,'Emily Williams','Hiring Manager','ewilliams@cloudsystems.com'),
(4,4,'David Brown','Senior Developer',NULL),
(5,5,'Lisa Garcia','Talent Acquisition','lgarcia@smarttech.com');

-- Assignment 7: requirements JSON for jobs 1 and 3.
UPDATE jobs SET requirements=JSON_OBJECT(
 'required_skills',JSON_ARRAY('Python','SQL','Git'),
 'preferred_skills',JSON_ARRAY('Flask','Docker','AWS'),
 'education','Bachelor in CS or related field','experience_years',2,'remote_option',TRUE)
WHERE job_id=1;
UPDATE jobs SET requirements=JSON_OBJECT(
 'required_skills',JSON_ARRAY('SQL','Excel','Tableau'),
 'preferred_skills',JSON_ARRAY('Python','R'),
 'education','Bachelor degree','experience_years',1,'remote_option',FALSE)
WHERE job_id=3;

-- Assignment 7: original interview JSON, followed by its JSON_SET, JSON_ARRAY_APPEND
-- and JSON_REMOVE exercises, producing the final expected JSON state.
UPDATE applications SET interview_data=JSON_OBJECT(
 'interview_rounds',2,
 'interviewers',JSON_ARRAY('Sarah Johnson','Mike Chen'),
 'technical_questions',JSON_ARRAY('SQL joins','Python basics','API design'),
 'feedback','Strong technical skills, good communication',
 'next_steps','Final round scheduled') WHERE application_id=2;
UPDATE applications SET interview_data=JSON_OBJECT(
 'interview_rounds',1,
 'interviewers',JSON_ARRAY('Emily Williams'),
 'technical_questions',JSON_ARRAY('Database normalization','Transaction isolation'),
 'feedback','Needs more experience with cloud platforms',
 'rating',3) WHERE application_id=5;
UPDATE applications SET interview_data=JSON_SET(interview_data,
 '$.next_steps','Offer extended!','$.offer_amount',85000) WHERE application_id=2;
UPDATE applications SET interview_data=JSON_ARRAY_APPEND(interview_data,
 '$.interviewers','David Brown') WHERE application_id=2;
UPDATE applications SET interview_data=JSON_REMOVE(interview_data,'$.rating') WHERE application_id=5;

COMMIT;

-- Assignment 3: optional performance indexes for the final schema.
-- Run separately if desired; do not re-run if these names already exist.
-- CREATE INDEX idx_job_title ON jobs(job_title);
-- CREATE INDEX idx_salary ON jobs(salary_min);
-- CREATE INDEX idx_company_type ON jobs(company_id,job_type);
-- CREATE INDEX idx_app_status ON applications(status);
-- CREATE INDEX idx_company_industry ON companies(industry);

-- Verify expected counts: 5 companies, 17 jobs, 5 applications, 5 contacts.
SELECT 'companies' AS table_name,COUNT(*) AS total FROM companies
UNION ALL SELECT 'jobs',COUNT(*) FROM jobs
UNION ALL SELECT 'applications',COUNT(*) FROM applications
UNION ALL SELECT 'contacts',COUNT(*) FROM contacts;
SELECT application_id,JSON_PRETTY(interview_data) AS interview_data
FROM applications WHERE interview_data IS NOT NULL ORDER BY application_id;
SELECT job_id,job_title,JSON_PRETTY(requirements) AS requirements
FROM jobs WHERE requirements IS NOT NULL ORDER BY job_id;
