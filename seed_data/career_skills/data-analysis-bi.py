"""Seed data for the Data Analysis & Business Intelligence 30-Day Skill Class."""

SKILL = {
    "slug": "data-analysis-bi",
    "name": "Data Analysis & Business Intelligence",
    "tagline": "Turn messy spreadsheets and raw numbers into the insights and dashboards that get decisions made.",
    "description": "Data analysis and business intelligence is the skill of taking raw, messy data and turning it into insights a business can act on, using tools like Excel, SQL, Power BI, and Python. For a Nigerian student, this is one of the fastest paths into a paid role because nearly every company, bank, telecom, NGO, and startup, needs someone who can clean data and build a dashboard, and the skill transfers directly into finance, marketing, operations, and consulting roles. This track takes you from basic spreadsheet literacy to analyzing a real dataset end-to-end and presenting insights the way a working analyst does.",
    "level": "beginner",
    "estimated_hours": 58,
    "course_title": "30-Day Data Analysis & Business Intelligence Career Track",
    "course_description": "After 30 days you will be able to clean and explore real datasets, write SQL queries to answer business questions, build interactive dashboards in Power BI or Excel, apply core statistics correctly, and present data-driven insights the way a working analyst does.",
    "final_project": {
        "title": "Analyze a Real Dataset and Deliver an Executive Insights Dashboard",
        "description": "Analyze a real-world dataset end-to-end, such as Nigerian e-commerce sales, telecom customer churn, public health statistics, or a local business's transaction records, and produce an executive dashboard/report that a non-technical manager could act on. The project must include a documented data-cleaning process, exploratory analysis that identifies at least three meaningful trends or patterns, a polished interactive dashboard (built in Excel, Power BI, or Python) with clear visualizations, and a one-page written summary of actionable recommendations tied directly to the data. Choose your own tool stack established across the 30 days (Excel, SQL, Power BI, and/or Python), but the final deliverable must look and read like something a real company would pay for, not a classroom exercise. This is exactly the kind of portfolio piece that gets a candidate shortlisted for junior data analyst or BI analyst roles.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["data cleaning", "exploratory data analysis", "SQL querying", "dashboard design", "data visualization", "statistical reasoning", "business storytelling"],
        "rubric": [
            {"name": "Data cleaning and preparation quality", "max_points": 25},
            {"name": "Depth and accuracy of analysis", "max_points": 30},
            {"name": "Dashboard design and visualization clarity", "max_points": 25},
            {"name": "Actionable insights and executive summary", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Thinking Like an Analyst",
            "title": "What a Data Analyst Actually Does, and Why Companies Pay for It",
            "learning_objective": "By the end of this class, you will be able to describe the end-to-end workflow a data analyst follows to turn raw data into a business decision.",
            "duration_minutes": 20,
            "content_html": """<p>Every bank, telecom, and e-commerce company in Nigeria collects far more data than anyone actually looks at. A data analyst's job is to close that gap: pulling raw numbers into something a manager can use to make a real decision, like which product to restock or which customers are about to churn.</p><h2>The Analyst Workflow</h2><p>A typical analysis project moves through five stages: understanding the business question, collecting and cleaning the data, exploring it for patterns, visualizing the findings, and communicating a recommendation.</p><pre><code>Business Question -> Collect Data -> Clean Data -> Explore & Analyze -> Visualize -> Recommend</code></pre><h2>Why This Track Is Structured This Way</h2><p>Over the next 30 days you will practice every one of these stages using real-world-style data, not just charts in isolation. By day 30 you will analyze a real dataset end-to-end and deliver an executive dashboard, the exact deliverable that gets junior analysts hired at Nigerian banks, telecoms, and startups, where "can you build a dashboard from messy data" is a standard interview task.</p>""",
            "key_concepts": ["data analyst workflow", "business questions", "data cleaning", "insight communication"],
            "practical_exercise": {
                "title": "Map a Business Question to an Analysis Plan",
                "instructions": "Pick a real business question (e.g. 'Why did sales drop last month?') and write a half-page plan listing what data you would need, how you would clean it, what patterns you would look for, and how you would present the answer to a manager. Submit the plan as a short text file."
            },
            "quiz": [
                {"question": "What is the main goal of a data analyst's work?", "options": ['To turn raw data into insights that support a real business decision', 'To collect as much data as possible', 'To write complex code with no business purpose', 'To replace managers with automated reports'], "correct_index": 0, "explanation": 'Data analysis exists to help people make better decisions, not just to process numbers for their own sake.'},
                {"question": 'Which stage comes immediately after collecting data in the analyst workflow?', "options": ['Visualizing the findings', 'Making a recommendation', 'Cleaning the data', 'Presenting to the board'], "correct_index": 2, "explanation": 'Raw collected data is almost always messy and must be cleaned before it can be reliably explored or analyzed.'},
                {"question": 'Why do Nigerian companies specifically value data analysis skills?', "options": ['They collect very little data', 'Data analysis is only useful abroad', 'Analysts are not needed once data is collected', 'They collect large amounts of data but often lack people who can turn it into decisions'], "correct_index": 3, "explanation": 'Many companies gather significant data but lack analysts to extract actionable insight from it, creating real demand for this skill.'}
            ],
            "resources": [
                {"label": "Kaggle Learn", "url": "https://www.kaggle.com/learn"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Thinking Like an Analyst",
            "title": "Spreadsheet Fundamentals: Navigating and Structuring Data in Excel",
            "learning_objective": "By the end of this class, you will be able to structure a clean, analysis-ready dataset in a spreadsheet using proper rows, columns, and headers.",
            "duration_minutes": 25,
            "content_html": """<p>Excel remains the single most-used analysis tool in Nigerian offices, from bank branches to small business back-offices, and a messy spreadsheet is often the first thing that makes an analyst's work slower and more error-prone. Getting the structure right before doing anything else saves hours later.</p><h2>What "Tidy Data" Looks Like</h2><p>Every column should be a single variable, every row a single observation, and the first row should contain clear headers, no merged cells, no blank rows in the middle of data.</p><pre><code>Good:
Date       | Product   | Region | Units Sold
2026-01-05 | Rice 5kg  | Lagos  | 42

Bad:
Jan sales (merged across 3 cells)
Rice, 42 units, Lagos region on the 5th</code></pre><h2>Why Structure Matters Before Analysis</h2><p>Formulas, pivot tables, and charts all assume this tidy row-and-column structure; a messy layout breaks them or forces manual workarounds. Every dataset you touch for the rest of this track, and your final project's dataset, will need this same tidy structure before any real analysis can begin.</p>""",
            "key_concepts": ["tidy data structure", "rows vs columns", "headers", "avoiding merged cells"],
            "practical_exercise": {
                "title": "Restructure a Messy Spreadsheet",
                "instructions": "Take a messy set of sales notes (e.g. mixed text like 'Jan 5: sold 42 bags of rice in Lagos, Jan 6: 30 bags in Abuja') and convert it into a tidy spreadsheet with proper columns (Date, Product, Region, Units Sold) and one row per observation, using at least six rows. Submit the spreadsheet file."
            },
            "quiz": [
                {"question": 'In tidy data, what should each row represent?', "options": ['An entire month of data', 'A column header', 'A chart', 'A single observation or record'], "correct_index": 3, "explanation": 'In a tidy dataset, each row represents one distinct observation, keeping the data consistent and analyzable.'},
                {"question": 'Why are merged cells problematic in a dataset meant for analysis?', "options": ['They make the file smaller', 'They break the row-and-column structure that formulas and pivot tables rely on', 'Excel does not allow merged cells', 'They only affect printing, not analysis'], "correct_index": 1, "explanation": 'Merged cells disrupt the consistent grid structure needed for formulas, sorting, and pivot tables to work correctly.'},
                {"question": 'What should the first row of a tidy dataset contain?', "options": ['Clear column headers describing each variable', 'A company logo', 'The total row count', 'A blank row for spacing'], "correct_index": 0, "explanation": 'Clear headers in the first row identify what each column represents, which tools and formulas depend on.'}
            ],
            "resources": [
                {"label": "Microsoft Excel Support", "url": "https://support.microsoft.com/excel"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Thinking Like an Analyst",
            "title": "Core Excel Formulas Every Analyst Uses Daily",
            "learning_objective": "By the end of this class, you will be able to use SUM, AVERAGE, COUNTIF, and IF formulas to summarize a dataset.",
            "duration_minutes": 25,
            "content_html": """<p>Before touching Power BI or SQL, every working analyst reaches for a handful of Excel formulas dozens of times a day. Fluency here is what makes you fast enough to answer a manager's question in the same meeting instead of "let me get back to you."</p><h2>The Essential Formulas</h2><p>SUM and AVERAGE summarize numbers, COUNTIF counts matching entries, and IF applies conditional logic.</p><pre><code>=SUM(D2:D50)
=AVERAGE(D2:D50)
=COUNTIF(C2:C50, "Lagos")
=IF(D2>50, "High", "Low")</code></pre><h2>Combining Formulas for Real Questions</h2><p>Real business questions usually need formulas combined, for example counting how many Lagos sales were above a threshold.</p><pre><code>=COUNTIFS(C2:C50, "Lagos", D2:D50, ">50")</code></pre><p>This exact skill, quickly answering "how many," "what's the average," and "which ones meet this condition," is what lets an analyst respond to ad hoc questions from managers on the spot, one of the most valued day-to-day skills in the role.</p>""",
            "key_concepts": ["SUM/AVERAGE", "COUNTIF/COUNTIFS", "IF logic", "conditional formulas"],
            "practical_exercise": {
                "title": "Summarize a Sales Dataset with Formulas",
                "instructions": "Using the tidy sales spreadsheet from Day 2 (or a similar one with at least 15 rows), write formulas to calculate total units sold, average units sold per row, a count of rows for one specific region, and an IF formula that labels each row 'High' or 'Low' based on a threshold you choose. Submit the spreadsheet with formulas visible."
            },
            "quiz": [
                {"question": "Which formula would you use to count how many rows have 'Lagos' in a Region column?", "options": ["=SUM(Region)", "=COUNTIF(Region, \"Lagos\")", "=AVERAGE(Region)", "=IF(Region, \"Lagos\")"], "correct_index": 1, "explanation": "COUNTIF counts the number of cells in a range that match a given condition, such as a specific text value."},
                {"question": "What does the formula =IF(D2>50, \"High\", \"Low\") do?", "options": ["Always returns 'High'", "Returns 'High' if D2 is greater than 50, otherwise returns 'Low'", "Sums all values greater than 50", "Deletes values under 50"], "correct_index": 1, "explanation": "The IF formula applies conditional logic, returning one value if the condition is true and another if false."},
                {"question": "What does COUNTIFS allow that a single COUNTIF does not?", "options": ["Counting based on multiple conditions across columns at once", "Averaging values instead of counting", "Counting only text values", "Counting rows in a different spreadsheet only"], "correct_index": 0, "explanation": "COUNTIFS extends COUNTIF to support multiple conditions across one or more ranges simultaneously."}
            ],
            "resources": [
                {"label": "Microsoft Excel Support", "url": "https://support.microsoft.com/excel"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Thinking Like an Analyst",
            "title": "Cleaning Messy Real-World Data",
            "learning_objective": "By the end of this class, you will be able to identify and fix common data quality issues like duplicates, inconsistent text, and missing values.",
            "duration_minutes": 30,
            "content_html": """<p>Real datasets are never clean. Duplicate rows, inconsistent spellings like "Lagos" and "lagos " with a trailing space, and missing values are the norm, not the exception, and analysts routinely spend more time cleaning data than analyzing it.</p><h2>Common Data Quality Problems</h2><p>Watch for exact and near-duplicate rows, inconsistent capitalization or spacing, and blank or placeholder values like "N/A" mixed with true blanks.</p><pre><code>Messy:                  Clean:
"lagos "                "Lagos"
"LAGOS"                 "Lagos"
"" (blank)              "Unknown" or removed with a documented reason</code></pre><h2>A Systematic Cleaning Approach</h2><p>Remove exact duplicates first, standardize text case and whitespace with functions like TRIM and PROPER, and decide deliberately how to handle missing values rather than ignoring them silently. Documenting every cleaning decision you make is critical, because your final project will be judged partly on whether your cleaning process is clear and defensible, not just whether the numbers look right.</p>""",
            "key_concepts": ["duplicate detection", "text standardization", "missing values", "TRIM/PROPER functions"],
            "practical_exercise": {
                "title": "Clean a Deliberately Messy Dataset",
                "instructions": "Create or use a dataset of at least 20 rows containing at least three duplicate rows, inconsistent capitalization in a text column, and at least two missing values, then clean it: remove duplicates, standardize text, and handle missing values with a documented reason. Submit the before and after spreadsheets plus a short list of every cleaning decision you made."
            },
            "quiz": [
                {"question": 'Why might "Lagos" and "lagos " be treated as two different values by analysis tools?', "options": ['They are always treated as identical', 'Tools automatically fix all text inconsistencies', 'Differences in capitalization and trailing spaces make text values technically different', 'Only numbers can have this problem'], "correct_index": 2, "explanation": 'Most analysis tools compare text exactly, so capitalization and whitespace differences create seemingly different categories.'},
                {"question": 'What should an analyst do when they find missing values in a dataset?', "options": ['Deliberately decide how to handle them and document that decision', 'Always delete the entire dataset', 'Ignore them silently and proceed', 'Automatically assume they are zero'], "correct_index": 0, "explanation": 'Missing values need a deliberate, documented handling strategy since silently ignoring them can distort analysis.'},
                {"question": 'What is the purpose of the TRIM function in spreadsheet cleaning?', "options": ['To delete an entire column', 'To remove extra leading, trailing, and repeated spaces from text', 'To convert text to numbers', 'To sort a column alphabetically'], "correct_index": 1, "explanation": 'TRIM removes unwanted extra spaces from text, a common source of inconsistent-looking duplicate categories.'}
            ],
            "resources": [
                {"label": "Microsoft Excel Support", "url": "https://support.microsoft.com/excel"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Thinking Like an Analyst",
            "title": "Summarizing Data Fast with Pivot Tables",
            "learning_objective": "By the end of this class, you will be able to build a pivot table to summarize and cross-tabulate data by category.",
            "duration_minutes": 25,
            "content_html": """<p>A pivot table can answer in seconds what would otherwise take a dozen manual formulas: total sales by region, average order size by month, count of customers by product category. It is the single most powerful everyday tool in an analyst's Excel toolkit.</p><h2>Building a Pivot Table</h2><p>Select your tidy data range, insert a pivot table, then drag fields into Rows, Columns, and Values to summarize.</p><pre><code>Rows: Region
Values: Sum of Units Sold

Result:
Lagos    1,240
Abuja      890
Kano       610</code></pre><h2>Cross-Tabulating Two Dimensions</h2><p>Adding a second field to Columns lets you see how two categories interact at once, for example units sold by region and by month side by side. This exact skill, quickly slicing data by category, is what most managers actually ask for day to day, and pivot tables are frequently a live test in data analyst interviews.</p>""",
            "key_concepts": ["pivot tables", "Rows/Columns/Values", "cross-tabulation", "quick aggregation"],
            "practical_exercise": {
                "title": "Build a Pivot Table Summary",
                "instructions": "Using your cleaned sales dataset, build a pivot table showing total units sold by region, then add a second pivot table showing average units sold by region and by product category cross-tabulated. Submit the spreadsheet with both pivot tables and a one-sentence takeaway for each."
            },
            "quiz": [
                {"question": 'What is the main advantage of a pivot table over writing many individual formulas?', "options": ['Pivot tables cannot summarize numeric data', 'It quickly summarizes and cross-tabulates data by category with far less manual effort', 'Pivot tables only work with text data', 'It permanently changes the original data'], "correct_index": 1, "explanation": 'Pivot tables let analysts summarize and rearrange large datasets quickly without writing many separate formulas.'},
                {"question": "In a pivot table, what does dragging a field into the 'Values' area typically do?", "options": ['Deletes that field from the data', 'Sorts the entire dataset alphabetically', 'Removes duplicate rows automatically', 'Aggregates that field, such as summing or averaging it'], "correct_index": 3, "explanation": 'Fields placed in the Values area are aggregated, commonly through sum, average, or count, to summarize the data.'},
                {"question": "What does adding a second field to a pivot table's Columns area allow you to do?", "options": ['Delete the first field', 'Convert the pivot table into a chart automatically', 'Cross-tabulate two categories to see how they interact', 'Remove all numeric values'], "correct_index": 2, "explanation": 'A second field in Columns lets you break down the summary by two categories simultaneously, revealing interactions between them.'}
            ],
            "resources": [
                {"label": "Microsoft Excel Support", "url": "https://support.microsoft.com/excel"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Querying and Visualizing Data",
            "title": "Writing Your First SQL Queries to Answer Business Questions",
            "learning_objective": "By the end of this class, you will be able to write basic SELECT, WHERE, and ORDER BY SQL queries to retrieve specific data from a table.",
            "duration_minutes": 30,
            "content_html": """<p>Spreadsheets fall apart once a dataset has hundreds of thousands of rows, which is exactly the scale most real companies operate at. SQL is the language analysts use to query data directly from a database, and it is listed as a required skill in the vast majority of data analyst job postings.</p><h2>The Core SELECT Statement</h2><p>A SQL query retrieves specific columns and rows from a table.</p><pre><code>SELECT product, region, units_sold
FROM sales
WHERE region = 'Lagos'
ORDER BY units_sold DESC;</code></pre><h2>Filtering with WHERE</h2><p>The WHERE clause filters rows based on a condition, and can combine multiple conditions with AND/OR.</p><pre><code>SELECT product, units_sold
FROM sales
WHERE region = 'Lagos' AND units_sold > 50;</code></pre><p>This exact pattern, SELECT, FROM, WHERE, ORDER BY, answers the majority of simple business questions analysts get asked, and it is the foundation every more advanced SQL skill in this track builds on.</p>""",
            "key_concepts": ["SELECT statement", "WHERE filtering", "ORDER BY", "combining conditions with AND/OR"],
            "practical_exercise": {
                "title": "Write Filtering and Sorting Queries",
                "instructions": "Using a sales table with at least columns product, region, units_sold, and date (create sample data if needed, e.g. in SQLite or a free online SQL sandbox), write three queries: all sales from one region sorted by units sold descending, all sales where units sold exceeds a chosen threshold, and all sales from one region AND above that threshold. Submit the three queries and their results."
            },
            "quiz": [
                {"question": "What does the WHERE clause do in a SQL query?", "options": ["Sorts the results alphabetically", "Filters rows based on a specified condition", "Deletes rows from the table permanently", "Creates a new table"], "correct_index": 1, "explanation": "WHERE filters the result set to only rows matching the specified condition."},
                {"question": "What does 'ORDER BY units_sold DESC' do?", "options": ["Groups rows by units_sold", "Sorts the results by units_sold from highest to lowest", "Deletes rows with low units_sold", "Filters out rows with units_sold equal to zero"], "correct_index": 1, "explanation": "ORDER BY sorts the query results, and DESC specifies descending order, from highest value to lowest."},
                {"question": "In 'WHERE region = 'Lagos' AND units_sold > 50', what must be true for a row to be included?", "options": ["Only that units_sold is greater than 50", "Only that the region is Lagos", "Both that the region is Lagos and units_sold is greater than 50", "Either condition can be true independently"], "correct_index": 2, "explanation": "AND requires both conditions to be true simultaneously for a row to be included in the results."}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Querying and Visualizing Data",
            "title": "Aggregating Data with GROUP BY and SQL Functions",
            "learning_objective": "By the end of this class, you will be able to use GROUP BY with SUM, COUNT, and AVG to produce summary statistics in SQL.",
            "duration_minutes": 30,
            "content_html": """<p>Almost every real business question involves aggregation: total revenue by region, average order value by month, number of customers by product category. GROUP BY is how SQL answers these questions directly against the full dataset, without exporting to Excel first.</p><h2>Grouping and Aggregating</h2><p>GROUP BY collapses rows sharing the same value in a column, and aggregate functions summarize each group.</p><pre><code>SELECT region, SUM(units_sold) AS total_units, AVG(units_sold) AS avg_units
FROM sales
GROUP BY region;</code></pre><h2>Filtering Groups with HAVING</h2><p>WHERE filters rows before grouping; HAVING filters groups after aggregation, for example only showing regions with total units above a threshold.</p><pre><code>SELECT region, SUM(units_sold) AS total_units
FROM sales
GROUP BY region
HAVING SUM(units_sold) > 500;</code></pre><p>Being able to write a GROUP BY query fluently is one of the most common live coding tasks in data analyst technical interviews, precisely because it mirrors the real daily work of answering "how much per category" questions.</p>""",
            "key_concepts": ["GROUP BY", "aggregate functions (SUM/COUNT/AVG)", "HAVING vs WHERE", "column aliases"],
            "practical_exercise": {
                "title": "Write Aggregation Queries",
                "instructions": "Using your sales table, write a query that shows total and average units sold grouped by region, then extend it with a HAVING clause to only show regions where total units sold exceeds a threshold you choose, and a third query that counts the number of distinct products sold per region. Submit the three queries and their results."
            },
            "quiz": [
                {"question": 'What does GROUP BY do in a SQL query?', "options": ['Collapses rows sharing the same value in a specified column so they can be aggregated', 'Deletes duplicate rows', 'Sorts results alphabetically', 'Filters rows before any aggregation happens'], "correct_index": 0, "explanation": 'GROUP BY groups rows with matching values in specified columns, enabling aggregate functions to summarize each group.'},
                {"question": 'What is the key difference between WHERE and HAVING?', "options": ['They are exactly the same and interchangeable', 'HAVING is used only for text columns', 'WHERE can only be used with GROUP BY', 'WHERE filters rows before grouping; HAVING filters groups after aggregation'], "correct_index": 3, "explanation": 'WHERE filters individual rows before grouping occurs, while HAVING filters the aggregated groups afterward.'},
                {"question": 'Which SQL function would you use to count the number of distinct products in a table?', "options": ['SUM(product)', 'COUNT(DISTINCT product)', 'AVG(product)', 'ORDER BY product'], "correct_index": 1, "explanation": 'COUNT(DISTINCT column) counts the number of unique values in that column, ignoring duplicates.'}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Querying and Visualizing Data",
            "title": "Combining Tables with SQL JOINs",
            "learning_objective": "By the end of this class, you will be able to combine data from two related tables using an INNER JOIN.",
            "duration_minutes": 30,
            "content_html": """<p>Real business data is almost never in one table. Customer information, orders, and product details usually live in separate tables that must be joined together to answer a full business question, like "which customers bought which products."</p><h2>The INNER JOIN</h2><p>A JOIN combines rows from two tables based on a matching key, typically an id.</p><pre><code>SELECT orders.order_id, customers.name, orders.total
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;</code></pre><h2>Why JOIN Matters for Real Analysis</h2><p>Without joins, you would need to manually cross-reference ids between tables, which does not scale past a handful of rows. Nearly every meaningful business question, revenue by customer segment, orders by region, requires joining at least two tables, making this one of the most tested SQL skills in analyst interviews and exactly what your final project's SQL work, if you choose that tool stack, will rely on.</p>""",
            "key_concepts": ["INNER JOIN", "joining on a key column", "multi-table queries", "table aliases"],
            "practical_exercise": {
                "title": "Join Two Related Tables",
                "instructions": "Create two related sample tables (e.g. customers with id and name, and orders with customer_id and total), then write a query joining them to list each order alongside the customer's name, and a second query using GROUP BY on the joined result to show total spending per customer. Submit both queries and their results."
            },
            "quiz": [
                {"question": 'What is the primary purpose of a SQL JOIN?', "options": ['To delete rows from one table', "To sort a single table's rows", 'To combine related rows from two or more tables based on a matching key', 'To create a duplicate copy of a table'], "correct_index": 2, "explanation": 'JOIN combines data from multiple tables by matching rows on a shared key, such as an id.'},
                {"question": "In 'FROM orders INNER JOIN customers ON orders.customer_id = customers.id', what determines which rows get matched together?", "options": ['The order in which the tables were created', 'Rows where orders.customer_id equals customers.id', 'Rows are matched randomly', 'All rows are matched regardless of values'], "correct_index": 1, "explanation": 'The ON clause specifies the condition, here matching customer_id in orders to id in customers, that determines which rows pair together.'},
                {"question": 'Why is joining tables necessary for most real business questions?', "options": ['Business data is always in a single table', 'Joins are only useful for very small datasets', 'Joins replace the need for GROUP BY entirely', 'Related data like customers and orders is typically split across separate tables that must be combined'], "correct_index": 3, "explanation": 'Real-world data is normalized into separate related tables, so joins are necessary to reconstruct a complete picture for analysis.'}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Querying and Visualizing Data",
            "title": "Choosing the Right Chart for Your Data",
            "learning_objective": "By the end of this class, you will be able to select an appropriate chart type to represent a given dataset and business question.",
            "duration_minutes": 20,
            "content_html": """<p>A beautiful chart that shows the wrong comparison is worse than no chart at all, because it misleads the decision-maker reading it. Choosing the right chart type for the question being asked is a core analyst skill that is frequently overlooked by beginners who default to bar charts for everything.</p><h2>Matching Chart to Question</h2><p>Use a line chart for trends over time, a bar chart for comparing categories, a pie chart sparingly for simple part-to-whole comparisons with few categories, and a scatter plot for showing the relationship between two numeric variables.</p><pre><code>Trend over time      -> Line chart
Compare categories    -> Bar chart
Part of a whole (2-5) -> Pie chart
Relationship between two numbers -> Scatter plot</code></pre><h2>Common Chart Mistakes to Avoid</h2><p>Avoid pie charts with more than five slices, avoid 3D charts which distort perception of size, and never use a chart type just because it looks impressive if it obscures the actual comparison being made. Choosing charts deliberately, not by default, is exactly the judgment call your final project's dashboard will be evaluated on.</p>""",
            "key_concepts": ["chart type selection", "line vs bar vs pie vs scatter", "avoiding misleading visuals"],
            "practical_exercise": {
                "title": "Match Charts to Business Questions",
                "instructions": "For four different business questions (e.g. 'How did sales change over the year?', 'Which region sold the most?', 'What share of sales came from each product category?', 'Is there a relationship between price and units sold?'), state which chart type you would use for each and explain why in one sentence per question. Submit your answers."
            },
            "quiz": [
                {"question": "Which chart type is best suited for showing a trend over time?", "options": ["Pie chart", "Line chart", "Scatter plot", "3D bar chart"], "correct_index": 1, "explanation": "Line charts are ideal for showing how a value changes continuously across a time period."},
                {"question": "Why should pie charts generally be avoided when there are more than five categories?", "options": ["Pie charts cannot display percentages", "Too many slices become hard to compare visually and the chart loses clarity", "Pie charts only work with numeric time data", "Excel does not support pie charts with many categories"], "correct_index": 1, "explanation": "With many slices, pie charts become cluttered and hard to compare accurately, reducing their usefulness."},
                {"question": "Which chart type is best for showing the relationship between two numeric variables, like price and units sold?", "options": ["Pie chart", "Line chart", "Scatter plot", "Bar chart"], "correct_index": 2, "explanation": "Scatter plots plot two numeric variables against each other, making them ideal for spotting relationships or correlations."}
            ],
            "resources": [
                {"label": "Microsoft Excel Support", "url": "https://support.microsoft.com/excel"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Querying and Visualizing Data",
            "title": "Building Your First Interactive Dashboard in Power BI",
            "learning_objective": "By the end of this class, you will be able to import data into Power BI and build a basic interactive dashboard with multiple visuals.",
            "duration_minutes": 35,
            "content_html": """<p>Power BI is one of the most in-demand BI tools in corporate Nigeria, used heavily in banking, telecom, and consulting. Unlike a static Excel chart, a Power BI dashboard lets a manager click a filter and instantly see how every visual updates, which is exactly the interactivity real stakeholders expect today.</p><h2>Importing Data and Adding Visuals</h2><p>Power BI Desktop connects to a spreadsheet or database, then lets you drag fields onto the canvas to build charts.</p><pre><code>Get Data -> Excel Workbook -> Load
Drag "Region" to Axis, "Units Sold" to Values -> Bar Chart appears</code></pre><h2>Making It Interactive with Slicers</h2><p>A slicer is a filter control that, once added, filters every visual on the page simultaneously when clicked, for example filtering all charts to just one region. This click-to-filter interactivity is precisely what separates a professional dashboard from a static report, and it is the baseline expectation for the dashboard you will build for your final project if you choose Power BI as your tool.</p>""",
            "key_concepts": ["Power BI Desktop", "importing data", "visuals", "slicers and interactivity"],
            "practical_exercise": {
                "title": "Build a Three-Visual Interactive Dashboard",
                "instructions": "Import your cleaned sales dataset into Power BI Desktop, build a bar chart of units sold by region, a line chart of units sold over time, and add a slicer for product category that filters both charts when clicked. Submit a screenshot of the dashboard with the slicer applied to one category."
            },
            "quiz": [
                {"question": 'What is a key advantage of a Power BI dashboard over a static Excel chart?', "options": ['Power BI charts cannot be exported', 'Power BI cannot connect to Excel data', 'Static charts always update automatically', 'Power BI dashboards support interactive filtering that updates all visuals at once'], "correct_index": 3, "explanation": "Power BI's interactivity, especially slicers, lets users filter and explore data live, unlike a fixed static chart."},
                {"question": 'What does a slicer do in a Power BI dashboard?', "options": ['Acts as a filter control that updates every visual on the page when a value is selected', 'Deletes selected data permanently', 'Only changes the color scheme of the dashboard', 'Exports the dashboard to PDF'], "correct_index": 0, "explanation": 'A slicer lets users interactively filter all visuals on a report page by selecting a value, such as a specific category.'},
                {"question": 'What is the first step to bring spreadsheet data into Power BI Desktop?', "options": ['Manually retype all the data into Power BI', 'Convert the file to a PDF first', "Use 'Get Data' to connect to and load the Excel workbook", 'Power BI cannot import Excel data'], "correct_index": 2, "explanation": "Power BI's 'Get Data' feature connects directly to sources like Excel workbooks and loads them into the report."}
            ],
            "resources": [
                {"label": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Analyzing Real Datasets",
            "title": "Exploratory Data Analysis: Finding the Story in a New Dataset",
            "learning_objective": "By the end of this class, you will be able to perform exploratory data analysis on a new dataset to identify its structure, quality issues, and initial patterns.",
            "duration_minutes": 30,
            "content_html": """<p>Before answering any specific business question, an analyst first needs to understand what a dataset actually contains: how many rows, what each column means, what ranges values fall in, and where the problems are. Skipping this step leads to analyses built on flawed assumptions.</p><h2>The EDA Checklist</h2><p>Check the number of rows and columns, the data type of each column, summary statistics (min, max, average) for numeric columns, and the unique values in categorical columns.</p><pre><code># Using Python/pandas
df.shape           # (rows, columns)
df.dtypes          # data type per column
df.describe()      # min, max, mean, etc.
df["region"].unique()  # distinct categories</code></pre><h2>Looking for Early Signals</h2><p>Even a first pass often reveals real patterns, like one region dominating sales, or a suspicious outlier that turns out to be a data entry error. This exploratory pass is exactly the first thing you will do with your final project's dataset, and it shapes every analysis decision that follows.</p>""",
            "key_concepts": ["exploratory data analysis", "df.shape/dtypes/describe", "unique values", "identifying outliers early"],
            "practical_exercise": {
                "title": "Run a Full EDA Pass on a New Dataset",
                "instructions": "Pick a real or realistic dataset with at least 100 rows and several columns (numeric and categorical), and produce a short EDA report covering: row/column count, data types, summary statistics for at least two numeric columns, unique values for one categorical column, and one interesting early observation. Submit the dataset and the EDA report."
            },
            "quiz": [
                {"question": 'What is the main purpose of exploratory data analysis before answering a specific business question?', "options": ['To immediately build the final dashboard', "To understand a dataset's structure, quality, and initial patterns before deeper analysis", 'To delete unnecessary columns permanently', 'To skip data cleaning entirely'], "correct_index": 1, "explanation": 'EDA builds foundational understanding of a dataset, preventing analysis built on incorrect assumptions about its structure or quality.'},
                {"question": "What does checking a column's data type help an analyst catch early?", "options": ['Cases where a numeric column was accidentally loaded as text, which would break calculations', 'Nothing useful; data types are irrelevant', 'The exact number of rows in a dataset', 'The chart type to use later'], "correct_index": 0, "explanation": 'Incorrect data types, like numbers stored as text, silently break calculations and must be caught before analysis.'},
                {"question": 'Why is finding a suspicious outlier during EDA valuable?', "options": ['Outliers should always be ignored', 'Outliers only matter in scatter plots', 'It has no impact on the rest of the analysis', 'It might reveal a data entry error or a genuinely important business signal worth investigating'], "correct_index": 3, "explanation": 'An outlier discovered early could indicate either a data quality issue or a real, important finding worth digging into further.'}
            ],
            "resources": [
                {"label": "Kaggle Learn", "url": "https://www.kaggle.com/learn"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Analyzing Real Datasets",
            "title": "Descriptive Statistics: Mean, Median, and Standard Deviation in Practice",
            "learning_objective": "By the end of this class, you will be able to calculate and correctly interpret mean, median, and standard deviation for a real dataset.",
            "duration_minutes": 25,
            "content_html": """<p>Reporting only an average can seriously mislead a manager if the data is skewed by a few extreme values, like one massive order distorting the average order size. Understanding when to use mean versus median, and how to describe spread, is a foundational statistical judgment every analyst must make correctly.</p><h2>Mean vs Median</h2><p>The mean is sensitive to extreme values; the median is not. If one customer orders 10,000 units while everyone else orders 10-50, the mean will look artificially high.</p><pre><code>Orders: 10, 20, 15, 30, 10000
Mean:   2015   (distorted by the outlier)
Median: 20     (a far more representative typical value)</code></pre><h2>Standard Deviation: Measuring Spread</h2><p>Standard deviation shows how spread out values are around the mean; a small standard deviation means values cluster tightly, a large one means they vary widely. Reporting the median alongside a standard deviation, instead of a lone average, is exactly the kind of statistically honest reporting that separates a credible analysis from a misleading one, and graders and employers alike will expect this judgment in your final project.</p>""",
            "key_concepts": ["mean vs median", "standard deviation", "outlier sensitivity", "choosing the right summary statistic"],
            "practical_exercise": {
                "title": "Compare Mean and Median on Real Data",
                "instructions": "Using a numeric column from your dataset that likely contains outliers (like order value or sales amount), calculate the mean, median, and standard deviation, then write two sentences explaining whether the mean or median better represents a 'typical' value for this data and why. Submit the calculations and your explanation."
            },
            "quiz": [
                {"question": 'Why can the mean be a misleading summary statistic for data with extreme outliers?', "options": ['The mean is always more accurate than the median', 'The mean cannot be calculated when outliers exist', 'A few extreme values can pull the mean far away from what most data points actually look like', 'Outliers only affect the median, not the mean'], "correct_index": 2, "explanation": "The mean incorporates every value's magnitude, so extreme outliers can distort it away from a representative 'typical' value."},
                {"question": 'What does the median represent in a dataset?', "options": ['The average of all values', 'The most frequently occurring value', 'The difference between the highest and lowest values', 'The middle value when data is sorted in order'], "correct_index": 3, "explanation": 'The median is the middle value of a sorted dataset, making it resistant to distortion from extreme outliers.'},
                {"question": 'What does a large standard deviation indicate about a dataset?', "options": ['All values are identical', 'Values are spread widely around the mean', 'The dataset has no numeric values', 'The median equals the mean exactly'], "correct_index": 1, "explanation": 'A large standard deviation indicates that data points are widely spread out from the mean, showing high variability.'}
            ],
            "resources": [
                {"label": "Khan Academy: Statistics", "url": "https://www.khanacademy.org/math/statistics-probability"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Analyzing Real Datasets",
            "title": "Analyzing Data with Python and pandas",
            "learning_objective": "By the end of this class, you will be able to load, filter, and summarize a dataset using the pandas library in Python.",
            "duration_minutes": 35,
            "content_html": """<p>Excel and SQL handle a lot, but pandas gives analysts far more flexibility for complex, repeatable analysis, especially when a dataset needs custom transformations that spreadsheets struggle with. It is one of the most requested tools in data analyst job postings alongside SQL.</p><h2>Loading and Exploring Data</h2><p>pandas loads a CSV into a DataFrame, a table-like structure you can filter and summarize with code.</p><pre><code>import pandas as pd

df = pd.read_csv("sales.csv")
print(df.head())
print(df["units_sold"].mean())</code></pre><h2>Filtering and Grouping</h2><p>pandas filtering and grouping mirror SQL's WHERE and GROUP BY, but in Python.</p><pre><code>lagos_sales = df[df["region"] == "Lagos"]
summary = df.groupby("region")["units_sold"].sum()
print(summary)</code></pre><p>Because pandas code is reusable and repeatable, rerunning the same analysis on updated data next month takes seconds, not hours, which is exactly why companies value analysts who can code their analysis instead of redoing manual spreadsheet work every time.</p>""",
            "key_concepts": ["pandas DataFrame", "read_csv", "filtering rows", "groupby aggregation"],
            "practical_exercise": {
                "title": "Analyze a CSV Dataset with pandas",
                "instructions": "Load a CSV dataset with at least 100 rows into pandas, filter it to rows matching one condition (e.g. one region or category), compute the sum and average of a numeric column for that filtered subset, and use groupby to summarize the full dataset by one categorical column. Submit the Python script and its printed output."
            },
            "quiz": [
                {"question": 'What does pd.read_csv() do in pandas?', "options": ['Deletes a CSV file', 'Converts a DataFrame into a CSV file', 'Connects to a live database only', 'Loads a CSV file into a DataFrame for analysis'], "correct_index": 3, "explanation": 'pd.read_csv() reads a CSV file and loads its contents into a pandas DataFrame, ready for analysis.'},
                {"question": 'What does \'df[df["region"] == "Lagos"]\' do?', "options": ['Deletes all Lagos rows', 'Sorts the DataFrame by region', "Filters the DataFrame to only rows where the region column equals 'Lagos'", 'Renames the region column'], "correct_index": 2, "explanation": "This boolean filtering syntax selects only the rows where the specified condition is true, similar to SQL's WHERE clause."},
                {"question": "What is the pandas equivalent of SQL's GROUP BY?", "options": ['df.groupby()', 'df.head()', 'df.read_csv()', 'df.describe()'], "correct_index": 0, "explanation": "pandas' groupby() method groups rows by a column's values, similar to SQL's GROUP BY, enabling aggregation per group."}
            ],
            "resources": [
                {"label": "Kaggle Learn: Pandas", "url": "https://www.kaggle.com/learn/pandas"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Analyzing Real Datasets",
            "title": "Visualizing Data Directly in Python with Matplotlib",
            "learning_objective": "By the end of this class, you will be able to create basic line, bar, and scatter charts from a pandas DataFrame using matplotlib.",
            "duration_minutes": 25,
            "content_html": """<p>When an analysis lives in a Python script or notebook, generating charts directly in Python, without exporting to Excel, keeps the whole workflow in one reproducible place. This is exactly how data teams at tech-forward companies operate.</p><h2>Building Basic Charts</h2><p>matplotlib works directly with pandas data to produce standard chart types.</p><pre><code>import matplotlib.pyplot as plt

summary = df.groupby("region")["units_sold"].sum()
summary.plot(kind="bar", title="Units Sold by Region")
plt.ylabel("Units Sold")
plt.savefig("units_by_region.png")
plt.show()</code></pre><h2>Labeling Charts Properly</h2><p>Every chart needs a title and axis labels, or a reader has to guess what they are looking at, which undermines the whole point of visualizing data. Saving charts as image files with plt.savefig() also lets you embed them directly into reports, exactly what you will do when assembling your final project's presentation materials.</p>""",
            "key_concepts": ["matplotlib", "bar/line/scatter plots from pandas", "titles and axis labels", "saving chart images"],
            "practical_exercise": {
                "title": "Generate Three Labeled Charts from Data",
                "instructions": "Using your pandas DataFrame, create a bar chart of a numeric total by category, a line chart showing a trend over a date column, and a scatter plot of the relationship between two numeric columns, each with a title and labeled axes, and save all three as image files. Submit the Python script and the three saved chart images."
            },
            "quiz": [
                {"question": 'Why is it important to add a title and axis labels to a chart?', "options": ['Without them, a reader cannot understand what the chart is actually showing', 'It is optional and rarely matters', 'Titles slow down chart rendering significantly', 'Only bar charts require labels'], "correct_index": 0, "explanation": 'Clear titles and axis labels are essential for a reader to correctly interpret what a chart represents.'},
                {"question": 'What does plt.savefig() do in matplotlib?', "options": ['Displays the chart on screen only', 'Deletes the chart from memory', 'Saves the current chart as an image file', 'Converts the chart into a pandas DataFrame'], "correct_index": 2, "explanation": 'plt.savefig() writes the currently generated chart to an image file, useful for embedding in reports.'},
                {"question": 'Why might an analyst prefer generating charts directly in Python over exporting to Excel each time?', "options": ['Python charts cannot be saved as images', 'Excel charts are always more accurate', 'Python cannot create bar or line charts', 'It keeps the entire analysis workflow reproducible and in one place'], "correct_index": 3, "explanation": 'Generating charts in the same script as the analysis keeps the whole workflow reproducible without manual export steps.'}
            ],
            "resources": [
                {"label": "Kaggle Learn: Data Visualization", "url": "https://www.kaggle.com/learn/data-visualization"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Analyzing Real Datasets",
            "title": "Spotting Correlation, and Why It Is Not the Same as Causation",
            "learning_objective": "By the end of this class, you will be able to calculate a correlation between two variables and correctly explain its limitations.",
            "duration_minutes": 25,
            "content_html": """<p>Finding that two variables move together, like marketing spend and sales, is one of the most common early findings in an analysis. But mistaking that relationship for proof of cause is one of the most common and damaging analyst mistakes, and interviewers frequently test whether candidates understand the difference.</p><h2>Measuring Correlation</h2><p>Correlation ranges from -1 to 1: close to 1 means strong positive relationship, close to -1 means strong negative relationship, near 0 means little linear relationship.</p><pre><code>correlation = df["marketing_spend"].corr(df["sales"])
print(correlation)  # e.g. 0.82 -> strong positive relationship</code></pre><h2>Why Correlation Is Not Causation</h2><p>Ice cream sales and drowning incidents both rise in summer, correlated, but ice cream does not cause drowning; heat is a third factor driving both. Every time you report a correlation in your final project or any real analysis, explicitly noting this limitation, and avoiding a causal claim you cannot back up, is exactly the kind of statistical discipline that builds trust with stakeholders.</p>""",
            "key_concepts": ["correlation coefficient", "positive/negative correlation", "correlation vs causation", "confounding variables"],
            "practical_exercise": {
                "title": "Calculate and Interpret a Correlation",
                "instructions": "Using two numeric columns from your dataset that you suspect are related (e.g. price and units sold), calculate their correlation coefficient, state whether it is weak, moderate, or strong, and write two sentences explaining a plausible reason the correlation might not imply direct causation. Submit the calculation and your written explanation."
            },
            "quiz": [
                {"question": 'What does a correlation coefficient close to 1 indicate?', "options": ['No relationship between the variables', 'A strong negative relationship between the variables', 'The variables are identical', 'A strong positive relationship between the variables'], "correct_index": 3, "explanation": 'A correlation coefficient near 1 indicates that as one variable increases, the other tends to increase as well, strongly.'},
                {"question": 'Why is it a mistake to assume correlation implies causation?', "options": ['Correlation always implies causation', 'A third, hidden factor might be driving both variables without one causing the other', 'Correlation coefficients are never accurate', 'Causation is impossible to prove in any dataset'], "correct_index": 1, "explanation": 'Two variables can move together due to a confounding factor influencing both, without either one causing the other directly.'},
                {"question": 'In the ice cream and drowning example, what is heat considered?', "options": ['A confounding variable driving both trends', 'The dependent variable', 'An outlier', 'The correlation coefficient'], "correct_index": 0, "explanation": 'Heat is a confounding variable, an underlying factor that independently increases both ice cream sales and swimming (and thus drowning risk).'}
            ],
            "resources": [
                {"label": "Khan Academy: Statistics", "url": "https://www.khanacademy.org/math/statistics-probability"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Building Business Intelligence Dashboards",
            "title": "Designing a Dashboard That a Manager Can Actually Use",
            "learning_objective": "By the end of this class, you will be able to design a dashboard layout that prioritizes clarity and answers a specific business question at a glance.",
            "duration_minutes": 30,
            "content_html": """<p>A dashboard crammed with every chart you could make is not useful; it overwhelms the person trying to make a decision. Good dashboard design is about deliberate restraint: showing exactly what a manager needs to answer their question, and nothing more.</p><h2>Designing for the Viewer, Not the Analyst</h2><p>Start every dashboard by writing down the specific question it should answer, for example "is regional sales performance on track this quarter?" Every visual on the page should serve that question directly.</p><pre><code>Top-left: Key metric card (Total Sales This Quarter)
Top-right: Trend line (Sales Over Time)
Bottom: Bar chart (Sales by Region), Slicer (Filter by Product)</code></pre><h2>Visual Hierarchy and Restraint</h2><p>Put the most important number in the top-left, where eyes land first, group related visuals together, and resist the urge to add "just one more chart." This design discipline, ruthlessly cutting anything that does not serve the core question, is exactly what separates an amateur dashboard from the polished, executive-ready one your final project requires.</p>""",
            "key_concepts": ["dashboard purpose", "visual hierarchy", "avoiding clutter", "designing for the viewer"],
            "practical_exercise": {
                "title": "Sketch a Dashboard Layout Before Building It",
                "instructions": "Choose a specific business question your dataset could answer, then sketch (on paper or in a simple drawing tool) a dashboard layout with a title, a key metric card, and two or three supporting charts, labeling where each element goes and why. Submit the sketch and one sentence justifying each visual's inclusion."
            },
            "quiz": [
                {"question": 'Why should a dashboard avoid including every possible chart from an analysis?', "options": ['More charts always make a dashboard better', 'Dashboards can only contain one chart by design rules', 'Too many charts overwhelm the viewer and obscure the specific question the dashboard should answer', 'Charts take too long to load if there are more than two'], "correct_index": 2, "explanation": "A cluttered dashboard makes it harder for viewers to find the specific insight they need, defeating the dashboard's purpose."},
                {"question": 'What should be the starting point when designing any dashboard?', "options": ['Identifying the specific business question the dashboard needs to answer', 'Choosing the color scheme first', 'Adding as many charts as possible', 'Picking a random layout template'], "correct_index": 0, "explanation": 'Good dashboard design starts by defining the specific question it must answer, which then guides every design decision.'},
                {"question": 'Why is placement in the top-left of a dashboard often reserved for the most important metric?', "options": ['It has no real effect on how viewers read a dashboard', "Viewers' eyes typically land there first, so key information gets seen immediately", 'Top-left is only relevant for chart colors', 'It is a technical requirement of Power BI'], "correct_index": 1, "explanation": "Viewers commonly scan a page starting from the top-left, so placing the most critical metric there ensures it's seen first."}
            ],
            "resources": [
                {"label": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Building Business Intelligence Dashboards",
            "title": "Writing DAX Measures for Custom Calculations in Power BI",
            "learning_objective": "By the end of this class, you will be able to write a basic DAX measure to calculate a custom metric in Power BI.",
            "duration_minutes": 30,
            "content_html": """<p>Power BI's built-in aggregations cover simple sums and averages, but real business metrics, like profit margin or year-over-year growth, need custom formulas. DAX (Data Analysis Expressions) is the formula language that makes this possible, and it is a specific, named skill on many Nigerian BI analyst job postings.</p><h2>Writing a Basic Measure</h2><p>A measure is a calculation that responds dynamically to whatever filters are applied on the dashboard.</p><pre><code>Total Revenue = SUM(sales[revenue])
Profit Margin % = DIVIDE(SUM(sales[profit]), SUM(sales[revenue]), 0)</code></pre><h2>Why Measures Beat Static Calculations</h2><p>Because a measure recalculates based on active filters and slicers, the same "Profit Margin %" measure automatically updates whether the dashboard is filtered to one region or showing all regions, without any manual rework. This dynamic recalculation is exactly what makes a Power BI dashboard genuinely interactive rather than just a set of static pre-computed charts.</p>""",
            "key_concepts": ["DAX measures", "SUM/DIVIDE functions", "dynamic recalculation with filters"],
            "practical_exercise": {
                "title": "Write Two Custom DAX Measures",
                "instructions": "In Power BI, using your sales dataset, write a measure that calculates total revenue, and a second measure using DIVIDE that calculates average revenue per unit sold, then add both as metric cards to your dashboard and confirm they update correctly when a slicer filter is applied. Submit a screenshot showing both measures and the filtered result."
            },
            "quiz": [
                {"question": "What is a key advantage of a DAX measure over a static calculated value?", "options": ["Measures cannot use filters at all", "A measure recalculates dynamically based on whatever filters or slicers are currently applied", "Measures are always slower than static values", "Static values update automatically like measures do"], "correct_index": 1, "explanation": "DAX measures respond to the current filter context, recalculating automatically as slicers or filters change, unlike static values."},
                {"question": "What does the DIVIDE function do differently from a plain division operator in DAX, as commonly used?", "options": ["It multiplies instead of dividing", "It safely handles division by zero by returning a specified fallback value", "It only works with text columns", "It deletes the denominator column"], "correct_index": 1, "explanation": "DIVIDE is commonly used in DAX because it gracefully handles division by zero, avoiding errors that plain division would throw."},
                {"question": "What does DAX stand for?", "options": ["Data Analysis Expressions", "Direct Access Xchange", "Dynamic Aggregate Xtension", "Database Access Extension"], "correct_index": 0, "explanation": "DAX stands for Data Analysis Expressions, the formula language used in Power BI for custom calculations."}
            ],
            "resources": [
                {"label": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Building Business Intelligence Dashboards",
            "title": "Analyzing Trends Over Time: Time Series Basics",
            "learning_objective": "By the end of this class, you will be able to analyze and visualize how a metric changes over time, including spotting seasonality.",
            "duration_minutes": 25,
            "content_html": """<p>Almost every business tracks performance over time, monthly revenue, weekly signups, daily transactions, and spotting whether a trend is genuinely changing or just following a predictable seasonal pattern is a core analyst responsibility.</p><h2>Aggregating by Time Period</h2><p>Time series analysis usually starts by aggregating raw transaction-level data up to a useful period, like month or week.</p><pre><code>SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;</code></pre><h2>Spotting Trend vs Seasonality</h2><p>A genuine trend moves consistently in one direction over a long period; seasonality is a repeating pattern tied to a calendar cycle, like retail sales spiking every December. Confusing a seasonal spike for real growth is a common mistake that leads to bad business decisions, so always compare a period to the same period last year, not just the previous month, exactly the kind of comparison your final project's time-based analysis should include if your dataset has a date dimension.</p>""",
            "key_concepts": ["time series aggregation", "trend vs seasonality", "year-over-year comparison"],
            "practical_exercise": {
                "title": "Analyze a Time Series for Trend and Seasonality",
                "instructions": "Using a dataset with a date column spanning at least a year, aggregate a numeric metric by month, plot it as a line chart, and write two sentences identifying whether you see a genuine trend, a seasonal pattern, or both, with a specific month or period as evidence. Submit the chart and your written observation."
            },
            "quiz": [
                {"question": 'What is the difference between a trend and seasonality in time series data?', "options": ['They are the same thing', 'A trend is a consistent long-term direction; seasonality is a repeating pattern tied to a calendar cycle', 'Seasonality only applies to weather data', 'A trend can only be negative'], "correct_index": 1, "explanation": 'A trend reflects sustained long-term change, while seasonality reflects a recurring pattern linked to a specific time cycle, like a season or month.'},
                {"question": "Why is comparing a month's performance to the same month last year often more meaningful than comparing it to the previous month?", "options": ['It has no real advantage', 'Previous-month comparisons are always more accurate', 'Year-over-year comparisons cannot include seasonality', 'It accounts for seasonal effects, avoiding the mistake of confusing a seasonal spike with real growth'], "correct_index": 3, "explanation": 'Year-over-year comparisons control for seasonal patterns, revealing whether change reflects a real trend rather than a predictable seasonal effect.'},
                {"question": 'What is a realistic example of seasonality in a Nigerian retail business?', "options": ['Random daily fluctuations with no pattern', 'A one-time permanent increase in customers', 'A consistent spike in sales every December due to holiday shopping', 'A gradual decline over five years'], "correct_index": 2, "explanation": 'A predictable, recurring spike tied to a calendar period, like December holiday shopping, is a classic example of seasonality.'}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Building Business Intelligence Dashboards",
            "title": "Segmenting Customers and Data for Deeper Insight",
            "learning_objective": "By the end of this class, you will be able to segment a dataset into meaningful groups to reveal patterns hidden in the aggregate.",
            "duration_minutes": 25,
            "content_html": """<p>An overall average often hides very different behavior within subgroups. A company's "average customer spend" might mask the fact that a small segment of high-value customers accounts for most of the revenue, a pattern only segmentation reveals.</p><h2>Basic Segmentation Approaches</h2><p>Segment by demographic (region, age group), by behavior (frequency of purchase, order size), or by value (top spenders vs occasional buyers).</p><pre><code>SELECT
  CASE
    WHEN total_spent > 100000 THEN 'High Value'
    WHEN total_spent > 20000 THEN 'Medium Value'
    ELSE 'Low Value'
  END AS segment,
  COUNT(*) AS customer_count
FROM customers
GROUP BY segment;</code></pre><h2>Why Segmentation Changes the Recommendation</h2><p>A blanket recommendation like "increase marketing spend" is far less useful than "increase marketing spend targeted at Medium Value customers, who show the highest growth potential." This kind of segmented insight, not just an aggregate number, is exactly what turns an analysis into something an executive can act on, and it is what your final project's recommendations should aim for.</p>""",
            "key_concepts": ["customer segmentation", "CASE WHEN logic", "value-based segments", "actionable segmented insights"],
            "practical_exercise": {
                "title": "Segment a Dataset and Compare Groups",
                "instructions": "Using your dataset, create at least three segments based on a numeric value (e.g. High/Medium/Low spenders using CASE WHEN in SQL or a formula in Excel/pandas), then calculate and compare the count and average value for each segment, and write two sentences on what business action this segmentation suggests. Submit the segmented output and your written recommendation."
            },
            "quiz": [
                {"question": 'Why can an overall average sometimes hide important patterns in a dataset?', "options": ['Different subgroups within the data may behave very differently, and the average blends them together', 'Averages are always fully representative of every subgroup', 'Averages cannot be calculated on segmented data', 'Segmentation always produces the same result as the average'], "correct_index": 0, "explanation": 'An aggregate average can mask meaningful differences between subgroups, making segmentation necessary to reveal them.'},
                {"question": 'What does a CASE WHEN statement in SQL allow an analyst to do?', "options": ['Delete rows based on a condition', 'Automatically create a chart', 'Join two unrelated tables', 'Assign categorical labels to rows based on conditional logic'], "correct_index": 3, "explanation": 'CASE WHEN evaluates conditions and assigns a label or value accordingly, commonly used to create custom segments.'},
                {"question": 'Why is a segmented recommendation generally more actionable than a blanket one?', "options": ['Segmented recommendations are always wrong', 'It targets specific groups with specific behavior, giving a manager a more precise action to take', 'Blanket recommendations are always better for large companies', 'Segmentation removes the need for any recommendation at all'], "correct_index": 1, "explanation": 'A recommendation targeted at a specific, well-understood segment gives decision-makers a clearer, more precise action than a generic one.'}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Building Business Intelligence Dashboards",
            "title": "Publishing and Sharing a Power BI Dashboard",
            "learning_objective": "By the end of this class, you will be able to publish a Power BI dashboard and configure it to be shared with others.",
            "duration_minutes": 25,
            "content_html": """<p>A dashboard sitting on your laptop as a .pbix file helps nobody. Publishing it so a manager or client can open it in a browser, without installing Power BI Desktop themselves, is the step that turns your analysis into something actually usable at work.</p><h2>Publishing to the Power BI Service</h2><p>From Power BI Desktop, publishing sends your report to the Power BI Service (app.powerbi.com), a free tier of which is enough for a portfolio project.</p><pre><code>Home tab -> Publish -> choose workspace -> report appears at app.powerbi.com</code></pre><h2>Sharing and Access Considerations</h2><p>Once published, you can share a link, set up scheduled data refresh so the dashboard stays current, and control who can view versus edit it. Being able to say "here is a live link to my dashboard" instead of "here is a screenshot" is a meaningfully stronger portfolio signal, and matches exactly how real BI analysts deliver their work to stakeholders.</p>""",
            "key_concepts": ["Power BI Service", "publishing reports", "sharing links", "scheduled refresh"],
            "practical_exercise": {
                "title": "Publish Your Dashboard and Share the Link",
                "instructions": "Publish your Power BI dashboard from Day 16-17 to the Power BI Service using a free account, and share the resulting link with view access (or export the report as a PDF if publishing is not available in your setup). Submit the shareable link or the exported PDF along with a screenshot confirming it loaded successfully."
            },
            "quiz": [
                {"question": 'Why does publishing a dashboard to the Power BI Service matter for real-world use?', "options": ['Publishing has no practical benefit over a local file', 'Publishing deletes the original data', 'It lets others view the dashboard in a browser without needing Power BI Desktop installed', 'Only Power BI Desktop can display any dashboard'], "correct_index": 2, "explanation": 'Publishing makes the dashboard accessible via a browser link, allowing stakeholders to view it without installing any software.'},
                {"question": 'What does scheduled refresh allow a published dashboard to do?', "options": ['Automatically delete old data', 'Automatically update its data on a regular schedule so it stays current', 'Change its visual design periodically', 'Convert itself into an Excel file'], "correct_index": 1, "explanation": "Scheduled refresh keeps a published dashboard's underlying data current without requiring manual re-publishing each time."},
                {"question": 'Why is a live shareable dashboard link generally a stronger portfolio signal than a static screenshot?', "options": ['Screenshots are always preferred by employers', 'Links load slower than screenshots', 'There is no meaningful difference between the two', 'A live link demonstrates a working, real deliverable rather than just an image of one'], "correct_index": 3, "explanation": 'A live, interactive dashboard proves the work is real and functional, a stronger signal than a static image.'}
            ],
            "resources": [
                {"label": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Advanced Analysis and Real-World Judgment",
            "title": "Detecting and Handling Outliers Without Distorting the Truth",
            "learning_objective": "By the end of this class, you will be able to detect outliers in a dataset and decide, with justification, whether to keep, adjust, or remove them.",
            "duration_minutes": 25,
            "content_html": """<p>An outlier can be a data entry error worth removing, or it can be the single most important data point in the whole dataset, like a fraud case or a breakout best-seller. Deciding which one you are looking at, rather than reflexively deleting it, is a judgment call that separates a careful analyst from a careless one.</p><h2>Detecting Outliers</h2><p>A common method flags values far outside the typical range using the interquartile range (IQR).</p><pre><code>Q1 = df["order_value"].quantile(0.25)
Q3 = df["order_value"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df["order_value"] < Q1 - 1.5*IQR) | (df["order_value"] > Q3 + 1.5*IQR)]</code></pre><h2>Deciding What to Do With Them</h2><p>Investigate each outlier before acting: is it a typo (10,000 units instead of 100), a genuine rare event worth highlighting, or noise? Whatever you decide, document it, because silently removing inconvenient data points without explanation is one of the fastest ways to lose credibility, and your final project's analysis must show this same documented judgment.</p>""",
            "key_concepts": ["outlier detection", "interquartile range (IQR)", "investigating before removing", "documenting decisions"],
            "practical_exercise": {
                "title": "Detect and Investigate Outliers",
                "instructions": "Using a numeric column from your dataset, calculate the IQR-based outlier boundaries, list any rows flagged as outliers, investigate at least two of them (checking if they look like errors or genuine rare events), and document your decision to keep, adjust, or remove each with a one-sentence justification. Submit the flagged outliers and your documented decisions."
            },
            "quiz": [
                {"question": 'What does the interquartile range (IQR) method use to flag potential outliers?', "options": ['The mean and standard deviation only', 'The total number of rows in the dataset', 'The most frequently occurring value', 'The range between the 25th and 75th percentile of the data'], "correct_index": 3, "explanation": 'The IQR method defines outlier boundaries based on the spread between the first quartile (Q1) and third quartile (Q3).'},
                {"question": "Why shouldn't an analyst automatically delete every detected outlier?", "options": ['Some outliers represent genuine, important events rather than errors, and deleting them could hide real insight', 'Outliers should never be examined at all', 'Deleting outliers is always required before any analysis', 'Outliers cannot be detected using IQR'], "correct_index": 0, "explanation": 'An outlier might reflect a real and important event, so it must be investigated rather than reflexively removed.'},
                {"question": 'Why is documenting the decision made about each outlier important?', "options": ['Documentation is not necessary if the numbers look right', 'Documentation replaces the need for any further analysis', 'It keeps the analysis transparent and defensible, avoiding the appearance of silently manipulating data', 'Outlier decisions never need to be justified'], "correct_index": 2, "explanation": 'Documenting outlier decisions maintains transparency and trust, showing the reasoning behind each choice rather than hiding it.'}
            ],
            "resources": [
                {"label": "Khan Academy: Statistics", "url": "https://www.khanacademy.org/math/statistics-probability"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Advanced Analysis and Real-World Judgment",
            "title": "Writing Advanced SQL: Subqueries and Window Functions",
            "learning_objective": "By the end of this class, you will be able to write a subquery and a basic window function to answer a multi-step business question.",
            "duration_minutes": 30,
            "content_html": """<p>Some business questions can't be answered with a single simple query, like "which customers spent above the average" or "what is each customer's rank by total spend." Subqueries and window functions are how SQL handles these more advanced, multi-step questions.</p><h2>Subqueries</h2><p>A subquery is a query nested inside another, often used to compare rows against an aggregate.</p><pre><code>SELECT customer_id, total_spent
FROM customers
WHERE total_spent > (SELECT AVG(total_spent) FROM customers);</code></pre><h2>Window Functions for Ranking</h2><p>Window functions calculate a value across a set of rows without collapsing them into a single group, useful for ranking.</p><pre><code>SELECT customer_id, total_spent,
  RANK() OVER (ORDER BY total_spent DESC) AS spend_rank
FROM customers;</code></pre><p>Being comfortable with subqueries and window functions is what separates a candidate who can write basic reports from one trusted with more complex, multi-step analysis, and both come up regularly in intermediate SQL interview rounds.</p>""",
            "key_concepts": ["subqueries", "window functions", "RANK() OVER", "multi-step SQL questions"],
            "practical_exercise": {
                "title": "Write a Subquery and a Ranking Query",
                "instructions": "Using your customer or sales table, write a query using a subquery to find all rows above the overall average of a numeric column, and a second query using RANK() OVER to rank rows by that same numeric column in descending order. Submit both queries and their results."
            },
            "quiz": [
                {"question": 'What is a subquery in SQL?', "options": ['A query that runs after the main query finishes entirely', 'A query nested inside another query, often used to compare against an aggregate value', 'A query that only works on a single row', 'A shortcut for deleting a table'], "correct_index": 1, "explanation": 'A subquery is a query embedded within another query, commonly used to compute a value like an average for comparison.'},
                {"question": 'What does the RANK() window function do?', "options": ['Assigns a rank to each row based on a specified ordering, without collapsing the rows into groups', 'Deletes duplicate rows', 'Groups rows into a single summary row', 'Filters rows before any calculation happens'], "correct_index": 0, "explanation": 'RANK() OVER assigns a rank to each row based on the specified order, while keeping all individual rows visible in the output.'},
                {"question": "In 'WHERE total_spent > (SELECT AVG(total_spent) FROM customers)', what does the subquery calculate?", "options": ['The total number of customers', 'The maximum total_spent value', 'A list of all customer names', 'The average total_spent across all customers, used as a comparison threshold'], "correct_index": 3, "explanation": 'The subquery computes the average total_spent, which the outer query then uses to filter for above-average customers.'}
            ],
            "resources": [
                {"label": "MDN: SQL/Database Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Advanced Analysis and Real-World Judgment",
            "title": "Automating Repeated Analysis with Python Scripts",
            "learning_objective": "By the end of this class, you will be able to write a reusable Python script that automates a repeated data-cleaning and summary task.",
            "duration_minutes": 25,
            "content_html": """<p>Redoing the same manual cleaning and summarizing steps every time new data arrives wastes hours an analyst could spend on actual insight generation. Writing the process once as a script that runs automatically on any new file is a skill that immediately makes an analyst more valuable.</p><h2>Turning Manual Steps into a Function</h2><p>Wrap your cleaning and summary steps into a reusable function that takes a filename and returns a clean summary.</p><pre><code>def clean_and_summarize(filepath):
    df = pd.read_csv(filepath)
    df = df.drop_duplicates()
    df["region"] = df["region"].str.strip().str.title()
    summary = df.groupby("region")["units_sold"].sum()
    return summary

result = clean_and_summarize("january_sales.csv")</code></pre><h2>Why Automation Matters for Analysts</h2><p>Once this function exists, processing next month's data takes one line of code instead of an hour of manual spreadsheet work, and it eliminates the human error risk of repeating steps slightly differently each time. This is exactly the kind of efficiency employers mean when a job posting lists "process automation" as a valued skill for a data analyst.</p>""",
            "key_concepts": ["reusable functions", "automating cleaning steps", "reducing manual repetition", "consistency across runs"],
            "practical_exercise": {
                "title": "Write a Reusable Cleaning-and-Summary Function",
                "instructions": "Write a Python function that takes a CSV filepath as input, removes duplicates, standardizes a text column, and returns a groupby summary, then run it on two different CSV files with the same structure to prove it works generically. Submit the function code and the two summary outputs."
            },
            "quiz": [
                {"question": 'What is the main benefit of wrapping repeated cleaning steps into a function?', "options": ['Functions make code run on a different computer automatically', 'Functions eliminate the need for any data cleaning at all', 'It lets the same process be reused on new data quickly and consistently, without manual repetition', 'It automatically publishes results to a dashboard'], "correct_index": 2, "explanation": 'A reusable function applies the exact same cleaning and summary logic to any new dataset instantly, saving time and reducing errors.'},
                {"question": 'Why does automating a repeated analysis task reduce the risk of errors?', "options": ['Automation introduces more manual steps', 'Automated scripts cannot process real data', 'Manual repetition is always more accurate than automation', 'It ensures the exact same steps are applied consistently every time, unlike manually repeating steps by hand'], "correct_index": 3, "explanation": 'Automated code applies identical logic every run, avoiding the inconsistencies that can creep in when steps are repeated manually.'},
                {"question": "In the example function, what does 'df.drop_duplicates()' do?", "options": ['Removes all rows from the DataFrame', 'Removes duplicate rows from the DataFrame', 'Deletes a specific column', 'Sorts the DataFrame alphabetically'], "correct_index": 1, "explanation": 'drop_duplicates() removes rows that are exact duplicates of another row, a common data-cleaning step.'}
            ],
            "resources": [
                {"label": "Kaggle Learn: Pandas", "url": "https://www.kaggle.com/learn/pandas"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Advanced Analysis and Real-World Judgment",
            "title": "Avoiding Misleading Charts and Statistical Traps",
            "learning_objective": "By the end of this class, you will be able to identify common misleading chart and statistics techniques and avoid them in your own work.",
            "duration_minutes": 25,
            "content_html": """<p>A chart can be technically accurate and still mislead the viewer, whether by accident or design, and analysts have a responsibility to avoid both. Recognizing these traps protects your own credibility and helps you critically evaluate reports made by others.</p><h2>Common Misleading Chart Techniques</h2><p>Truncating a bar chart's y-axis to not start at zero exaggerates small differences; using inconsistent time intervals on a line chart distorts trend perception; showing percentages without stating the base number can hide a tiny sample size.</p><pre><code>Misleading: Bar chart y-axis from 90 to 100 makes a 2-point difference look huge
Honest: Bar chart y-axis from 0 to 100 shows the true proportional difference</code></pre><h2>Statistical Traps to Watch For</h2><p>Cherry-picking a favorable time window, reporting an average without mentioning sample size, and comparing groups of very different sizes without noting it are all common ways numbers get distorted, intentionally or not. Avoiding every one of these in your final project's dashboard and report is essential, because a single misleading chart can undermine trust in an otherwise excellent analysis.</p>""",
            "key_concepts": ["truncated axes", "cherry-picked time windows", "misleading percentages", "analyst credibility"],
            "practical_exercise": {
                "title": "Identify and Fix a Misleading Chart",
                "instructions": "Deliberately create a misleading bar chart from your data (e.g. with a truncated y-axis that exaggerates a small difference), then create an honest version of the same chart with a proper zero-based axis, and write two sentences explaining how the misleading version could lead to a bad decision. Submit both charts and your explanation."
            },
            "quiz": [
                {"question": "Why does truncating a bar chart's y-axis (not starting at zero) mislead viewers?", "options": ['It has no effect on how the chart is perceived', 'It makes bars completely invisible', 'It only affects line charts, not bar charts', 'It exaggerates the visual size of small differences between bars'], "correct_index": 3, "explanation": 'A truncated y-axis makes small numeric differences appear visually much larger than they actually are, misleading viewers.'},
                {"question": 'What is a risk of reporting a percentage without stating the underlying sample size?', "options": ['Percentages are always more accurate than raw numbers', 'Sample size never affects the reliability of a percentage', 'A large-sounding percentage might come from a tiny, unreliable sample size', 'Percentages cannot be calculated without a base number'], "correct_index": 2, "explanation": 'A striking percentage can be misleading if it comes from a very small sample, since small samples are less statistically reliable.'},
                {"question": "What does 'cherry-picking a time window' mean in the context of misleading analysis?", "options": ['Deliberately choosing a favorable time period that supports a desired conclusion while ignoring the full picture', 'Randomly selecting data with no bias', 'Using all available historical data', 'Analyzing data from multiple unrelated companies'], "correct_index": 0, "explanation": 'Cherry-picking a time window means selectively choosing a period that favors a particular narrative rather than showing the complete, honest trend.'}
            ],
            "resources": [
                {"label": "Khan Academy: Statistics", "url": "https://www.khanacademy.org/math/statistics-probability"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Advanced Analysis and Real-World Judgment",
            "title": "Turning Analysis into a Business Recommendation",
            "learning_objective": "By the end of this class, you will be able to translate a data finding into a specific, actionable business recommendation.",
            "duration_minutes": 25,
            "content_html": """<p>"Sales in Kano are declining" is a finding, not a recommendation. Turning a finding into something a manager can actually act on, with a specific suggested action and expected impact, is the final and most valuable step of any analysis, and it is the step beginners most often skip.</p><h2>From Finding to Recommendation</h2><p>A finding describes what happened; a recommendation says what to do about it, ideally with a reason grounded in the data.</p><pre><code>Finding: "Kano sales dropped 18% in Q3, driven mainly by the Snacks category."

Recommendation: "Investigate Snacks category stock levels and pricing in Kano
specifically; if stock-outs are the cause, prioritizing restocking there could
recover an estimated 12-15% of the lost revenue based on historical demand."</code></pre><h2>Making Recommendations Specific and Grounded</h2><p>A vague recommendation like "improve marketing" is far weaker than one tied to a specific segment, number, or root cause found in the data. Every recommendation in your final project's executive summary should follow this pattern: a finding, a specific suggested action, and where possible, an estimated impact.</p>""",
            "key_concepts": ["findings vs recommendations", "root-cause grounding", "specific actionable suggestions", "estimating impact"],
            "practical_exercise": {
                "title": "Turn Three Findings into Recommendations",
                "instructions": "Write three specific findings from your dataset analysis so far (each one sentence, stating a clear fact backed by numbers), then write a specific, actionable recommendation for each finding, following the pattern of what to do and why it should help. Submit the three finding-recommendation pairs."
            },
            "quiz": [
                {"question": "What is the key difference between a 'finding' and a 'recommendation' in an analysis?", "options": ['A finding describes what happened in the data; a recommendation specifies what action to take because of it', 'They are the same thing, just worded differently', 'A recommendation never needs to be based on a finding', 'Findings are always more useful than recommendations'], "correct_index": 0, "explanation": 'A finding states an observed fact from the data, while a recommendation translates that fact into a specific suggested action.'},
                {"question": "Why is 'improve marketing' considered a weak recommendation?", "options": ['It is specific and grounded in data', 'Marketing recommendations are never useful', 'It is vague and not tied to a specific segment, cause, or number from the analysis', 'It always requires no budget to execute'], "correct_index": 2, "explanation": 'Vague recommendations lack the specificity needed to guide a real action, unlike ones tied directly to a data-backed finding.'},
                {"question": 'According to the lesson, what should a strong recommendation ideally include beyond the suggested action?', "options": ['Nothing else is needed beyond the action itself', 'A list of unrelated company policies', 'A complete redesign of the dashboard', 'An estimated impact or expected benefit grounded in the data'], "correct_index": 3, "explanation": "A strong recommendation ties the suggested action to an estimated impact, making the case for why it's worth doing."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "What Hiring Managers Look for in a Data Analyst Portfolio",
            "learning_objective": "By the end of this class, you will be able to evaluate your own analysis portfolio the way a hiring manager would and identify gaps to fix.",
            "duration_minutes": 25,
            "content_html": """<p>Most beginner data portfolios look the same: a Titanic dataset analysis with a few charts and no real business framing. Hiring managers reviewing analyst applications are looking for evidence that a candidate can handle messy real data and connect it to an actual business decision, not just make charts from a clean, famous dataset.</p><h2>What Actually Stands Out</h2><p>A project using a messier, less common dataset beats yet another Titanic analysis. Documented data-cleaning decisions beat silently pre-cleaned data. A clear written recommendation beats a dashboard with no narrative. An interactive, published dashboard beats a folder of static screenshots.</p><pre><code>Weak signal:  Titanic survival chart, no write-up, no cleaning shown
Strong signal: Real messy dataset, documented cleaning, dashboard + written recommendations</code></pre><h2>Auditing Your Own Work</h2><p>Go through your projects from this track and score them honestly against these signals. This is exactly what your final project must nail, because it is the single piece of work most likely to sit at the top of your portfolio when applying for data analyst or BI roles.</p>""",
            "key_concepts": ["portfolio signals", "hiring manager perspective", "avoiding generic datasets", "self-audit"],
            "practical_exercise": {
                "title": "Audit Your Portfolio Against Hiring Signals",
                "instructions": "List your two or three strongest projects from this track, and for each one, score it 0-2 on four signals: dataset realism/messiness, documented cleaning process, presence of a written recommendation, and dashboard interactivity/polish, for a possible 8 points per project. Submit the scores and one specific fix you will make to your weakest-scoring project."
            },
            "quiz": [
                {"question": 'Why does using a messier, real-world dataset stand out more than a commonly used clean dataset like Titanic?', "options": ['Clean, famous datasets are always more impressive', 'Messy datasets are easier to analyze correctly', 'Hiring managers never look at the underlying dataset', 'It demonstrates the ability to handle the kind of messy, imperfect data analysts actually encounter on the job'], "correct_index": 3, "explanation": 'Real business data is messy, so working with realistic, imperfect data proves practical skill beyond just following a clean tutorial dataset.'},
                {"question": 'Why does documenting the data-cleaning process strengthen a portfolio project?', "options": ['Documentation is irrelevant to hiring decisions', "It shows the reviewer the candidate's judgment and process, not just a final polished result", 'Cleaning steps should always be hidden from reviewers', 'It replaces the need for any actual analysis'], "correct_index": 1, "explanation": "Documenting cleaning decisions reveals the candidate's reasoning and judgment, which a final result alone does not show."},
                {"question": 'What does the lesson identify as a common weakness in typical beginner data portfolios?', "options": ['Overused clean datasets with no real business framing or narrative', 'Too much focus on real business questions', 'Too many documented cleaning steps', 'Excessive interactivity in dashboards'], "correct_index": 0, "explanation": 'Many beginner portfolios reuse the same famous, pre-cleaned datasets without any real business context or recommendation, making them forgettable.'}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Answering Common Data Analyst Interview Questions",
            "learning_objective": "By the end of this class, you will be able to answer common data analyst interview questions clearly, using examples from your own projects.",
            "duration_minutes": 25,
            "content_html": """<p>Data analyst interviews commonly combine technical questions (write this SQL query) with judgment questions (walk me through how you would approach this ambiguous business problem). Practicing both types, and grounding answers in your own project experience, is what makes interview performance feel natural instead of rehearsed.</p><h2>Common Analyst Interview Questions</h2><p>Expect questions like: "Walk me through a project where you found an unexpected insight," "How would you handle a dataset with 20% missing values?," and "SQL: find the top 3 customers by total spend."</p><pre><code>Q: "How would you explain a complex finding to a non-technical manager?"
A: "I'd lead with the business impact in one sentence, show one clear chart,
   then offer the specific recommendation, saving technical detail for
   follow-up questions rather than the opening explanation."</code></pre><h2>Using Your Own Projects as Evidence</h2><p>Every answer becomes stronger tied to a real project: "I actually faced this exact missing-data problem in my [dataset] analysis, and here's how I handled it..." Building this habit now means walking into interviews with concrete stories instead of generic theory.</p>""",
            "key_concepts": ["technical vs judgment interview questions", "explaining findings simply", "using project evidence", "SQL live coding questions"],
            "practical_exercise": {
                "title": "Draft Answers to Common Interview Questions",
                "instructions": "Write out your spoken answers to three questions: 'Walk me through a project where you found an unexpected insight,' 'How would you handle a dataset with significant missing values?,' and 'How would you explain a complex finding to a non-technical manager?' Each answer must reference a specific project or example from this track. Submit the three written answers."
            },
            "quiz": [
                {"question": 'What two general types of questions do data analyst interviews commonly combine?', "options": ['Only questions about salary expectations', 'Only coding questions unrelated to data', 'Technical questions (like SQL) and judgment questions (like handling ambiguous problems)', "Only questions about the company's history"], "correct_index": 2, "explanation": 'Analyst interviews typically test both hard technical skill and softer judgment about handling real, messy business problems.'},
                {"question": 'According to the lesson, how should a complex finding be explained to a non-technical manager?', "options": ['Lead with the business impact, show one clear chart, then give the recommendation', 'Start with all the technical methodology first', 'Avoid mentioning any recommendation at all', 'Only use raw numbers with no visual support'], "correct_index": 0, "explanation": 'Leading with business impact and a clear visual, saving technical depth for follow-up, communicates findings effectively to non-technical audiences.'},
                {"question": 'Why does referencing a specific project strengthen an interview answer?', "options": ['It makes the answer sound more theoretical', 'It gives the interviewer concrete, verifiable evidence of real skill rather than an abstract claim', 'Interviewers prefer answers with no examples', 'Specific examples are considered irrelevant in analyst interviews'], "correct_index": 1, "explanation": 'Concrete project examples give interviewers tangible proof of skill, making an answer far more convincing than a generic statement.'}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Presenting Data to a Non-Technical Audience",
            "learning_objective": "By the end of this class, you will be able to structure and deliver a short data presentation tailored to a non-technical audience.",
            "duration_minutes": 25,
            "content_html": """<p>An analyst who can build a brilliant model but cannot explain it clearly to a manager loses most of that work's value. Presenting findings simply, without dumbing down the substance, is a distinct skill from doing the analysis itself, and it is often what determines whether recommendations actually get acted on.</p><h2>Structuring a Short Data Presentation</h2><p>Lead with the headline finding and recommendation, not the methodology. Save technical detail for questions, not the main narrative.</p><pre><code>1. Headline: "Kano region sales dropped 18% in Q3, driven by Snacks stock-outs."
2. One supporting chart showing the trend.
3. Recommendation: "Prioritize Snacks restocking in Kano this quarter."
4. (If asked) How the analysis was done.</code></pre><h2>Avoiding Jargon and Over-Explaining Methodology</h2><p>Terms like "standard deviation," "correlation coefficient," or "IQR" mean little to a non-technical manager mid-meeting; translate them into plain business language instead. Practicing this exact structure, headline first, is what you will use to present your final project, and it is a skill that directly affects whether your analysis gets acted on or ignored.</p>""",
            "key_concepts": ["headline-first structure", "avoiding jargon", "presenting to non-technical stakeholders", "leading with the recommendation"],
            "practical_exercise": {
                "title": "Draft a Headline-First Presentation",
                "instructions": "Using a finding and recommendation from your analysis so far, write a short presentation script following the headline-first structure: headline finding and recommendation first, one supporting chart described, then the recommendation restated, with all statistical jargon translated into plain language. Submit the script."
            },
            "quiz": [
                {"question": 'What should come first when presenting data findings to a non-technical manager?', "options": ['A detailed explanation of the statistical methodology', 'The headline finding and recommendation', 'A list of every chart type considered but not used', 'The raw dataset itself'], "correct_index": 1, "explanation": 'Leading with the headline finding and recommendation immediately communicates what matters most, before any supporting detail.'},
                {"question": "Why should technical jargon like 'standard deviation' generally be avoided in a presentation to a non-technical audience?", "options": ['Jargon always makes a presentation sound more credible', 'Non-technical managers always understand statistical terms', 'Avoiding jargon removes the need for any explanation', 'It means little to a non-technical audience and can obscure rather than clarify the message'], "correct_index": 3, "explanation": 'Technical jargon can confuse a non-technical audience, so plain business language communicates the point more effectively.'},
                {"question": 'Where should detailed methodology typically go in a presentation to a business audience, according to the lesson?', "options": ['At the very beginning, before any findings', 'It should never be mentioned even if asked', 'Saved for follow-up questions, not the main narrative', 'It should replace the recommendation entirely'], "correct_index": 2, "explanation": 'Methodology detail is best reserved for follow-up questions, keeping the main presentation focused on findings and recommendations.'}
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Planning Your Final Project: Dataset, Questions, and Tool Stack",
            "learning_objective": "By the end of this class, you will be able to select a dataset, define analysis questions, and choose a tool stack for a complete end-to-end analysis project.",
            "duration_minutes": 30,
            "content_html": """<p>Starting a big analysis project without a plan usually leads to hours spent wandering through the data with no clear direction. Real analysts scope a project's questions and approach before diving in, and doing this today sets you up to deliver a polished, complete final project instead of an unfocused one.</p><h2>Choosing a Dataset and Questions</h2><p>Pick a real-world-style dataset (Nigerian e-commerce sales, telecom churn, public health stats, or a local business's records) and write down three to five specific business questions it should answer, not just "explore the data."</p><pre><code>Must-answer questions:
1. Which region/segment drives the most revenue?
2. Is there a meaningful trend over time?
3. Which factor most strongly relates to [key outcome]?</code></pre><h2>Choosing Your Tool Stack and Milestones</h2><p>Decide which combination of Excel, SQL, Power BI, and/or Python you will use, and break the remaining work into milestones: Day 1 - clean and explore, Day 2 - deep analysis and answer the key questions, Day 3 - build the dashboard, Day 4 - write the executive summary. Writing this plan today, before day 30, is exactly the project-scoping skill that keeps real analysis work focused instead of sprawling indefinitely.</p>""",
            "key_concepts": ["dataset selection", "defining analysis questions", "tool stack choice", "milestone planning"],
            "practical_exercise": {
                "title": "Write Your Final Project Plan",
                "instructions": "Choose your final project dataset (a real or realistic one you have access to), write three to five specific business questions it should answer, decide your tool stack (Excel, SQL, Power BI, and/or Python), and write a milestone plan for how you will build the analysis and dashboard. Submit this plan; it will be the direct starting point for Day 30."
            },
            "quiz": [
                {"question": "Why should a final project define specific business questions instead of just 'exploring the data'?", "options": ['Specific questions give the analysis clear direction and prevent aimless wandering through the data', 'Specific questions have no real effect on the analysis', 'Exploration is always more valuable than defined questions', 'Business questions cannot be answered with real data'], "correct_index": 0, "explanation": 'Defined questions give an analysis a clear target, keeping the work focused instead of unstructured exploration with no endpoint.'},
                {"question": 'What is the benefit of choosing a tool stack (Excel, SQL, Power BI, Python) before starting the final project?', "options": ['Tool stack choice has no effect on planning', 'Every final project must use all four tools equally', 'Choosing tools always slows down the project', 'It lets the student plan concrete milestones around specific tools rather than deciding ad hoc partway through'], "correct_index": 3, "explanation": 'Deciding the tool stack upfront allows for a concrete, realistic milestone plan rather than switching approaches mid-project.'},
                {"question": 'According to the lesson, what should the milestone plan for the final project include?', "options": ["Only a single step: 'analyze everything'", 'Distinct phases such as cleaning/exploring, deep analysis, dashboard building, and writing the executive summary', 'A plan for a completely different, unrelated project', 'No plan is needed if the dataset is interesting'], "correct_index": 1, "explanation": 'A good milestone plan breaks the project into clear phases, moving from cleaning through analysis to dashboard building and summary writing.'}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Final Project: Kick Off Analyzing Your Dataset and Building the Executive Dashboard",
            "learning_objective": "By the end of this class, you will be able to begin executing your final project plan by cleaning your dataset and running its first exploratory analysis.",
            "duration_minutes": 35,
            "content_html": """<p>Today you begin "Analyze a Real Dataset and Deliver an Executive Insights Dashboard," the capstone of this entire track. Every skill from the last 29 days, data cleaning, SQL, pivot tables, pandas, statistics, dashboard design, and business storytelling, comes together in this one project, and it is the piece of work most likely to get you shortlisted for your first data analyst or BI role.</p><h2>Turning Your Day 29 Plan into Real Work</h2><p>Start executing exactly what you scoped yesterday: load your chosen dataset, run your data-cleaning checklist (duplicates, inconsistent text, missing values), and document every cleaning decision as you make it.</p><pre><code># Example starting point
df = pd.read_csv("your_dataset.csv")
print(df.shape, df.dtypes)
df = df.drop_duplicates()
# document: "Removed 14 exact duplicate rows"</code></pre><h2>What Full Completion Looks Like</h2><p>Over the coming days of independent work, run your exploratory analysis to answer your three to five business questions, identify at least three meaningful patterns, build your interactive dashboard with clear visuals in your chosen tool, and write a one-page executive summary with specific, actionable recommendations. Each of these is a skill you already practiced this track; today's job is simply to start, with real cleaned data and a documented first analysis pass.</p>""",
            "key_concepts": ["final project kickoff", "executing the cleaning checklist", "applying the full analysis workflow", "milestone execution"],
            "practical_exercise": {
                "title": "Start Building Your Final Project",
                "instructions": "This IS the start of your final project: load your chosen dataset, run and document your full data-cleaning process (duplicates, inconsistent text, missing values), and produce an initial exploratory summary (row/column counts, key statistics, first observations). Submit the cleaned dataset, your documented cleaning log, and initial EDA summary as the beginning of your Analyze a Real Dataset and Deliver an Executive Insights Dashboard project."
            },
            "quiz": [
                {"question": "What should today's work be directly based on?", "options": ['A brand new dataset unrelated to any prior planning', 'A randomly selected tutorial dataset', 'The dataset, business questions, and tool stack chosen on Day 29', "Someone else's finished dashboard"], "correct_index": 2, "explanation": 'Day 30 begins executing the specific dataset, questions, and tool stack the student already planned out on Day 29.'},
                {"question": "Why must every data-cleaning decision be documented as part of today's work?", "options": ['Documentation is optional and can be skipped for the final project', 'It keeps the analysis transparent and defensible, which is part of what the final project is graded on', 'Cleaning decisions never affect the final analysis', 'Documentation replaces the need for actual cleaning'], "correct_index": 1, "explanation": "Documented cleaning decisions are part of the final project's required deliverable and keep the analysis process transparent and credible."},
                {"question": 'Which of these is explicitly part of what full completion of the final project requires?', "options": ['Only a cleaned spreadsheet with no dashboard or recommendations', 'A single chart with no supporting analysis', 'Skipping the executive summary since the dashboard speaks for itself', 'At least three identified patterns, an interactive dashboard, and a written executive summary with recommendations'], "correct_index": 3, "explanation": 'The final project requires the full workflow: meaningful findings, a polished dashboard, and a written summary of actionable recommendations, not just a clean dataset.'}
            ],
            "resources": [
                {"label": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning"},
                {"label": "Kaggle Learn", "url": "https://www.kaggle.com/learn"}
            ]
        }
    ]
}
