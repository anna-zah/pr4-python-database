



from tabulate import tabulate
import pass_to_server



def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")
        return None
    finally:
        cursor.close()



def log_query_to_db(connection, genre, year, actor, rating, keywords, runtime, language, countries, title):
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO query_movies_users (genre, year, actor, rating, keywords, runtime, language, countries, title)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (genre, year, actor, rating, keywords, runtime, language, countries, title))
        connection.commit()
    except Exception as e:
        print(f"Ошибка логирования: {e}")
    finally:
        cursor.close()



def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
        


def normalize_input(value, field):
    if value:
        return value.strip().title() 
    return None



def search_movies():
    genre = input("Введите жанр (или оставьте поле пустым): ").strip()
    year = input("Введите год [2009 - 2016] (или оставьте поле пустым): ").strip()
    actor = input("Введите актера (или оставьте поле пустым): ").strip()
    rating = input("Введите минимальный рейтинг фильма (или оставьте поле пустым): ").strip()
    keywords = input("Введите ключевые слова (или оставьте поле пустым): ").strip()
    runtime = input("Введите минимальную продолжительность (в минутах, или оставьте поле пустым): ").strip()
    language = input("Введите язык (или оставьте поле пустым): ").strip()
    countries = input("Введите страну (или оставьте поле пустым): ").strip()



    genre = normalize_input(genre, 'genre') if genre else None
    year = safe_int(year) if year else None
    actor = normalize_input(actor, 'actor') if actor else None
    rating = safe_float(rating) if rating else None
    keywords = normalize_input(keywords, 'keywords') if keywords else None
    runtime = safe_int(runtime) if runtime else None
    language = normalize_input(language, 'language') if language else None
    countries = normalize_input(countries, 'country') if countries else None
    print(f"Genre: {genre}, Year: {year}, Actor: {actor}, Rating: {rating}, Keywords: {keywords}, Runtime: {runtime}, Language: {language}, Countries: {countries}")


 
    log_conn = connect_to_log_database()
    log_query_to_db(log_conn, genre, year, actor, rating, keywords, runtime, language, countries, None)
    log_conn.close()



    conditions = []
    params = []

    if genre:
        conditions.append("genres LIKE %s")
        params.append(f"%{genre}%")
    if year:
        conditions.append("year = %s")
        params.append(year)
    if actor:
        conditions.append("cast LIKE %s")
        params.append(f"%{actor}%")
    if rating is not None:
        conditions.append("imdb.rating >= %s")
        params.append(rating)
    if keywords:
        conditions.append("(title LIKE %s OR plot LIKE %s)")
        params.extend([f"%{keywords}%", f"%{keywords}%"])
    if runtime is not None:
        conditions.append("runtime >= %s")
        params.append(runtime)
    if language:
        conditions.append("languages LIKE %s")
        params.append(f"%{language}%")
    if countries:
        conditions.append("countries LIKE %s")
        params.append(f"%{countries}%")



    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT title, year, `imdb.rating`, genres, runtime, languages, countries
        FROM movies
        WHERE {where_clause}
    """


    imdb_conn = connect_to_imdb_database()
    result = execute_query(imdb_conn, query, params)
    imdb_conn.close()

    return result, genre, year, actor, rating, keywords, runtime, language, countries



def log_titles(result, genre, year, actor, rating, keywords, runtime, language, countries):
    log_conn = connect_to_log_database()
    if result:
        for row in result:
            found_title = row[0]  
            log_query_to_db(log_conn, genre, year, actor, rating, keywords, runtime, language, countries, found_title)
    else:
        log_query_to_db(log_conn, genre, year, actor, rating, keywords, runtime, language, countries, None)
    log_conn.close()



def search_and_log_movies():
    results, genre, year, actor, rating, keywords, runtime, language, countries = search_movies()
    log_titles(results, genre, year, actor, rating, keywords, runtime, language, countries)
    print_results(results)



def print_results(results):
    if results:
        headers = ["Title", "Year", "Rating", "Genres", "Runtime", "Languages", "Countries"]
        print("Результаты поиска:")
        print(tabulate(results, headers, tablefmt="grid"))
    else:
        print("Ничего не нашлось.")
