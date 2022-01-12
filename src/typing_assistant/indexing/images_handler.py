import asyncio
import pickle
from io import BytesIO
from typing import Dict, List

from PIL import Image

import aiohttp

import matplotlib.pyplot as plt


class ImagesHandler:

    DUMP_PATH: str = 'binaries/images_handler.pkl'

    def __init__(self):
        self.images_url: Dict[int, str] = None

    def dump(self):
        with open(ImagesHandler.DUMP_PATH, 'wb') as fp:
            pickle.dump(self, fp)

    def set_images_url(self, images_url: Dict[int, str]):
        self.images_url = dict(images_url)

    @staticmethod
    async def get_image(session: aiohttp.ClientSession, url: str) -> bytes:
        try:
            async with session.get(url=url) as response:
                return await response.read()
        except Exception as e:
            print('Unable to get url {} due to {}.'.format(url, e.__class__))

    @staticmethod
    async def get_images(urls: List[str]) -> List[bytes]:
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(*[ImagesHandler.get_image(session, url) for url in urls])

    @staticmethod
    async def __draw_image(raw_image: bytes):
        img = Image.open(BytesIO(raw_image))
        plt.figure()
        plt.imshow(img)
        #  plt.show()

    @staticmethod
    async def __draw_images(raw_images: List[bytes]):
        await asyncio.gather(*[ImagesHandler.__draw_image(image) for image in raw_images])

    def download_images(self, doc_ids: List[int]) -> List[bytes]:
        urls = [self.images_url[doc_id] for doc_id in doc_ids]
        return asyncio.run(ImagesHandler.get_images(urls))

    def draw_images(self, images: List[bytes]):
        asyncio.run(ImagesHandler.__draw_images(images))


def load_images_handler(images_handler_dump_path) -> ImagesHandler:
    with open(images_handler_dump_path, 'rb') as fp:
        images_handler = pickle.load(fp)
    return images_handler
