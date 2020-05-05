import requests
import time
import json

TOKENnetology = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

#получение списка id групп
id='171691064'
def ids_of_victim_groups():
    response = requests.get('https://api.vk.com/method/groups.get',
                            params={
                                'access_token': TOKENnetology,
                                'v': 5.52,
                                'extended': 1,
                                'user_id': id
                            })
    victim_data = response.json()
    victim_groups=[]
    for items in (victim_data['response']['items']):
        a=items['id']
        victim_groups.append(a)
    print ('Список id групп пользователя:')
    print(*victim_groups, sep=', ')
    return victim_groups

#получение всех id друзей
def friends_list_getting():
    response = requests.get('https://api.vk.com/method/friends.get?user_id=171691064',
                            params={
                                'access_token': TOKENnetology,
                                'v': 5.52,
                            })

    friends_ids=response.json()
    friends_ids_list=[]
    for items in (friends_ids['response']['items']):
        b=items
        friends_ids_list.append(b)
    return friends_ids_list

#функция вывода списка групп всех друзей
def getting_ids_groups():
    i=0
    idslist=[]
    print ('Отcчёт говорит о том, что программа работает и завершит свою работу, когда число отсчёта совпадёт с количеством друзей пользователя.')
    for ids in friends_list_getting():
            print (i)
            time.sleep(3)
            response = requests.get('https://api.vk.com/method/groups.get?user_id=171691064',
                                    params={
                                        'access_token': TOKENnetology,
                                        'v': 5.52,
                                        'extended': 1,
                                        'user_id': ids,
                                    })
            answer=response.json()
            try:
                items = (answer['response']['items'])
                for elements in items:
                    idsnumbers=elements['id']
                    idslist.append(idsnumbers)
                i += 1
            except KeyError:
                idsnumbers=''
                idslist.append(idsnumbers)
                i += 1
    return idslist

#вывод списка групп, которые есть только у пользователя
def recieving_only_victim_groups():
    victim_set=set(ids_of_victim_groups())
    friends_set=set(getting_ids_groups())
    final_set = victim_set.difference(friends_set)
    groups_names = []
    i=0
    for ids in final_set:
        time.sleep(3)
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params={
                                    'access_token': TOKENnetology,
                                    'v': 5.52,
                                    'group_ids': ids,
                                    'fields': 'name'
                                })
        answer = response.json()
        group_name = (answer['response'][0]['name'])
        groups_names.append(group_name)
        i += 1
    with open('results.json', 'w') as file:
        j = 1
        for element in groups_names:
            file.write(f'№{j} {element}\n')
            j += 1
    print ('Файл results.json, в котором сформирован список групп в ВК, в которых состоит пользователь, но не состоит никто из его друзей, находится в папке проекта.')
recieving_only_victim_groups()
