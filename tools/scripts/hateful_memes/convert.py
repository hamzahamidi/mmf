import argparse
import hashlib
import os
import zipfile

from mmf.utils.configuration import Configuration
from mmf.utils.download import decompress, move
from mmf.utils.file_io import PathManager


class HMConverter:
    IMAGE_FILES = ["img.tar.gz"]
    JSONL_FILES = ["train.jsonl", "dev.jsonl", "test.jsonl"]
    CHECKSUM = "d8f1073f5fbf1b08a541cc2325fc8645619ab8ed768091fb1317d5c3a6653a77"

    def __init__(self):
        self.parser = self.get_parser()
        self.args = self.parser.parse_args()
        self.configuration = Configuration()

    def assert_files(self, folder):
        files_needed = self.IMAGE_FILES + self.JSONL_FILES

        for file in files_needed:
            assert PathManager.exists(
                os.path.join(folder, "data", file)
            ), f"{file} doesn't exist in {folder}"

    def get_parser(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument(
            "--zip_file",
            required=True,
            type=str,
            help="Zip file downloaded from the DrivenData",
        )

        parser.add_argument(
            "--password", required=True, type=str, help="Password for the zip file"
        )
        parser.add_argument(
            "--mmf_data_folder", required=None, type=str, help="MMF Data folder"
        )
        return parser

    def convert(self):
        config = self.configuration.get_config()
        data_dir = config.env.data_dir

        if self.args.mmf_data_folder:
            data_dir = self.args.mmf_data_folder

        print(f"Data folder is {data_dir}")
        print(f"Zip path is {self.args.zip_file}")

        base_path = os.path.join(data_dir, "datasets", "hateful_memes", "defaults")

        images_path = os.path.join(base_path, "images")
        PathManager.mkdirs(images_path)

        src = self.args.zip_file
        self.checksum(self.args.zip_file, self.CHECKSUM)
        print(f"Moving {src}")
        dest = images_path
        move(src, dest)

        print("Unzipping {src}")
        self.decompress_zip(
            dest, fname=os.path.basename(src), password=self.args.password
        )

        self.assert_files(images_path)

        annotations_path = os.path.join(base_path, "annotations")
        PathManager.mkdirs(annotations_path)
        annotations = self.JSONL_FILES

        for annotation in annotations:
            print(f"Moving {annotation}")
            src = os.path.join(images_path, "data", annotation)
            dest = annotations_path
            move(src, dest)

        images = self.IMAGE_FILES

        for image_file in images:
            print(f"Moving {image_file}")
            src = os.path.join(images_path, "data", image_file)
            dest = images_path
            move(src, dest)
            decompress(dest, fname=image_file, delete_original=False)

    def checksum(self, file, hash):
        sha256_hash = hashlib.sha256()
        destination = file

        with PathManager.open(destination, "rb") as f:
            print("Starting checksum for {}".format(os.path.basename(file)))
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() != hash:
                # remove_dir(download_path)
                raise AssertionError(
                    f"Checksum of downloaded file does not match the expected "
                    + "checksum. Please try again."
                )
            else:
                print("[ Checksum successful]")

    def decompress_zip(self, dest, fname, password=None):
        obj = zipfile.ZipFile(os.path.join(dest, fname), "r")
        if password:
            obj.setpassword(password.encode("utf-8"))
        obj.extractall(path=dest)
        obj.close()


def main():
    converter = HMConverter()
    converter.convert()


if __name__ == "__main__":
    main()
