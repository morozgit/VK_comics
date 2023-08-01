import requests
import os
from dotenv import load_dotenv, find_dotenv


def download_picture(picture):
    response = requests.get(picture)
    response.raise_for_status()
    filename = 'Comics.png'
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_response = response.json()
    comics_url = comics_response['img']
    comics_coment = comics_response['alt']
    print(comics_coment)

    download_picture(comics_url)
    load_dotenv(find_dotenv())
    client_id = os.environ.get("App_ID")
    vk_payload = {
        'client_id': client_id,
        'display': 'page',
        'scope': 'photos,groups,wall',
        'response_type': 'token',
        'v': '5.131',
        }
    vk_url_token = 'https://oauth.vk.com/authorize'
    vk_response = requests.get(vk_url_token, params=vk_payload)
    vk_response.raise_for_status()
    print(vk_response.url)

    vk_access_token = os.environ.get("ACCESS_TOKEN")
    vk_groups_payload = {
        'extended': '1',
        'filter': 'groups',
        'count': '3',
        'v': '5.131',
        'access_token': vk_access_token
    }
    vk_groups_url = 'https://api.vk.com/method/groups.get'
    vk_groups_response = requests.get(vk_groups_url, params=vk_groups_payload)
    vk_groups_response.raise_for_status()
    vk_groups = vk_groups_response.json()
    print(vk_groups)



if __name__ == '__main__':
    main()
