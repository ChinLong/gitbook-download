#!/usr/bin/python

import hashlib
import json
import os
import urllib.request


def sha256_checksum(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(), b''):
            sha256.update(block)
    return sha256.hexdigest()


def remote_sha256_checksum(url):
    sha256 = hashlib.sha256()
    with urllib.request.urlopen(url) as f:
        for block in iter(lambda: f.read(), b''):
            sha256.update(block)
    return sha256.hexdigest()


def download_file(url, file_name):
    urllib.request.urlretrieve(url, file_name)


def gitbook_download():
    path = './books/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open('./gitbook.json', 'r') as file:
        json_data = json.load(file)
        for js in json_data:
            file_name = js['name']
            file_url = js['url']
            file_path = path + file_name
            if os.path.isfile(file_path):
                old_sha256 = sha256_checksum(file_path)
                new_sha256 = remote_sha256_checksum(file_url)
                if old_sha256 != new_sha256:
                    download_file(file_url, file_path)
            else:
                download_file(file_url, file_path)


if __name__ == '__main__':
    gitbook_download()
