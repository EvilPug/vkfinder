import psycopg2
from psycopg2.extensions import AsIs

from .vk_finder import *

conn = psycopg2.connect(dbname='vk', user='postgres',
                        password='postgres', host='localhost')
cur = conn.cursor()


def groups_add(groups_info) -> None:

    for num, group_info in enumerate(groups_info):

        cur.execute("ISERT INTO vk_groups (group_id, name, screen_name, " +
                    "photo_id, members_count, is_closed, type, members_list) " +
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT " +
                    "ON CONSTRAINT group_id_pkey DO NOTHING;", group_info)


def users_add(users_info) -> None:


    for raw in users_info:
        raw_copy = deepcopy(raw)
        for key in raw:
            try:
                for key2 in raw[key]:
                    raw_copy.update({'{}_{}'.format(key, key2):
                                     '{}'.format(raw_copy[key][key2])})
            except TypeError:
                continue
            try:
                raw_copy.pop(key)
            except ValueError:
                continue

        columns = raw_copy.keys()
        values = [str(raw_copy[column]) for column in columns]

        insert_statement = "INSERT INTO vk_users (%s) VALUES %s" +\
        "ON CONFLICT ON CONSTRAINT user_id_pkey DO NOTHING;"
        try:
            cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(columns)),
                                                       tuple(values))))
        except Exception as e:
            print(e)
            print(raw_copy)

        conn.commit()


def users_add_groups(user_ids: list, group_lists: list):

    for num, user_id in enumerate(user_ids):
        cur.execute("UPDATE vk_users SET group_list=%s WHERE id=%s", (group_lists[num], user_id, ))
        conn.commit()


def users_add_friends(user_ids: list, friend_lists: list):

    for num, user_id in enumerate(user_ids):
        cur.execute("UPDATE vk_users SET friend_list=%s WHERE id=%s", (friend_lists[num], user_id, ))
        conn.commit()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_ids_in_db():
    cur.execute("SELECT id FROM vk_users")
    existing_ids = list(row[0] for row in cur)
    return existing_ids


def get_user_in_db(user_id, fields):
    """
        Find user by user_id, add new if not exists.
        Add user friends and groups if not exist.
        Return user info.
    """


    cur.execute(f"SELECT {fields} FROM vk_users WHERE id={user_id};")

    if cur.rowcount == 0:
        print(f'User {user_id} does not exist in db. Adding.')

        info = get_user_info(user_id)
        users_add(info)

        user_groups = get_user_groups(user_id)
        users_add_groups([user_id], [user_groups])

        user_friends = get_user_friends(user_id)
        users_add_friends([user_id], [user_friends])

        cur.execute(f"SELECT {fields} FROM vk_users WHERE id={user_id};")

        return cur.fetchall()[0]

    else:
        cur.execute(f"SELECT group_list FROM vk_users WHERE id={user_id};")

        if cur.fetchall()[0][0] == None:
            print(f'User {user_id} exists in db, but does not have groups or friends. Adding.')

            user_groups = get_user_groups(user_id)
            users_add_groups([user_id], [user_groups])

            user_friends = get_user_friends(user_id)
            users_add_friends([user_id], [user_friends])

            cur.execute(f"SELECT {fields} FROM vk_users WHERE id={user_id};")
            return cur.fetchall()[0]

        else:
            cur.execute(f"SELECT {fields} FROM vk_users WHERE id={user_id};")
            return cur.fetchall()[0]


def add_group_users_to_db(group_id) -> None:

    n = 200 # Оптимальное количество пользователей
    count = 0
    member_ids = get_group_member_ids(group_id)
    existing_ids = get_ids_in_db()
    filtered_ids = list(set(member_ids) - set(existing_ids))
    print('Adding {} with {} members'.format(group_id, len(member_ids)))
    print('Ignoring {} already existing'.format(len(existing_ids)))

    for num, chunk in enumerate(chunks(filtered_ids, n)):

        buffer = get_user_info(user_ids = chunk)
        users_add(buffer)

        count += len(buffer)
        print('{}/{} uploaded'.format(count, len(filtered_ids)))


def add_invites_to_db(invite_list: list) -> None:

    for invite in invite_list:
        print(invite)
        try:
            cur.execute("INSERT INTO invites (invite_code, user_id, date_joined, ip_adress) VALUES (%s, %s, %s, %s)", (invite, None, None, None))
        except Exception as e:
            print(e)
    conn.commit()


def search_users(fields, city_title, limit='5'):
    cur.execute(f"SELECT {fields} FROM vk_users WHERE city_title='{city_title}' LIMIT {limit}")
    print(cur.fetchall())
    return cur.fetchall()


if __name__ == '__main__':
    print('OK!')

    # print(get_user_in_db(218902184, 'city_title, photo_200_orig, group_list'))
    # add_group_users_to_db('stlbn')
