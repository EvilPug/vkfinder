import psycopg2


conn = psycopg2.connect(dbname='vk', user='postgres',
                        password='postgres', host='localhost')
cur = conn.cursor()


cur.execute("CREATE TABLE  IF NOT EXISTS vk_users (user_id INTEGER, " +
            "is_closed BOOLEAN, first_name TEXT, last_name TEXT, " +
            "sex INTEGER, bdate DATE, status TEXT, city_id INTEGER, " +
            "city_title TEXT, site TEXT, " +
            "mobile_phone TEXT, home_phone TEXT, " +
            "groups_list INTEGER [], groups_admin INTEGER [], " +
            "last_seen_plaform INTEGER, last_seen_time BIGINT, " +
            "audio TEXT [], university_name TEXT);")


conn.commit()


cur.execute("CREATE TABLE IF NOT EXISTS vk_groups (group_id INTEGER, " +
            "name TEXT, screen_name TEXT, " +
            "members_count INTEGER, is_closed BOOLEAN, type TEXT, " +
            "members_list INTEGER [])")


conn.commit()
