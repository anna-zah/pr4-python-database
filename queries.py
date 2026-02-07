


import pass_to_server


def top_movies_by_year(n, year):
    query = """
    SELECT title, COUNT(*) AS search_count
    FROM query_movies_users
    WHERE year = %s
    GROUP BY title
    ORDER BY search_count DESC
    LIMIT %s
    """
    log_conn = connect_to_log_database()
    result = execute_query(log_conn, query, (year, n))
    log_conn.close()
    return result


def top_movies_by_rating(n, min_rating):
    query = """
    SELECT title, AVG(rating) AS avg_rating
    FROM query_movies_users
    WHERE rating >= %s AND title IS NOT NULL
    GROUP BY title
    HAVING avg_rating >= %s
    ORDER BY avg_rating DESC
    LIMIT %s
    """
    log_conn = connect_to_log_database()
    result = execute_query(log_conn, query, (min_rating, min_rating, n))
    log_conn.close()
    return result


def top_actors_by_search_count(n):
    query = """
    SELECT actor, COUNT(*) AS search_count
    FROM query_movies_users
    WHERE actor IS NOT NULL
    GROUP BY actor
    ORDER BY search_count DESC
    LIMIT %s
    """
    log_conn = connect_to_log_database()
    result = execute_query(log_conn, query, (n,))
    log_conn.close()
    return result


def top_countries_by_genre_from_logs(n, genre):
    query = """
    SELECT countries, genre, COUNT(*) AS search_count
    FROM query_movies_users
    WHERE genre = %s AND countries IS NOT NULL
    GROUP BY countries, genre
    ORDER BY search_count DESC
    LIMIT %s
    """
    log_conn = connect_to_log_database()
    result = execute_query(log_conn, query, (genre, n))
    log_conn.close()
    return result


def movies_above_avg_by_genre():
    query = """
    SELECT title, genres, imdb.rating
    FROM movies m
    WHERE imdb.rating > (
        SELECT AVG(imdb.rating)
        FROM movies
        WHERE m.genres = genres
    )
    ORDER BY imdb.rating DESC
    LIMIT 20
    """
    imdb_conn = connect_to_imdb_database()
    result = execute_query(imdb_conn, query)
    imdb_conn.close()
    return result


def frequent_actors_between_years(start_year=2009, end_year=2016, limit=10):
    query = """
    SELECT actor_name, COUNT(*) AS appearances
    FROM (
        SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(cast, ',', numbers.n), ',', -1) AS actor_name
        FROM movies
        JOIN (
            SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
            UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
        ) numbers ON CHAR_LENGTH(cast) - CHAR_LENGTH(REPLACE(cast, ',', '')) >= numbers.n - 1
        WHERE year BETWEEN %s AND %s
    ) AS actors
    GROUP BY actor_name
    ORDER BY appearances DESC
    LIMIT %s
    """
    imdb_conn = connect_to_imdb_database()
    result = execute_query(imdb_conn, query, (start_year, end_year, limit))
    imdb_conn.close()
    return result
 

def long_movies_by_country():
    query = """
    SELECT title, countries, runtime
    FROM movies m
    WHERE runtime > (
        SELECT AVG(runtime)
        FROM movies
        WHERE countries = m.countries
    )
    ORDER BY runtime DESC
    LIMIT 20
    """
    imdb_conn = connect_to_imdb_database()
    result = execute_query(imdb_conn, query)
    imdb_conn.close()
    return result


def most_searched_keywords_movies(n):
    query = """
    SELECT title, COUNT(*) AS keyword_hits
    FROM query_movies_users
    WHERE keywords IS NOT NULL
    GROUP BY title
    ORDER BY keyword_hits DESC
    LIMIT %s
    """
    log_conn = connect_to_log_database()
    result = execute_query(log_conn, query, (n,))
    log_conn.close()
    return result