from etl.load import get_pg_conn

def join_users_posts():
    conn = get_pg_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.id AS post_id,
            p.title AS post_title,
            p.body AS post_body,
            u.name AS user_name,
            u.email AS user_email
        FROM staging_posts p
        JOIN staging_users u ON p.user_id = u.id;
    """)

    results = cur.fetchall()

    # Convert to list of dicts
    transformed_data = [
        {
            "post_id": row[0],
            "post_title": row[1],
            "post_body": row[2],
            "user_name": row[3],
            "user_email": row[4]
        }
        for row in results
    ]

    cur.close()
    conn.close()

    return transformed_data
