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


def update_user(user_id, email, first_name, last_name):
    try:
       
        email = email.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        # password = password.strip()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE "Classifier"."User"
                    SET "Email" = %s,
                        "FirstName" = %s,
                        "LastName" = %s
                    WHERE "UserId" = %s
                """, (email, first_name, last_name, user_id))
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






def get_category_by_name(category_name):
    """Get category details by name"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = 'SELECT "CategoryId", "CategoryName" FROM "Classifier"."Category" WHERE "CategoryName" = %s'
                cursor.execute(query, (category_name,))
                result = cursor.fetchone()
                return result
    except Exception as e:
        print("Error fetching category:", e)
        return None

def get_subcategory_by_name(subcategory_name, category_id):
    """Get subcategory details by name and category"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = '''SELECT "SubCategoryId", "SubCategoryName", "Description" 
                          FROM "Classifier"."SubCategory" 
                          WHERE "SubCategoryName" = %s AND "SubCategoryCategoryId" = %s'''
                cursor.execute(query, (subcategory_name, category_id))
                result = cursor.fetchone()
                return result
    except Exception as e:
        print("Error fetching subcategory:", e)
        return None

def update_category(category_id, new_category_name):
    """Update category name"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = 'UPDATE "Classifier"."Category" SET "CategoryName" = %s WHERE "CategoryId" = %s'
                cursor.execute(query, (new_category_name.strip(), category_id))
                conn.commit()
                print(f"Category {category_id} updated successfully")
                return True
    except Exception as e:
        print("Error updating category:", e)
        return False

# def update_subcategory(subcategory_id, new_subcategory_name, new_description):
#     """Update subcategory name and description"""
#     try:
#         with get_connection() as conn:
#             with conn.cursor() as cursor:
#                 query = '''UPDATE "Classifier"."SubCategory" 
#                           SET "SubCategoryName" = %s, "Description" = %s 
#                           WHERE "SubCategoryId" = %s'''
#                 cursor.execute(query, (new_subcategory_name.strip(), new_description.strip(), subcategory_id))
#                 conn.commit()
#                 print(f"Subcategory {subcategory_id} updated successfully")
#                 return True
#     except Exception as e:
#         print("Error updating subcategory:", e)
#         return False




from django.db import connection

def update_subcategory(current_category_name, current_subcategory_name, new_subcategory_name, new_description, new_category_name=None):
    """
    Update subcategory name, description, and optionally move it to another category.
    """
    try:
        # Step 1: Get the new category ID
        get_category_query = '''
            SELECT "CategoryId"
            FROM "Classifier"."Category"
            WHERE "CategoryName" = %s
        '''
        with connection.cursor() as cursor:
            cursor.execute(get_category_query, (new_category_name,))
            category_result = cursor.fetchone()

        if not category_result:
            raise Exception("New category not found")

        new_category_id = category_result[0]

        # Step 2: Perform the update
        update_query = '''
            UPDATE "Classifier"."SubCategory"
            SET "SubCategoryName" = %s,
                "Description" = %s,
                "SubCategoryCategoryId" = %s
            WHERE "SubCategoryName" = %s
              AND "SubCategoryCategoryId" = (
                  SELECT "CategoryId"
                  FROM "Classifier"."Category"
                  WHERE "CategoryName" = %s
              )
        '''

        with connection.cursor() as cursor:
            cursor.execute(update_query, (
                new_subcategory_name.strip(),
                new_description.strip(),
                new_category_id,
                current_subcategory_name,
                current_category_name
            ))

        return True

    except Exception as e:
        print("Error updating subcategory:", e)
        return False




def add_category(category_name):
    """Add new category"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = 'INSERT INTO "Classifier"."Category" ("CategoryName") VALUES (%s) RETURNING "CategoryId"'
                cursor.execute(query, (category_name.strip(),))
                category_id = cursor.fetchone()[0]
                conn.commit()
                print(f"Category added successfully with ID: {category_id}")
                return category_id
    except Exception as e:
        print("Error adding category:", e)
        return None

def add_subcategory(category_id, subcategory_name, description):
    """Add new subcategory"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = '''INSERT INTO "Classifier"."SubCategory" 
                          ("SubCategoryName", "Description", "SubCategoryCategoryId") 
                          VALUES (%s, %s, %s) RETURNING "SubCategoryId"'''
                cursor.execute(query, (subcategory_name.strip(), description.strip(), category_id))
                subcategory_id = cursor.fetchone()[0]
                conn.commit()
                print(f"Subcategory added successfully with ID: {subcategory_id}")
                return subcategory_id
    except Exception as e:
        print("Error adding subcategory:", e)
        return None
    



