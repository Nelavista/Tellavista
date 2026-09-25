"""Seed data for the Data Engineering 30-Day Skill Class."""

SKILL = {
    "slug": "data-engineering",
    "name": "Data Engineering",
    "tagline": "Learn to build the pipelines that move and clean the data every company runs on.",
    "description": "Data engineering is the discipline of building reliable systems that collect, clean, and deliver data so analysts, data scientists, and applications can use it. Nigerian fintechs, telcos, and startups all run on pipelines built by data engineers, and the role is one of the highest-paid entry points into tech because bad data breaks everything downstream. This track takes you from your first SQL query to building and documenting a full ETL pipeline you can show an employer or client.",
    "level": "beginner",
    "estimated_hours": 62,
    "course_title": "30-Day Data Engineering Career Track",
    "course_description": "After 30 days you will be able to extract data from files, APIs, and databases, clean and transform it with Python and SQL, load it into a proper database, and automate and document the whole pipeline like a working data engineer.",
    "final_project": {
        "title": "Build an End-to-End ETL Pipeline",
        "description": "Design and build a real ETL pipeline that pulls data from at least two sources (for example a public CSV dataset and a REST API), cleans and validates it with Python, transforms it into an analysis-ready shape, and loads it into a PostgreSQL or SQLite database. The pipeline must run as a single reproducible script or Airflow DAG, include a README explaining the architecture and how to run it, and handle at least one realistic data-quality problem (missing values, duplicates, or mismatched types) with a documented fix. This is the exact kind of project hiring managers and freelance clients ask to see before they trust you with their data.",
        "difficulty": "advanced",
        "estimated_hours": 10,
        "skills_demonstrated": ["Python", "SQL", "ETL design", "data cleaning", "database loading", "pipeline documentation", "API integration"],
        "rubric": [
            {"name": "Pipeline correctness and reproducibility", "max_points": 35},
            {"name": "Data cleaning and transformation quality", "max_points": 25},
            {"name": "Database design and loading", "max_points": 20},
            {"name": "Documentation and code clarity", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Data Engineering Foundations",
            "title": "What Data Engineers Actually Build and Why Companies Pay for It",
            "learning_objective": "By the end of this class, you will be able to describe the data engineering role and trace the journey of data from a raw source to a business dashboard.",
            "duration_minutes": 25,
            "content_html": """<p>Every app, dashboard, and machine learning model you have ever used depends on data arriving clean and on time somewhere behind the scenes. That is the data engineer's job: build and maintain the pipelines that move data from messy sources into a shape other people can trust and use. In Nigeria, banks, fintechs like Flutterwave and Paystack, telcos, and logistics startups all hire data engineers to keep their reporting and product data flowing, often before they hire data scientists, because you cannot analyze data that has not been collected and cleaned yet.</p><h2>The Data Journey</h2><p>Data typically moves through four stages: it is <strong>extracted</strong> from a source (an app database, a CSV export, a third-party API), <strong>cleaned</strong> to fix errors and inconsistencies, <strong>transformed</strong> into a useful shape (aggregated, joined, reshaped), and <strong>loaded</strong> into a destination like a data warehouse where analysts query it. This is the classic ETL pattern you will build toward across this track.</p><h2>A Real Example</h2><p>Imagine a Nigerian delivery startup with rider location pings landing in a raw events table every second. A data engineer writes a pipeline that pulls those pings nightly, removes duplicate or corrupted entries, calculates each rider's daily distance covered, and loads the result into a summary table the operations team checks every morning. That summary table only exists because someone built and maintained the pipeline behind it.</p>""",
            "key_concepts": ["data engineering role", "ETL pattern", "data pipeline", "data warehouse", "extract, transform, load"],
            "practical_exercise": {
                "title": "Map a Data Pipeline You Use Daily",
                "instructions": "Pick one app or website you use often (a banking app, a food delivery app, or a school portal). Write a half-page description of what raw data it probably collects, how that data might need to be cleaned, and what final report or feature that data likely powers. Submit your write-up as a short text document."
            },
            "quiz": [
                {"question": "What is the primary job of a data engineer?", "options": ["Design visual dashboards only", "Build and maintain pipelines that move and clean data", "Write marketing copy for data products", "Manage company social media accounts"], "correct_index": 1, "explanation": "Data engineers build the systems that extract, clean, transform, and load data so others can use it reliably."},
                {"question": "What does the 'T' in ETL stand for?", "options": ["Transfer", "Test", "Transform", "Track"], "correct_index": 2, "explanation": "ETL stands for Extract, Transform, Load — the transform step reshapes and cleans the data."},
                {"question": "Why might a company hire a data engineer before a data scientist?", "options": ["Data engineers are cheaper to hire", "You cannot analyze data that has not been collected and cleaned yet", "Data scientists do not use data", "It is a legal requirement"], "correct_index": 1, "explanation": "Data scientists need clean, reliable data to work with, which is exactly what data engineering pipelines provide."}
            ],
            "resources": [
                {"label": "Kaggle Learn: Intro to Programming and Data", "url": "https://www.kaggle.com/learn"},
                {"label": "MDN: Introduction to Data", "url": "https://developer.mozilla.org/"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Data Engineering Foundations",
            "title": "Setting Up Your Python, SQL, and Git Toolkit for Data Engineering",
            "learning_objective": "By the end of this class, you will be able to install and configure Python, a SQL client, and Git so you can start writing and version-controlling data pipeline code.",
            "duration_minutes": 30,
            "content_html": """<p>Before you write a single pipeline, you need a working toolkit. Data engineers live in three tools daily: Python for writing pipeline logic, SQL for querying and shaping data inside databases, and Git for tracking changes to their code so nothing gets lost and mistakes can be undone. Getting comfortable with this setup now saves you hours of frustration later when a pipeline breaks and you need to debug it quickly.</p><h2>What You Need Installed</h2><p>Install Python 3.10 or newer, a code editor like VS Code, and Git. Then create a virtual environment for each project so its packages do not conflict with other projects on your machine.</p><pre><code>python -m venv venv
venv\\Scripts\\activate
pip install pandas sqlalchemy psycopg2-binary</code></pre><h2>Why Virtual Environments Matter</h2><p>Without a virtual environment, every Python project on your laptop shares the same package versions, and upgrading one project can silently break another. A virtual environment isolates each project's dependencies, which is exactly how professional data teams avoid the classic 'it works on my machine' problem. You will use this same venv-and-install pattern for every project in this track and in your future job.</p>""",
            "key_concepts": ["Python environment setup", "virtual environments", "pip", "Git basics", "SQL client"],
            "practical_exercise": {
                "title": "Set Up Your Working Environment",
                "instructions": "Install Python, VS Code, and Git on your machine. Create a project folder called data-eng-track, initialize a virtual environment inside it, install pandas and sqlalchemy, and initialize a Git repository. Take a screenshot of your terminal showing the successful pip install output and submit it."
            },
            "quiz": [
                {"question": "What is the purpose of a Python virtual environment?", "options": ["To make code run faster", "To isolate a project's package dependencies from other projects", "To connect to the internet", "To replace Git"], "correct_index": 1, "explanation": "Virtual environments keep each project's dependencies separate, avoiding version conflicts between projects."},
                {"question": "Which command creates a new virtual environment in a folder called venv?", "options": ["pip install venv", "python -m venv venv", "git init venv", "sql create venv"], "correct_index": 1, "explanation": "python -m venv venv creates a new isolated Python environment in a folder named venv."},
                {"question": "Why do data engineers use Git?", "options": ["To design dashboards", "To track and version-control changes to their pipeline code", "To send emails", "To clean CSV files"], "correct_index": 1, "explanation": "Git tracks changes to code over time, letting engineers collaborate safely and undo mistakes."}
            ],
            "resources": [
                {"label": "Python Docs: Getting Started", "url": "https://docs.python.org/3/"},
                {"label": "GitHub", "url": "https://github.com/"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Data Engineering Foundations",
            "title": "Reading, Inspecting, and Writing CSV and JSON Data with Python",
            "learning_objective": "By the end of this class, you will be able to load CSV and JSON files into Python with pandas and inspect their structure before working with them.",
            "duration_minutes": 25,
            "content_html": """<p>CSV and JSON are the two file formats you will encounter constantly as a data engineer: CSV from spreadsheet exports, bank statements, and government open-data portals, and JSON from APIs and web applications. Before you can clean or transform any dataset, you need to load it correctly and understand its shape, column names, and data types.</p><h2>Loading and Inspecting Data</h2><p>The pandas library is the standard tool for this. Loading a file takes one line, but inspecting it properly is what separates a careful engineer from someone about to ship a broken pipeline.</p><pre><code>import pandas as pd

df = pd.read_csv("students.csv")
print(df.shape)
print(df.head())
print(df.dtypes)
print(df.isnull().sum())</code></pre><h2>Reading JSON</h2><p>JSON files often contain nested structures, unlike the flat rows of a CSV. pandas can still load simple JSON directly, but nested JSON (common from APIs) usually needs json_normalize to flatten it into rows and columns.</p><pre><code>import json
with open("results.json") as f:
    data = json.load(f)
df = pd.json_normalize(data)</code></pre><p>Always check shape, dtypes, and null counts before doing anything else. This five-second habit catches most data surprises before they cause bugs three steps later in your pipeline.</p>""",
            "key_concepts": ["CSV files", "JSON files", "pandas DataFrame", "data inspection", "json_normalize"],
            "practical_exercise": {
                "title": "Load and Inspect a Public Dataset",
                "instructions": "Download any public CSV dataset from Kaggle (for example a Nigeria population or Lagos traffic dataset). Load it with pandas, print its shape, column names, data types, and null counts. Write three sentences summarizing what you notice about the data quality. Submit your script and summary."
            },
            "quiz": [
                {"question": "Which pandas function loads a CSV file into a DataFrame?", "options": ["pd.load_csv()", "pd.read_csv()", "pd.open_csv()", "pd.import_csv()"], "correct_index": 1, "explanation": "pd.read_csv() is the standard pandas function for loading CSV files."},
                {"question": "What does df.isnull().sum() tell you?", "options": ["The total number of rows", "The number of missing values in each column", "The average value of each column", "The file size"], "correct_index": 1, "explanation": "df.isnull().sum() counts missing (null) values per column, which is essential for spotting data quality issues early."},
                {"question": "Why might nested JSON need json_normalize before analysis?", "options": ["JSON files cannot be read by Python", "Nested JSON needs to be flattened into rows and columns to work like a table", "json_normalize deletes duplicate data", "JSON is always faster than CSV"], "correct_index": 1, "explanation": "json_normalize flattens nested JSON structures into a flat table shape that pandas can analyze like a spreadsheet."}
            ],
            "resources": [
                {"label": "pandas Documentation", "url": "https://pandas.pydata.org/docs/"},
                {"label": "Kaggle Learn: Pandas", "url": "https://www.kaggle.com/learn/pandas"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Data Engineering Foundations",
            "title": "Understanding Data Types, Schemas, and Structured vs Unstructured Data",
            "learning_objective": "By the end of this class, you will be able to identify a dataset's schema and classify its data as structured, semi-structured, or unstructured.",
            "duration_minutes": 20,
            "content_html": """<p>Every pipeline decision you make depends on understanding what kind of data you are dealing with. A <strong>schema</strong> is the blueprint of a dataset: the column names, their data types, and the rules about what values are allowed. Getting the schema wrong early is one of the most common causes of pipeline failures further down the line, so data engineers spend real time understanding it before writing transformation code.</p><h2>Structured, Semi-Structured, and Unstructured</h2><p><strong>Structured data</strong> fits neatly into rows and columns, like a bank transactions table with fixed fields for date, amount, and account number. <strong>Semi-structured data</strong>, like JSON from an API, has some organization but flexible fields that can vary between records. <strong>Unstructured data</strong>, like a folder of PDF resumes or WhatsApp chat logs, has no fixed format at all and needs extra processing before it becomes usable.</p><h2>Reading a Schema in Practice</h2><pre><code>import pandas as pd
df = pd.read_csv("transactions.csv")
print(df.dtypes)
# amount     float64
# date       object
# account_id int64</code></pre><p>Notice that dates often load as generic 'object' type rather than a real date type — this is a common schema mismatch you will fix constantly as a data engineer, because a date stored as text cannot be sorted or filtered correctly until it is converted.</p>""",
            "key_concepts": ["schema", "structured data", "semi-structured data", "unstructured data", "data types"],
            "practical_exercise": {
                "title": "Classify Three Real Data Sources",
                "instructions": "List three data sources you interact with weekly (for example a bank statement, an Instagram post, and a school timetable). For each, state whether it is structured, semi-structured, or unstructured, and explain why in one sentence. Submit your classification as a short document."
            },
            "quiz": [
                {"question": "What is a schema?", "options": ["A type of chart", "The blueprint of a dataset defining column names, types, and rules", "A password for a database", "A JSON file format"], "correct_index": 1, "explanation": "A schema describes the structure of a dataset: its columns, their types, and any constraints on valid values."},
                {"question": "Which of these is an example of unstructured data?", "options": ["A SQL table of customer orders", "A folder of scanned PDF documents", "A CSV of exam scores", "A JSON array of product prices"], "correct_index": 1, "explanation": "Scanned PDFs have no fixed row-and-column structure, making them unstructured data."},
                {"question": "Why do dates often need to be converted after loading a CSV?", "options": ["CSVs cannot store numbers", "Dates often load as plain text (object type) instead of a true date type", "Dates are always stored in JSON only", "pandas cannot read CSV files with dates"], "correct_index": 1, "explanation": "CSV has no native date type, so pandas often reads dates as generic text objects that need explicit conversion."}
            ],
            "resources": [
                {"label": "W3Schools SQL Data Types", "url": "https://www.w3schools.com/sql/sql_datatypes.asp"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Data Engineering Foundations",
            "title": "Querying Data with SQL: SELECT, WHERE, GROUP BY, and JOIN",
            "learning_objective": "By the end of this class, you will be able to write SQL queries that filter, aggregate, and join data across tables.",
            "duration_minutes": 30,
            "content_html": """<p>SQL is the language every data engineer uses to talk to databases, and it shows up in nearly every data engineering job interview. Unlike Python, which processes data row by row in memory, SQL lets you ask a database directly for the exact slice of data you need, which is often far faster for large datasets.</p><h2>The Core Four</h2><p>SELECT chooses columns, WHERE filters rows, GROUP BY aggregates rows into summaries, and JOIN combines data from multiple tables using a shared key.</p><pre><code>SELECT customer_id, SUM(amount) AS total_spent
FROM transactions
WHERE transaction_date >= "2026-01-01"
GROUP BY customer_id
ORDER BY total_spent DESC;</code></pre><h2>Joining Tables</h2><p>Real databases split data across multiple tables to avoid repetition. A JOIN connects them using a shared column, like customer_id, so you can answer questions that span both tables.</p><pre><code>SELECT c.customer_name, SUM(t.amount) AS total_spent
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_name;</code></pre><p>Every data engineering job posting you will see lists SQL as a required skill, often above Python, because so much of the world's data still lives in relational databases queried this way.</p>""",
            "key_concepts": ["SELECT", "WHERE", "GROUP BY", "JOIN", "relational databases"],
            "practical_exercise": {
                "title": "Write Five SQL Queries Against a Sample Database",
                "instructions": "Using SQLite or an online SQL sandbox, load any sample dataset with at least two related tables (customers and orders work well). Write five queries: one SELECT with a WHERE filter, one GROUP BY with an aggregate function, one JOIN, and two of your own choice. Submit the queries and their output."
            },
            "quiz": [
                {"question": "Which SQL clause is used to filter rows before aggregation?", "options": ["GROUP BY", "WHERE", "ORDER BY", "JOIN"], "correct_index": 1, "explanation": "WHERE filters individual rows before any grouping or aggregation happens."},
                {"question": "What does a JOIN allow you to do?", "options": ["Delete rows from a table", "Combine data from multiple tables using a shared key", "Change a column's data type", "Create a new database"], "correct_index": 1, "explanation": "JOIN combines rows from two or more tables based on a related column between them."},
                {"question": "In the query 'SELECT customer_id, SUM(amount) FROM transactions GROUP BY customer_id', what does GROUP BY do?", "options": ["Sorts the results alphabetically", "Groups rows sharing the same customer_id so SUM can total each group", "Deletes duplicate customer_ids", "Filters out null amounts"], "correct_index": 1, "explanation": "GROUP BY collapses rows with the same customer_id into one group so aggregate functions like SUM can total each group."}
            ],
            "resources": [
                {"label": "W3Schools SQL Tutorial", "url": "https://www.w3schools.com/sql/"},
                {"label": "Khan Academy: SQL", "url": "https://www.khanacademy.org/"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Cleaning and Modeling Real Data",
            "title": "Cleaning Messy Real-World Data with Pandas",
            "learning_objective": "By the end of this class, you will be able to identify and fix missing values, duplicates, and inconsistent formatting in a raw dataset.",
            "duration_minutes": 30,
            "content_html": """<p>Real data is never clean. Names are misspelled, phone numbers have inconsistent formats, dates come in three different styles, and rows get duplicated when systems glitch. Data cleaning typically consumes 60 to 80 percent of a data engineer's actual working time, which is why it deserves a full class of its own rather than a quick mention.</p><h2>Handling Missing Values</h2><p>You generally have three choices for missing data: drop the row, fill it with a sensible default, or flag it for review. The right choice depends on how much data you would lose and how important that field is.</p><pre><code>df = df.dropna(subset=["customer_id"])
df["region"] = df["region"].fillna("Unknown")</code></pre><h2>Removing Duplicates and Standardizing Formats</h2><p>Duplicate rows commonly appear when an API is called twice or a file is imported more than once. Inconsistent text formatting, like "lagos" versus "Lagos" versus "LAGOS ", breaks grouping and filtering unless you standardize it first.</p><pre><code>df = df.drop_duplicates()
df["city"] = df["city"].str.strip().str.title()</code></pre><p>A pipeline that skips this step will silently produce wrong totals and wrong reports, and nobody may notice until a manager questions a number in a meeting.</p>""",
            "key_concepts": ["missing values", "duplicates", "data standardization", "dropna", "fillna"],
            "practical_exercise": {
                "title": "Clean a Deliberately Messy Dataset",
                "instructions": "Take any CSV dataset (or intentionally add 5 duplicate rows and 5 missing values to a clean one). Write a pandas script that reports the number of missing values and duplicates found, then fixes both issues with a documented decision for each fix. Submit the before-and-after row counts and your script."
            },
            "quiz": [
                {"question": "Roughly how much of a data engineer's time is typically spent on data cleaning?", "options": ["About 5 percent", "About 20 percent", "60 to 80 percent", "It is never needed"], "correct_index": 2, "explanation": "Industry surveys consistently show data cleaning consumes the majority of a data professional's time."},
                {"question": "Which pandas method removes duplicate rows?", "options": ["df.dropna()", "df.drop_duplicates()", "df.fillna()", "df.unique()"], "correct_index": 1, "explanation": "drop_duplicates() removes rows that are exact duplicates of another row in the DataFrame."},
                {"question": "Why might 'lagos' and 'Lagos' cause a bug in a grouping operation?", "options": ["pandas cannot read lowercase text", "They are treated as two different values because text comparison is case-sensitive", "SQL does not support text data", "CSV files cannot contain city names"], "correct_index": 1, "explanation": "Without standardizing case, pandas and SQL treat differently-cased strings as distinct values, splitting what should be one group into two."}
            ],
            "resources": [
                {"label": "pandas Documentation", "url": "https://pandas.pydata.org/docs/"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Cleaning and Modeling Real Data",
            "title": "Transforming Data with Pandas: Filtering, Aggregating, and Reshaping",
            "learning_objective": "By the end of this class, you will be able to transform a cleaned dataset into a summarized, analysis-ready shape using pandas.",
            "duration_minutes": 30,
            "content_html": """<p>Once data is clean, the next job is transforming it into the shape someone actually needs. Raw transaction-level data is rarely useful on its own; a manager wants monthly totals per region, not ten thousand individual rows. Transformation is where a data engineer turns raw facts into business-ready information.</p><h2>Filtering and Aggregating</h2><p>groupby is the core transformation tool in pandas, letting you summarize data by category.</p><pre><code>monthly_sales = df.groupby(["region", "month"])["amount"].sum().reset_index()
top_regions = monthly_sales.sort_values("amount", ascending=False).head(5)</code></pre><h2>Reshaping with Pivot and Merge</h2><p>Sometimes you need to reshape data from long format (one row per event) to wide format (one row per entity with columns per category), which pivot_table handles well. merge combines two DataFrames the same way a SQL JOIN combines two tables.</p><pre><code>pivot = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
combined = pd.merge(orders_df, customers_df, on="customer_id", how="left")</code></pre><p>Knowing when to use groupby versus pivot versus merge is a skill that only comes from practice, so today you will apply all three to one dataset and compare the outputs.</p>""",
            "key_concepts": ["groupby", "pivot_table", "merge", "data reshaping", "aggregation"],
            "practical_exercise": {
                "title": "Transform a Sales Dataset into a Summary Report",
                "instructions": "Using any sales or transactions dataset, write a pandas script that produces: a groupby summary of total amount by category, a pivot table of amount by region and month, and a merge with a second small lookup table you create yourself. Submit your script and the three resulting tables."
            },
            "quiz": [
                {"question": "What does the pandas groupby function do?", "options": ["Deletes rows with missing values", "Groups rows by shared values in a column so you can aggregate each group", "Converts a DataFrame to JSON", "Sorts a DataFrame alphabetically"], "correct_index": 1, "explanation": "groupby splits data into groups based on column values, enabling aggregate calculations per group."},
                {"question": "Which pandas function is most similar to a SQL JOIN?", "options": ["merge()", "pivot_table()", "groupby()", "dropna()"], "correct_index": 0, "explanation": "pandas merge() combines two DataFrames based on a shared key, just like a SQL JOIN combines two tables."},
                {"question": "What is the main use of pivot_table?", "options": ["To remove duplicate rows", "To reshape data from a long row-based format into a wide summary format", "To connect to a database", "To convert text to numbers"], "correct_index": 1, "explanation": "pivot_table reshapes long-format data into a wide summary table with categories as rows and columns."}
            ],
            "resources": [
                {"label": "pandas Documentation: GroupBy", "url": "https://pandas.pydata.org/docs/"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Cleaning and Modeling Real Data",
            "title": "Designing a Relational Schema: Keys, Normalization, and ER Diagrams",
            "learning_objective": "By the end of this class, you will be able to design a normalized relational schema with primary and foreign keys for a real-world scenario.",
            "duration_minutes": 30,
            "content_html": """<p>Before loading data into a database, a data engineer has to decide how it should be organized. A poorly designed schema causes duplicate data, slow queries, and bugs that are painful to fix once a pipeline is live in production, so schema design is a skill worth doing carefully rather than rushing.</p><h2>Primary and Foreign Keys</h2><p>A <strong>primary key</strong> uniquely identifies each row in a table, like a student_id in a students table. A <strong>foreign key</strong> is a column in one table that references the primary key of another, creating a relationship between the two.</p><pre><code>CREATE TABLE students (
  student_id INTEGER PRIMARY KEY,
  full_name TEXT
);
CREATE TABLE enrollments (
  enrollment_id INTEGER PRIMARY KEY,
  student_id INTEGER REFERENCES students(student_id),
  course_name TEXT
);</code></pre><h2>Normalization in Plain Terms</h2><p>Normalization means splitting data into separate tables to avoid repeating the same information. Instead of storing a student's full name in every single enrollment row, you store it once in a students table and reference it by id elsewhere. This keeps updates simple: change a student's name once, and every related record stays correct.</p><p>Sketching an ER (entity-relationship) diagram on paper before writing any CREATE TABLE statement is a habit every experienced data engineer relies on.</p>""",
            "key_concepts": ["primary key", "foreign key", "normalization", "ER diagram", "relational schema"],
            "practical_exercise": {
                "title": "Design a Schema for a Campus Bookshop",
                "instructions": "Design a normalized relational schema for a campus bookshop with students, books, and purchases. Sketch or list your tables with primary and foreign keys clearly marked, then write the CREATE TABLE SQL statements for all three tables. Submit your ER sketch (photo or drawing is fine) and your SQL."
            },
            "quiz": [
                {"question": "What does a primary key do?", "options": ["Encrypts a table", "Uniquely identifies each row in a table", "Deletes duplicate rows automatically", "Connects a database to the internet"], "correct_index": 1, "explanation": "A primary key is a column (or set of columns) that uniquely identifies every row in a table."},
                {"question": "What is the purpose of normalization?", "options": ["To make queries run in a random order", "To split data into separate tables to avoid repeating the same information", "To convert SQL into Python", "To delete all foreign keys"], "correct_index": 1, "explanation": "Normalization reduces redundancy by storing each piece of information in only one place, connected via keys."},
                {"question": "What does a foreign key do?", "options": ["Sets a table's storage location", "References the primary key of another table to create a relationship", "Deletes rows from a table", "Encrypts sensitive columns"], "correct_index": 1, "explanation": "A foreign key links a row to a row in another table, enforcing a relationship between the two."}
            ],
            "resources": [
                {"label": "W3Schools SQL Keys", "url": "https://www.w3schools.com/sql/sql_primarykey.asp"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Cleaning and Modeling Real Data",
            "title": "Loading Data into PostgreSQL with Python and SQLAlchemy",
            "learning_objective": "By the end of this class, you will be able to load a cleaned pandas DataFrame into a PostgreSQL database using SQLAlchemy.",
            "duration_minutes": 30,
            "content_html": """<p>Cleaning and transforming data in pandas is only useful if the result ends up somewhere other people and applications can query it. PostgreSQL is one of the most widely used open-source databases in the industry, and SQLAlchemy is the standard Python library for talking to it, so this combination shows up in data engineering jobs constantly.</p><h2>Connecting and Loading</h2><p>SQLAlchemy creates a connection "engine" that pandas can then use directly to write a DataFrame into a table.</p><pre><code>from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://user:password@localhost:5432/mydb")
df = pd.read_csv("clean_sales.csv")
df.to_sql("sales", engine, if_exists="replace", index=False)</code></pre><h2>Choosing if_exists Carefully</h2><p>The if_exists parameter controls what happens if the table already has data: "replace" wipes and recreates the table, "append" adds new rows on top of existing ones, and "fail" stops with an error if the table exists. Picking the wrong option in production can silently delete real data, so this is a decision worth making deliberately every time, not by default.</p><p>Once loaded, you can confirm the data arrived correctly with a simple SELECT COUNT(*) query from any SQL client.</p>""",
            "key_concepts": ["SQLAlchemy", "PostgreSQL", "to_sql", "database connection engine", "if_exists parameter"],
            "practical_exercise": {
                "title": "Load a Cleaned Dataset into a Local Database",
                "instructions": "Install PostgreSQL or use SQLite as a substitute. Take a dataset you cleaned in an earlier class, connect to your database with SQLAlchemy, and load it into a new table using to_sql. Then run a SELECT query to confirm the row count matches your DataFrame. Submit your script and the query result."
            },
            "quiz": [
                {"question": "What does the SQLAlchemy create_engine function do?", "options": ["Creates a new CSV file", "Creates a connection to a database that pandas and Python can use", "Deletes a database", "Converts SQL to Python code"], "correct_index": 1, "explanation": "create_engine builds a reusable connection object that libraries like pandas use to talk to a database."},
                {"question": "What happens if you use if_exists='replace' when loading a table that already has important data?", "options": ["The new data is appended safely", "The existing table is wiped and recreated, losing the old data", "Nothing happens until you confirm manually", "It automatically creates a backup first"], "correct_index": 1, "explanation": "'replace' drops and recreates the table, which permanently deletes whatever data was there before."},
                {"question": "Which pandas method writes a DataFrame directly into a SQL database table?", "options": ["df.to_csv()", "df.to_sql()", "df.read_sql()", "df.to_json()"], "correct_index": 1, "explanation": "df.to_sql() writes a DataFrame's contents into a specified database table through a SQLAlchemy engine."}
            ],
            "resources": [
                {"label": "SQLAlchemy Documentation", "url": "https://www.sqlalchemy.org/"},
                {"label": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Cleaning and Modeling Real Data",
            "title": "Building Your First End-to-End Mini ETL Script",
            "learning_objective": "By the end of this class, you will be able to write a single Python script that extracts, cleans, transforms, and loads data from start to finish.",
            "duration_minutes": 35,
            "content_html": """<p>Today you combine everything from week one into one working pipeline. This is the moment the individual skills — reading files, cleaning data, writing SQL, loading into a database — click together into what a data engineer actually ships: a script that takes raw data in and produces clean, queryable data out, with no manual steps in between.</p><h2>Structuring the Script</h2><p>A good mini ETL script separates its logic into clear functions, one per stage, so each part can be tested and understood independently.</p><pre><code>def extract(path):
    return pd.read_csv(path)

def clean(df):
    df = df.drop_duplicates()
    df = df.dropna(subset=["customer_id"])
    return df

def transform(df):
    return df.groupby("region")["amount"].sum().reset_index()

def load(df, engine, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)

if __name__ == "__main__":
    df = extract("sales.csv")
    df = clean(df)
    df = transform(df)
    load(df, engine, "region_sales_summary")
    print("Pipeline complete:", len(df), "rows loaded")</code></pre><h2>Why the print Statement Matters</h2><p>That final print statement is a small but real habit: every pipeline should report what it did when it finishes, so whoever runs it (including future you) knows it worked without having to check the database manually.</p>""",
            "key_concepts": ["ETL script structure", "function separation", "pipeline stages", "extract-clean-transform-load"],
            "practical_exercise": {
                "title": "Build a Complete Mini ETL Script",
                "instructions": "Write a single Python script with separate extract, clean, transform, and load functions that reads a CSV, removes duplicates and nulls, aggregates it by one category, and loads the result into a SQLite or PostgreSQL table. Run it end to end and confirm the output table exists with correct data. Submit your full script."
            },
            "quiz": [
                {"question": "Why should an ETL script separate its logic into distinct functions?", "options": ["Python requires it", "It makes each stage easier to test, debug, and understand independently", "It makes the script run faster automatically", "Functions are required for database connections"], "correct_index": 1, "explanation": "Separating extract, clean, transform, and load into functions makes each stage independently testable and easier to maintain."},
                {"question": "What is the benefit of printing a completion message at the end of a pipeline script?", "options": ["It is required by Python syntax", "It confirms to whoever runs the script that it finished successfully and what it did", "It speeds up the database load", "It automatically emails the team"], "correct_index": 1, "explanation": "A completion message gives immediate, visible confirmation that the pipeline ran successfully without needing to check the database manually."},
                {"question": "In the ETL pattern, which stage typically comes right after extract?", "options": ["Load", "Clean/transform", "Deploy", "Schedule"], "correct_index": 1, "explanation": "After data is extracted from its source, it is cleaned and transformed before being loaded into its destination."}
            ],
            "resources": [
                {"label": "Python Docs: Functions", "url": "https://docs.python.org/3/tutorial/controlflow.html"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Building Real Pipelines",
            "title": "Understanding the ETL vs ELT Pattern and When to Use Each",
            "learning_objective": "By the end of this class, you will be able to explain the difference between ETL and ELT and decide which pattern fits a given scenario.",
            "duration_minutes": 25,
            "content_html": """<p>As datasets grow larger, transforming data before loading it (ETL) is not always the best approach. Modern cloud data warehouses like BigQuery, Snowflake, and Redshift are powerful enough to handle raw data directly, which gave rise to a second pattern: ELT, where you load raw data first and transform it afterward inside the warehouse itself.</p><h2>ETL vs ELT</h2><p>In <strong>ETL</strong>, transformation happens in your pipeline code (Python or a dedicated tool) before the data ever reaches its destination. In <strong>ELT</strong>, raw data is loaded as-is, and transformation happens afterward using SQL inside the warehouse, often with a tool like dbt. ELT has become more popular for large-scale analytics because cloud warehouses can transform huge datasets faster than a single Python script running on one machine.</p><h2>Choosing Between Them</h2><p>ETL still makes sense when you need to clean sensitive data before it is stored, when your destination system cannot handle heavy transformation, or when working with smaller datasets like the ones in this track. ELT makes sense at larger scale where storage is cheap and the warehouse's compute power can be used for transformation. Most working data engineers today use a mix of both depending on the pipeline.</p>""",
            "key_concepts": ["ETL", "ELT", "data warehouse transformation", "dbt", "pipeline architecture decisions"],
            "practical_exercise": {
                "title": "Compare ETL and ELT for a Real Scenario",
                "instructions": "Write a one-page comparison for a hypothetical Nigerian e-commerce company with 10 million daily transaction rows. Explain whether you would recommend ETL or ELT for their reporting pipeline and justify your choice with at least three specific reasons tied to their scale and needs."
            },
            "quiz": [
                {"question": "In ELT, when does data transformation happen?", "options": ["Before extraction", "After raw data is already loaded into the destination", "It never happens", "Only during extraction"], "correct_index": 1, "explanation": "ELT loads raw data first, then transforms it inside the destination warehouse, reversing the order used in ETL."},
                {"question": "Why has ELT become popular with modern cloud data warehouses?", "options": ["Cloud warehouses cannot store raw data", "Cloud warehouses have enough compute power to transform large datasets efficiently after loading", "ELT does not require any coding", "ELT is always cheaper regardless of scale"], "correct_index": 1, "explanation": "Modern cloud warehouses can handle large-scale transformation efficiently, making it practical to load raw data first and transform later."},
                {"question": "What tool is commonly used to perform transformations inside a warehouse in the ELT pattern?", "options": ["dbt", "Photoshop", "Excel macros", "Git"], "correct_index": 0, "explanation": "dbt (data build tool) is a widely used tool for writing SQL-based transformations that run inside the warehouse in an ELT workflow."}
            ],
            "resources": [
                {"label": "Google Cloud: BigQuery Docs", "url": "https://cloud.google.com/bigquery/docs"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Building Real Pipelines",
            "title": "Extracting Data from a Real REST API",
            "learning_objective": "By the end of this class, you will be able to authenticate with and pull data from a real REST API using Python.",
            "duration_minutes": 30,
            "content_html": """<p>Not all data lives in files or databases you already have access to. A huge amount of real-world data engineering work involves pulling data from external APIs: currency exchange rates, weather data, social media metrics, or a partner company's product catalog. Knowing how to reliably extract from an API is a core, constantly-used skill.</p><h2>Making a Request</h2><p>The requests library is the standard way to call an API from Python. Most APIs return JSON, which you then convert into a DataFrame.</p><pre><code>import requests
import pandas as pd

response = requests.get("https://api.exchangerate-api.com/v4/latest/NGN")
data = response.json()
df = pd.json_normalize(data["rates"])</code></pre><h2>Handling Status Codes and Rate Limits</h2><p>A production-quality extraction always checks whether the request actually succeeded before trying to use the data, and respects any rate limits the API sets to avoid getting blocked.</p><pre><code>if response.status_code == 200:
    data = response.json()
else:
    print("Request failed:", response.status_code)</code></pre><p>Many APIs also require an API key sent in the headers for authentication — never hardcode that key directly in your script; store it in an environment variable instead so it does not end up committed to Git by accident.</p>""",
            "key_concepts": ["REST API", "requests library", "JSON response", "status codes", "API authentication"],
            "practical_exercise": {
                "title": "Extract Data from a Public API",
                "instructions": "Choose any free public API (a currency exchange API, a weather API, or a public sports/football data API). Write a Python script that calls the API, checks the status code, converts the JSON response into a pandas DataFrame, and saves it as a CSV. Submit your script and the resulting CSV."
            },
            "quiz": [
                {"question": "What Python library is most commonly used to call a REST API?", "options": ["pandas", "requests", "sqlalchemy", "matplotlib"], "correct_index": 1, "explanation": "The requests library provides simple functions for making HTTP calls to APIs from Python."},
                {"question": "What does a status code of 200 typically mean?", "options": ["The request failed", "The request succeeded", "The API key is invalid", "The server is down"], "correct_index": 1, "explanation": "HTTP status code 200 means the request was successful."},
                {"question": "Where should an API key be stored instead of hardcoding it in a script?", "options": ["In the script's comments", "In an environment variable", "In the file name", "In the README title"], "correct_index": 1, "explanation": "Storing API keys in environment variables keeps them out of source code and prevents them from being committed to Git."}
            ],
            "resources": [
                {"label": "Python Requests Documentation", "url": "https://docs.python-requests.org/"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Building Real Pipelines",
            "title": "Handling Data Quality Issues: Validation, Deduplication, and Nulls at Scale",
            "learning_objective": "By the end of this class, you will be able to write validation checks that catch data quality problems before they reach a production table.",
            "duration_minutes": 30,
            "content_html": """<p>Cleaning data once is easy. Making sure a pipeline that runs every day keeps producing clean data, even when the source data changes unexpectedly, is the harder and more valuable skill. Data validation means writing explicit checks that catch problems automatically instead of hoping a human notices them.</p><h2>Writing Validation Checks</h2><p>A validation check is just a rule your pipeline tests against every run, raising an alert or stopping the pipeline if it fails.</p><pre><code>def validate(df):
    assert df["amount"].min() >= 0, "Negative amounts found"
    assert df["customer_id"].isnull().sum() == 0, "Missing customer_id"
    assert df.duplicated().sum() == 0, "Duplicate rows found"
    print("Validation passed:", len(df), "rows")</code></pre><h2>Why This Matters More at Scale</h2><p>When you run a pipeline once manually, you can eyeball the output. When a pipeline runs automatically every night for a year, nobody is watching it, so silent data corruption can go unnoticed for weeks, leading to wrong business decisions based on wrong numbers. Adding validation checks that fail loudly, rather than passing bad data through silently, is what separates a hobby script from a production-grade pipeline that employers trust you to build.</p>""",
            "key_concepts": ["data validation", "assertions", "pipeline reliability", "silent data corruption", "automated checks"],
            "practical_exercise": {
                "title": "Add Validation Checks to Your Pipeline",
                "instructions": "Take the mini ETL script you built on Day 10 and add at least three validation checks (for example, no negative values, no nulls in a key column, no duplicate rows). Intentionally introduce a bad row into your test data and confirm your validation catches it. Submit your updated script and a screenshot of the validation failure."
            },
            "quiz": [
                {"question": "What is the purpose of a data validation check in a pipeline?", "options": ["To make the pipeline run faster", "To automatically catch data quality problems before they reach production", "To encrypt the data", "To format the code"], "correct_index": 1, "explanation": "Validation checks test the data against expected rules and alert or stop the pipeline when something is wrong."},
                {"question": "Why is validation especially important for pipelines that run automatically every day?", "options": ["Automatic pipelines do not need validation", "Nobody is manually watching the output, so bad data could go unnoticed for a long time", "Daily pipelines are always error-free", "Validation only matters for small datasets"], "correct_index": 1, "explanation": "Without validation, an automated pipeline can silently produce and propagate bad data for a long time before anyone notices."},
                {"question": "What should a well-designed pipeline do when a validation check fails?", "options": ["Ignore it and continue silently", "Fail loudly or alert someone instead of passing bad data through", "Automatically delete the entire database", "Restart the computer"], "correct_index": 1, "explanation": "A production-grade pipeline should stop or alert clearly on failed validation rather than silently passing corrupted data downstream."}
            ],
            "resources": []
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Building Real Pipelines",
            "title": "Working with Larger Datasets Using Chunking and Efficient Pandas",
            "learning_objective": "By the end of this class, you will be able to process a dataset too large to fit comfortably in memory using chunking techniques.",
            "duration_minutes": 25,
            "content_html": """<p>The techniques you have used so far load an entire file into memory at once, which works fine for small datasets but breaks down when a file has millions of rows and your laptop runs out of RAM. Real company datasets are often far bigger than the sample files used for learning, so knowing how to process data in pieces is a practical necessity.</p><h2>Reading Files in Chunks</h2><p>pandas can read a large CSV in smaller pieces called chunks, processing and discarding each one before moving to the next, which keeps memory usage low.</p><pre><code>chunk_size = 100_000
results = []
for chunk in pd.read_csv("huge_file.csv", chunksize=chunk_size):
    cleaned = chunk.dropna(subset=["customer_id"])
    summary = cleaned.groupby("region")["amount"].sum()
    results.append(summary)

final = pd.concat(results).groupby(level=0).sum()</code></pre><h2>Other Memory-Saving Habits</h2><p>Choosing efficient data types (using int32 instead of int64 where possible, or category type for repeated text values) can cut memory use significantly. Selecting only the columns you actually need with usecols also helps a lot before doing any heavier processing on a large file.</p>""",
            "key_concepts": ["chunking", "memory efficiency", "chunksize", "large dataset processing", "dtype optimization"],
            "practical_exercise": {
                "title": "Process a Large File in Chunks",
                "instructions": "Find or generate a CSV with at least 200,000 rows (you can duplicate a smaller dataset to reach this size). Write a script that reads it in chunks of 50,000 rows, cleans and aggregates each chunk, then combines the results into one final summary. Submit your script and the final output."
            },
            "quiz": [
                {"question": "Why would a data engineer read a large CSV file in chunks instead of all at once?", "options": ["Chunking makes the file smaller on disk", "It avoids running out of memory when the full file cannot fit in RAM", "Chunking is required by pandas for all files", "It automatically removes duplicates"], "correct_index": 1, "explanation": "Chunking processes a file piece by piece, keeping memory usage manageable for datasets too large to load all at once."},
                {"question": "Which pandas read_csv parameter controls how many rows are loaded per chunk?", "options": ["batch_size", "chunksize", "row_limit", "page_size"], "correct_index": 1, "explanation": "chunksize tells pandas how many rows to read into memory at a time when iterating over a large file."},
                {"question": "What is one way to reduce memory usage besides chunking?", "options": ["Always use the largest data type available", "Use more efficient data types like int32 or category where appropriate", "Load every column even if unused", "Avoid using pandas entirely"], "correct_index": 1, "explanation": "Choosing smaller, appropriate data types and loading only needed columns significantly reduces memory usage."}
            ],
            "resources": [
                {"label": "pandas Documentation", "url": "https://pandas.pydata.org/docs/"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Building Real Pipelines",
            "title": "Automating a Pipeline Run with Python Scripts and Scheduling Basics",
            "learning_objective": "By the end of this class, you will be able to schedule a Python pipeline script to run automatically on a recurring basis.",
            "duration_minutes": 25,
            "content_html": """<p>A pipeline that only runs when you manually type a command is not really automated. Real production pipelines run on a schedule — nightly, hourly, or even every few minutes — without anyone touching a keyboard. Understanding basic scheduling is the bridge between a script you run for a class assignment and a system that actually operates in a business.</p><h2>Scheduling with Cron</h2><p>On Linux and Mac servers, cron is the classic tool for scheduling any command, including a Python script, to run at fixed times.</p><pre><code># Run every day at 2 AM
0 2 * * * /usr/bin/python3 /home/user/pipeline.py >> /home/user/log.txt 2>&1</code></pre><h2>Logging What Happened</h2><p>Notice the log.txt redirect in that cron line — an automated pipeline should always write its output to a log file, since nobody is watching the terminal to see if it succeeded or failed. On Windows, Task Scheduler provides similar functionality through a graphical interface, and cloud platforms offer their own scheduling services as well. The key idea that carries forward into tomorrow's orchestration tools is the same: separate "what the pipeline does" from "when it runs," so you can change the schedule without touching the pipeline logic itself.</p>""",
            "key_concepts": ["cron scheduling", "automation", "pipeline logging", "Task Scheduler", "recurring jobs"],
            "practical_exercise": {
                "title": "Write a Cron Schedule and a Logging Wrapper",
                "instructions": "Write a cron expression that would run your Day 10 pipeline script every day at 6 AM, and explain what each field in the expression means. Then modify your pipeline script to write a timestamped log line to a log.txt file every time it runs, recording success or failure. Submit both the cron line and your updated script."
            },
            "quiz": [
                {"question": "What is cron primarily used for?", "options": ["Cleaning data", "Scheduling commands or scripts to run automatically at set times", "Writing SQL queries", "Connecting to APIs"], "correct_index": 1, "explanation": "cron is a time-based job scheduler on Linux/Mac systems used to automatically run scripts on a recurring schedule."},
                {"question": "Why should an automated pipeline write to a log file?", "options": ["Log files make the pipeline run faster", "Nobody is watching the terminal, so logs are the only record of success or failure", "Logging is required by Python syntax", "It replaces the need for validation checks"], "correct_index": 1, "explanation": "Since automated pipelines run unattended, a log file is essential for confirming whether a run succeeded or diagnosing why it failed."},
                {"question": "What is the benefit of separating 'what a pipeline does' from 'when it runs'?", "options": ["It makes the code run twice as fast", "You can change the schedule without modifying the pipeline logic itself", "It removes the need for a database", "It automatically fixes bugs"], "correct_index": 1, "explanation": "Keeping scheduling separate from pipeline logic means you can adjust timing independently without touching the code that does the actual work."}
            ],
            "resources": []
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Orchestration and Warehousing",
            "title": "Introduction to Workflow Orchestration with Apache Airflow",
            "learning_objective": "By the end of this class, you will be able to explain what a workflow orchestrator does and why pipelines outgrow simple cron scheduling.",
            "duration_minutes": 25,
            "content_html": """<p>Cron works fine for one simple script, but real pipelines usually have multiple steps that depend on each other — extract must finish before clean can start, and clean must finish before load can start. Apache Airflow is the industry-standard tool for managing these multi-step dependencies, retrying failed steps automatically, and giving you a visual dashboard of what ran and what failed.</p><h2>DAGs: The Core Idea</h2><p>Airflow organizes work into a <strong>DAG</strong> (Directed Acyclic Graph) — a set of tasks with defined dependencies and no circular loops. Each task is a unit of work, like "extract from API" or "load into warehouse," and Airflow guarantees tasks run in the correct order.</p><pre><code>from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("sales_pipeline", start_date=datetime(2026, 1, 1), schedule="@daily") as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    clean_task = PythonOperator(task_id="clean", python_callable=clean)
    extract_task >> clean_task</code></pre><h2>Why Employers Care</h2><p>Airflow (or similar tools like Prefect and Dagster) is listed on the majority of mid-level data engineering job postings, because any company running more than a couple of pipelines needs a system to manage dependencies, retries, and monitoring — which is exactly what orchestration tools provide.</p>""",
            "key_concepts": ["Apache Airflow", "DAG", "workflow orchestration", "task dependencies", "PythonOperator"],
            "practical_exercise": {
                "title": "Design a DAG on Paper",
                "instructions": "Take your Day 10 mini ETL pipeline (extract, clean, transform, load) and sketch it as a DAG diagram showing each step as a box and arrows showing dependencies. Then write the Airflow Python code (using PythonOperator and >> syntax) that would represent this DAG, even if you do not run it yet. Submit your sketch and code."
            },
            "quiz": [
                {"question": "What does DAG stand for in Airflow?", "options": ["Data Analysis Group", "Directed Acyclic Graph", "Database Access Gateway", "Daily Automated Generation"], "correct_index": 1, "explanation": "A DAG is a Directed Acyclic Graph — a set of tasks connected by dependencies with no circular loops."},
                {"question": "Why do pipelines outgrow simple cron scheduling?", "options": ["Cron cannot run Python scripts", "Real pipelines often have multiple dependent steps that need ordering, retries, and monitoring", "Cron is more expensive than Airflow", "Cron only works on weekends"], "correct_index": 1, "explanation": "As pipelines grow multiple interdependent steps, they need dependency management, automatic retries, and visibility that cron alone does not provide."},
                {"question": "In Airflow's task_a >> task_b syntax, what does the >> mean?", "options": ["task_a and task_b run at the same time", "task_a must complete before task_b starts", "task_b deletes task_a's output", "It has no functional meaning"], "correct_index": 1, "explanation": "The >> operator defines a dependency, meaning the task on the left must finish before the task on the right begins."}
            ],
            "resources": [
                {"label": "Apache Airflow Documentation", "url": "https://airflow.apache.org/docs/"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Orchestration and Warehousing",
            "title": "Building Your First Airflow DAG for a Multi-Step Pipeline",
            "learning_objective": "By the end of this class, you will be able to install Airflow locally and run a working multi-task DAG end to end.",
            "duration_minutes": 35,
            "content_html": """<p>Today you move from reading about Airflow to running it. Getting a DAG to actually execute, with real logs and a real UI showing task status, makes the concept concrete in a way that reading code alone cannot.</p><h2>Setting Up Airflow Locally</h2><p>The quickest way to try Airflow without a complex install is through Docker, using Airflow's official quick-start setup, which spins up the scheduler, webserver, and database together.</p><pre><code>docker pull apache/airflow
# Follow the official quick-start docker-compose steps
docker compose up airflow-init
docker compose up</code></pre><h2>Writing a Real Multi-Task DAG</h2><p>Build on yesterday's sketch by turning your extract, clean, transform, and load functions into an actual runnable DAG file, then trigger it from the Airflow web UI at localhost:8080 and watch each task turn green as it succeeds.</p><pre><code>extract_task >> clean_task >> transform_task >> load_task</code></pre><p>When something fails, Airflow's UI shows exactly which task failed and lets you view its logs directly, which is far faster for debugging than digging through a plain text log file. This visual feedback loop is one of the biggest reasons teams adopt orchestration tools once their pipelines grow past a handful of scripts.</p>""",
            "key_concepts": ["Airflow local setup", "Docker for Airflow", "multi-task DAG", "Airflow UI", "task debugging"],
            "practical_exercise": {
                "title": "Run a Working DAG End to End",
                "instructions": "Install Airflow locally using Docker (or an alternative like a hosted free-tier Airflow sandbox if Docker is not available on your machine). Build a DAG with your four pipeline functions as separate tasks connected in order, trigger it from the UI, and confirm all tasks complete successfully. Submit a screenshot of your DAG graph view showing all tasks green."
            },
            "quiz": [
                {"question": "What is a common way to run Airflow locally for learning purposes?", "options": ["It can only run on a cloud server", "Using Docker with Airflow's official quick-start setup", "By installing it as a browser extension", "It requires a paid license"], "correct_index": 1, "explanation": "Docker with Airflow's official docker-compose quick-start is the standard way to try Airflow locally without a complex manual install."},
                {"question": "What does the Airflow web UI let you do when a task fails?", "options": ["Nothing, you must check plain text files manually", "View exactly which task failed and inspect its logs directly", "Automatically fix the code", "Delete the entire DAG"], "correct_index": 1, "explanation": "The Airflow UI shows task-level status and logs, making it much faster to diagnose failures than searching through raw log files."},
                {"question": "What does it mean when a task shows green in the Airflow graph view?", "options": ["The task is currently running", "The task completed successfully", "The task failed", "The task was skipped"], "correct_index": 1, "explanation": "Green in the Airflow graph view indicates a task has completed successfully."}
            ],
            "resources": [
                {"label": "Apache Airflow Documentation", "url": "https://airflow.apache.org/docs/"},
                {"label": "Docker Get Started", "url": "https://www.docker.com/get-started/"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Orchestration and Warehousing",
            "title": "Data Warehousing Concepts: Star Schemas, Fact and Dimension Tables",
            "learning_objective": "By the end of this class, you will be able to design a star schema with fact and dimension tables for an analytics use case.",
            "duration_minutes": 25,
            "content_html": """<p>The relational schema you designed on Day 8 was built for storing transactional data efficiently. Data warehouses, which exist purely to support fast analytics and reporting, often use a different design pattern called a <strong>star schema</strong>, optimized for the kinds of aggregate questions analysts ask constantly, like "total sales by region by month."</p><h2>Fact and Dimension Tables</h2><p>A <strong>fact table</strong> holds the numeric measurements you want to analyze, like sales amount or quantity sold, along with foreign keys pointing to related context. <strong>Dimension tables</strong> hold the descriptive context, like customer details, product details, or date details, that give meaning to those numbers.</p><pre><code>-- Fact table
CREATE TABLE fact_sales (
  sale_id INTEGER PRIMARY KEY,
  date_id INTEGER,
  product_id INTEGER,
  customer_id INTEGER,
  amount NUMERIC
);
-- Dimension table
CREATE TABLE dim_product (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT,
  category TEXT
);</code></pre><h2>Why "Star" Schema</h2><p>When you draw this out, one central fact table connects to several surrounding dimension tables, forming a star shape. This design makes common analytical queries fast and intuitive, which is exactly why nearly every company's reporting warehouse is built this way rather than using a fully normalized transactional schema.</p>""",
            "key_concepts": ["star schema", "fact table", "dimension table", "data warehousing", "analytical schema design"],
            "practical_exercise": {
                "title": "Design a Star Schema for a Ride-Hailing App",
                "instructions": "Design a star schema for a ride-hailing company that wants to analyze trips by driver, rider, date, and city. Define one fact table (fact_trips) and at least three dimension tables, listing each table's columns and keys. Submit your schema as SQL CREATE TABLE statements or a clearly labeled diagram."
            },
            "quiz": [
                {"question": "What does a fact table typically store?", "options": ["Descriptive text about customers only", "Numeric measurements plus foreign keys to related dimension tables", "Only usernames and passwords", "Application source code"], "correct_index": 1, "explanation": "Fact tables store measurable, numeric data (like sales amounts) along with keys linking to dimension tables for context."},
                {"question": "What is the purpose of a dimension table?", "options": ["To store the pipeline's log files", "To hold descriptive context, like product or customer details, that gives meaning to fact table numbers", "To replace the need for a fact table", "To store Python code"], "correct_index": 1, "explanation": "Dimension tables provide the descriptive attributes (who, what, where, when) that make the numbers in a fact table meaningful."},
                {"question": "Why is this design pattern called a 'star schema'?", "options": ["It was invented by a company called Star", "A central fact table connects to surrounding dimension tables, visually forming a star shape", "It only works with astronomical data", "It requires exactly five tables"], "correct_index": 1, "explanation": "When diagrammed, one central fact table surrounded by multiple connected dimension tables visually resembles a star."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Orchestration and Warehousing",
            "title": "Working with Cloud Data Storage: Amazon S3 Basics for Data Engineers",
            "learning_objective": "By the end of this class, you will be able to upload, organize, and read data files from a cloud object storage bucket.",
            "duration_minutes": 25,
            "content_html": """<p>Companies do not store their raw data files on one laptop's hard drive; they store them in cloud object storage, where data can be accessed reliably by many pipelines and people at once, at massive scale. Amazon S3 is the most widely used object storage service and a near-universal building block in real data engineering architectures.</p><h2>Buckets, Keys, and Basic Operations</h2><p>An S3 "bucket" is a container for files, and each file is stored with a "key" that acts like its file path. Many pipelines land raw data in S3 first (this is often called a data lake) before it gets cleaned and loaded into a warehouse.</p><pre><code>import boto3

s3 = boto3.client("s3")
s3.upload_file("clean_sales.csv", "my-data-bucket", "raw/2026/01/sales.csv")

response = s3.get_object(Bucket="my-data-bucket", Key="raw/2026/01/sales.csv")
df = pd.read_csv(response["Body"])</code></pre><h2>Organizing a Data Lake</h2><p>A common, sensible convention is organizing files by source and date, like raw/sales/2026/01/15/file.csv, which makes it easy to find and reprocess a specific day's data later. AWS offers a free tier generous enough to practice all of this without spending money, which is exactly what you will use today.</p>""",
            "key_concepts": ["Amazon S3", "object storage", "data lake", "buckets and keys", "boto3"],
            "practical_exercise": {
                "title": "Upload and Read Data from S3",
                "instructions": "Create a free-tier AWS account and an S3 bucket. Using boto3, write a Python script that uploads a cleaned CSV file to the bucket under a dated folder path, then reads it back into a pandas DataFrame directly from S3. Submit your script and a screenshot of the file listed in your S3 bucket."
            },
            "quiz": [
                {"question": "What is an S3 bucket?", "options": ["A type of SQL query", "A container in Amazon S3 that holds files", "A Python library", "A data cleaning function"], "correct_index": 1, "explanation": "A bucket is the top-level container in Amazon S3 where files (objects) are stored."},
                {"question": "What is a 'data lake'?", "options": ["A database with only clean, transformed data", "A storage layer, often cloud object storage, that holds raw data before it is processed", "A type of SQL join", "A visualization tool"], "correct_index": 1, "explanation": "A data lake is a storage area for raw, often unprocessed data, commonly implemented using services like S3."},
                {"question": "What Python library is commonly used to interact with AWS S3?", "options": ["pandas", "boto3", "requests", "sqlalchemy"], "correct_index": 1, "explanation": "boto3 is the official AWS SDK for Python, used to upload, download, and manage S3 objects programmatically."}
            ],
            "resources": [
                {"label": "AWS Getting Started", "url": "https://aws.amazon.com/getting-started/"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Orchestration and Warehousing",
            "title": "Combining Multiple Data Sources into One Clean Dataset",
            "learning_objective": "By the end of this class, you will be able to combine data extracted from a file, a database, and an API into a single unified dataset.",
            "duration_minutes": 30,
            "content_html": """<p>Real pipelines rarely pull from just one source. A typical business question — "which regions have the highest customer lifetime value" — might need transaction data from a database, customer signup data from a CSV export, and current exchange rates from an API, all combined into one dataset before it can be answered.</p><h2>Combining Sources with a Common Key</h2><p>The trick to combining multiple sources cleanly is always the same: find (or create) a shared key that exists in each source, and merge on it step by step.</p><pre><code>db_df = pd.read_sql("SELECT * FROM transactions", engine)
signup_df = pd.read_csv("signups.csv")
rates = requests.get(fx_api_url).json()
rates_df = pd.json_normalize(rates)

combined = db_df.merge(signup_df, on="customer_id", how="left")
combined = combined.merge(rates_df, on="currency_code", how="left")
combined["amount_ngn"] = combined["amount"] * combined["rate_to_ngn"]</code></pre><h2>Watching for Mismatches</h2><p>Merging across sources almost always exposes mismatches you did not expect — a customer_id in the database that has no matching signup record, or a currency code the exchange rate API does not cover. Checking row counts before and after each merge, and investigating any unexpected drop, is the habit that catches these silent data losses.</p>""",
            "key_concepts": ["multi-source integration", "merge keys", "data unification", "row count validation", "cross-source consistency"],
            "practical_exercise": {
                "title": "Combine Three Data Sources into One Dataset",
                "instructions": "Using a database table, a CSV file, and a public API result (reuse ones from earlier classes if convenient), merge all three into a single combined dataset on a shared key. Report the row count before and after each merge step, and explain any row count changes you observe. Submit your script and your explanation."
            },
            "quiz": [
                {"question": "What is the key strategy for combining data from multiple different sources?", "options": ["Load them all into separate files and never combine them", "Find or create a shared key present in each source and merge on it", "Always use the largest source only", "Convert everything to PDF first"], "correct_index": 1, "explanation": "A shared key that exists across sources is what allows you to accurately merge and align records between them."},
                {"question": "Why should you check row counts before and after merging datasets?", "options": ["It is required by pandas syntax", "To catch unexpected data loss caused by mismatched keys between sources", "It makes the merge run faster", "Row counts are not useful for merges"], "correct_index": 1, "explanation": "Comparing row counts before and after a merge reveals whether records were unexpectedly dropped due to key mismatches."},
                {"question": "In a merge like db_df.merge(signup_df, on='customer_id', how='left'), what does how='left' mean?", "options": ["Only matching rows from both tables are kept", "All rows from db_df are kept, with matching signup_df data added where available", "All rows from signup_df are kept instead", "The merge fails if any row does not match"], "correct_index": 1, "explanation": "A left merge keeps every row from the left DataFrame (db_df) and adds matching data from the right DataFrame where a match exists."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Production-Grade Pipelines",
            "title": "Writing Data Quality Tests and Pipeline Validation Checks",
            "learning_objective": "By the end of this class, you will be able to write automated tests using pytest that verify a pipeline's transformation logic is correct.",
            "duration_minutes": 30,
            "content_html": """<p>Day 13 covered validating the data itself. Today is about validating the code that produces it. A pipeline function can look correct but silently produce wrong results when the input data shifts even slightly — automated tests catch that before it reaches production, not after a manager spots a wrong number in a report.</p><h2>Writing a Test with pytest</h2><p>pytest is the standard Python testing framework. A good test feeds a function a small, known input and checks that the output matches exactly what you expect.</p><pre><code>import pandas as pd
from pipeline import clean

def test_clean_removes_nulls():
    df = pd.DataFrame({"customer_id": [1, None, 3], "amount": [10, 20, 30]})
    result = clean(df)
    assert result["customer_id"].isnull().sum() == 0
    assert len(result) == 2

def test_clean_removes_duplicates():
    df = pd.DataFrame({"customer_id": [1, 1], "amount": [10, 10]})
    result = clean(df)
    assert len(result) == 1</code></pre><h2>Why Tests Beat Manual Checking</h2><p>Running <code>pytest</code> re-checks every function automatically in seconds, every single time you change your code, which manual eyeballing simply cannot keep up with. Data engineering job interviews increasingly ask candidates to write or discuss tests, because untested pipelines are a common source of costly production incidents.</p>""",
            "key_concepts": ["pytest", "unit testing", "test-driven pipeline development", "automated testing", "regression prevention"],
            "practical_exercise": {
                "title": "Write pytest Tests for Your Pipeline Functions",
                "instructions": "Install pytest and write at least four tests covering your clean and transform functions from earlier classes, each using a small hand-crafted input DataFrame with a known expected output. Run pytest and confirm all tests pass. Submit your test file and a screenshot of the passing test output."
            },
            "quiz": [
                {"question": "What is the main purpose of writing automated tests for a pipeline's functions?", "options": ["To make the code look more professional", "To automatically catch when code changes silently break expected behavior", "To replace the need for data validation", "To speed up database queries"], "correct_index": 1, "explanation": "Automated tests verify that functions still produce correct, expected output every time the code changes, catching regressions early."},
                {"question": "What Python library is the standard tool for writing and running tests?", "options": ["pandas", "pytest", "boto3", "requests"], "correct_index": 1, "explanation": "pytest is the widely used standard framework for writing and running automated tests in Python."},
                {"question": "In a good unit test, what should the input data typically look like?", "options": ["The full production dataset", "A small, hand-crafted input with a known, predictable expected output", "Random data generated each run", "Empty with no data at all"], "correct_index": 1, "explanation": "Small, controlled inputs with known expected outputs make it clear and reliable to verify a function behaves correctly."}
            ],
            "resources": [
                {"label": "pytest Documentation", "url": "https://docs.pytest.org/"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Production-Grade Pipelines",
            "title": "Version Controlling Data Pipelines with Git and Reproducible Environments",
            "learning_objective": "By the end of this class, you will be able to structure and commit a data pipeline project so anyone can clone and reproduce it exactly.",
            "duration_minutes": 25,
            "content_html": """<p>A pipeline that only works on your machine is not finished. For it to be usable by a team, or judged fairly by a hiring manager, another person needs to be able to clone your repository and get it running without guessing what you had installed or configured. This is called reproducibility, and it is expected of every serious data engineering project.</p><h2>What a Reproducible Repo Looks Like</h2><p>At minimum, a reproducible pipeline project includes a requirements.txt listing exact package versions, a clear folder structure, and a README with setup instructions.</p><pre><code>pip freeze > requirements.txt</code></pre><pre><code>project/
  pipeline/
    extract.py
    clean.py
    transform.py
    load.py
  tests/
    test_pipeline.py
  requirements.txt
  README.md
  .gitignore</code></pre><h2>What Belongs in .gitignore</h2><p>Sensitive files like .env (holding database passwords and API keys) and generated files like venv/ or __pycache__/ should never be committed to Git — a .gitignore file tells Git to skip them automatically. Committing secrets to a public GitHub repo is a real, common, and embarrassing mistake even experienced engineers make, so building this habit now protects you later.</p>""",
            "key_concepts": ["reproducibility", "requirements.txt", "project structure", ".gitignore", "environment portability"],
            "practical_exercise": {
                "title": "Structure and Commit a Reproducible Pipeline Repo",
                "instructions": "Reorganize your pipeline project into a clear folder structure with separate modules, generate a requirements.txt with pip freeze, write a README explaining how to set up and run the project, and add a proper .gitignore excluding venv and any secrets. Commit and push it to a GitHub repository. Submit the repository link."
            },
            "quiz": [
                {"question": "What does 'reproducibility' mean for a data pipeline project?", "options": ["The pipeline runs faster each time", "Another person can clone the project and get it running without guessing configuration", "The pipeline never has bugs", "It only refers to the data output, not the code"], "correct_index": 1, "explanation": "Reproducibility means someone else can set up and run your project reliably using only what is documented and committed."},
                {"question": "What is the purpose of a requirements.txt file?", "options": ["To store database passwords", "To list the exact Python packages and versions a project depends on", "To hold the pipeline's log output", "To store raw data"], "correct_index": 1, "explanation": "requirements.txt lists a project's dependencies so anyone can install the exact same package versions with one command."},
                {"question": "Why should a .env file containing database passwords be added to .gitignore?", "options": ["It makes the repository load faster", ".env files are not valid Python", "To prevent sensitive secrets from being committed and exposed in the Git history", "Git cannot track .env files at all"], "correct_index": 2, "explanation": ".gitignore prevents sensitive files like .env from being committed, avoiding accidental exposure of secrets in a public or shared repository."}
            ],
            "resources": [
                {"label": "GitHub Docs: gitignore", "url": "https://github.com/"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Production-Grade Pipelines",
            "title": "Logging, Monitoring, and Handling Failures in Data Pipelines",
            "learning_objective": "By the end of this class, you will be able to add structured logging and error handling that surfaces pipeline failures clearly.",
            "duration_minutes": 30,
            "content_html": """<p>Pipelines fail. An API goes down, a file arrives in an unexpected format, a database connection times out. What separates a professional pipeline from a fragile script is not the absence of failure but how gracefully and visibly it handles failure when it happens.</p><h2>Structured Logging</h2><p>Python's built-in logging module is far more useful than scattered print statements because it timestamps every message and lets you control severity levels.</p><pre><code>import logging
logging.basicConfig(filename="pipeline.log", level=logging.INFO,
                     format="%(asctime)s %(levelname)s %(message)s")

logging.info("Pipeline started")
try:
    df = extract("sales.csv")
    logging.info("Extracted %d rows", len(df))
except Exception as e:
    logging.error("Extraction failed: %s", e)
    raise</code></pre><h2>Failing Loudly, Not Silently</h2><p>Notice the try/except above still re-raises the error after logging it — a common mistake is catching an error just to hide it, which lets a broken pipeline appear to "succeed" while actually producing nothing or garbage. In a real job, this kind of monitoring is often connected to alerting tools like Slack or email notifications, so the team knows immediately when a pipeline breaks rather than discovering it days later when a report looks wrong.</p>""",
            "key_concepts": ["logging module", "error handling", "try/except", "alerting", "graceful failure"],
            "practical_exercise": {
                "title": "Add Logging and Error Handling to Your Pipeline",
                "instructions": "Replace any print statements in your pipeline with Python's logging module, writing timestamped info and error logs to a file. Wrap each pipeline stage in a try/except that logs the specific error and re-raises it. Intentionally break one stage (for example, point to a missing file) and confirm the failure is logged clearly. Submit your updated script and the resulting log file."
            },
            "quiz": [
                {"question": "Why is Python's logging module generally preferred over print statements in a pipeline?", "options": ["print statements do not work in Python 3", "logging adds timestamps, severity levels, and can write to files automatically", "logging is faster to type", "print statements cannot show error messages"], "correct_index": 1, "explanation": "The logging module provides structured, timestamped, severity-leveled output that can be directed to files, unlike plain print statements."},
                {"question": "What is a common mistake when using try/except in a pipeline?", "options": ["Using too many try blocks", "Catching an error just to silence it, letting the pipeline appear to succeed with broken results", "Logging the error message", "Re-raising the exception after logging it"], "correct_index": 1, "explanation": "Silently swallowing an exception without re-raising or properly handling it can let a pipeline appear successful while it actually failed or produced bad output."},
                {"question": "Why might a company connect pipeline monitoring to Slack or email alerts?", "options": ["To replace the need for logging entirely", "So the team is notified immediately when a pipeline fails, instead of discovering it days later", "It is required by Python", "To make the pipeline run faster"], "correct_index": 1, "explanation": "Real-time alerts ensure failures are caught and addressed quickly, rather than being discovered much later through a downstream report error."}
            ],
            "resources": [
                {"label": "Python Docs: logging", "url": "https://docs.python.org/3/library/logging.html"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Production-Grade Pipelines",
            "title": "Optimizing SQL Queries and Pipeline Performance",
            "learning_objective": "By the end of this class, you will be able to identify and fix common causes of slow SQL queries and slow pipeline steps.",
            "duration_minutes": 25,
            "content_html": """<p>A pipeline that works correctly but takes six hours to run every night is a real problem in production — it delays every report and dashboard downstream of it, and it costs real money in cloud compute time. Performance is not a nice-to-have; it directly affects whether a pipeline is usable at all.</p><h2>Indexing for Faster Queries</h2><p>Without an index, a database scans every single row to find matches, which gets painfully slow as tables grow. An index on frequently filtered or joined columns lets the database jump directly to relevant rows.</p><pre><code>CREATE INDEX idx_customer_id ON transactions(customer_id);
EXPLAIN ANALYZE SELECT * FROM transactions WHERE customer_id = 4521;</code></pre><h2>Common Pipeline Performance Fixes</h2><p>Beyond indexing, avoid pulling more data than you need — filter with WHERE inside the database query rather than loading everything and filtering in pandas afterward. Selecting only needed columns, aggregating in SQL instead of Python where possible, and processing data in chunks (from Day 14) all reduce runtime. The EXPLAIN ANALYZE command shown above is one of the most useful habits in SQL: it shows exactly how the database plans to execute your query, revealing whether it is scanning the whole table or using an index efficiently.</p>""",
            "key_concepts": ["query optimization", "database indexing", "EXPLAIN ANALYZE", "filtering at the source", "pipeline performance"],
            "practical_exercise": {
                "title": "Diagnose and Fix a Slow Query",
                "instructions": "Using a database table with at least a few thousand rows, run a query filtering on an unindexed column and record its execution time or plan using EXPLAIN ANALYZE. Add an index on that column, rerun the same query, and record the new plan. Submit both EXPLAIN ANALYZE outputs and a short explanation of the difference."
            },
            "quiz": [
                {"question": "What is the main benefit of adding a database index to a frequently filtered column?", "options": ["It makes the table smaller", "It lets the database find matching rows without scanning the entire table", "It automatically removes duplicate rows", "It encrypts the column"], "correct_index": 1, "explanation": "An index allows the database to quickly locate matching rows instead of scanning every row in the table."},
                {"question": "What does the SQL command EXPLAIN ANALYZE do?", "options": ["Deletes slow queries", "Shows how the database plans to execute a query and how long it actually took", "Creates a new index automatically", "Converts SQL into Python"], "correct_index": 1, "explanation": "EXPLAIN ANALYZE reveals the database's actual execution plan and timing, helping identify performance bottlenecks."},
                {"question": "Why is it usually faster to filter data with a WHERE clause in SQL rather than loading everything into pandas first?", "options": ["pandas cannot filter data at all", "The database avoids sending unnecessary rows over the network in the first place", "WHERE clauses are illegal in production", "pandas filtering always fails on large data"], "correct_index": 1, "explanation": "Filtering at the database level reduces the amount of data transferred and processed, which is typically much faster than pulling everything and filtering afterward."}
            ],
            "resources": [
                {"label": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Production-Grade Pipelines",
            "title": "Documenting a Data Pipeline So Another Engineer Can Run It",
            "learning_objective": "By the end of this class, you will be able to write documentation that lets another engineer understand and run your pipeline without asking you questions.",
            "duration_minutes": 20,
            "content_html": """<p>An undocumented pipeline is a liability, not an asset. When you move to a new team, go on leave, or simply forget the details six months later, documentation is what keeps a pipeline maintainable. Employers explicitly value engineers who document their work, because it reduces the risk and cost of relying on any one person's memory.</p><h2>What Good Pipeline Documentation Covers</h2><p>A strong README for a data pipeline answers: what does this pipeline do, what are its inputs and outputs, how do you set it up and run it, and what should you do if it fails.</p><pre><code># Sales ETL Pipeline

## What it does
Extracts daily sales from the transactions API, cleans and aggregates
by region, and loads the result into the region_sales_summary table.

## Setup
1. pip install -r requirements.txt
2. Copy .env.example to .env and fill in your database credentials
3. Run: python pipeline/main.py

## Troubleshooting
If extraction fails with a 401 error, your API key has likely expired.</code></pre><h2>Architecture Diagrams Help Too</h2><p>Even a simple box-and-arrow diagram showing extract to clean to transform to load, with the tools used at each stage labeled, helps a new engineer understand your pipeline in seconds rather than by reading every line of code.</p>""",
            "key_concepts": ["pipeline documentation", "README structure", "setup instructions", "troubleshooting notes", "architecture diagrams"],
            "practical_exercise": {
                "title": "Write a Complete README for Your Pipeline",
                "instructions": "Write a README.md for your pipeline project covering what it does, its inputs and outputs, step-by-step setup instructions, how to run it, and at least two troubleshooting tips for likely failures. Include a simple text or hand-drawn architecture diagram. Submit your README file."
            },
            "quiz": [
                {"question": "Why is documentation valuable even for a pipeline you built yourself?", "options": ["It is only useful for other people, never for you", "You are likely to forget the details over time, and others need to maintain it too", "Documentation makes the code run faster", "It is required by Python syntax"], "correct_index": 1, "explanation": "Documentation protects against memory loss over time and allows others (or future you) to maintain and run the pipeline confidently."},
                {"question": "Which of these should a good pipeline README include?", "options": ["Only the author's name", "What the pipeline does, its inputs/outputs, setup steps, and troubleshooting notes", "The entire Git commit history", "A list of unrelated projects"], "correct_index": 1, "explanation": "Effective documentation clearly explains purpose, setup, usage, and how to handle common failures."},
                {"question": "What is one benefit of including a simple architecture diagram in documentation?", "options": ["It replaces the need for a README entirely", "It helps a new engineer understand the pipeline's flow quickly without reading all the code", "Diagrams are required by Git", "It makes the pipeline run automatically"], "correct_index": 1, "explanation": "A visual diagram gives a fast, high-level understanding of how data flows through the pipeline, complementing written documentation."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Job-Ready Data Engineering",
            "title": "What Data Engineering Interviews Actually Test (SQL, Python, System Design)",
            "learning_objective": "By the end of this class, you will be able to describe the typical stages of a data engineering interview and practice one SQL and one system design question.",
            "duration_minutes": 25,
            "content_html": """<p>Data engineering interviews at most companies, from Nigerian startups to multinationals, tend to follow a predictable pattern: a SQL screening round, a Python or coding round, and a system design round for more senior roles. Knowing what to expect lets you prepare deliberately instead of guessing.</p><h2>The SQL Round</h2><p>Expect questions like "find the second-highest salary per department" or "find customers with no orders in the last 90 days" — these test JOIN, GROUP BY, subqueries, and window functions, all built on what you practiced in weeks one through three.</p><pre><code>SELECT customer_id, RANK() OVER (ORDER BY total_spent DESC) AS rank
FROM customer_totals;</code></pre><h2>The System Design Round</h2><p>For pipeline design questions like "design a pipeline to process 10 million events per day," interviewers want to hear you reason about the source, the extraction method, how you would handle failures and retries, where the data lands, and how it is validated — the exact structure of everything covered in this track. A strong answer references trade-offs (ETL vs ELT, batch vs streaming) rather than naming one tool and stopping there.</p>""",
            "key_concepts": ["technical interview structure", "SQL interview questions", "system design questions", "window functions", "interview preparation"],
            "practical_exercise": {
                "title": "Answer a SQL and a System Design Interview Question",
                "instructions": "Write the SQL query to find the top 3 highest-spending customers per region using a window function. Then write a half-page answer to: 'Design a pipeline to ingest and process 5 million daily transaction events for a Nigerian mobile money company,' covering source, extraction, cleaning, storage, and failure handling. Submit both answers."
            },
            "quiz": [
                {"question": "What SQL feature is commonly used to rank rows within groups, such as top customers per region?", "options": ["GROUP BY alone", "Window functions like RANK() OVER", "DELETE statements", "CREATE INDEX"], "correct_index": 1, "explanation": "Window functions like RANK() OVER (PARTITION BY ... ORDER BY ...) allow ranking within groups without collapsing the result set."},
                {"question": "In a system design interview about pipelines, what should a strong answer include besides naming tools?", "options": ["Only the name of one specific tool", "Reasoning about trade-offs like ETL vs ELT and how failures are handled", "A list of unrelated programming languages", "The interviewer's résumé"], "correct_index": 1, "explanation": "Interviewers want to see reasoning about trade-offs and failure handling, not just tool names, since that reflects real engineering judgment."},
                {"question": "Which of these is a typical SQL interview question type?", "options": ["Design a company logo", "Find customers with no orders in the last 90 days", "Write a poem about databases", "Draw a flowchart with no SQL"], "correct_index": 1, "explanation": "Questions involving filtering, joining, and aggregating data — like finding inactive customers — are classic SQL interview questions."}
            ],
            "resources": [
                {"label": "W3Schools SQL Tutorial", "url": "https://www.w3schools.com/sql/"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Job-Ready Data Engineering",
            "title": "Building a Data Pipeline Portfolio Project That Gets You Hired",
            "learning_objective": "By the end of this class, you will be able to plan a portfolio-quality data engineering project and write a compelling project summary for your resume or LinkedIn.",
            "duration_minutes": 25,
            "content_html": """<p>A GitHub profile full of tutorial copies does not stand out. Hiring managers and freelance clients want to see a project that solves a real, specific problem end to end, with clean code and clear documentation, because that is the closest proxy they have to seeing you actually work.</p><h2>What Makes a Project Stand Out</h2><p>Choose a real dataset (Nigerian public data on data.gov.ng, or an interesting Kaggle dataset), solve a specific and explainable problem rather than a generic one, and show the full pipeline: extraction, cleaning, transformation, loading, and ideally some validation or testing. A project with a clear "why" is far more memorable than one with no stated purpose.</p><h2>Writing the Project Summary</h2><p>Your README or LinkedIn post should state the problem in one sentence, the tools used, one specific technical challenge you solved, and a link to the code. For example: "Built a pipeline that ingests daily NGN/USD exchange rates and Lagos fuel prices, flags days with unusual volatility, and loads results into PostgreSQL for a dashboard — solved a tricky deduplication bug caused by the API returning partial-day data twice." This kind of specificity is what makes a recruiter stop scrolling.</p>""",
            "key_concepts": ["portfolio projects", "project storytelling", "specific problem framing", "resume/LinkedIn summaries", "public datasets"],
            "practical_exercise": {
                "title": "Draft Your Portfolio Project Plan and Summary",
                "instructions": "Choose a real dataset or data source relevant to a problem you care about (Nigerian public data, fintech data, agriculture data, or similar). Write a one-page project plan stating the specific problem, your planned pipeline steps, and the tools you will use. Then write a 3-sentence project summary as if posting it on LinkedIn. Submit both."
            },
            "quiz": [
                {"question": "Why do tutorial-copy projects fail to impress hiring managers?", "options": ["Tutorials are always technically wrong", "They do not demonstrate that you can solve a real, specific problem independently", "GitHub does not allow tutorial projects", "Tutorials take too long to complete"], "correct_index": 1, "explanation": "Hiring managers want evidence of independent problem-solving on a real, specific problem, which generic tutorial copies do not demonstrate."},
                {"question": "What should a strong project summary for a resume or LinkedIn include?", "options": ["Only the programming languages used, nothing else", "The specific problem solved, tools used, and one concrete technical challenge overcome", "A list of every file in the repository", "Generic phrases like 'worked with data'"], "correct_index": 1, "explanation": "A specific, concrete summary showing what problem was solved and how stands out far more than vague, generic descriptions."},
                {"question": "Where might you find real Nigerian public datasets for a portfolio project?", "options": ["Only from private company databases", "Public data portals and platforms like Kaggle or government open-data sites", "You cannot use real data for a portfolio project", "Only from paid subscriptions"], "correct_index": 1, "explanation": "Public open-data portals and platforms like Kaggle provide free, real datasets suitable for portfolio projects."}
            ],
            "resources": [
                {"label": "Kaggle Datasets", "url": "https://www.kaggle.com/datasets"},
                {"label": "GitHub", "url": "https://github.com/"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Job-Ready Data Engineering",
            "title": "Working with Real-Time and Streaming Data Concepts (Kafka Overview)",
            "learning_objective": "By the end of this class, you will be able to explain the difference between batch and streaming pipelines and describe how Apache Kafka fits into streaming architectures.",
            "duration_minutes": 25,
            "content_html": """<p>Everything you have built so far in this track is a <strong>batch</strong> pipeline: it processes a chunk of data (a day's transactions, a full file) all at once, on a schedule. Some use cases, like fraud detection or live ride-tracking, cannot wait for the next scheduled batch run — they need data processed within seconds of it being generated. This is <strong>streaming</strong> data engineering.</p><h2>How Kafka Fits In</h2><p>Apache Kafka is the most widely used tool for streaming architectures. Producers publish events (like "a payment just happened") to a Kafka "topic" continuously, and consumers read and process those events in near real time, rather than waiting for a scheduled batch job.</p><pre><code># Conceptual example, not runnable without a Kafka cluster
producer.send("payment-events", {"user_id": 123, "amount": 5000})

for message in consumer:
    process_payment_event(message.value)</code></pre><h2>Batch vs Streaming: When to Use Which</h2><p>Batch is simpler to build, debug, and reason about, and is perfectly fine for daily reports and most analytics. Streaming is necessary when the business genuinely needs sub-minute reaction time, but it adds real complexity in infrastructure and debugging. Most data engineers work primarily in batch pipelines and only reach for streaming when the use case truly demands it — knowing this trade-off is itself a sign of engineering maturity in an interview.</p>""",
            "key_concepts": ["batch vs streaming", "Apache Kafka", "producers and consumers", "real-time data processing", "streaming trade-offs"],
            "practical_exercise": {
                "title": "Compare Batch and Streaming for Three Scenarios",
                "instructions": "For each of these three scenarios, decide whether batch or streaming is the right approach and justify your choice in 2-3 sentences: (1) a weekly sales report for management, (2) fraud detection on mobile money transfers, (3) a daily student attendance summary. Submit your three answers."
            },
            "quiz": [
                {"question": "What is the main difference between batch and streaming data processing?", "options": ["Batch is always faster than streaming", "Batch processes data in scheduled chunks; streaming processes events continuously in near real time", "Streaming does not use any tools", "There is no real difference"], "correct_index": 1, "explanation": "Batch processing handles data in scheduled groups, while streaming processes each event as it arrives, in near real time."},
                {"question": "What role does Apache Kafka play in a streaming architecture?", "options": ["It replaces the need for any database", "It lets producers publish events to topics that consumers read and process in near real time", "It only works for batch pipelines", "It is a data visualization tool"], "correct_index": 1, "explanation": "Kafka acts as a distributed event stream: producers publish events to topics, and consumers process them continuously."},
                {"question": "When is streaming generally the right choice over batch?", "options": ["Always, streaming is strictly better", "When the business genuinely needs sub-minute reaction time, like fraud detection", "Only for weekly reports", "Never, streaming is outdated"], "correct_index": 1, "explanation": "Streaming is worth its added complexity specifically when near-instant reaction to data is a real business requirement."}
            ],
            "resources": [
                {"label": "Apache Kafka Documentation", "url": "https://kafka.apache.org/documentation/"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Job-Ready Data Engineering",
            "title": "Data Engineering on the Job: Working with Analysts, Scientists, and Stakeholders",
            "learning_objective": "By the end of this class, you will be able to describe how data engineers collaborate with other roles and translate a vague business request into a clear pipeline requirement.",
            "duration_minutes": 20,
            "content_html": """<p>Technical skill alone does not make a great data engineer. On the job, you constantly work with data analysts who query your tables, data scientists who need specific features prepared, and business stakeholders who often describe what they want in vague, non-technical language. Translating a fuzzy request into a precise, buildable pipeline is a daily skill, not a one-time task.</p><h2>Turning a Vague Request into Requirements</h2><p>When a stakeholder says "I want to see how our customers are doing," a data engineer's job is to ask clarifying questions: Doing in what sense — retention, spend, engagement? Over what time period? Broken down by what dimension — region, product, age group? These questions turn an unusable request into a concrete pipeline spec.</p><h2>Working Well with Analysts and Data Scientists</h2><p>Analysts need tables that are well-named, documented, and stable — changing a column's meaning without warning breaks their dashboards. Data scientists often need raw or semi-processed data rather than heavily aggregated summaries, since they may need to engineer their own features. Understanding what each role actually needs from your pipelines, and communicating changes before you make them, is what makes you someone teams want to keep working with.</p>""",
            "key_concepts": ["stakeholder communication", "requirements gathering", "cross-functional collaboration", "clarifying questions", "data contracts"],
            "practical_exercise": {
                "title": "Turn a Vague Request into a Pipeline Spec",
                "instructions": "A stakeholder tells you: 'I want to understand if our marketing is working.' Write down five clarifying questions you would ask them, then write a one-paragraph pipeline specification (data sources, transformations, output table) based on reasonable assumed answers to those questions. Submit your questions and specification."
            },
            "quiz": [
                {"question": "Why is asking clarifying questions important when a stakeholder makes a vague data request?", "options": ["It delays the project unnecessarily", "It turns an unusable, ambiguous request into a concrete, buildable pipeline specification", "Stakeholders always give perfectly clear requirements", "It is only useful for junior engineers"], "correct_index": 1, "explanation": "Clarifying questions convert vague business language into specific, actionable requirements a pipeline can actually be built around."},
                {"question": "What kind of data do data scientists often need compared to data analysts?", "options": ["Only final dashboard screenshots", "Raw or semi-processed data, since they may need to engineer their own features", "No data at all", "Only the pipeline's log files"], "correct_index": 1, "explanation": "Data scientists frequently need less-aggregated data so they can build their own features, unlike analysts who often work from summarized tables."},
                {"question": "Why does changing a table's column meaning without warning cause problems?", "options": ["It has no real impact on anyone", "It can silently break dashboards and reports that analysts built relying on that column", "Columns cannot be changed in a database", "It only affects the data engineer, not others"], "correct_index": 1, "explanation": "Downstream consumers like analysts rely on stable table structures; unannounced changes can silently break their existing work."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Job-Ready Data Engineering",
            "title": "Final Project Day: Building Your End-to-End ETL Pipeline",
            "learning_objective": "By the end of this class, you will be able to plan and begin building your complete end-to-end ETL pipeline final project from source data to a documented, loaded result.",
            "duration_minutes": 35,
            "content_html": """<p>Today you start the capstone project: a real ETL pipeline that pulls data from at least two sources, cleans and validates it, transforms it into an analysis-ready shape, and loads it into a PostgreSQL or SQLite database, with a README explaining the architecture and a documented fix for a real data-quality problem. Every skill from the last 29 days feeds directly into this one deliverable.</p><h2>How to Approach It</h2><p>Start by picking your two data sources — a CSV plus an API works well, matching what you practiced on Days 3 and 12. Sketch your pipeline stages on paper first, exactly like the DAG design from Day 16, before writing code. Build extract, clean, transform, and load as separate functions like Day 10, add validation checks like Day 13, and write at least a few pytest tests like Day 21.</p><h2>What "Done" Looks Like</h2><p>A finished submission runs end to end with one command, loads real data into a real database table you can query, includes a README following the Day 25 structure, and documents one specific data-quality problem you found and how you fixed it. Do not aim for perfection today — aim to get your two sources extracting and your schema designed, since the remaining days of your own practice time will be for cleaning, transforming, loading, testing, and documenting.</p>""",
            "key_concepts": ["capstone planning", "end-to-end pipeline execution", "project scoping", "final project kickoff"],
            "practical_exercise": {
                "title": "Start Your Final Project: Build the ETL Pipeline",
                "instructions": "This is the literal start of your final project. Choose your two data sources, sketch your pipeline architecture (extract, clean, transform, load stages and the tools each uses), create your project repository with the folder structure from Day 22, and write working extract functions for both sources that successfully pull and print sample data. Submit your architecture sketch and your working extraction code as the first deliverable toward your final ETL pipeline project."
            },
            "quiz": [
                {"question": "What are the two minimum data sources required for the final ETL project?", "options": ["Only one CSV file", "At least two sources, for example a CSV dataset and a REST API", "Five different databases", "Only manually typed data"], "correct_index": 1, "explanation": "The final project requires pulling data from at least two distinct sources, such as a file-based dataset and a live API."},
                {"question": "Why does the class recommend sketching the pipeline architecture before writing code?", "options": ["Sketching is required by the database", "Planning the stages first, like the DAG design practice, clarifies the pipeline before implementation details get in the way", "Code cannot be written without a sketch", "It replaces the need for a README"], "correct_index": 1, "explanation": "Planning the pipeline stages on paper first, as practiced during the Airflow DAG design class, helps clarify the architecture before diving into implementation."},
                {"question": "What should today's work realistically focus on finishing?", "options": ["The entire finished project including full documentation", "Choosing sources, sketching architecture, and getting basic extraction working", "Only writing the README", "Deploying to a cloud server"], "correct_index": 1, "explanation": "Day 30 is the kickoff of the final project — the goal is to scope it and get initial extraction working, with cleaning, transforming, loading, and documentation completed afterward."}
            ],
            "resources": []
        }
    ]
}
