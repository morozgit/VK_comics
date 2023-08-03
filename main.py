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


def download_comics():
    total_comics = 2809
    url = 'https://xkcd.com/{}/info.0.json'.format(random.randrange(0, total_comics))
    response = requests.get(url)
    response.raise_for_status()
    comics_response = response.json()
    comics_url = comics_response['img']
    comics_comment = comics_response['alt']
    download_picture(comics_url)
    return comics_comment


def get_address_server(vk_access_token, vk_group_id):
    vk_groups_address_server_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_groups_address_server_payload = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
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
        url_for_upload = vk_server_url['response']['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url_for_upload, files=files)
    response.raise_for_status()
    vk_answer = response.json()
    return vk_answer


def save_picture_to_wall(vk_access_token,
                         vk_group_id,
                         comics_in_server,
                         hash_in_server,
                         vk_server):
    vk_save_photo_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_save_photo_payload = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'photo': comics_in_server,
        'server': vk_server,
        'hash': hash_in_server,
        'v': 5.131,
    }
    vk_save_photo_response = requests.post(vk_save_photo_url,
                                           params=vk_save_photo_payload)
    vk_save_photo_response.raise_for_status()
    vk_answer = vk_save_photo_response.json()
    return vk_answer


def publish_picture_to_wall(vk_access_token,
                            vk_group_id,
                            comics_coment,
                            vk_save_photo_owner_id,
                            vk_save_photo_id):
    vk_publish_photo_url = 'https://api.vk.com/method/wall.post'
    vk_publish_photo_payload = {
        'access_token': vk_access_token,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': 'photo{0}_{1}'.format(vk_save_photo_owner_id,
                                             vk_save_photo_id),
        'message': comics_coment,
        'v': 5.131,
    }
    vk_publish_photo_response = requests.post(vk_publish_photo_url,
                                              params=vk_publish_photo_payload)
    vk_publish_photo_response.raise_for_status()


def main():
    load_dotenv(find_dotenv())
    vk_access_token = os.environ.get("ACCESS_TOKEN")
    vk_group_id = os.environ.get("GROUP_ID")
    comics_comment = download_comics()
    vk_server_url = get_address_server(vk_access_token, vk_group_id)
    vk_answer_from_server = upload_picture_to_server(vk_server_url)
    comics_in_server = vk_answer_from_server['photo']
    hash_in_server = vk_answer_from_server['hash']
    vk_server = vk_answer_from_server['server']
    vk_answer_after_upload = save_picture_to_wall(vk_access_token,
                                                  vk_group_id,
                                                  comics_in_server,
                                                  hash_in_server,
                                                  vk_server)
    vk_save_photo_id = vk_answer_after_upload['response'][0]['id']
    vk_save_photo_owner_id = vk_answer_after_upload['response'][0]['owner_id']
    publish_picture_to_wall(vk_access_token, vk_group_id, comics_comment,
                            vk_save_photo_owner_id, vk_save_photo_id)


if __name__ == '__main__':
    main()
