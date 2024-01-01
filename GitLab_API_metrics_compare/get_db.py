#!/usr/bin/env python3
"""
    The script will download users database from Gitlab
"""

import os
import time
import requests
from globals import *

# import globals
# import json


def dl_data_files(url, token, request, s_dir):
    """Download json files"""
    page = 1
    max_page_count = 120
    # create directory to store JSON files
    os.makedirs(s_dir, exist_ok=True)
    # get JSON files
    while True:
        with open(f"{s_dir}/{page}.json", "wb") as file_stream:
            request_handler = requests.get(
                f"{url}?{request}&page={page}",
                allow_redirects=True,
                timeout=30,
                headers={
                    "PRIVATE-TOKEN": token,
                    "Accept": "application/json",
                    "encoding": "utf-8",
                },
            )
            if request_handler.status_code != 200:
                raise ConnectionError
            if len(request_handler.content) > 10:
                print(f"URI = {url}?{request}&page={page}")
                page += 1
            else:
                return
            file_stream.write(request_handler.content)
        time.sleep(3)  # Sleep for 3 seconds
        if page > max_page_count:
            print("Maximum allowed number of iterations exceeded")
            exit(0)


def dl_prod_data():
    """Get only data from production Gitlab server"""
    # get prod users
    dl_data_files(
        f"{GITLAB_PROD_SRV}{GITLAB_API_PATH}{GITLAB_API_FOR_USR}",
        GITLAB_PROD_ACCESS_TOKEN,
        GITLAB_API_REQUEST,
        PROD_USR_DIR,
    )

    # get prod projects
    dl_data_files(
        f"{GITLAB_PROD_SRV}{GITLAB_API_PATH}{GITLAB_API_FOR_PROJECTS}",
        GITLAB_PROD_ACCESS_TOKEN,
        GITLAB_API_REQUEST,
        PROD_PROJECT_DIR,
    )


def dl_restored_data():
    """Get only data from restored Gitlab"""
    # get restored users
    dl_data_files(
        f"{GITLAB_RESTORED_SRV}{GITLAB_API_PATH}{GITLAB_API_FOR_USR}",
        GITLAB_RESTORED_ACCESS_TOKEN,
        GITLAB_API_REQUEST,
        RESTORED_USR_DIR,
    )

    # get restored projects
    dl_data_files(
        f"{GITLAB_RESTORED_SRV}{GITLAB_API_PATH}{GITLAB_API_FOR_PROJECTS}",
        GITLAB_RESTORED_ACCESS_TOKEN,
        GITLAB_API_REQUEST,
        RESTORED_PROJECT_DIR,
    )


def main():
    """Main"""
    dl_prod_data()
    dl_restored_data()


if __name__ == "__main__":
    main()
