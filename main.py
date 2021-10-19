import requests

from api_token import token
import vk_api
from time import sleep


def get_photo_ids(start, amount, owner_id, album_id="saved"):
    session = vk_api.VkApi(token=token)

    params_get_photo = {
        "owner_id": owner_id,
        "album_id": album_id,
        "count": amount,
        "offset": start
    }

    photos = session.method("photos.get", params_get_photo)

    return photos["items"]


def like_album(owner_id, photo_ids):
    session = vk_api.VkApi(token=token)

    params_like = {
        "type": "photo",
        "owner_id": owner_id,
    }

    for index, photo_id in enumerate(photo_ids, 1):
        params_like["item_id"] = photo_id['id']

        try:
            session.method("likes.add", params_like)
        except vk_api.exceptions.Captcha:
            print("Необходимо ввести капчу")
            sleep(30)
        except vk_api.exceptions.ApiError:
            print("Прервано на фотографии", index)
            break

        if index % 10 == 0:
            sleep(5)
            if index % 50 == 0:
                sleep(20)


def main():
    lisa_id = 214111638
    start_position = 1000
    number_of_photos = 100

    photo_ids = get_photo_ids(start_position, number_of_photos, lisa_id)
    like_album(lisa_id, photo_ids)


if __name__ == '__main__':
    main()
