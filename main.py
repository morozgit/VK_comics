import requests
import os
from dotenv import load_dotenv, find_dotenv
import random


def download_picture(picture):
    response = requests.get(picture)
    response.raise_for_status()
    filename = 'Comics.png'
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_address_server(vk_access_token):
    vk_groups_address_server_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_groups_address_server_payload = {
        'access_token': vk_access_token,
        'group_id': 221841479,
        'v': '5.131',
    }
    vk_groups_address_server_response = requests.get(
        vk_groups_address_server_url,
        params=vk_groups_address_server_payload
        )
    vk_groups_address_server_response.raise_for_status()
    vk_groups_address_server = vk_groups_address_server_response.json()
    return vk_groups_address_server

def upload_picture_to_server(vk_server_url):
    with open('Comics.png', 'rb') as file:
        # url = 'https://pu.vk.com/c842229/ss2120/upload.php?act=do_add&mid=141246322&aid=-14&gid=221841479&hash=524a084e53e41ed076465bb760958a9d&rhash=f5f90a684d4781a4eaad7adda9f6678e&swfupload=1&api=1&wallphoto=1'
        url_for_upload = vk_server_url['response']['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url_for_upload, files=files)
    response.raise_for_status()
    comics_in_server = response.json()['photo']
    hash_in_server = response.json()['hash']
        # print('hash_in_server', hash_in_server)
        # print('comics_in_server', comics_in_server)
        # print(response.json())



def main():
    #Скачивание комикса
    total_comics = 2809
    url = 'https://xkcd.com/{}/info.0.json'.format(random.randrange(0,total_comics))
    response = requests.get(url)
    response.raise_for_status()
    comics_response = response.json()
    comics_url = comics_response['img']
    comics_coment = comics_response['alt']
    print(comics_response)
    download_picture(comics_url)

    #Получение ссылки ACCESS_TOKEN
    load_dotenv(find_dotenv())
    # client_id = os.environ.get("App_ID")
    # vk_payload = {
    #     'client_id': client_id,
    #     'display': 'page',
    #     'scope': 'photos,groups,wall',
    #     'response_type': 'token',
    #     'v': '5.131',
    #     }
    # vk_url_token = 'https://oauth.vk.com/authorize'
    # vk_response = requests.get(vk_url_token, params=vk_payload)
    # vk_response.raise_for_status()
    # print(vk_response.url)

    #Получения списка групп
    vk_access_token = os.environ.get("ACCESS_TOKEN")
    # print('vk_access_token', vk_access_token)
    vk_groups_payload = {
        'extended': '1',
        'filter': 'groups',
        'count': '3', # в ответе 3 группы
        'v': '5.131',
        'access_token': vk_access_token
    }
    vk_groups_url = 'https://api.vk.com/method/groups.get'
    vk_groups_response = requests.get(vk_groups_url, params=vk_groups_payload)
    vk_groups_response.raise_for_status()
    vk_groups = vk_groups_response.json()
    # print(vk_groups)

    vk_server_url = get_address_server(vk_access_token)

    

    # Сохранение картинки на стене сообщества
    # vk_group_token = os.environ.get('GROUP_TOKEN')
    vk_save_photo_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_save_photo_payload = {
        'access_token': vk_access_token,
        'group_id': 221841479,
        'photo': comics_in_server,
        'server': 842229,
        'hash': hash_in_server,
        'v': 5.131,
    }
    vk_save_photo_response = requests.post(vk_save_photo_url, params=vk_save_photo_payload)
    vk_save_photo_response.raise_for_status()
    vk_save_photo_id = vk_save_photo_response.json()['response'][0]['id']
    vk_save_photo_owner_id = vk_save_photo_response.json()['response'][0]['owner_id']
    # print(vk_save_photo_id, vk_save_photo_owner_id)

    # Публикация картинки на стене сообщества
    vk_publish_photo_url = 'https://api.vk.com/method/wall.post'
    vk_publish_photo_payload = {
        'access_token': vk_access_token,
        'owner_id': -221841479,
        'from_group': 1,
        'attachments': 'photo{0}_{1}'.format(vk_save_photo_owner_id, vk_save_photo_id),
        'message': comics_coment,
        'v': 5.131,
    }
    vk_publish_photo_response = requests.post(vk_publish_photo_url, params=vk_publish_photo_payload)
    vk_publish_photo_response.raise_for_status()
    # print(vk_publish_photo_response.json())


if __name__ == '__main__':
    main()
