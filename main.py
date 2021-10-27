from time import sleep
import os
import vk_api
from dotenv import load_dotenv

def get_photo_ids(session, start, amount, owner_id, album_id="saved"):
    params_get_photo = {
        "owner_id": owner_id,
        "album_id": album_id,
        "count": amount,
        "offset": start
    }

    photos = session.method("photos.get", params_get_photo)

    return photos["items"]


def like_album(session, owner_id, photo_ids):
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
    load_dotenv()
    token = os.getenv("token")
    session = vk_api.VkApi(token=token)

    start_position = 1000
    number_of_photos = 100
    lisa_id = os.getenv("lisa_id")

    photo_ids = get_photo_ids(session, start_position, number_of_photos, lisa_id)
    like_album(session, lisa_id, photo_ids)


if __name__ == '__main__':
    main()
