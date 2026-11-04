# Fully Funded MSc Scholarship Tracker

### A Data-Driven Scholarship and Master's Programme Exploration System

## 1. Project Overview

The Fully Funded MSc Scholarship Tracker is a Python-based web application developed using Streamlit.

The project is designed to help international students explore scholarship opportunities, discover Master's programmes, check preliminary eligibility, track applications, and monitor important deadlines.

It combines scholarship information management, programme exploration, application tracking, and data visualization in a single interactive platform.

The initial focus is on opportunities relevant to students interested in Statistics, Biostatistics, Epidemiology, Public Health, Applied Statistics, and Data Science.

## 2. Project Objectives

The main objectives are:

* Develop an interactive scholarship information platform.
* Organize international scholarship opportunities.
* Explore Master's programmes across different countries.
* Provide a preliminary scholarship eligibility screening tool.
* Track scholarship application progress.
* Monitor upcoming application deadlines.
* Visualize scholarship and programme information through interactive charts.
* Maintain source information to support data verification.

## 3. Key Features

### Scholarship Dashboard

* Total scholarship statistics.
* Fully funded scholarship overview.
* Country-wise distribution.
* Study field distribution.
* Scholarship information table.

### Eligibility Checker

* Nationality-based screening.
* CGPA-based preliminary screening.
* IELTS score-based screening.
* Study field matching.
* Degree-level matching.

### Application Tracker

* Add scholarship applications.
* Record application deadlines.
* Update application status.
* Maintain application notes.
* Monitor application progress.

### Deadline Reminder

* Identify upcoming deadlines.
* Highlight urgent applications.
* Monitor expired deadlines.
* Display application deadline summaries.

### University Database

* Explore universities by country.
* Filter universities by study field.
* Access university websites.
* Download university information.

### Analytics Dashboard

* Country-wise scholarship distribution.
* Study field analysis.
* Funding distribution.
* CGPA requirement visualization.
* IELTS requirement visualization.
* Monthly deadline analysis.

### Verified Scholarship Database

* Store official scholarship programme information.
* Maintain official website references.
* Record eligibility information sources.
* Track the last verification date.
* Distinguish programme information from confirmed application requirements.

### Master's Programme Explorer

* Search Master's programmes.
* Filter by study area.
* Filter by programme country.
* Explore scholarship associations.
* Access official programme websites.

## 4. Technology Stack

| Technology         | Purpose                             |
| ------------------ | ----------------------------------- |
| Python             | Main programming language           |
| Streamlit          | Interactive web application         |
| Pandas             | Data manipulation                   |
| Plotly             | Interactive visualization           |
| SQLite             | Application tracking database       |
| CSV                | Scholarship and university datasets |
| Git and GitHub     | Version control and project hosting |
| Visual Studio Code | Development environment             |

## 5. Project Structure

```text
MSc-Scholarship-Tracker/
│
├── app.py
│
├── data/
│   ├── scholarships.csv
│   ├── universities.csv
│   ├── verified_scholarships.csv
│   └── programs.csv
│
├── database/
│   └── scholarship.db
│
├── pages/
│   ├── 1_Eligibility_Checker.py
│   ├── 2_Application_Tracker.py
│   ├── 3_Deadline_Reminder.py
│   ├── 4_University_Database.py
│   ├── 5_Analytics.py
│   ├── 6_Verified_Scholarship_Database.py
│   └── 7_Programme_Explorer.py
│
├── assets/
│
└── README.md
```

## 6. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Directory

```bash
cd MSc-Scholarship-Tracker
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install streamlit pandas plotly
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 7. Data Sources and Verification(Using Demo Data)

The project is designed to prioritize official scholarship providers, government agencies, universities, and programme websites.

Examples of official information sources include:

* Erasmus Mundus and the European Commission.
* DAAD.
* Japanese Ministry of Education, Culture, Sports, Science and Technology (MEXT).
* Fulbright Foreign Student Program.
* Australia Awards.

Each scholarship or programme record should ideally contain:

* Official website.
* Eligibility information source.
* Funding information.
* Application cycle.
* Deadline.
* Last verification date.
* Verification status.

## 8. Important Data Disclaimer

Some records currently included in the project are sample or demonstration data.

The presence of a scholarship or Master's programme in this application does not guarantee:

* Eligibility for a particular applicant.
* Scholarship availability for the 2028 intake.
* Confirmed application deadlines.
* Admission to a particular university.
* Full funding for every programme.

Applicants should always consult the relevant official scholarship provider and university before making application decisions.

The eligibility checker provides preliminary screening only. It does not replace official eligibility assessment.

## 9. Future Development

Planned improvements include:

* Integration of verified 2028 scholarship opportunities.
* Programme-specific eligibility assessment.
* Automated deadline monitoring.
* Email notifications.
* Advanced scholarship recommendation system.
* User authentication and personalized profiles.
* More advanced statistical analysis.
* Deployment as a publicly accessible web application.

## 10. Author
Delwar Hossan Rony 
Statistics & Data Science
Jatiya Kabi Kazi Nazrul Islam, University




