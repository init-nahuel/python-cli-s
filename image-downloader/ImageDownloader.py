from utils import format_name
import requests
from typing import Optional

import os


class ImageDownloader:
    """
    An image downloader class with the option for apply watermark to images

    Attributes:
        WATERMARK_RESOURCE_ENDPOINT (str): The endpoint for the watermark resource.
        TIMEOUT (int): The timeout for the requests.
    """

    WATERMARK_RESOURCE_ENDPOINT = 'https://quickchart.io/watermark'
    TIMEOUT = 10

    def __init__(self):
        pass

    def _apply_watermark(self, img_url: str, watermark_url: str) -> Optional[bytes]:
        """
        Downloads an image from a public url applying a watermark to it. The resource from where the watermark is applied is Watermark.io

        Args:
            img_url (str): The public url of the image.
            watermark_url (str): The public url of the watermark.
        Returns:
            Optional[bytes]: The image content with the watermark
        """

        json = json = {
            "mainImageUrl": img_url,
            "markImageUrl": watermark_url,
            "opacity": 1.0,
            "markRatio": 1.0,
            "position": "bottomMiddle",
            "positionX": 0.0,
            "positionY": 0.0
        }

        try:
            r = requests.get(ImageDownloader.WATERMARK_RESOURCE_ENDPOINT,
                             json=json, timeout=ImageDownloader.TIMEOUT)
            if r.status_code == 200:
                return r.content
        except Exception as e:
            print(f'{e}. Could not apply watermark to the image.')

    def _download_image(self, img_url: str) -> Optional[bytes]:
        """
        Downloads an image from a public url.

        Args:
            img_url (str): The public url of the image.
        Returns:
            Optional[bytes]: The image content.
        """
        try:
            r = requests.get(img_url, timeout=ImageDownloader.TIMEOUT)

            if r.status_code == 200:
                return r.content
        except Exception as e:
            print(
                f'{e}. Could not download the image from: {img_url}')

    def _save_image(self, img: bytes, filename: str, filepath: str = None) -> None:
        """
        Save an image to a file.

        Args:
            img (bytes): The image content.
            filename (str): The file name for the image.
            filepath (str, optional): The filepath where the image will be saved.
        Returns:
            None
        """

        if filepath:
            os.makedirs(filepath, exist_ok=True)

        filename = filepath.rstrip(
            '/') + '/' + filename.lstrip('/') if filepath else filename
        filename = format_name(filename)
        with open(filename, 'wb') as f:
            f.write(img)

    def download_image(self, img_url: str, filename: str, filepath: str = None, watermark_url: str = None) -> None:
        """
        Downloads an image from a public url. If a watermark is provided , it applies to the image.

        Args:
            img_url (str): The public url of the image.
            filename (str): The file name for the image.
            filepath (str, optional): The filepath where the image will be saved.
            watermark_url (str, optional): The public url for the watermark.
        Returns:
            None
        """

        if watermark_url:
            img = self._apply_watermark(img_url, watermark_url)
        else:
            img = self._download_image(img_url)

        self._save_image(img, filename, filepath)

    def download_images(self, img_urls: list, filenames: list, filepath: str = None, watermark_url: str = None) -> None:
        """
        Downloads a list of images from public urls. If a watermark is provided , it applies to the images.

        Args:
            img_urls (list): The public urls of the images.
            filenames (list): The file names for the images.
            filepath (str, optional): The filepath where the images will be saved.
            watermark_url (str, optional): The public url for the watermark.
        Returns:
            None
        """
        try:
            for img_url, filename in zip(img_urls, filenames, stric=True):
                self.download_image(img_url, filename, filepath, watermark_url)
        except ValueError:
            print('The number of images and filenames must be the same.')
