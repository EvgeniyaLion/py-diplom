import requests
import time
import json


def get_group(user_id, token):
    """
    Функция возвращает множество ID групп пользователя user_id.
    Если не удается получить информацию о пользовате, то возвращается
    пустое множество.
    Параметры:
    ----------
    user_id : str
        ID пользователя
    token : str
        Токен
    """
    response = requests.get(
        url='https://api.vk.com/method/groups.get',
        params=dict(
            access_token=token,
            v=5.61,
            extended=1,
            user_id=user_id
        )
    )
    victim_data = response.json()
    victim_groups = set()
    try:
        for items in (victim_data['response']['items']):
            victim_groups.add(items['id'])
        return victim_groups
    except KeyError:
        return victim_groups


def get_friends(user_id, token):
    """
    Функция возвращает список ID друзей для пользователя user_id.
    Если не удается получить информацию о пользовате, то возвращается
    пустой список.
    Параметры:
    ----------
    user_id : str
        ID пользователя
    token : str
        Токен
    """
    response = requests.get(
        url='https://api.vk.com/method/friends.get',
        params=dict(
            user_id=user_id,
            access_token=token,
            v=5.61
        )
    )
    try:
        return response.json()['response']['items']
    except KeyError:
        return []


def get_frinds_group_id(user_id, token):
    """
    Функция возвращает множество ID групп друзей для пользователя user_id
    Параметры:
    ----------
    user_id : str
        ID пользователя
    token : str
        Токен
    """
    result = set()
    friends = get_friends(user_id, token)
    for k, friend_id in enumerate(friends):
        print(f'Нашли группы {k / len(friends) * 100:.2f} % друзей', end="\r")
        friend_group = get_group(friend_id, token)
        result.update(friend_group)
        time.sleep(0.4)
    print(f'Нашли группы 100 % друзей', end="\r")
    return result

# Вводим токен и ID пользователя
token = input('Введите токен: ')
user_id = input('Введите ID или username пользователя: ')

# Если было введено username, то преобразуем его в user_id
response = requests.get(
    url='https://api.vk.com/method/users.get',
    params=dict(
        user_ids=user_id,
        access_token=token,
        v=5.61,
    )
)
user_id = response.json()['response'][0]['id']

# Считываем данные о группах
user_group = get_group(user_id, token)
user_frinds_group = get_frinds_group_id(user_id, token)
unique_group = user_group - user_frinds_group

# Записываем json файл
result = []
for k, group in enumerate(unique_group):
    # Получаем информацию об уникальных группах пользователя
    response = requests.get(
        url='https://api.vk.com/method/groups.getById',
        params=dict(
            group_id=group,
            access_token=token,
            v=5.61,
            fields='members_count'
        )
    )
    response = response.json()['response'][0]
    if 'members_count' in response.keys():
        members_count = response['members_count']
    else:
        members_count = 'Не известно'
    result.append(
        dict(
            name=response['name'],
            gid=response['id'],
            members_count=members_count
        )
    )
    time.sleep(0.4)
    print(
        f'Нашли информацию о {k/len(unique_group)*100:.2f} % уникальных группах',
        end="\r"
    )
with open('groups.json', 'w') as fout:
    json.dump(result, fout, ensure_ascii=True, indent=4)
