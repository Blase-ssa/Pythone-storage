"""Global variables and common functions"""
import os

GITLAB_PROD_SRV = ""  # Server 1 URL
GITLAB_RESTORED_SRV = ""  # Server 2 URL
GITLAB_PROD_ACCESS_TOKEN = ""  # Server 1 access token
GITLAB_RESTORED_ACCESS_TOKEN = ""  # Server 2 access token

GITLAB_API_PATH = "/api/v4"
GITLAB_API_FOR_USR = "/users"
GITLAB_API_FOR_PROJECTS = "/projects"
GITLAB_API_FILTER = "active=true"
GITLAB_API_PER_PAGE = "50"  # count of objects per page, affect API request and count of objects in single json file
# GITLAB_API_REQUEST = f"{GITLAB_API_FILTER}&per_page={GITLAB_API_PER_PAGE}"
GITLAB_API_REQUEST = f"per_page={GITLAB_API_PER_PAGE}"

# directory name to store json files from first server
PROD_ROOT_DIR = "prod"
PROD_USR_DIR = f"{PROD_ROOT_DIR}/users"
PROD_PROJECT_DIR = f"{PROD_ROOT_DIR}/projects"

# directory name to store json files from second server
RESTORED_ROOT_DIR = "restored"
RESTORED_USR_DIR = f"{RESTORED_ROOT_DIR}/users"
RESTORED_PROJECT_DIR = f"{RESTORED_ROOT_DIR}/projects"

EXTENSION = ".json"


def get_files(s_dir) -> list:
    """Get list o files with EXTENSION in current directory"""
    file_list = os.listdir(s_dir)
    result = []
    for filename in file_list:
        if EXTENSION in filename and os.stat(f"{s_dir}/{filename}").st_size > 0:
            result.append(f"{s_dir}/{filename}")
    return result
