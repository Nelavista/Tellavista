"""Seed data for the Artificial Intelligence & Machine Learning 30-Day Skill Class."""

SKILL = {
    "slug": "ai-machine-learning",
    "name": "Artificial Intelligence & Machine Learning",
    "tagline": "Learn to build, evaluate, and explain real machine learning models that solve business problems.",
    "description": "Artificial Intelligence and Machine Learning is the discipline of teaching computers to find patterns in data and make predictions or decisions from them. Nigerian banks, telecoms, fintechs, and startups are hiring for this skill to fight fraud, predict churn, score credit risk, and personalize products. This track takes a student from zero coding experience with data to building and evaluating a complete, defensible machine learning model on a real dataset.",
    "level": "beginner",
    "estimated_hours": 65,
    "course_title": "30-Day Artificial Intelligence & Machine Learning Career Track",
    "course_description": "After finishing all 30 days, a student can clean a real dataset, build and tune a supervised machine learning model, evaluate it honestly, explain its predictions, and package the results into a professional model report.",
    "final_project": {
        "title": "Build and Evaluate a Real Machine Learning Model",
        "description": "Choose a real public dataset (for example from Kaggle or UCI) that represents a genuine prediction problem, such as predicting customer churn, loan default, disease risk, or house prices. Clean the data, engineer useful features, and train at least two different models to solve the problem, then compare them using appropriate evaluation metrics. Use an explainability technique to show which features drive the predictions, and write a model results report (a model card) that explains the problem, the data, the approach, the metrics, the limitations, and your recommendation. This mirrors exactly what a junior data scientist is asked to deliver in a first work assignment, and it becomes the centerpiece of your portfolio.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["data cleaning", "feature engineering", "model training", "model evaluation", "explainable AI", "technical writing"],
        "rubric": [
            {"name": "Data preparation and feature engineering", "max_points": 25},
            {"name": "Model building and comparison", "max_points": 30},
            {"name": "Evaluation rigor and explainability", "max_points": 25},
            {"name": "Model report quality and clarity", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Foundations of Machine Learning",
            "title": "What Machine Learning Actually Does and Where Companies Use It",
            "learning_objective": "By the end of this class, you will be able to explain what machine learning is and identify three real business problems it solves.",
            "duration_minutes": 25,
            "content_html": "<p>Every time a bank flags a suspicious transaction, a streaming app recommends a show, or a telecom predicts which customer is about to leave, machine learning is working behind the scenes. Instead of a programmer writing exact rules for every situation, a machine learning system studies past examples and learns the pattern itself. This is why it can handle messy, real-world problems that plain rule-based code cannot.</p><h2>How Machine Learning Differs From Traditional Programming</h2><p>In traditional programming, you write rules and the computer produces answers. In machine learning, you show the computer answers from the past (data) and it produces the rules. For example, instead of writing thousands of if-else statements to detect loan default, you give the model thousands of past loan records labeled default or repaid, and it learns which patterns matter.</p><h2>Where Nigerian and African Companies Use This Today</h2><p>Fintechs like credit-scoring startups use machine learning to decide who gets a loan without a credit history. Telecoms use it to predict which subscribers will churn to a competitor. Insurance companies use it to price risk. Agritech platforms use it to predict crop yield from satellite data. These are not future jobs, they are being hired for right now, and the skill you are building over the next 30 days is exactly what those teams use daily.</p>",
            "key_concepts": ["machine learning", "supervised learning", "data-driven rules", "real-world applications"],
            "practical_exercise": {
                "title": "Find Three Machine Learning Products Around You",
                "instructions": "Write a short document listing three apps or services you use in Nigeria (banking app, jumia, streaming app, social media, etc) that likely use machine learning. For each one, describe in two sentences what problem you think the model is solving and what data it probably learns from. Submit this as a one-page text document."
            },
            "quiz": [
                {"question": "What is the main difference between traditional programming and machine learning?", "options": ["Machine learning does not use a computer", "Traditional programming learns rules from data, machine learning is hand-coded", "Machine learning learns rules from data instead of a programmer writing them by hand", "There is no real difference"], "correct_index": 2, "explanation": "Machine learning systems learn patterns from historical data instead of relying on manually written rules."},
                {"question": "Which of these is a realistic use of machine learning at a Nigerian fintech?", "options": ["Printing physical bank statements", "Predicting which loan applicants are likely to default", "Designing the company logo", "Answering phone calls manually"], "correct_index": 1, "explanation": "Credit risk and default prediction is one of the most common machine learning use cases at fintech companies."},
                {"question": "What do you call the past examples used to train a machine learning model?", "options": ["Output", "Code", "Data", "Interface"], "correct_index": 2, "explanation": "Historical data is what a model studies in order to learn patterns and make future predictions."}
            ],
            "resources": [
                {"label": "Google AI: What is Machine Learning", "url": "https://developers.google.com/machine-learning/crash-course"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Foundations of Machine Learning",
            "title": "The Difference Between AI, Machine Learning, and Deep Learning",
            "learning_objective": "By the end of this class, you will be able to correctly place AI, machine learning, and deep learning in relation to each other and give an example of each.",
            "duration_minutes": 20,
            "content_html": "<p>People use the words AI, machine learning, and deep learning interchangeably, but mixing them up in an interview or a client conversation makes you sound unprepared. Understanding the relationship between these three terms will help you talk confidently about what you are actually building.</p><h2>Three Nested Circles</h2><p>Artificial Intelligence is the broadest idea: making machines behave intelligently, whether through hard-coded rules, search algorithms, or learning. Machine Learning is a subset of AI where the system learns from data instead of following fixed rules. Deep Learning is a subset of machine learning that uses layered neural networks, and it is what powers image recognition, voice assistants, and large language models like the ones behind ChatGPT.</p><h2>A Concrete Example</h2><p>A chess program that follows programmed strategies is AI but not machine learning. A spam filter that studies thousands of emails to learn what spam looks like is machine learning. A system that reads a photo and identifies a human face using many layers of a neural network is deep learning, which is also machine learning, which is also AI. Over the next 30 days, this track focuses mostly on classical machine learning techniques, which are still what most entry-level data roles in Nigeria actually use day to day, because they are cheaper to build, easier to explain to a client, and work extremely well on the tabular business data most companies have.</p>",
            "key_concepts": ["artificial intelligence", "machine learning", "deep learning", "neural networks"],
            "practical_exercise": {
                "title": "Classify Five Technologies",
                "instructions": "List five AI-related technologies you have heard of (for example: Siri, a chess engine, ChatGPT, a spam filter, a self-driving car). For each one, label it as AI only, machine learning, or deep learning, and write one sentence justifying your choice."
            },
            "quiz": [
                {"question": "Which statement correctly describes the relationship between AI, machine learning, and deep learning?", "options": ["They are three unrelated fields", "Deep learning contains machine learning which contains AI", "AI contains machine learning, which contains deep learning", "Machine learning contains AI and deep learning"], "correct_index": 2, "explanation": "AI is the broadest category, machine learning is a subset of AI, and deep learning is a subset of machine learning."},
                {"question": "A rule-based chess program with no learning from data is best described as what?", "options": ["Deep learning", "Machine learning", "AI but not machine learning", "Not AI at all"], "correct_index": 2, "explanation": "It behaves intelligently through programmed rules, which qualifies as AI, but it does not learn from data, so it is not machine learning."},
                {"question": "What technique specifically powers most modern voice assistants and large language models?", "options": ["Spreadsheet formulas", "Deep learning with neural networks", "Manual rule writing", "Basic statistics only"], "correct_index": 1, "explanation": "Deep learning, using layered neural networks, is the technique behind modern voice assistants and large language models."}
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Foundations of Machine Learning",
            "title": "Setting Up Your Python Data Science Toolkit",
            "learning_objective": "By the end of this class, you will be able to install and launch a working Python environment with Jupyter Notebook for data science work.",
            "duration_minutes": 30,
            "content_html": "<p>Before you can build a single model, you need a workspace. Every data scientist you will work with or compete against uses roughly the same toolkit: Python, a package manager, and Jupyter Notebook for interactive experimentation. Getting this set up correctly today saves you hours of frustration later.</p><h2>Installing Anaconda</h2><p>The fastest way to get everything you need in one install is Anaconda, a Python distribution that bundles Python itself with the most important data science libraries and Jupyter Notebook. Download it from the official site for your operating system, install it, then open Anaconda Navigator and launch Jupyter Notebook from there.</p><h2>Your First Notebook Cell</h2><p>A Jupyter Notebook lets you run small chunks of Python code called cells and immediately see the output, which is perfect for exploring data. Create a new notebook and type the following into the first cell, then run it:</p><pre><code>import pandas as pd\nimport numpy as np\nimport sklearn\nprint(\"Environment ready:\", pd.__version__)</code></pre><p>If this runs without an error and prints a version number, your environment is ready for the rest of this track. These three libraries, pandas for tables of data, numpy for numerical arrays, and scikit-learn for machine learning, will appear in almost every single class from here on.</p>",
            "key_concepts": ["Anaconda", "Jupyter Notebook", "pandas", "numpy", "scikit-learn"],
            "practical_exercise": {
                "title": "Confirm Your Working Environment",
                "instructions": "Install Anaconda (or a plain Python plus pip and Jupyter setup if you prefer), open a new Jupyter Notebook, and run the import code from this lesson. Take a screenshot showing the printed pandas version with no errors, and submit it along with the file name you saved the notebook as."
            },
            "quiz": [
                {"question": "What is Jupyter Notebook mainly used for in data science work?", "options": ["Sending emails", "Running code interactively in cells and seeing immediate output", "Designing company logos", "Managing a company payroll"], "correct_index": 1, "explanation": "Jupyter Notebook lets you run small pieces of code and see results immediately, which is ideal for exploring data."},
                {"question": "Which library is used specifically for working with tables of data in Python?", "options": ["numpy", "pandas", "matplotlib", "sklearn"], "correct_index": 1, "explanation": "pandas provides the DataFrame structure, which is the standard way to work with tabular data in Python."},
                {"question": "What does Anaconda provide that makes setup easier for beginners?", "options": ["A single install that bundles Python with major data science libraries and Jupyter", "A cloud database", "A web hosting service", "A spreadsheet application"], "correct_index": 0, "explanation": "Anaconda bundles Python, key libraries, and Jupyter Notebook together so you do not have to install each piece separately."}
            ],
            "resources": [
                {"label": "Project Jupyter Documentation", "url": "https://docs.jupyter.org/"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Foundations of Machine Learning",
            "title": "Python Refresher for Data Work: NumPy Arrays and Pandas DataFrames",
            "learning_objective": "By the end of this class, you will be able to create and manipulate a pandas DataFrame to select, filter, and summarize data.",
            "duration_minutes": 35,
            "content_html": "<p>Almost every machine learning task starts with a table of data, and pandas is the tool that lets you load, inspect, filter, and reshape that table before a model ever sees it. Mastering DataFrames today means you will move faster through every remaining class in this track.</p><h2>Creating and Inspecting a DataFrame</h2><p>A DataFrame is a table with labeled rows and columns, similar to an Excel sheet but far more powerful for code-driven work. You can load one from a CSV file and immediately inspect it:</p><pre><code>import pandas as pd\ndf = pd.read_csv(\"customers.csv\")\nprint(df.head())\nprint(df.shape)\nprint(df.dtypes)</code></pre><p>head() shows the first five rows, shape tells you the number of rows and columns, and dtypes shows what kind of data is in each column, which matters because machine learning models need numbers, not raw text.</p><h2>Filtering and Selecting Data</h2><p>You will constantly need to select specific columns or filter rows that meet a condition. For example, to find all customers older than 30 who are also active:</p><pre><code>active_over_30 = df[(df[\"age\"] > 30) & (df[\"is_active\"] == True)]\nprint(active_over_30[[\"name\", \"age\"]])</code></pre><p>This single line replaces what would be many lines of loops in plain Python, and this exact pattern of filtering rows by conditions is something you will use in almost every data cleaning task in this track.</p>",
            "key_concepts": ["DataFrame", "NumPy array", "row filtering", "column selection", "data types"],
            "practical_exercise": {
                "title": "Explore a Sample Dataset with Pandas",
                "instructions": "Download any small public CSV dataset (for example a sample sales or student dataset from Kaggle), load it into a pandas DataFrame, and write code that prints the shape, the column data types, the first 10 rows, and one filtered subset based on a condition of your choice. Submit your notebook file with the code and its output visible."
            },
            "quiz": [
                {"question": "What does the pandas head() function do by default?", "options": ["Deletes the first five rows", "Shows the first five rows of a DataFrame", "Sorts the entire dataset", "Counts missing values"], "correct_index": 1, "explanation": "head() displays the first five rows of a DataFrame by default, which is useful for a quick first look at the data."},
                {"question": "Why do machine learning models need numeric data rather than raw text?", "options": ["Text takes up less memory", "Models perform mathematical calculations that require numbers", "Text is not allowed in Python", "Numbers load faster from CSV files"], "correct_index": 1, "explanation": "Machine learning algorithms are built on mathematical operations, so text columns must eventually be converted to numeric form."},
                {"question": "In the filtering example, what does the & symbol do between two conditions?", "options": ["It divides the two conditions", "It combines both conditions so both must be true", "It ignores the second condition", "It converts the DataFrame to a list"], "correct_index": 1, "explanation": "The & operator combines two boolean conditions in pandas, keeping only rows where both are true."}
            ],
            "resources": [
                {"label": "pandas Documentation", "url": "https://pandas.pydata.org/docs/"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Foundations of Machine Learning",
            "title": "Finding and Loading Real Datasets from Kaggle and UCI",
            "learning_objective": "By the end of this class, you will be able to find a suitable real-world dataset on Kaggle or the UCI repository and load it correctly into a notebook.",
            "duration_minutes": 25,
            "content_html": "<p>Every project in this track, including your final capstone, depends on finding a real dataset that represents a genuine problem. Knowing where to look and how to judge whether a dataset is good enough is a skill in itself, and it is the first thing you do on any real data science job before touching a single model.</p><h2>Where to Find Good Datasets</h2><p>Kaggle hosts thousands of free, real-world datasets with descriptions of what each column means, and it is the most common source used by working data scientists for practice and portfolio projects. The UCI Machine Learning Repository is an older, well-respected academic source, especially strong for classic problems like predicting disease, wine quality, or student performance. Government open data portals and World Bank data are also excellent sources for African-context datasets.</p><h2>What Makes a Dataset Usable</h2><p>A good dataset for this track has at least a few hundred rows, a clear target you are trying to predict, and columns that plausibly relate to that target. When you download a dataset, always read the accompanying description file first, because it tells you what each column means, which prevents you from misinterpreting a code like 0 or 1 in a column that is not obvious.</p><pre><code>import pandas as pd\ndf = pd.read_csv(\"telco_churn.csv\")\nprint(df.columns.tolist())\nprint(df[\"Churn\"].value_counts())</code></pre><p>Checking value_counts() on your target column early tells you immediately whether the problem is balanced or skewed, which changes how you will approach modeling later in this track.</p>",
            "key_concepts": ["Kaggle", "UCI repository", "dataset selection", "target variable", "value_counts"],
            "practical_exercise": {
                "title": "Select Your Working Dataset",
                "instructions": "Search Kaggle or the UCI repository and find a real dataset with at least 300 rows and a clear column you could predict (for example churn, price, or disease outcome). Load it into a notebook, print its shape and column list, and write two sentences explaining what business or real-world question this dataset could answer. Keep this dataset, you will use it again in upcoming classes."
            },
            "quiz": [
                {"question": "Why should you read a dataset description file before analyzing it?", "options": ["It is required by law", "It explains what each column means so you do not misinterpret the data", "It makes the file load faster", "It removes missing values automatically"], "correct_index": 1, "explanation": "Column descriptions prevent you from misunderstanding coded values or units, which leads to incorrect analysis."},
                {"question": "What is a key requirement for a dataset to be usable for a supervised learning project?", "options": ["It must be in Excel format only", "It must have a clear target variable you are trying to predict", "It must have exactly 100 rows", "It must contain only numeric columns already"], "correct_index": 1, "explanation": "Supervised learning requires a labeled target variable that the model learns to predict."},
                {"question": "What does checking value_counts() on your target column tell you early on?", "options": ["The file size of the dataset", "Whether the classes are balanced or skewed", "The programming language used", "The number of columns"], "correct_index": 1, "explanation": "value_counts() shows how many rows belong to each class, revealing class imbalance that affects modeling choices later."}
            ],
            "resources": [
                {"label": "Kaggle Datasets", "url": "https://www.kaggle.com/datasets"},
                {"label": "UCI Machine Learning Repository", "url": "https://archive.ics.uci.edu/"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Exploring and Preparing Real Data",
            "title": "Exploratory Data Analysis: Reading a Dataset Before You Touch a Model",
            "learning_objective": "By the end of this class, you will be able to perform a structured exploratory data analysis on a new dataset to understand its shape, quality, and structure.",
            "duration_minutes": 30,
            "content_html": "<p>Jumping straight into modeling without exploring your data first is one of the most common mistakes beginners make, and it produces models that fail silently. Exploratory Data Analysis, or EDA, is the disciplined process of understanding your dataset before you touch a single algorithm, and every professional data scientist spends significant time here.</p><h2>A Standard EDA Checklist</h2><p>A solid first pass answers a handful of questions: how many rows and columns are there, what type is each column, how many values are missing in each column, and what does the target column look like. Running this checklist takes minutes and prevents hours of wasted modeling later.</p><pre><code>print(df.info())\nprint(df.describe())\nprint(df.isnull().sum())</code></pre><p>info() shows column types and non-null counts, describe() shows statistical summaries like mean and standard deviation for numeric columns, and isnull().sum() counts missing values per column.</p><h2>Reading the Story in the Numbers</h2><p>Suppose describe() shows a customer age column with a minimum of negative 5 and a maximum of 200. That immediately tells you there are data entry errors that need cleaning before modeling, something a model trained blindly would never catch. This kind of detective work, spotting what looks wrong before it breaks your model, is exactly what separates a junior analyst who ships broken predictions from one who is trusted with real production data.</p>",
            "key_concepts": ["exploratory data analysis", "info()", "describe()", "missing values", "data quality"],
            "practical_exercise": {
                "title": "Run a Full EDA Checklist",
                "instructions": "Using the dataset you selected on Day 5, run info(), describe(), and isnull().sum() on it. Write a short summary of at least five findings, including the shape of the data, any suspicious values you spotted, and which columns have missing data. Submit the notebook and the written summary."
            },
            "quiz": [
                {"question": "What is the main purpose of exploratory data analysis?", "options": ["To immediately train the most accurate model possible", "To understand the shape, quality, and structure of the data before modeling", "To delete all missing data", "To visualize only the target column"], "correct_index": 1, "explanation": "EDA is about understanding your data thoroughly before any modeling decisions are made."},
                {"question": "Which pandas function shows statistical summaries like mean and standard deviation for numeric columns?", "options": ["head()", "isnull()", "describe()", "shape"], "correct_index": 2, "explanation": "describe() generates summary statistics such as mean, minimum, maximum, and standard deviation for numeric columns."},
                {"question": "If a customer age column shows a minimum value of negative 5, what should you conclude?", "options": ["The dataset is perfect and ready for modeling", "There is likely a data entry error that needs cleaning", "Negative ages are normal in real datasets", "You should delete the entire dataset"], "correct_index": 1, "explanation": "A negative age is not physically possible, signaling a data quality issue that must be investigated and cleaned."}
            ],
            "resources": []
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Exploring and Preparing Real Data",
            "title": "Cleaning Messy Data: Missing Values, Duplicates, and Outliers",
            "learning_objective": "By the end of this class, you will be able to handle missing values, remove duplicates, and treat outliers in a real dataset.",
            "duration_minutes": 35,
            "content_html": "<p>Real datasets are never clean. Customers leave fields blank, systems log the same transaction twice, and sensors record impossible values. A model trained on dirty data learns dirty patterns, so cleaning is not optional, it is most of the actual work in a real machine learning job.</p><h2>Handling Missing Values</h2><p>You generally have two choices: remove rows or columns with too much missing data, or fill them in using a sensible estimate, called imputation. For a numeric column, filling missing values with the median is a common, safe default because it resists being skewed by extreme values.</p><pre><code>df[\"income\"] = df[\"income\"].fillna(df[\"income\"].median())\ndf = df.drop_duplicates()\nprint(\"Duplicates removed, remaining rows:\", df.shape[0])</code></pre><h2>Spotting and Treating Outliers</h2><p>An outlier is a value far outside the normal range, like a transaction of 50 million naira in a dataset where most transactions are under 50,000 naira. Sometimes an outlier is a genuine rare event worth keeping, and sometimes it is a data entry mistake worth removing or capping. A common technique is the interquartile range method, where you flag values far below the 25th percentile or far above the 75th percentile as potential outliers, then investigate each case rather than deleting automatically. Blindly deleting outliers can remove exactly the fraud cases or high-value customers you were trying to detect in the first place, so always ask what an outlier means in context before treating it.</p>",
            "key_concepts": ["missing value imputation", "median fill", "duplicate removal", "outliers", "interquartile range"],
            "practical_exercise": {
                "title": "Clean Your Working Dataset",
                "instructions": "On your Day 5 dataset, identify all columns with missing values and decide, with a one-sentence justification each, whether to fill or drop them. Remove any duplicate rows, and identify at least one potential outlier using the interquartile range method. Submit the cleaning code along with a short before-and-after comparison of the row count and missing value counts."
            },
            "quiz": [
                {"question": "Why is the median often preferred over the mean when filling missing numeric values?", "options": ["The median is always larger", "The median is not easily skewed by extreme values", "The median is faster to calculate", "The mean cannot be calculated in pandas"], "correct_index": 1, "explanation": "The median resists distortion from extreme outliers, making it a safer default for imputation than the mean."},
                {"question": "What is the danger of blindly deleting all detected outliers?", "options": ["It always improves model accuracy", "You might remove genuine rare but important events like fraud cases", "It makes the dataset load faster", "Outliers cannot actually be detected"], "correct_index": 1, "explanation": "Some outliers represent real, important events, so removing them without investigation can hurt exactly the cases you care about."},
                {"question": "What does drop_duplicates() do in pandas?", "options": ["Removes rows that are exact repeats of another row", "Removes all missing values", "Sorts the DataFrame", "Converts text columns to numbers"], "correct_index": 0, "explanation": "drop_duplicates() removes rows that are identical to another row in the DataFrame."}
            ],
            "resources": [
                {"label": "scikit-learn: Imputation of Missing Values", "url": "https://scikit-learn.org/stable/modules/impute.html"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Exploring and Preparing Real Data",
            "title": "Visualizing Data with Matplotlib and Seaborn to Spot Patterns",
            "learning_objective": "By the end of this class, you will be able to create histograms, bar charts, and correlation heatmaps to identify patterns in a dataset.",
            "duration_minutes": 30,
            "content_html": "<p>A well-chosen chart can reveal a pattern in five seconds that would take an hour to find by scrolling through raw rows. Visualization is how data scientists build intuition about a dataset before deciding what modeling approach makes sense.</p><h2>Distributions and Relationships</h2><p>A histogram shows how a single numeric column is distributed, revealing whether it is normal, skewed, or has strange spikes. A bar chart is best for comparing counts across categories, like how many customers fall into each subscription plan.</p><pre><code>import seaborn as sns\nimport matplotlib.pyplot as plt\n\nsns.histplot(df[\"monthly_charges\"], bins=30)\nplt.title(\"Distribution of Monthly Charges\")\nplt.show()</code></pre><h2>Correlation Heatmaps</h2><p>A correlation heatmap shows how strongly every numeric column relates to every other numeric column, using color intensity. This is especially useful for spotting which features might actually help predict your target before you build anything.</p><pre><code>corr = df.corr(numeric_only=True)\nsns.heatmap(corr, annot=True, cmap=\"coolwarm\")\nplt.show()</code></pre><p>If a heatmap shows that tenure has a strong negative correlation with churn, that is a strong early signal that customers who have been around longer are less likely to leave, which is exactly the kind of insight that guides which features you prioritize when you start building models next week.</p>",
            "key_concepts": ["histogram", "bar chart", "correlation heatmap", "seaborn", "matplotlib"],
            "practical_exercise": {
                "title": "Visualize Your Dataset",
                "instructions": "On your working dataset, create one histogram of a numeric column, one bar chart comparing a categorical column, and one correlation heatmap of the numeric features. Write two sentences describing the most interesting pattern you noticed. Submit the notebook with all three charts visible."
            },
            "quiz": [
                {"question": "Which chart type is best for showing how a single numeric column is distributed?", "options": ["Bar chart", "Histogram", "Correlation heatmap", "Pie chart only"], "correct_index": 1, "explanation": "A histogram groups numeric values into bins and shows their frequency, revealing the shape of the distribution."},
                {"question": "What does a correlation heatmap help you identify before modeling?", "options": ["The exact accuracy your model will achieve", "Which features might relate strongly to each other or to the target", "The programming language used to build the dataset", "The number of missing values"], "correct_index": 1, "explanation": "A correlation heatmap visually reveals relationships between numeric variables, helping guide feature selection."},
                {"question": "In the churn example, a strong negative correlation between tenure and churn suggests what?", "options": ["Longer-tenured customers are more likely to churn", "Tenure has no relationship with churn", "Longer-tenured customers are less likely to churn", "Tenure should be deleted from the dataset"], "correct_index": 2, "explanation": "A negative correlation means as tenure increases, churn tends to decrease, suggesting loyal customers churn less."}
            ],
            "resources": [
                {"label": "Seaborn Documentation", "url": "https://seaborn.pydata.org/"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Exploring and Preparing Real Data",
            "title": "Feature Engineering: Turning Raw Columns into Model-Ready Signals",
            "learning_objective": "By the end of this class, you will be able to create at least two new engineered features from raw columns in a dataset.",
            "duration_minutes": 30,
            "content_html": "<p>Raw data rarely arrives in the exact shape a model needs to perform well. Feature engineering is the craft of transforming and combining raw columns into new signals that make patterns easier for a model to learn, and experienced practitioners will tell you it often matters more than which algorithm you choose.</p><h2>Creating New Features from Existing Ones</h2><p>Suppose you have a signup_date and a last_active_date column. Neither raw date is very useful to a model on its own, but the number of days between them, a customer's activity span, could be a powerful predictor of churn.</p><pre><code>df[\"signup_date\"] = pd.to_datetime(df[\"signup_date\"])\ndf[\"last_active_date\"] = pd.to_datetime(df[\"last_active_date\"])\ndf[\"days_active\"] = (df[\"last_active_date\"] - df[\"signup_date\"]).dt.days</code></pre><h2>Binning and Ratios</h2><p>Turning a continuous column into categories, called binning, can also help. For example, converting exact age into groups like 18 to 25, 26 to 35, and so on can reveal patterns that get lost in the noise of exact numbers. Ratios are another powerful technique: total_spend divided by number_of_orders gives you average order value, a single number that often predicts behavior better than either raw column alone. The features you engineer today, days_active and average_order_value, are exactly the kind of columns that will meaningfully lift your model's performance when you start building predictive models in week three.</p>",
            "key_concepts": ["feature engineering", "date differences", "binning", "ratio features", "derived columns"],
            "practical_exercise": {
                "title": "Engineer Two New Features",
                "instructions": "On your working dataset, create at least two new engineered features (for example a date difference, a ratio, or a binned category) that you believe could help predict your target column. Explain in one sentence per feature why you believe it will be useful. Submit the code and your written justification."
            },
            "quiz": [
                {"question": "What is feature engineering?", "options": ["Deleting all columns except the target", "Transforming and combining raw columns into new, more useful signals", "Writing the final model report", "Installing Python libraries"], "correct_index": 1, "explanation": "Feature engineering creates new, more predictive columns from raw data to help a model learn patterns more effectively."},
                {"question": "What could days_active, calculated as the difference between two dates, help predict?", "options": ["The company's stock price", "Customer churn based on activity span", "The programming language used", "The number of columns in the dataset"], "correct_index": 1, "explanation": "The length of time a customer has been active is a common and useful predictor of churn."},
                {"question": "What does a ratio feature like total_spend divided by number_of_orders represent?", "options": ["Total number of customers", "Average order value", "The dataset file size", "A missing value indicator"], "correct_index": 1, "explanation": "Dividing total spend by number of orders produces the average order value, a commonly useful derived feature."}
            ],
            "resources": []
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Exploring and Preparing Real Data",
            "title": "Understanding Supervised vs Unsupervised Learning with Real Examples",
            "learning_objective": "By the end of this class, you will be able to correctly classify a real business problem as supervised or unsupervised learning.",
            "duration_minutes": 25,
            "content_html": "<p>Before choosing an algorithm, you must first know what type of problem you are solving. This single decision, supervised or unsupervised, determines your entire approach for the rest of the project, so getting it right is the most important early judgment call you will make.</p><h2>Supervised Learning: Learning from Labeled Answers</h2><p>Supervised learning is used when you have historical examples that already include the correct answer, called a label. Predicting whether a loan will default uses past loans that are already labeled default or repaid. Predicting a house price uses past house sales where the actual sale price is known. Supervised learning splits further into classification, predicting a category like churn or not churn, and regression, predicting a number like price or salary.</p><h2>Unsupervised Learning: Finding Structure Without Labels</h2><p>Unsupervised learning is used when you do not have labeled answers, and instead want the algorithm to find hidden structure on its own. A marketing team with no predefined customer categories might use clustering to automatically group similar customers by their purchase behavior, discovering segments like bargain hunters and loyal high spenders without ever telling the algorithm those labels exist beforehand. Recognizing which situation you are in early saves enormous time, because trying to force a clustering algorithm to predict a specific label, or trying to force a classifier onto unlabeled data, simply will not work.</p>",
            "key_concepts": ["supervised learning", "unsupervised learning", "classification", "regression", "clustering"],
            "practical_exercise": {
                "title": "Classify Five Business Problems",
                "instructions": "Write down five different business problems (for example predicting salary, grouping customers, detecting fraud, predicting exam scores, segmenting products). For each one, label it as classification, regression, or clustering, and justify your answer in one sentence."
            },
            "quiz": [
                {"question": "What distinguishes supervised learning from unsupervised learning?", "options": ["Supervised learning uses labeled historical answers, unsupervised learning does not", "Unsupervised learning is always more accurate", "Supervised learning cannot use real data", "There is no meaningful difference"], "correct_index": 0, "explanation": "Supervised learning relies on labeled examples with known correct answers, while unsupervised learning finds structure without labels."},
                {"question": "Predicting an exact house sale price in naira is an example of which type of problem?", "options": ["Clustering", "Classification", "Regression", "Unsupervised learning"], "correct_index": 2, "explanation": "Predicting a continuous numeric value like price is a regression problem."},
                {"question": "A marketing team wants to discover unknown customer segments with no predefined categories. Which approach fits best?", "options": ["Regression", "Classification", "Clustering", "Supervised classification"], "correct_index": 2, "explanation": "Clustering is an unsupervised technique used to discover natural groupings in data without predefined labels."}
            ],
            "resources": [
                {"label": "scikit-learn: Supervised Learning", "url": "https://scikit-learn.org/stable/supervised_learning.html"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Building Your First Predictive Models",
            "title": "Building Your First Linear Regression Model to Predict a Number",
            "learning_objective": "By the end of this class, you will be able to train and use a linear regression model to predict a numeric value in scikit-learn.",
            "duration_minutes": 35,
            "content_html": "<p>Today you build your first real machine learning model. Linear regression is the simplest and most interpretable algorithm for predicting a number, and it is still widely used in real jobs, including pricing models, salary estimation, and demand forecasting, because it is fast, explainable, and hard to misuse.</p><h2>How Linear Regression Works</h2><p>Linear regression finds the straight-line relationship between your input features and the number you want to predict. For a single feature, it fits a line of the form y equals mx plus b, where the model learns the best m (slope) and b (intercept) from your training data.</p><h2>Training Your First Model</h2><pre><code>from sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\n\nX = df[[\"square_meters\", \"bedrooms\"]]\ny = df[\"price\"]\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\npredictions = model.predict(X_test)\nprint(predictions[:5])</code></pre><p>fit() is where the actual learning happens, the model studies X_train and y_train to find the best-fitting line. predict() then applies what it learned to new data it has never seen, X_test, which is the real test of whether the model generalizes. You will use this exact fit-then-predict pattern for almost every algorithm in this track, so understanding it well today pays off for the rest of the course.</p>",
            "key_concepts": ["linear regression", "fit and predict", "train_test_split", "slope and intercept", "regression"],
            "practical_exercise": {
                "title": "Train Your First Regression Model",
                "instructions": "Using a dataset with a numeric target (or a public housing or salary dataset if your Day 5 dataset does not have one), train a linear regression model using at least two input features. Print the first five predictions next to the actual test values for comparison. Submit the notebook with the working code and output."
            },
            "quiz": [
                {"question": "What does the fit() method do when training a scikit-learn model?", "options": ["It deletes the training data", "It studies the training data to learn the best model parameters", "It makes predictions on new data", "It visualizes the dataset"], "correct_index": 1, "explanation": "fit() is the training step where the model learns patterns and parameters from the training data."},
                {"question": "Why do we split data into training and test sets before training a model?", "options": ["To make the code run faster", "To evaluate the model on data it has never seen, testing real generalization", "Because scikit-learn requires exactly two files", "To reduce the number of features"], "correct_index": 1, "explanation": "Testing on unseen data reveals how well the model generalizes rather than just memorizing the training data."},
                {"question": "Linear regression is best suited for predicting what kind of target?", "options": ["A category with no order, like a color", "A continuous numeric value, like price", "An image", "A block of text"], "correct_index": 1, "explanation": "Linear regression predicts continuous numeric outputs, making it suitable for problems like price prediction."}
            ],
            "resources": [
                {"label": "scikit-learn: Linear Models", "url": "https://scikit-learn.org/stable/modules/linear_model.html"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Building Your First Predictive Models",
            "title": "Classification with Logistic Regression: Predicting Yes or No Outcomes",
            "learning_objective": "By the end of this class, you will be able to train a logistic regression model to classify data into two categories.",
            "duration_minutes": 30,
            "content_html": "<p>Many of the highest-value business problems are yes-or-no questions: will this customer churn, will this transaction turn out to be fraud, will this loan be repaid. Logistic regression is the classic, still-widely-used algorithm for exactly these binary classification problems, and it is almost always the first model a professional tries before reaching for anything more complex.</p><h2>From a Line to a Probability</h2><p>Despite the name, logistic regression is a classification algorithm, not a regression one. It calculates a probability between 0 and 1 that a row belongs to the positive class, then applies a threshold, usually 0.5, to turn that probability into a final yes or no decision.</p><pre><code>from sklearn.linear_model import LogisticRegression\n\nX = df[[\"tenure_months\", \"monthly_charges\"]]\ny = df[\"churn\"]\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nclf = LogisticRegression()\nclf.fit(X_train, y_train)\nprobabilities = clf.predict_proba(X_test)\npredictions = clf.predict(X_test)</code></pre><h2>Why Probability Matters</h2><p>predict_proba() returns the actual probability, not just the final label, which matters a great deal in real business use. A bank might treat a 51 percent probability of default very differently from a 95 percent probability, even though logistic regression would label both as default at the default 0.5 threshold. Understanding and adjusting that threshold based on business risk tolerance is a skill that separates a junior analyst from someone who can be trusted with production risk decisions.</p>",
            "key_concepts": ["logistic regression", "binary classification", "probability threshold", "predict_proba", "positive class"],
            "practical_exercise": {
                "title": "Build a Yes or No Classifier",
                "instructions": "Using your working dataset (or a churn or default dataset if yours lacks a binary target), train a logistic regression model to predict a two-category outcome. Print both the predicted labels and predicted probabilities for the first five test rows, and write one sentence explaining what changing the decision threshold from 0.5 to 0.3 would do to your predictions."
            },
            "quiz": [
                {"question": "Despite its name, what type of problem is logistic regression actually used for?", "options": ["Predicting a continuous numeric value", "Classification, predicting a category", "Clustering unlabeled data", "Image generation"], "correct_index": 1, "explanation": "Logistic regression is a classification algorithm despite having regression in its name."},
                {"question": "What does predict_proba() return that predict() does not?", "options": ["The exact feature names", "The actual probability estimates behind each prediction", "The training data itself", "The model file size"], "correct_index": 1, "explanation": "predict_proba() gives the underlying probability for each class, while predict() only gives the final chosen label."},
                {"question": "Why might a bank want to look at the actual probability rather than just the final yes/no label?", "options": ["Probabilities are always more accurate than labels", "A 51 percent risk and a 95 percent risk deserve very different business responses", "Labels cannot be computed from probabilities", "The threshold is always fixed at 0.9"], "correct_index": 1, "explanation": "Two cases could both be labeled the same class at the default threshold, yet carry very different real risk levels."}
            ],
            "resources": [
                {"label": "scikit-learn: Logistic Regression", "url": "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Building Your First Predictive Models",
            "title": "Decision Trees and Random Forests for Higher Accuracy Predictions",
            "learning_objective": "By the end of this class, you will be able to train a decision tree and a random forest model and explain why random forests usually outperform a single tree.",
            "duration_minutes": 35,
            "content_html": "<p>Decision trees and their more powerful cousin, random forests, are among the most commonly used algorithms in real industry work because they handle messy, non-linear data well and require very little preprocessing compared to linear models.</p><h2>How a Decision Tree Thinks</h2><p>A decision tree splits your data repeatedly using simple yes-or-no questions on your features, such as is monthly_charges greater than 70, building a tree of decisions until it reaches a final prediction. This mirrors how a human loan officer might reason through a decision, which makes trees easy to explain to non-technical stakeholders.</p><h2>Why Random Forests Are Usually Better</h2><p>A single decision tree tends to overfit, meaning it memorizes quirks of the training data rather than learning general patterns. A random forest fixes this by training hundreds of different decision trees, each on a random subset of the data and features, then averaging their predictions.</p><pre><code>from sklearn.ensemble import RandomForestClassifier\n\nrf = RandomForestClassifier(n_estimators=200, random_state=42)\nrf.fit(X_train, y_train)\npredictions = rf.predict(X_test)\n\nimportances = pd.Series(rf.feature_importances_, index=X.columns)\nprint(importances.sort_values(ascending=False))</code></pre><p>feature_importances_ is one of the most valuable outputs a random forest gives you, ranking exactly which columns drove the model's decisions the most, which is often the actual business insight a client is paying for, even more than the prediction itself.</p>",
            "key_concepts": ["decision tree", "random forest", "overfitting", "ensemble learning", "feature importance"],
            "practical_exercise": {
                "title": "Compare a Tree to a Forest",
                "instructions": "On your working dataset, train both a DecisionTreeClassifier and a RandomForestClassifier (or regressor if predicting a number) using the same features. Print the accuracy or error of each on the test set, and print the random forest's feature importances. Write two sentences comparing the results."
            },
            "quiz": [
                {"question": "Why do random forests usually outperform a single decision tree?", "options": ["They use less data", "They average many trees trained on random subsets, reducing overfitting", "They never make mistakes", "They only work on text data"], "correct_index": 1, "explanation": "Averaging many diverse trees reduces the overfitting problem that a single decision tree is prone to."},
                {"question": "What does the feature_importances_ attribute of a trained random forest tell you?", "options": ["The exact accuracy of the model", "Which features contributed most to the model's predictions", "The number of trees in the forest", "The size of the dataset"], "correct_index": 1, "explanation": "feature_importances_ ranks how much each input feature contributed to the model's decisions."},
                {"question": "What does it mean when a decision tree overfits the training data?", "options": ["It generalizes very well to new data", "It memorizes quirks of the training data rather than learning general patterns", "It has too few splits", "It cannot be trained at all"], "correct_index": 1, "explanation": "Overfitting means the model captures noise specific to the training set instead of patterns that generalize."}
            ],
            "resources": [
                {"label": "scikit-learn: Ensemble Methods", "url": "https://scikit-learn.org/stable/modules/ensemble.html"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Building Your First Predictive Models",
            "title": "Splitting Data the Right Way: Train, Validation, and Test Sets",
            "learning_objective": "By the end of this class, you will be able to correctly split a dataset into training, validation, and test sets and explain the purpose of each.",
            "duration_minutes": 25,
            "content_html": "<p>One of the fastest ways to produce a dishonest model is to evaluate it on the same data it was trained on. Today's class covers the discipline of splitting data correctly, a small technical step that has enormous consequences for whether your results can be trusted.</p><h2>Why One Split Is Not Always Enough</h2><p>A basic train-test split, commonly 80 percent training and 20 percent testing, is the minimum requirement. But if you also want to compare different models or tune settings before your final evaluation, using the test set repeatedly for that tuning secretly leaks information into your results, inflating how good your model looks. This is why professionals often add a third split, a validation set, used purely for tuning decisions, leaving the test set untouched until the very end.</p><pre><code>from sklearn.model_selection import train_test_split\n\nX_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)\nX_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)\n\nprint(len(X_train), len(X_val), len(X_test))</code></pre><h2>Cross-Validation as an Alternative</h2><p>When you have a smaller dataset, splitting three ways can leave too little data for reliable testing. Cross-validation solves this by rotating which portion of the training data acts as validation across several rounds, giving you a more stable performance estimate without permanently sacrificing data. You will use cross-validation directly in an upcoming class on fighting overfitting.</p>",
            "key_concepts": ["train-test split", "validation set", "data leakage", "cross-validation", "random_state"],
            "practical_exercise": {
                "title": "Perform a Three-Way Split",
                "instructions": "On your working dataset, perform a three-way split into training (70 percent), validation (15 percent), and test (15 percent) sets. Print the row count of each split, and write two sentences explaining, in your own words, why the test set should not be touched until final evaluation."
            },
            "quiz": [
                {"question": "Why is evaluating a model on the same data it was trained on a problem?", "options": ["It takes too much computing power", "It gives an overly optimistic, dishonest picture of performance", "It is not technically possible in scikit-learn", "It always produces a validation error"], "correct_index": 1, "explanation": "A model tested on its own training data appears far more accurate than it truly is on new, unseen data."},
                {"question": "What is the purpose of a validation set, separate from the test set?", "options": ["To permanently store the raw data", "To make tuning decisions without touching the final test set", "To replace the need for a test set entirely", "To visualize the dataset"], "correct_index": 1, "explanation": "A validation set lets you compare models and tune settings while keeping the test set untouched for a final, honest evaluation."},
                {"question": "When might cross-validation be preferred over a fixed three-way split?", "options": ["When the dataset is very small and a three-way split leaves too little data", "When you never want to evaluate a model", "When the dataset has no missing values", "When using only linear regression"], "correct_index": 0, "explanation": "Cross-validation makes efficient use of limited data by rotating the validation portion across multiple rounds."}
            ],
            "resources": [
                {"label": "scikit-learn: Cross-Validation", "url": "https://scikit-learn.org/stable/modules/cross_validation.html"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Building Your First Predictive Models",
            "title": "Measuring Model Performance: Accuracy, Precision, Recall, and F1 Score",
            "learning_objective": "By the end of this class, you will be able to calculate and correctly interpret accuracy, precision, recall, and F1 score for a classification model.",
            "duration_minutes": 30,
            "content_html": "<p>A model that is 95 percent accurate sounds impressive, until you learn that only 5 percent of the data belongs to the class you actually care about, like fraud, meaning a model that predicts no fraud every single time would also score 95 percent. Today you learn the metrics that actually reveal whether a model is useful.</p><h2>Beyond Accuracy</h2><p>Precision answers: of everything the model predicted as positive, how much was actually correct. Recall answers: of everything that was actually positive, how much did the model correctly catch. These two often trade off against each other, and which one matters more depends entirely on the business context.</p><pre><code>from sklearn.metrics import classification_report, confusion_matrix\n\nprint(confusion_matrix(y_test, predictions))\nprint(classification_report(y_test, predictions))</code></pre><h2>Choosing the Right Metric for the Job</h2><p>For fraud detection, missing an actual fraud case (low recall) is usually far more costly than flagging an honest transaction for review (lower precision), so recall is often prioritized. For a spam filter, wrongly blocking an important email (low precision) is often worse than letting a few spam messages through, so precision matters more there. The F1 score balances both into a single number, useful when you need one metric to compare models quickly. Knowing which metric to lead with in a report is exactly the judgment call that shows a hiring manager you understand the business, not just the code.</p>",
            "key_concepts": ["accuracy", "precision", "recall", "F1 score", "confusion matrix"],
            "practical_exercise": {
                "title": "Evaluate Your Classifier Properly",
                "instructions": "On a classification model you built earlier in this track, print the confusion matrix and classification report. Identify the precision and recall for the positive class, and write three sentences explaining which metric matters more for your specific problem and why."
            },
            "quiz": [
                {"question": "Why can accuracy be a misleading metric on an imbalanced dataset?", "options": ["Accuracy cannot be calculated on imbalanced data", "A model can score high accuracy just by always predicting the majority class", "Accuracy only works for regression problems", "Accuracy requires a validation set"], "correct_index": 1, "explanation": "On imbalanced data, always predicting the majority class produces a high accuracy score while being practically useless."},
                {"question": "In fraud detection, why is recall often prioritized over precision?", "options": ["Because precision cannot be measured for fraud", "Because missing an actual fraud case is usually more costly than a false alarm", "Because recall is always higher than precision", "Because fraud detection does not use classification"], "correct_index": 1, "explanation": "Catching as much real fraud as possible (high recall) is typically more important than avoiding false alarms."},
                {"question": "What does the F1 score represent?", "options": ["The total number of predictions made", "A balance between precision and recall in a single number", "The number of features used", "The training time of the model"], "correct_index": 1, "explanation": "The F1 score is the harmonic mean of precision and recall, giving a single balanced metric."}
            ],
            "resources": [
                {"label": "scikit-learn: Model Evaluation", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Improving and Applying Models to Real Problems",
            "title": "Fighting Overfitting: Regularization, Cross-Validation, and Simplicity",
            "learning_objective": "By the end of this class, you will be able to detect overfitting in a model and apply at least one technique to reduce it.",
            "duration_minutes": 30,
            "content_html": "<p>A model that performs beautifully on training data but poorly on new data is not actually useful, and this exact failure, overfitting, is one of the most common reasons real projects fail after deployment. Recognizing and fixing it is a core professional skill.</p><h2>Spotting Overfitting</h2><p>The clearest sign of overfitting is a large gap between training performance and test performance. If your model scores 98 percent accuracy on training data but only 70 percent on test data, it has memorized the training set rather than learned generalizable patterns.</p><pre><code>train_score = model.score(X_train, y_train)\ntest_score = model.score(X_test, y_test)\nprint(\"Train:\", train_score, \"Test:\", test_score)</code></pre><h2>Techniques to Fix It</h2><p>Regularization adds a penalty for overly complex models, discouraging the algorithm from relying too heavily on any single feature; scikit-learn's LogisticRegression and Ridge models support this through the C or alpha parameter. Reducing model complexity, such as limiting the max_depth of a decision tree, also helps directly. Cross-validation, covered on Day 14, gives you a more honest sense of how a model will generalize before you ever touch the test set, letting you catch overfitting during development rather than discovering it too late.</p><pre><code>from sklearn.model_selection import cross_val_score\nscores = cross_val_score(model, X_train, y_train, cv=5)\nprint(\"Cross-val scores:\", scores, \"Mean:\", scores.mean())</code></pre>",
            "key_concepts": ["overfitting", "regularization", "cross_val_score", "max_depth", "generalization"],
            "practical_exercise": {
                "title": "Diagnose and Fix Overfitting",
                "instructions": "On a model you trained earlier, compare its training score to its test score to check for overfitting. If a gap exists, apply one fix (limit max_depth for a tree, or adjust the C parameter for logistic regression) and report the new scores. Write two sentences explaining whether the fix helped."
            },
            "quiz": [
                {"question": "What is the clearest sign that a model is overfitting?", "options": ["It runs slowly", "A large gap between training performance and test performance", "It has too few features", "It uses cross-validation"], "correct_index": 1, "explanation": "A big difference between training and test scores signals the model has memorized training data rather than generalized."},
                {"question": "What does regularization do to help fight overfitting?", "options": ["It adds more training data automatically", "It penalizes overly complex models to discourage over-reliance on any single feature", "It deletes the test set", "It increases the number of features"], "correct_index": 1, "explanation": "Regularization adds a penalty term that discourages excessive complexity, helping the model generalize better."},
                {"question": "How does limiting a decision tree's max_depth help with overfitting?", "options": ["It makes the tree deeper and more complex", "It reduces the tree's ability to memorize fine-grained noise in the training data", "It removes the need for a test set", "It increases training accuracy artificially"], "correct_index": 1, "explanation": "A shallower tree is less able to capture noise specific to the training data, reducing overfitting."}
            ],
            "resources": []
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Improving and Applying Models to Real Problems",
            "title": "Working with Categorical Data: Encoding Techniques That Actually Work",
            "learning_objective": "By the end of this class, you will be able to correctly encode categorical columns using one-hot encoding and label encoding.",
            "duration_minutes": 25,
            "content_html": "<p>Machine learning models cannot directly understand text categories like state names or subscription plans, they need numbers. How you convert categories into numbers, called encoding, can significantly affect model performance, and choosing the wrong method is a common beginner mistake.</p><h2>One-Hot Encoding for Unordered Categories</h2><p>For a column like payment_method with values such as card, transfer, and cash, there is no natural order between them. One-hot encoding creates a separate 0 or 1 column for each category, avoiding the mistake of implying a false order.</p><pre><code>encoded = pd.get_dummies(df[\"payment_method\"], prefix=\"payment\")\ndf = pd.concat([df, encoded], axis=1)</code></pre><h2>Label Encoding for Ordered Categories</h2><p>For a column like education_level with a natural order such as secondary, undergraduate, and postgraduate, label encoding assigns increasing numbers that preserve that order, which one-hot encoding would incorrectly discard.</p><pre><code>from sklearn.preprocessing import LabelEncoder\nle = LabelEncoder()\ndf[\"education_encoded\"] = le.fit_transform(df[\"education_level\"])</code></pre><p>Using label encoding on an unordered column like payment_method would be a mistake, because it would falsely tell the model that transfer is mathematically greater than card, which the algorithm might treat as meaningful. Choosing the right encoding for each column is a small decision with a real effect on model accuracy.</p>",
            "key_concepts": ["one-hot encoding", "label encoding", "categorical variables", "get_dummies", "ordinal data"],
            "practical_exercise": {
                "title": "Encode Categorical Columns Correctly",
                "instructions": "Identify at least two categorical columns in your working dataset, one that has a natural order and one that does not. Apply label encoding to the ordered column and one-hot encoding to the unordered column, and explain in one sentence each why you chose that method."
            },
            "quiz": [
                {"question": "Why is one-hot encoding preferred over label encoding for unordered categories?", "options": ["It uses less memory", "It avoids implying a false numeric order between categories", "It only works for numeric columns", "It is required by every model"], "correct_index": 1, "explanation": "One-hot encoding creates independent binary columns, avoiding a misleading numeric order for categories with no natural ranking."},
                {"question": "When is label encoding an appropriate choice?", "options": ["When the categories have a natural, meaningful order", "When there are more than 1000 categories", "Only for numeric columns", "Never, it should always be avoided"], "correct_index": 0, "explanation": "Label encoding preserves order, making it suitable for ordinal data like education level."},
                {"question": "What does pandas get_dummies() do?", "options": ["Removes categorical columns entirely", "Creates separate binary columns for each category value", "Converts numbers into text", "Fills missing values"], "correct_index": 1, "explanation": "get_dummies() performs one-hot encoding, creating a binary column for each unique category value."}
            ],
            "resources": [
                {"label": "scikit-learn: Preprocessing Categorical Features", "url": "https://scikit-learn.org/stable/modules/preprocessing.html"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Improving and Applying Models to Real Problems",
            "title": "Scaling and Normalizing Features for Distance-Based Models",
            "learning_objective": "By the end of this class, you will be able to explain when feature scaling is necessary and apply standardization to a dataset.",
            "duration_minutes": 25,
            "content_html": "<p>Imagine a dataset with an age column ranging from 18 to 70 and an income column ranging from 50,000 to 5,000,000. Some algorithms would let income dominate every decision simply because its numbers are larger, not because it is actually more important. Feature scaling fixes this imbalance.</p><h2>Which Models Need Scaling</h2><p>Distance-based algorithms like K-Nearest Neighbors, K-Means clustering, and anything using gradient descent optimization (including logistic regression and neural networks) are sensitive to feature scale. Tree-based models like decision trees and random forests, by contrast, split on thresholds per feature independently and generally do not need scaling.</p><h2>Standardization in Practice</h2><pre><code>from sklearn.preprocessing import StandardScaler\n\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)</code></pre><p>StandardScaler transforms each feature to have a mean of 0 and a standard deviation of 1, putting every feature on the same footing. Notice fit_transform() is used on the training data, but only transform() is used on the test data, this is deliberate: the scaler must learn its scaling parameters only from training data, otherwise information from the test set leaks into training, producing an overly optimistic evaluation later.</p>",
            "key_concepts": ["feature scaling", "StandardScaler", "distance-based algorithms", "fit_transform vs transform", "data leakage"],
            "practical_exercise": {
                "title": "Scale Your Features Correctly",
                "instructions": "On your working dataset, identify at least two numeric columns with very different ranges. Apply StandardScaler correctly, using fit_transform on the training set and transform only on the test set, and explain in two sentences why using fit_transform on the test set would be a mistake."
            },
            "quiz": [
                {"question": "Which type of model is generally NOT sensitive to feature scale?", "options": ["K-Nearest Neighbors", "Logistic regression", "Tree-based models like random forests", "K-Means clustering"], "correct_index": 2, "explanation": "Tree-based models split on per-feature thresholds independently, so differing feature scales do not distort their decisions."},
                {"question": "Why should you use fit_transform() only on the training data and transform() on the test data?", "options": ["It saves memory", "Using fit on test data leaks test set information into the scaling, inflating results", "transform() does not work on test data", "There is no real difference"], "correct_index": 1, "explanation": "Fitting the scaler only on training data prevents test set information from leaking into the training process."},
                {"question": "What does StandardScaler do to a feature?", "options": ["Removes the feature entirely", "Transforms it to have a mean of 0 and a standard deviation of 1", "Converts it to a categorical column", "Sorts the values"], "correct_index": 1, "explanation": "StandardScaler standardizes a feature so it has a mean of 0 and a standard deviation of 1."}
            ],
            "resources": [
                {"label": "scikit-learn: Preprocessing Data", "url": "https://scikit-learn.org/stable/modules/preprocessing.html"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Improving and Applying Models to Real Problems",
            "title": "Clustering Customers with K-Means for Market Segmentation",
            "learning_objective": "By the end of this class, you will be able to apply K-Means clustering to group data points and interpret the resulting clusters.",
            "duration_minutes": 30,
            "content_html": "<p>Not every business problem has a labeled answer. Marketing teams often want to know: what natural groups exist among our customers, without knowing in advance what those groups should look like. K-Means clustering is the standard tool for exactly this kind of unsupervised discovery.</p><h2>How K-Means Groups Data</h2><p>K-Means works by picking K cluster centers, assigning every data point to its nearest center, then repeatedly moving each center to the average position of its assigned points until the clusters stabilize. You choose K, the number of clusters, in advance.</p><pre><code>from sklearn.cluster import KMeans\n\nX_scaled = scaler.fit_transform(df[[\"annual_spend\", \"purchase_frequency\"]])\nkmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\ndf[\"segment\"] = kmeans.fit_predict(X_scaled)\nprint(df.groupby(\"segment\")[[\"annual_spend\", \"purchase_frequency\"]].mean())</code></pre><h2>Choosing K With the Elbow Method</h2><p>Picking the right number of clusters is not always obvious. The elbow method runs K-Means for a range of K values and plots the resulting error, looking for the point where adding more clusters stops meaningfully reducing error, which looks like an elbow bend on the chart. Once you have your clusters, the real work is interpretation: naming segment 0 high-spend frequent buyers and segment 2 low-spend occasional shoppers based on their average behavior is what turns a mathematical output into a business insight a marketing team can act on.</p>",
            "key_concepts": ["K-Means", "clustering", "elbow method", "customer segmentation", "n_clusters"],
            "practical_exercise": {
                "title": "Segment Customers with K-Means",
                "instructions": "On your working dataset (or a retail or customer dataset if yours does not fit), select two or three numeric columns, scale them, and run K-Means with 3 or 4 clusters. Print the average feature values per cluster and write a one-sentence descriptive name for each cluster based on its behavior pattern."
            },
            "quiz": [
                {"question": "What is the main goal of K-Means clustering?", "options": ["To predict a labeled target using historical answers", "To group similar data points together without predefined labels", "To calculate precision and recall", "To scale features to a fixed range"], "correct_index": 1, "explanation": "K-Means is an unsupervised algorithm that groups data points based on similarity, without using labeled answers."},
                {"question": "What is the purpose of the elbow method in K-Means?", "options": ["To clean missing data", "To help choose a reasonable number of clusters, K", "To encode categorical variables", "To split data into train and test sets"], "correct_index": 1, "explanation": "The elbow method plots error against different K values to help identify a reasonable number of clusters."},
                {"question": "After running K-Means, why is interpreting each cluster's average behavior important?", "options": ["It is not important, the cluster numbers are enough on their own", "It turns a mathematical grouping into an actionable business insight", "It is required to run the algorithm", "It replaces the need for scaling"], "correct_index": 1, "explanation": "Giving clusters meaningful descriptions based on their characteristics is what makes the output useful to a business team."}
            ],
            "resources": [
                {"label": "scikit-learn: Clustering", "url": "https://scikit-learn.org/stable/modules/clustering.html"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Improving and Applying Models to Real Problems",
            "title": "Mini-Project: Predicting Customer Churn with a Real Telecom Dataset",
            "learning_objective": "By the end of this class, you will be able to independently combine data cleaning, feature engineering, model training, and evaluation into one complete churn prediction workflow.",
            "duration_minutes": 40,
            "content_html": "<p>Today you bring together everything from the first three weeks into one complete, realistic project: predicting which telecom customers are likely to churn, one of the single most common real machine learning tasks assigned to junior data scientists across Nigerian and global telecom and fintech companies.</p><h2>The Full Workflow, End to End</h2><p>A complete workflow follows a consistent sequence: load and explore the data, clean missing values and duplicates, engineer useful features like tenure buckets or spend ratios, encode categorical columns, split into train and test sets, train at least one model, and evaluate it with the right metrics for the business problem.</p><pre><code>from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import classification_report\n\n# Assume df is cleaned, encoded, and features/target selected\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n\nmodel = RandomForestClassifier(n_estimators=200, random_state=42)\nmodel.fit(X_train, y_train)\nprint(classification_report(y_test, model.predict(X_test)))</code></pre><h2>Why This Exact Project Matters for Your Career</h2><p>Notice the stratify=y parameter above, it ensures your train and test splits keep the same churn proportion as the full dataset, which matters because churn datasets are usually imbalanced. This mini-project is deliberately close to your final capstone, giving you a full practice run at the entire pipeline before you tackle it independently in week six, on a dataset and problem of your own choosing.</p>",
            "key_concepts": ["end-to-end pipeline", "churn prediction", "stratified split", "classification report", "workflow integration"],
            "practical_exercise": {
                "title": "Complete a Full Churn Prediction Pipeline",
                "instructions": "Using a telecom churn dataset from Kaggle (search for telco customer churn), complete the full pipeline: clean the data, engineer at least one new feature, encode categorical columns, split the data with stratification, train a classification model, and print a full classification report. Submit the complete notebook as one continuous, runnable workflow."
            },
            "quiz": [
                {"question": "What does the stratify=y parameter do in train_test_split?", "options": ["It removes the target column", "It keeps the same class proportions in both train and test sets", "It scales all features automatically", "It selects only numeric columns"], "correct_index": 1, "explanation": "Stratifying by the target ensures both splits maintain the same proportion of each class, important for imbalanced data."},
                {"question": "Why is churn prediction such a common entry-level task at telecom and fintech companies?", "options": ["It requires no data at all", "Retaining existing customers is usually cheaper than acquiring new ones, making churn prediction high business value", "It cannot be solved with machine learning", "It only applies to companies outside Africa"], "correct_index": 1, "explanation": "Churn prediction directly supports customer retention strategy, which is typically far cheaper than acquiring new customers."},
                {"question": "What is the correct order of steps in a complete supervised learning workflow?", "options": ["Train model, then clean data, then explore data", "Explore and clean data, engineer features, split data, train model, evaluate", "Evaluate the model before training it", "Skip cleaning and go straight to evaluation"], "correct_index": 1, "explanation": "A sound workflow explores and cleans data first, then engineers features, splits the data, trains, and finally evaluates."}
            ],
            "resources": [
                {"label": "Kaggle: Telco Customer Churn", "url": "https://www.kaggle.com/datasets"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Advanced Techniques and Model Trust",
            "title": "Gradient Boosting with XGBoost for Competition-Grade Accuracy",
            "learning_objective": "By the end of this class, you will be able to train a gradient boosting model with XGBoost and explain why it often outperforms a random forest.",
            "duration_minutes": 35,
            "content_html": "<p>If you look at the winning solutions in almost any Kaggle competition involving tabular business data, gradient boosting libraries like XGBoost or LightGBM appear constantly. These are the algorithms professional data science teams reach for when accuracy on structured data really matters.</p><h2>How Boosting Differs from a Random Forest</h2><p>A random forest builds many trees independently and averages them. Gradient boosting instead builds trees one at a time, where each new tree is trained specifically to correct the mistakes of the trees built before it. This sequential error-correction is what typically gives boosting an edge in accuracy over a random forest on structured, tabular data.</p><pre><code>from xgboost import XGBClassifier\n\nxgb_model = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4, random_state=42)\nxgb_model.fit(X_train, y_train)\npredictions = xgb_model.predict(X_test)\nprint(classification_report(y_test, predictions))</code></pre><h2>Key Parameters to Know</h2><p>learning_rate controls how much each new tree is allowed to correct previous mistakes, smaller values are usually more accurate but need more trees (n_estimators) to compensate. max_depth controls how complex each individual tree is allowed to be, and keeping it relatively shallow, often between 3 and 6, tends to reduce overfitting in boosted models. Being able to say in an interview that you have used XGBoost and understand these three parameters immediately signals real, practical experience beyond textbook linear regression.</p>",
            "key_concepts": ["gradient boosting", "XGBoost", "learning_rate", "sequential error correction", "n_estimators"],
            "practical_exercise": {
                "title": "Train and Compare a Boosted Model",
                "instructions": "Install xgboost (pip install xgboost) and train an XGBClassifier or XGBRegressor on your working dataset. Compare its test set performance directly against your earlier random forest result on the same data, and write two sentences on which performed better and by how much."
            },
            "quiz": [
                {"question": "How does gradient boosting differ from a random forest in how it builds trees?", "options": ["Boosting builds all trees at exactly the same time", "Boosting builds trees sequentially, each correcting the errors of the previous ones", "Random forests build only one tree total", "There is no structural difference"], "correct_index": 1, "explanation": "Gradient boosting builds trees one after another, with each new tree focused on correcting the errors of prior trees."},
                {"question": "What does the learning_rate parameter control in XGBoost?", "options": ["The number of rows in the dataset", "How much each new tree is allowed to correct previous mistakes", "The programming language used", "The test set size"], "correct_index": 1, "explanation": "learning_rate scales the contribution of each new tree, controlling how aggressively the model corrects prior errors."},
                {"question": "Why is max_depth often kept relatively shallow in gradient boosting models?", "options": ["To make training take longer", "To reduce overfitting since trees are already combined sequentially", "Because scikit-learn requires it", "Because shallow trees cannot make any predictions"], "correct_index": 1, "explanation": "Shallow individual trees combined with many boosting rounds tend to generalize better and overfit less."}
            ],
            "resources": [
                {"label": "XGBoost Documentation", "url": "https://xgboost.readthedocs.io/"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Advanced Techniques and Model Trust",
            "title": "Handling Imbalanced Datasets: Fraud, Churn, and Rare-Event Prediction",
            "learning_objective": "By the end of this class, you will be able to identify class imbalance in a dataset and apply at least one technique to address it.",
            "duration_minutes": 30,
            "content_html": "<p>Fraud, disease, and equipment failure all share something in common: the event you actually care about predicting is rare, often less than 5 percent of all cases. A model trained naively on this kind of imbalanced data tends to simply ignore the rare class, which is exactly the class that matters most.</p><h2>Why Imbalance Breaks Naive Models</h2><p>If only 2 percent of transactions are fraudulent, a model can achieve 98 percent accuracy by predicting not fraud every single time, while being completely useless. This is why the metrics from Day 15, precision and recall, matter so much more than accuracy on imbalanced problems.</p><h2>Techniques to Address Imbalance</h2><p>Class weighting tells the model to treat mistakes on the rare class as more costly during training, which is often the simplest fix.</p><pre><code>from sklearn.ensemble import RandomForestClassifier\n\nmodel = RandomForestClassifier(n_estimators=200, class_weight=\"balanced\", random_state=42)\nmodel.fit(X_train, y_train)</code></pre><p>Resampling techniques are another option: oversampling duplicates or synthesizes more examples of the rare class (a popular method is called SMOTE), while undersampling removes some examples of the common class. Each technique has trade-offs, oversampling can lead to overfitting on duplicated patterns, undersampling throws away potentially useful data, so testing more than one approach and comparing recall and precision on the rare class is the professional way to decide which works best for your specific dataset.</p>",
            "key_concepts": ["class imbalance", "class_weight", "oversampling", "undersampling", "SMOTE"],
            "practical_exercise": {
                "title": "Address Imbalance in Your Dataset",
                "instructions": "Check the class balance of your target column using value_counts(). If it is imbalanced (one class under 30 percent), retrain your classifier using class_weight=\"balanced\" and compare the precision and recall for the minority class before and after. If your dataset is already balanced, find and use a public fraud or disease dataset instead."
            },
            "quiz": [
                {"question": "Why can a model achieve high accuracy on an imbalanced dataset while still being useless?", "options": ["Accuracy cannot be computed on imbalanced data", "It can simply predict the majority class every time and still score high", "Imbalanced datasets always have missing values", "High accuracy is impossible on imbalanced data"], "correct_index": 1, "explanation": "On imbalanced data, always predicting the majority class yields high accuracy without correctly identifying the rare, important class."},
                {"question": "What does setting class_weight=\"balanced\" do in scikit-learn?", "options": ["It deletes the minority class", "It makes mistakes on the minority class more costly during training", "It scales all features to the same range", "It removes the need for a test set"], "correct_index": 1, "explanation": "class_weight=\"balanced\" adjusts the training process to penalize misclassifying the minority class more heavily."},
                {"question": "What is a downside of oversampling the minority class?", "options": ["It always reduces the dataset size", "It can lead to overfitting on duplicated or synthesized patterns", "It is not possible in Python", "It only works on numeric targets"], "correct_index": 1, "explanation": "Oversampling can cause a model to overfit on repeated or artificially generated minority class patterns."}
            ],
            "resources": [
                {"label": "scikit-learn: Imbalanced Data Strategies", "url": "https://scikit-learn.org/stable/modules/ensemble.html"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Advanced Techniques and Model Trust",
            "title": "Explainable AI: Using SHAP to Show Why Your Model Made a Decision",
            "learning_objective": "By the end of this class, you will be able to generate and interpret a SHAP explanation for individual predictions from a trained model.",
            "duration_minutes": 35,
            "content_html": "<p>A model that predicts a loan applicant will default is not enough for most real businesses, because regulators, managers, and customers all ask the same question: why. Explainable AI techniques answer that question, and SHAP is the industry-standard tool for doing it.</p><h2>What SHAP Actually Measures</h2><p>SHAP, short for SHapley Additive exPlanations, calculates how much each feature pushed a specific prediction higher or lower compared to the average prediction, based on ideas borrowed from game theory about fairly splitting credit among contributors.</p><pre><code>import shap\n\nexplainer = shap.TreeExplainer(model)\nshap_values = explainer.shap_values(X_test)\n\nshap.summary_plot(shap_values, X_test)</code></pre><h2>Reading a SHAP Explanation</h2><p>A summary plot ranks features by their overall impact across all predictions, showing not just that tenure matters, but whether low tenure pushes predictions toward churn or away from it. For a single customer, a SHAP force plot can show exactly which features (low tenure, high monthly charges) pushed their individual churn probability up, information a customer retention team can act on directly. This is precisely the kind of output banking regulators in Nigeria and elsewhere increasingly require before approving an automated credit decision system, making explainability a genuinely valuable, employable skill rather than an academic nice-to-have.</p>",
            "key_concepts": ["explainable AI", "SHAP", "feature attribution", "summary plot", "model transparency"],
            "practical_exercise": {
                "title": "Explain Your Model's Predictions",
                "instructions": "Install shap (pip install shap) and generate a SHAP summary plot for a tree-based model you trained earlier in this track. Identify the top three most influential features shown in the plot, and write three sentences explaining what the plot reveals about how those features affect the prediction."
            },
            "quiz": [
                {"question": "What does SHAP fundamentally measure for a prediction?", "options": ["The total training time of the model", "How much each feature pushed a specific prediction higher or lower than average", "The number of missing values in the dataset", "The accuracy of the model on the test set"], "correct_index": 1, "explanation": "SHAP attributes a contribution value to each feature, showing how it influenced an individual prediction relative to the average."},
                {"question": "Why would a bank want SHAP explanations for an automated credit decision model?", "options": ["To make the model train faster", "Regulators and stakeholders often require transparency into why a decision was made", "To remove the need for a test set", "SHAP is required to load the data"], "correct_index": 1, "explanation": "Regulatory and business requirements often demand explainability for high-stakes automated decisions like credit approval."},
                {"question": "What does a SHAP summary plot show across the whole dataset?", "options": ["The raw source code of the model", "Which features have the greatest overall impact on predictions and in what direction", "Only the model's final accuracy score", "The number of rows removed during cleaning"], "correct_index": 1, "explanation": "A summary plot ranks features by importance and shows how their values relate to pushing predictions up or down."}
            ],
            "resources": [
                {"label": "SHAP Documentation", "url": "https://shap.readthedocs.io/"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Advanced Techniques and Model Trust",
            "title": "Deploying a Trained Model as a Simple API with Flask",
            "learning_objective": "By the end of this class, you will be able to save a trained model and serve it through a simple Flask API endpoint that returns predictions.",
            "duration_minutes": 35,
            "content_html": "<p>A model sitting inside a Jupyter Notebook creates zero business value on its own, it needs to be reachable by an application, a website, or another system. Today you take the final step of turning your trained model into something other software can actually call.</p><h2>Saving Your Trained Model</h2><p>Rather than retraining a model every time you need a prediction, you save the trained model object to disk using joblib, then load it instantly whenever needed.</p><pre><code>import joblib\njoblib.dump(model, \"churn_model.joblib\")\nloaded_model = joblib.load(\"churn_model.joblib\")</code></pre><h2>Serving Predictions Through an API</h2><p>Flask is a lightweight Python web framework that is commonly used to wrap a model in a simple API endpoint that other applications can send data to and receive a prediction back from.</p><pre><code>from flask import Flask, request, jsonify\nimport joblib\n\napp = Flask(__name__)\nmodel = joblib.load(\"churn_model.joblib\")\n\n@app.route(\"/predict\", methods=[\"POST\"])\ndef predict():\n    data = request.get_json()\n    features = [[data[\"tenure_months\"], data[\"monthly_charges\"]]]\n    prediction = model.predict(features)\n    return jsonify({\"churn_prediction\": int(prediction[0])})\n\nif __name__ == \"__main__\":\n    app.run(debug=True)</code></pre><p>Running this file and sending a POST request with customer data to the /predict route returns a live prediction, exactly the same pattern used in production systems, just at a smaller scale. This single skill, wrapping a model behind an API, is often what separates a data science exercise from something an engineering team can actually integrate into a product.</p>",
            "key_concepts": ["model serialization", "joblib", "Flask API", "REST endpoint", "model deployment"],
            "practical_exercise": {
                "title": "Serve Your Model Through an API",
                "instructions": "Save one of your trained models using joblib, then build a minimal Flask app with a /predict endpoint that accepts input features as JSON and returns a prediction. Test it locally by sending a sample request (using a tool like Postman, curl, or Python requests) and include a screenshot of the returned prediction."
            },
            "quiz": [
                {"question": "Why is saving a trained model with joblib useful?", "options": ["It automatically improves model accuracy", "It lets you reuse the trained model without retraining it every time", "It converts the model into a different algorithm", "It removes the need for a test set"], "correct_index": 1, "explanation": "joblib serializes a trained model to disk so it can be loaded and reused instantly without retraining."},
                {"question": "What is the purpose of the Flask /predict route in the example?", "options": ["To clean the training data", "To accept input data and return a live model prediction", "To visualize the dataset", "To calculate SHAP values"], "correct_index": 1, "explanation": "The /predict route receives input data via a request and returns the model's prediction as a response."},
                {"question": "Why does wrapping a model in an API matter for real business use?", "options": ["It is purely decorative and has no practical use", "It lets other applications and systems call the model to get predictions", "It removes the need to train the model at all", "It automatically fixes data imbalance"], "correct_index": 1, "explanation": "An API makes the model accessible to other software, turning a notebook exercise into an integrable product component."}
            ],
            "resources": [
                {"label": "Flask Documentation", "url": "https://flask.palletsprojects.com/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Advanced Techniques and Model Trust",
            "title": "Tracking Experiments and Versioning Models Like a Professional",
            "learning_objective": "By the end of this class, you will be able to systematically log model experiments, including parameters and results, to compare them over time.",
            "duration_minutes": 25,
            "content_html": "<p>Real projects rarely involve training just one model. You will try different algorithms, features, and settings dozens of times, and without a system for tracking what you tried and what results it produced, you will lose track of which version actually performed best, a common and costly mistake on real teams.</p><h2>Why Ad-Hoc Tracking Fails</h2><p>Scrolling back through old notebook cells trying to remember which combination of parameters produced your best F1 score does not scale, especially once you are collaborating with other data scientists who need to see your results too.</p><h2>A Simple Logging Approach</h2><p>Even without specialized tools, a disciplined analyst can keep a structured experiment log as a simple table:</p><pre><code>import pandas as pd\n\nlog = pd.DataFrame([\n    {\"experiment\": \"rf_baseline\", \"model\": \"RandomForest\", \"n_estimators\": 100, \"f1\": 0.71},\n    {\"experiment\": \"rf_tuned\", \"model\": \"RandomForest\", \"n_estimators\": 300, \"f1\": 0.76},\n    {\"experiment\": \"xgb_v1\", \"model\": \"XGBoost\", \"learning_rate\": 0.05, \"f1\": 0.81},\n])\nlog.to_csv(\"experiment_log.csv\", index=False)</code></pre><p>For more serious production work, dedicated tools like MLflow automate this logging, recording parameters, metrics, and even the model file itself for every run automatically. Whichever approach you use, the professional habit is the same: never trust your memory to track which experiment actually produced your best result, write it down every single time.</p>",
            "key_concepts": ["experiment tracking", "reproducibility", "MLflow", "model versioning", "hyperparameters"],
            "practical_exercise": {
                "title": "Log Three Model Experiments",
                "instructions": "Train at least three different model variations on your working dataset (different algorithms or different parameter settings), and build a structured experiment log as a DataFrame or CSV recording the settings and the resulting metric for each. Submit the log file along with a one-sentence conclusion on which experiment performed best."
            },
            "quiz": [
                {"question": "Why is relying on memory to track which experiment performed best a risky habit?", "options": ["Memory is always perfectly accurate", "It does not scale once you run many experiments or collaborate with others", "Experiments never need to be compared", "Python automatically remembers all past runs"], "correct_index": 1, "explanation": "Without structured logging, it becomes nearly impossible to reliably track and compare many experiments over time."},
                {"question": "What kind of information belongs in a good experiment log?", "options": ["Only the final model file name", "The model type, key parameters, and the resulting performance metric", "Only the dataset file size", "The programmer's personal notes unrelated to results"], "correct_index": 1, "explanation": "A useful experiment log records enough detail, model, parameters, and metrics, to compare runs meaningfully later."},
                {"question": "What does a tool like MLflow automate compared to a manual CSV log?", "options": ["It automatically increases model accuracy", "It automatically records parameters, metrics, and model files for each run", "It replaces the need for a test set", "It writes the final report for you"], "correct_index": 1, "explanation": "MLflow and similar tools automatically capture experiment details, reducing the manual effort of tracking runs."}
            ],
            "resources": [
                {"label": "MLflow Documentation", "url": "https://mlflow.org/docs/latest/index.html"}
            ]
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career Readiness and the Capstone Project",
            "title": "Writing a Model Card and Results Report Employers Can Trust",
            "learning_objective": "By the end of this class, you will be able to write a structured model card documenting a machine learning model's purpose, data, performance, and limitations.",
            "duration_minutes": 30,
            "content_html": "<p>A model without documentation is a liability, not an asset. Anyone reviewing your work, whether a hiring manager, a client, or a teammate, needs to quickly understand what the model does, how well it performs, and where it might fail. This is exactly what your final capstone will require of you.</p><h2>The Core Sections of a Model Card</h2><p>A professional model card typically covers: the problem statement (what business question does this solve), the data used (source, size, and any known biases), the modeling approach (which algorithms were tried and why the final one was chosen), performance metrics (with the specific numbers and why those metrics were chosen), and limitations (where the model is likely to be wrong or should not be trusted).</p><h2>Writing for a Non-Technical Reader</h2><p>The best model cards translate technical results into plain language a manager can act on. Instead of writing that the model achieved an F1 score of 0.81, write that the model correctly identifies 8 out of 10 customers who are about to churn, while occasionally flagging a loyal customer for review. Always state limitations honestly: if your model was trained mostly on data from one region or one customer segment, say so, because a model that silently underperforms on the group you did not test well is far more dangerous than one whose weaknesses are clearly documented.</p>",
            "key_concepts": ["model card", "documentation", "limitations disclosure", "plain-language reporting", "stakeholder communication"],
            "practical_exercise": {
                "title": "Draft a Model Card for a Past Model",
                "instructions": "Choose one model you built earlier in this track and write a one-page model card covering the problem statement, data used, modeling approach, performance metrics explained in plain language, and at least two honest limitations. Submit this as a text document, you will reuse this structure for your final capstone."
            },
            "quiz": [
                {"question": "Why should a model card include limitations, not just strong results?", "options": ["Limitations are not actually important", "A model that silently underperforms on untested groups is more dangerous than one with documented weaknesses", "Limitations make the report shorter", "Only the accuracy score matters in a model card"], "correct_index": 1, "explanation": "Honestly documenting limitations helps users avoid trusting the model in situations where it is likely to fail."},
                {"question": "What is the benefit of translating a metric like F1 score into plain language for a report?", "options": ["It removes the need to calculate the metric at all", "It helps non-technical stakeholders understand and act on the result", "It makes the metric more accurate", "Plain language is required by scikit-learn"], "correct_index": 1, "explanation": "Translating technical metrics into concrete, understandable language helps decision-makers act on the findings."},
                {"question": "Which of these belongs in the data section of a model card?", "options": ["The exact Python version installed", "The data source, size, and any known biases", "The developer's personal email address", "The company's marketing slogan"], "correct_index": 1, "explanation": "The data section should describe where the data came from, how much there is, and any known limitations or biases."}
            ],
            "resources": [
                {"label": "Google Model Cards Guide", "url": "https://modelcards.withgoogle.com/about"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career Readiness and the Capstone Project",
            "title": "What Machine Learning Interviews Actually Test and How to Prepare",
            "learning_objective": "By the end of this class, you will be able to describe the typical stages of a machine learning interview and practice answering one common technical question.",
            "duration_minutes": 25,
            "content_html": "<p>Machine learning interviews, whether for a full-time role, an internship, or a freelance contract, tend to follow a fairly predictable structure across Nigerian and global companies alike. Knowing what is coming lets you prepare deliberately instead of guessing.</p><h2>The Typical Stages</h2><p>Most processes include a screening conversation about your background and past projects, a technical round covering core concepts (often including the exact topics from this track: overfitting, evaluation metrics, and handling imbalanced data), sometimes a take-home task where you are given a dataset and asked to build a model within a few days, and a final conversation about how you would approach an open-ended business problem.</p><h2>A Common Interview Question, Answered</h2><p>A frequently asked question is how you would handle a dataset where only 2 percent of the records belong to the class you are trying to predict. A strong answer references specific techniques from this track: check whether accuracy is misleading, prioritize precision and recall over raw accuracy, consider class weighting or resampling like SMOTE, and choose an evaluation metric that reflects the real business cost of missing a rare case versus raising a false alarm. Notice that a strong answer is specific and technical, not vague, this is exactly why building real projects, not just watching tutorials, is what prepares you to answer confidently.</p>",
            "key_concepts": ["technical interviews", "take-home assessment", "imbalanced data question", "interview preparation", "portfolio projects"],
            "practical_exercise": {
                "title": "Write Your Own Answer to a Common Question",
                "instructions": "Write a full, structured answer, in your own words, to the question: how would you handle a dataset where only 2 percent of records belong to the class you are predicting. Reference at least three specific techniques from this track by name, and practice saying your answer out loud in under 90 seconds."
            },
            "quiz": [
                {"question": "What does a take-home assessment in a machine learning interview process typically involve?", "options": ["A general knowledge quiz unrelated to data", "Being given a dataset and asked to build a model within a set timeframe", "A typing speed test", "Only a phone call with no technical content"], "correct_index": 1, "explanation": "Take-home assessments typically test practical skills by having candidates build a model on a provided dataset."},
                {"question": "What makes an answer about handling imbalanced data strong in an interview?", "options": ["Being vague and avoiding technical terms", "Referencing specific techniques like class weighting, resampling, and appropriate metrics", "Only mentioning that accuracy is a good metric", "Refusing to answer the question"], "correct_index": 1, "explanation": "Specific, technically grounded answers that name real techniques demonstrate genuine hands-on experience."},
                {"question": "Why does building real projects prepare you better for interviews than only watching tutorials?", "options": ["Projects are not related to interview questions", "Hands-on project experience gives you specific, concrete examples and techniques to reference confidently", "Tutorials always cover more advanced material", "Interviewers never ask about projects"], "correct_index": 1, "explanation": "Real project experience gives you specific details and confidence that generic tutorial-watching does not provide."}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career Readiness and the Capstone Project",
            "title": "Building an ML Portfolio on GitHub and Kaggle That Gets You Hired",
            "learning_objective": "By the end of this class, you will be able to set up a GitHub repository and a Kaggle profile structured to showcase your machine learning work professionally.",
            "duration_minutes": 25,
            "content_html": "<p>Hiring managers and clients almost always check a candidate's GitHub or Kaggle profile before an interview, and a messy, empty, or unexplained profile can quietly disqualify you before you even get a chance to speak. Today you build the professional shell that will hold your capstone project and future work.</p><h2>Structuring a GitHub Repository</h2><p>Every project repository should include a clear README file explaining what the project does, what dataset was used, what techniques were applied, and what the results were, ideally with a chart or two visible directly in the README. Organize your code into clearly named files rather than one giant messy notebook, and never commit large raw data files directly, link to the dataset source instead.</p><h2>Using Kaggle to Build Credibility</h2><p>Publishing a notebook on Kaggle, even a smaller practice project, on a public dataset gives you a second, independently verifiable place where your work is visible, and participating in even one beginner competition demonstrates initiative that a plain portfolio project does not. Both platforms serve the same purpose: turning your 30 days of learning into evidence a stranger can verify in five minutes, which is exactly how most technical hiring decisions in this field actually get made.</p>",
            "key_concepts": ["GitHub portfolio", "README documentation", "Kaggle notebooks", "project presentation", "employer verification"],
            "practical_exercise": {
                "title": "Set Up Your Portfolio Home",
                "instructions": "Create a GitHub repository for your machine learning work from this track (or clean up an existing one) with a clear README describing at least one project, the dataset used, and the results. If you do not already have one, create a free Kaggle account and publish one notebook from an earlier exercise in this track."
            },
            "quiz": [
                {"question": "Why is a clear README important in a machine learning GitHub repository?", "options": ["GitHub requires it to allow uploads", "It helps a reviewer quickly understand the project, data, and results without reading all the code", "It replaces the need for actual code", "It is only useful for very large companies"], "correct_index": 1, "explanation": "A good README lets a reviewer, like a hiring manager, quickly understand your project without digging through code."},
                {"question": "What should you generally do instead of committing large raw data files to GitHub?", "options": ["Delete the project entirely", "Link to the original dataset source instead", "Compress it into a single massive file", "Email it to recruiters directly"], "correct_index": 1, "explanation": "Linking to the dataset source keeps the repository lean and avoids storage and licensing issues with large raw files."},
                {"question": "What advantage does publishing on Kaggle provide beyond a personal GitHub repository?", "options": ["It guarantees a job offer", "It provides an independently verifiable public record of your work", "It removes the need for a README", "It automatically trains your models for you"], "correct_index": 1, "explanation": "Kaggle offers a public, independently checkable platform where employers can see your work and activity directly."}
            ],
            "resources": [
                {"label": "GitHub Docs: About READMEs", "url": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"},
                {"label": "Kaggle Learn", "url": "https://www.kaggle.com/learn"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career Readiness and the Capstone Project",
            "title": "Ethics, Bias, and Data Privacy in African AI Deployments",
            "learning_objective": "By the end of this class, you will be able to identify at least two sources of bias in a dataset and describe how to responsibly handle personal data in a model.",
            "duration_minutes": 25,
            "content_html": "<p>A model that discriminates unfairly against a group of people, or that leaks private information, does not just cause harm, it also creates legal and reputational risk for the company that deployed it. Understanding these risks is part of being a trustworthy practitioner, not an optional extra topic.</p><h2>Where Bias Enters a Model</h2><p>Bias often comes from the training data itself. If a historical loan dataset reflects past unfair lending practices against a particular region or group, a model trained on it will learn and repeat that same unfairness, even without anyone intending it to. Sample bias, where your dataset overrepresents one group (for example, mostly urban customers in a country where most people are rural), produces a model that performs poorly for underrepresented groups.</p><h2>Handling Personal Data Responsibly</h2><p>When working with real customer data, sensitive fields like national ID numbers, phone numbers, and exact addresses should be removed or anonymized before analysis whenever possible, and access to raw personal data should be limited to what is strictly necessary for the task. Nigeria's Data Protection Act and similar regulations across Africa increasingly require this kind of careful handling by law, not just as good practice. Before deploying any model that affects real people's access to credit, jobs, or services, a responsible practitioner checks: does this model perform similarly well across different demographic groups, and can I explain, using tools like SHAP from Day 23, why it made a given decision.</p>",
            "key_concepts": ["algorithmic bias", "sample bias", "data privacy", "anonymization", "responsible AI"],
            "practical_exercise": {
                "title": "Audit a Model for Bias Risk",
                "instructions": "Choose one dataset you used earlier in this track. Identify one demographic or group-related column (or explain why none exists), and write a short analysis of whether the dataset might overrepresent or underrepresent any group. Propose one concrete step you would take before deploying a model trained on this data."
            },
            "quiz": [
                {"question": "How can historical training data cause a model to become biased?", "options": ["Training data cannot influence model behavior", "If the data reflects past unfair patterns, the model can learn and repeat that unfairness", "Bias only comes from the choice of algorithm, never the data", "Bias is impossible in machine learning"], "correct_index": 1, "explanation": "Models learn patterns present in their training data, including any historical unfairness embedded in that data."},
                {"question": "What is sample bias?", "options": ["A bug in the scikit-learn library", "When a dataset overrepresents one group relative to the real population", "A type of missing value", "A metric like precision or recall"], "correct_index": 1, "explanation": "Sample bias occurs when certain groups are overrepresented or underrepresented in the collected data compared to reality."},
                {"question": "Before deploying a model affecting access to credit or services, what should a responsible practitioner check?", "options": ["Only the overall accuracy score", "Whether the model performs similarly across demographic groups and can be explained", "Whether the code compiles without errors", "Whether the dataset file is under 1 megabyte"], "correct_index": 1, "explanation": "Checking for consistent performance across groups and ensuring explainability are key responsible AI practices before deployment."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career Readiness and the Capstone Project",
            "title": "Kicking Off Your Capstone: Building and Evaluating a Real ML Model",
            "learning_objective": "By the end of this class, you will be able to select your capstone dataset and produce a complete project plan for building and evaluating a real machine learning model.",
            "duration_minutes": 35,
            "content_html": "<p>Today you begin your final project: choosing a real public dataset that represents a genuine problem, such as predicting customer churn, loan default, disease risk, or house prices, and using it to train, compare, and evaluate at least two different models before writing a full model report. This is the project that goes at the top of your portfolio.</p><h2>How to Approach the Capstone</h2><p>Start by selecting a dataset using the criteria from Day 5: a real, clear target, at least a few hundred rows, and a problem you can explain in one sentence. Follow the exact pipeline you practiced on Day 20: explore, clean, engineer features, encode, split, train, evaluate, and this time, add explainability with SHAP from Day 23 and honest documentation using the model card structure from Day 26.</p><h2>What Your Final Deliverable Must Include</h2><ul><li>A cleaned dataset with documented, justified decisions about missing values and outliers</li><li>At least two trained and compared models with a clear reason for the final choice</li><li>Evaluation using metrics appropriate to the problem, not just accuracy</li><li>A SHAP or feature-importance explanation of what drives the predictions</li><li>A written model results report (model card) covering the problem, data, approach, metrics, and limitations</li></ul><p>Treat this exactly like your first real assignment on a data science job, because that is precisely what it is designed to simulate, and it is the single strongest piece of evidence you will have when applying for roles or freelance contracts after this track.</p>",
            "key_concepts": ["capstone planning", "dataset selection", "model comparison", "final report", "portfolio project"],
            "practical_exercise": {
                "title": "Start Your Final Capstone Project",
                "instructions": "This exercise is the start of your final project. Select your capstone dataset today, write a one-paragraph problem statement describing what you will predict and why it matters, and complete the exploration and cleaning steps on it. Submit your dataset choice, problem statement, and initial exploratory analysis as the first deliverable toward your final model results report."
            },
            "quiz": [
                {"question": "What is the first concrete step in starting the capstone project today?", "options": ["Immediately writing the final report before touching any data", "Selecting a real dataset with a clear target and writing a problem statement", "Deploying a model to a live server", "Skipping data cleaning entirely"], "correct_index": 1, "explanation": "The capstone begins with selecting a suitable dataset and clearly stating the problem before any modeling work."},
                {"question": "Which technique from earlier in this track should be included to explain the capstone model's predictions?", "options": ["K-Means clustering", "SHAP explainability", "One-hot encoding only", "The elbow method"], "correct_index": 1, "explanation": "SHAP, covered on Day 23, is the explainability technique the capstone should use to show what drives predictions."},
                {"question": "What should the final written deliverable of the capstone be structured as?", "options": ["A single line of code with no explanation", "A model results report, or model card, covering problem, data, approach, metrics, and limitations", "A list of every line of raw data", "A video with no written component required"], "correct_index": 1, "explanation": "The capstone concludes with a structured model card style report, exactly as practiced on Day 26."}
            ],
            "resources": [
                {"label": "Kaggle Datasets", "url": "https://www.kaggle.com/datasets"}
            ]
        }
    ]
}
