import os
import random
import datetime
import time
import zipfile
import getpass
import logging
import queue
import threading
from requests import request


class YaDiskBackup:

    """
    Class implementing the following:
    1. Walking through the 'target_directory' and adding a random digit to the file extension
    (using multithreading).
    2. Zipping 'target_directory' with modified files.
    3. Changing the archive extension to 'kek_zip'.
    4. Uploading the archive to Yandex Disk.

    Attributes
    ----------
    target_path: str
        Path to target folder. It can be specified either in an absolute (UNIX-style) or a relative
        (from the script directory) way.
    yandex_username: str
        Login to Yandex services (e-mail at yandex.ru).
    archive_name: str
        The name of archive file, created by the 'archive' method.

    Methods
    -------
    add_random_num(que: queue)
        Adds random digit to the file extension. Requires the que attribute (the queue from files to rename).
    rename_files()
        Walking through the 'target_directory' and adding a random digit to the file extension
    in multiple threads using queue.
    archive()
        Zipping 'target_directory' with modified files and changing the archive extension to 'kek_zip'.
    upload()
        Uploads the archive to Yandex Disk. !!!PLEASE NOTE!!! The function uses HTTP Basic Authentication,
        not OAuth token and therefore will require the password for Yandex Disk 'for applications'!
        How to set it: https://yandex.ru/support/id/authorization/app-passwords.html
    """

    def __init__(self, target_path: str, yandex_username: str) -> None:
        logging.basicConfig(level=logging.INFO)
        self.target_path = target_path
        self.yandex_username = yandex_username
        self.archive_name = None
        self.logger = logging.getLogger("YaDiskBackup")

    @staticmethod
    def add_random_num(que: queue) -> None:
        while True:
            job = que.get()
            filename, file_extension = os.path.splitext(job)
            file_extension = file_extension + str(random.randint(1, 9))
            os.rename(job,
                      str(filename + file_extension))
            que.task_done()

    def rename_files(self) -> None:
        que = queue.Queue()
        self.logger.info("Starting renaming files")
        for dirname, subdir, files in os.walk(self.target_path):
            for file in files:
                que.put(os.path.join(dirname, file))
        if que.qsize():
            n_thread = 2
            for _ in range(n_thread):
                th = threading.Thread(target=self.add_random_num, args=(que,), daemon=True)
                th.start()
            que.join()
        self.logger.info("Renaming succeed")

    def archive(self) -> None:
        self.logger.info("Starting archiving data")
        self.archive_name = f"backup_{datetime.datetime.now().date()}.kek_zip"
        with zipfile.ZipFile(self.archive_name, mode="w", allowZip64=True) as zf:
            for dirname, subdir, files in os.walk(self.target_path):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
        self.logger.info("Archiving succeed")

    def upload(self) -> None:
        self.logger.info("Connecting to Yandex Disk")
        headers = {"Accept": "*/*", "Expect": "100-continue", "Content-Type": "application/binary"}
        base_url = "https://webdav.yandex.ru"
        add_url = f"/{self.archive_name}"
        url = base_url + add_url
        with open(self.archive_name, "rb") as file:
            try:
                resp = request("PUT", url, headers=headers,
                               auth=(self.yandex_username,
                                     getpass.getpass(prompt="Please enter the App password for Yandex Disk: ")),
                               data=file)
                if resp.status_code != 201:
                    self.logger.info(f"Error while connecting to Yandex Disk. HTTP response code: {resp.status_code}")
                else:
                    self.logger.info("Archive uploaded successfully")
            except Exception as e:
                self.logger.error(e, exc_info=True)


if __name__ == "__main__":
    path = input("Please enter the path to the target folder: ")
    # "/home/user/Projects/Test/test/subdirectory" or "test" from "Test" directory

    yandex_login = input("Please enter your Yandex login: ")
    # your_email@yandex.ru

    try:
        if not os.path.exists(path):
            raise FileNotFoundError

        start = time.monotonic()
        test = YaDiskBackup(target_path=path, yandex_username=yandex_login)
        test.rename_files()
        test.archive()
        test.upload()

        print(f"Done in {time.monotonic() - start} sec.")
    except FileNotFoundError:
        print(f"Sorry, there is no such file or directory: {path}")


