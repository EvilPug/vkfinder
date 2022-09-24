from collections import Counter
from copy import deepcopy
import requests as rq
import time
import json
import os


vk = {
    'domain': 'https://api.vk.com/method',
    'version': '5.103',
    'service_token': '4d2c09574d2c09574d2c0957d24d49e4c644d2c4d2c095716a712aec8566434d2797899',
    'access_token': '8e5a0f8340bd67c62f1fc0b4a9b5ac1a2d1362a972a3f5457d1fea485a540b1d35b139b8bcdeea3c439b9',
    'token_link': 'https://oauth.vk.com/authorize?client_id=6679953&display=page&scope=friends&response_type=token&v=5.103&state=123456',
}


def get(url: str, params={}, timeout=5, max_retries=10):

    for n in range(max_retries):
        try:
            response = rq.get(url, params=params, timeout=(timeout, 3))
            return response
        except rq.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            delay = 0.3 * 2 ** n
            time.sleep(delay)


def count_items(group_id):

    query_params = {
        'access_token': vk['access_token'],
        'group_id': group_id,
        'v': vk['version']
    }

    query = "{domain}/groups.getMembers?".format(domain=vk['domain'])
    response = get(query, query_params)

    try:
        count = round(response.json()['response']['count'])
    except KeyError:
        print(response.json())

    return count


def get_user_info(user_ids: list, fields="", offset=0) -> dict:

    time.sleep(0.33)


    fields = 'photo_id, verified, sex, bdate, city, country, home_town, \
    has_photo, photo_50, photo_100, photo_200_orig, photo_200, \
    photo_400_orig, photo_max, photo_max_orig, online, domain, \
    has_mobile, contacts, site, education, universities, schools, \
    status, last_seen, followers_count, common_count, occupation, \
    nickname, relatives, relation, personal, connections, exports, \
    activities, interests, music, movies, tv, books, games, about, \
    quotes, can_post, can_see_all_posts, can_see_audio, \
    can_write_private_message, can_send_friend_request, is_favorite, \
    is_hidden_from_feed, timezone, screen_name, maiden_name, \
    career, military, \
    blacklisted_by_me, can_be_invited_group'

    query_params = {
        'access_token': vk['access_token'],
        'user_ids': str(user_ids),
        'fields': fields,
        'v': vk['version']
    }

    query = "{domain}/users.get?".format(domain=vk['domain'])

    response = get(query, query_params)

    try:
        doc = response.json()["response"]
        return doc
    except:
        print(response.text)
        return None


def count_user_subs(user_id):

    time.sleep(0.33)

    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'v': vk['version']
    }

    query = "{domain}/groups.get?".format(domain=vk['domain'])
    response = get(query, query_params)
    return response.json()['response']['count']


def get_user_friends(user_id):

    time.sleep(0.33)
    friend_list = []

    for i in range(100):

        offset = 1000 * i
        query_params = {
            'access_token': vk['access_token'],
            'user_id': user_id,
            'offset': offset,
            'count': 5000,
            'v': vk['version']
        }

        query = "{domain}/friends.get?".format(domain=vk['domain'])
        response = get(query, query_params)

        if response.json()['response']['items'] != []:
            friend_list += response.json()['response']['items']

        else:
            break

    return friend_list


def get_user_groups(user_id, fields=""):

    time.sleep(0.33)

    user_groups = []
    num = round(count_user_subs(user_id)/1000) + 1

    for i in range(num):

        time.sleep(0.33)

        offset = 1000*i
        query_params = {
            'access_token': vk['access_token'],
            'user_id': user_id,
            'offset': offset,
            'count': 1000,
            'fields': fields,
            'v': vk['version']
        }

        query = "{domain}/groups.get?".format(domain=vk['domain'])
        response = get(query, query_params)
        user_groups += response.json()['response']['items']

    return user_groups


def get_members(group_id):

    i=0
    members = []
    have_more=True

    print(f'Parsing {group_id}')

    while have_more:

        time.sleep(0.33)

        offset = 25000*i

        query_params = {
            'access_token': vk['access_token'],
            'group_id': group_id,
            'offset': offset,
            'v': vk['version']
        }

        query = "{domain}/execute.get_members?".format(domain=vk['domain'])
        response = get(query, query_params).json()


        try:
            ids = response['response']['members']
            if ids != []:
                members += ids
                mass = response['response']['mass']
                i+=1

                print(f'Parsed {len(ids)} of {mass}')
            else:
                have_more = False
        except:
            print(response)

    print('Parsed {} from {}'.format(len(members), group_id))

    return members


if __name__=='__main__':
    print('OK!')
    print(get_members('monstercat'))
