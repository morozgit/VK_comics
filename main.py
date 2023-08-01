import requests


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


if __name__ == '__main__':
    main()
