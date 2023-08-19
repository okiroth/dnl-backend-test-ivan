import psycopg2
import psycopg2.extras
import json

def save_data_to_DB():
    file_data = open('results.json', 'r')
    data = json.loads(file_data.read())
    file_data.close()

    file_schema = open('DB_SCHEMA.sql', 'r')
    schema = file_schema.read()
    file_schema.close()

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="db",
        database="urparts",
        user="ivan",
        password="some123"
    )
    cursor = connection.cursor()

    cursor.execute(schema)
    connection.commit()

    print('SAVING DATA')

    # Iterate through the JSON data and insert into the tables
    for brand in data["brands"]:
        brand_name = brand["name"]
        brand_url = brand["url"]

        cursor.execute("INSERT INTO brands (name, url) VALUES (%s, %s) RETURNING id", (brand_name, brand_url))
        brand_id = cursor.fetchone()[0]

        for category in brand["categories"]:
            category_name = category["name"]
            category_url = category["url"]

            cursor.execute("INSERT INTO categories (brand_id, name, url) VALUES (%s, %s, %s) RETURNING id", (brand_id, category_name, category_url))
            category_id = cursor.fetchone()[0]
            
            for model in category["models"]:
                model_name = model["name"]
                model_url = model["url"]

                cursor.execute("INSERT INTO models (category_id, name, url) VALUES (%s, %s, %s) RETURNING id", (category_id, model_name, model_url))
                model_id = cursor.fetchone()[0]

                psycopg2.extras.execute_values(cursor, """
                    INSERT INTO model_parts (model_id, code, name, url) VALUES %s;
                    """, [
                        (model_id, part.get('code', ''), part['name'], part['url']) for part in model["model_parts"]
                    ])
                
                print(f"{brand_name} -> {category_name} -> {model_name} -> {len(model['model_parts'])} parts")

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

    print('DATA SAVED')