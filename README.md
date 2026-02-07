# pr4-python-database
# Movie Search in MySQL (Python + Jupyter)

Movie Search in MySQL is a Python project for searching and exploring movies in a MySQL (Sakila) database. The project is implemented in Python scripts, with a Jupyter Notebook included to demonstrate the functionality and output of the searches.

## Project Goal
The goal of this project is to provide a tool for searching movies in a database, with features to:
- Search movies by title keywords
- Filter movies by genre and release year range
- Record search history and analyze popular queries

## Features
1. Movie Search
   - By keyword
     - Results limited to 10 movies per query
     - Users can continue exploring additional results
   - By genre and year range
     - Shows available genres and the full range of release years
     - Users can specify a range (e.g., 2005–2012) or a single year
     - Results displayed in batches of 10

2. Search History
   - All queries are stored in MySQL
   - Logs include query type, parameters, number of results, and timestamp

3. Statistics
   - Displays the top 5 most popular queries based on frequency and recent searches

## Technologies
- Python 3
- MySQL (Sakila database)
- Jupyter Notebook (for demonstration)
- Python modules: pymysql, pandas, prettytable

## Key Features
- Main functionality implemented in Python scripts
- Jupyter Notebook for interactive demonstration of results
- Readable and modular code with proper error handling
- Easy to extend with additional filters (e.g., by rating or country)
