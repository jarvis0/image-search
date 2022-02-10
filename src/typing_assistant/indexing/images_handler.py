import asyncio
import pickle
from io import BytesIO
from os.path import join
from typing import Dict, List, Optional, Tuple

from PIL import Image

import aiohttp

import matplotlib.pyplot as plt

from ..context import Context


class ImagesHandler:

    DUMP_PATH: str = 'binaries/images_handler.pkl'

    @staticmethod
    async def get_image(session: aiohttp.ClientSession, url: str) -> Optional[bytes]:
        try:
            async with session.get(url=url) as response:
                return await response.read()
        except Exception as e:
            print('Unable to get url {} due to {}.'.format(url, e.__class__))
            return None

    @staticmethod
    async def get_images(urls: List[str]) -> List[bytes]:
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(*[ImagesHandler.get_image(session, url) for url in urls])

    @staticmethod
    async def __draw_image(image: bytes, caption: str):
        img = Image.open(BytesIO(image))
        plt.figure()
        plt.title(caption, wrap=True)
        plt.imshow(img)
        plt.show()

    @staticmethod
    async def __draw_images(images_captions: List[Tuple[bytes, str]]):
        await asyncio.gather(*[ImagesHandler.__draw_image(image, caption) for image, caption in images_captions])

    def __init__(self, context: Context):
        self.__max_images = context.max_images
        self.__images_url: Dict[int, str]

    @property
    def images_url(self) -> Dict[int, str]:
        return self.__images_url

    @images_url.setter
    def images_url(self, images_url: Dict[int, str]):
        self.__images_url = {**images_url}

    def get_url(self, doc_id: int) -> str:
        return self.images_url[doc_id]

    def download_images(self, doc_ids: List[int]) -> List[bytes]:
        urls = [self.images_url[doc_id] for doc_id in doc_ids][: self.__max_images]
        return asyncio.run(ImagesHandler.get_images(urls))

    def draw_images(self, images_captions: List[Tuple[bytes, str]]):
        asyncio.run(ImagesHandler.__draw_images(images_captions))

    def dump(self, root: str):
        with open(join(root, ImagesHandler.DUMP_PATH), 'wb') as fp:
            pickle.dump(self, fp)


def load_images_handler(root: str) -> ImagesHandler:
    with open(join(root, ImagesHandler.DUMP_PATH), 'rb') as fp:
        images_handler = pickle.load(fp)
    return images_handler
