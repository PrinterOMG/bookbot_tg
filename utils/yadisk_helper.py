import yadisk

from data.config import YADISK_TOKEN


async def download_book(yandex_path):
    y = yadisk.YaDisk(token=YADISK_TOKEN)

    meta = y.get_meta(yandex_path)
    file_path = f"../data/temp/{meta.name}"
    y.download(yandex_path, file_path)

    return file_path


# def check():
#     y = yadisk.YaDisk(token=YADISK_TOKEN)
#
#     [print(file.name) for file in y.listdir("disk:/PLL/Библиотека v2/I. Экономика/Кейнс Д. Общая теория занятости.pdf")]
#
# check()
