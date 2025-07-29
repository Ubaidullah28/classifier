import psycopg
import json

def get_connection():
    # Returns a connection object, not a tuple of (conn, cursor)
    return psycopg.connect(
        user='postgres',
        password='axiom@0900',
        dbname='DocumentClassifierDatabase',
        host='192.168.99.53',
        port='5432'
    )

def fetch_data(cursor):
    query = """
        SELECT
            CC."CategoryName",
            CS."SubCategoryName",
            CS."Description"
        FROM
            "Classifier"."Category" CC
        LEFT JOIN
            "Classifier"."SubCategory" CS
        ON
            CC."CategoryId" = CS."SubCategoryCategoryId"
    """
    cursor.execute(query)
    return cursor.fetchall()

def transform_to_nested_json(rows):
    category_map = {}
    for CategoryName, SubCategoryName, Description in rows:
        if CategoryName not in category_map:
            category_map[CategoryName] = []
        if SubCategoryName is not None:
            category_map[CategoryName].append({
                "SubCategoryName": SubCategoryName,
                "Description": Description
            })
    result = [
        {
            "CategoryName": cat,
            "SubCategory": subs
        }
        for cat, subs in category_map.items()
    ]
    return result

def write_to_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    output_file = "output.json"  # Define the output file name
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        rows = fetch_data(cursor)
        nested_data = transform_to_nested_json(rows)
        write_to_json_file(nested_data, output_file)
        print(f"Data exported successfully to '{output_file}'.")
    except Exception as e:
        print(":x: Error:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()