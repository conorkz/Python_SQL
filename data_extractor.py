import os
import csv
import psycopg2
from psycopg2 import sql

def extract_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = {}
        summary_text = []
        in_summary = False
        for line in file:
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                data[key] = value
            if any(line.strip().startswith(keyword) for keyword in ["1-Page Summary", "Description: About the Summary", "Critical summary review"]):
                in_summary = True
                continue
            if in_summary:
                summary_text.append(line.strip())
    keys_to_extract = ["Link", "Title", "Subtitle", "Author", "Time to read and listen",
                       "Book cover", "Amazon link", "Berlin time", "Number of reads",
                       "ISBN", "Publisher", "Published on", "Genres", "Popularity_read_count",
                       "Popularity_user_count"]
    extracted_data = {key.lower().replace(' ', '_'): data.get(key, 'No info') for key in keys_to_extract}
    extracted_data['summary_text'] = ' '.join(summary_text)
    return extracted_data

def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS extracted_data (
        id SERIAL PRIMARY KEY,
        link TEXT,
        title TEXT,
        subtitle TEXT,
        author TEXT,
        time_to_read_and_listen TEXT,
        book_cover TEXT,
        amazon_link TEXT,
        berlin_time TEXT,
        number_of_reads TEXT,
        isbn TEXT,
        publisher TEXT,
        published_on TEXT,
        genres TEXT,
        popularity_read_count TEXT,
        popularity_user_count TEXT,
        summary_text TEXT
    );
    """
    cursor.execute(create_table_query)

def process_directory(directory_path, connection):
    with connection.cursor() as cursor:
        create_table(cursor)
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    extracted_data = extract_data_from_file(file_path)
                    columns = extracted_data.keys()
                    values = extracted_data.values()
                    insert_query = sql.SQL("""
                        INSERT INTO extracted_data ({})
                        VALUES ({})
                    """).format(
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )
                    cursor.execute(insert_query, extracted_data)

        connection.commit()

if __name__ == "__main__":
    input_directory = r'YOUR_DIR'
    db_params = {
        'dbname': '-',
        'user': 'postgres',
        'password': '-',
        'host': 'localhost',
        'port': '-',
    }
    connection = psycopg2.connect(**db_params)
    try:
        process_directory(input_directory, connection)
    finally:
        connection.close()
