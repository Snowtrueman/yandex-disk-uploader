import logging
import os
import zipfile
import time


class YaDiskDecrypt:

    """
    Class implementing the following:
    1. Renaming the provided zip archive with 'kek_zip' extension.
    2. Unzipping it to the cwd.
    3. Normalizing the extension of the files in unzipped folder (removing the random number from extension
    added in 'encrypt.py').

    Attributes
    ----------
    archive_name: str
        The name of archive file provided by user.
    target_path: str
        The name of unzipped folder.

    Methods
    -------
    remove_random_num(target_path: str)
        Normalizes the extension of the files in unzipped folder. Requires the 'target_path' attribute
        (the name of unzipped folder).
    decrypt()
        Removes the random number from extension.
    unarchive()
        Unzips the archive to the current working directory.

    !!!PLEASE NOTE!!!
    In the beginning of the work the script will ask for the archive name. It can be specified either in
    an absolute (UNIX-style) or a relative (from the script directory) way.
    """

    def __init__(self, archive_name: str) -> None:
        logging.basicConfig(level=logging.INFO)
        self.archive_name = archive_name
        self.target_path = None
        self.logger = logging.getLogger("YaDiskDecrypt")

    @staticmethod
    def remove_random_num(target_path: str) -> None:
        filename, file_extension = os.path.splitext(target_path)
        os.rename(target_path,
                  str(filename + file_extension[:-1]))

    def decrypt(self) -> None:
        self.logger.info("Starting renaming files")
        for dirname, subdir, files in os.walk(self.target_path):
            for file in files:
                self.remove_random_num(os.path.join(dirname, file))
        self.logger.info("All files renamed successfully")

    def unarchive(self) -> None:
        self.logger.info(f"Starting unzipping {self.archive_name}")
        filename, file_extension = os.path.splitext(self.archive_name)
        self.target_path = filename
        os.rename(self.archive_name, filename + ".zip")
        os.makedirs(filename)
        with zipfile.ZipFile(filename + ".zip", 'r') as zf:
            zf.extractall(filename)
        self.logger.info("Unzipping succeed")


if __name__ == "__main__":
    archive_file = input("Please enter the path to the archive file: ")
    # "/home/user/Projects/Test/backup_2022-10-10.kek_zip" or "backup_2022-10-10.kek_zip" from "Test" directory

    if os.path.exists(archive_file):
        start = time.monotonic()
        test = YaDiskDecrypt(archive_name=archive_file)
        test.unarchive()
        test.decrypt()
        print(f"Done in {time.monotonic() - start} sec.")
    else:
        print(f"Sorry, there is no such file or directory: {archive_file}")

