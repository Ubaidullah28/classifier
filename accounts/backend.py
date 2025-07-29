import psycopg


def get_connection():
    return psycopg.connect(
        user='postgres',
        password='axiom@0900',
        dbname='DocumentClassifierDatabase',
        host='192.168.99.53',
        port='5432'
    )

# def check_user(email, password):
#     print("Checking user with email:", email)
#     print("Checking user with password:", password)
#     with get_connection() as conn:
#         with conn.cursor() as cursor:
#             query = 'SELECT * FROM "Classifier"."User" WHERE "Email" = %s AND "Password" = %s '
#             cursor.execute(query, (email, password))
#             result = cursor.fetchone()
#             print("User check result:", result)
#             return result



def check_user(email, password):
    print("Checking user with email:", email)
    print("Checking user with password:", password)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Modified query to include isAdmin column
            query = 'SELECT "UserId", "Email", "FirstName", "LastName", "Password", "IsAdmin" FROM "Classifier"."User" WHERE "Email" = %s AND "Password" = %s '
            cursor.execute(query, (email, password))
            result = cursor.fetchone()
            print("User check result:", result)
            return result
      
    


def fetch_all_users():
    conn = get_connection()
    users = conn.execute("SELECT \"UserId\", \"Email\", \"FirstName\", \"LastName\",\"Password\"  FROM \"Classifier\".\"User\"")
    conn.close()
    return users


def update_user(user_id, email, first_name, last_name, password):
    try:
       
        email = email.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        password = password.strip()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE "Classifier"."User"
                    SET "Email" = %s,
                        "FirstName" = %s,
                        "LastName" = %s,
                        "Password" = %s
                    WHERE "UserId" = %s
                """, (email, first_name, last_name, password, user_id))
                conn.commit()
                print(f"User with ID {user_id} updated successfully.")
    except Exception as e:
        print("Error updating user:", e)




def add_user(email, first_name, last_name, password):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO "Classifier"."User" ("Email", "FirstName", "LastName", "Password")
                    VALUES (%s, %s, %s, %s)
                """, (email, first_name, last_name, password))
                conn.commit()
    except Exception as e:
        print("Error adding user:", e)