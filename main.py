import os
import random
import sys

import requests
from dotenv import find_dotenv, load_dotenv


def handling_error(answer):
    try:
        if answer['error']:
            raise requests.HTTPError
    except requests.HTTPError:
        error_msg = answer['error']['error_msg']
        error_code = answer['error']['error_code']
        print('Код ошибки:', error_msg)
        print('Текст ошибки:', error_code)
        sys.exit()


def download_picture(picture):
    response = requests.get(picture)
    response.raise_for_status()
    filename = 'Comics.png'
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_random_comics():
    total_comics = 2809
    url = 'https://xkcd.com/{}/info.0.json'.format(random.randrange(0, total_comics))
    response = requests.get(url)
    response.raise_for_status()
    comics_response = response.json()
    comics_url = comics_response['img']
    comics_comment = comics_response['alt']
    download_picture(comics_url)
    return comics_comment


def get_upload_address(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'v': '5.131',
    }
    response = requests.get(
        url,
        params=payload
        )
    vk_answer = response.json()
    handling_error(vk_answer)
    response.raise_for_status()
    return vk_answer


def upload_picture_to_server(upload_url):
    with open('Comics.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    vk_answer = response.json()
    handling_error(vk_answer)
    response.raise_for_status()
    return vk_answer


def save_picture_to_wall(vk_access_token,
                         vk_group_id,
                         vk_comics,
                         vk_hash,
                         vk_server):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'photo': vk_comics,
        'server': vk_server,
        'hash': vk_hash,
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    vk_answer = response.json()
    handling_error(vk_answer)
    response.raise_for_status()
    return vk_answer


def publish_picture_to_wall(vk_access_token,
                            vk_group_id,
                            comics_coment,
                            vk_save_photo_owner_id,
                            vk_save_photo_id):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': vk_access_token,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': 'photo{0}_{1}'.format(vk_save_photo_owner_id,
                                             vk_save_photo_id),
        'message': comics_coment,
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    vk_answer = response.json()
    handling_error(vk_answer)
    response.raise_for_status()


def main():
    load_dotenv(find_dotenv())
    vk_access_token = os.environ["VK_ACCESS_TOKEN"]
    vk_group_id = os.environ["VK_GROUP_ID"]
    try:
        comics_comment = download_random_comics()
        vk_server_url = get_upload_address(vk_access_token, vk_group_id)
        upload_url = vk_server_url['response']['upload_url']
        vk_answer_upload = upload_picture_to_server(upload_url)
        vk_comics = vk_answer_upload['photo']
        vk_hash = vk_answer_upload['hash']
        vk_server = vk_answer_upload['server']
        vk_answer_post = save_picture_to_wall(vk_access_token,
                                                    vk_group_id,
                                                    vk_comics,
                                                    vk_hash,
                                                    vk_server)
        photo_id = vk_answer_post['response'][0]['id']
        owner_id = vk_answer_post['response'][0]['owner_id']
        publish_picture_to_wall(vk_access_token, vk_group_id, comics_comment,
                                owner_id, photo_id)
    finally:
        os.remove('Comics.png')


if __name__ == '__main__':
    main()
