#!/usr/bin/env python3
"""
    The script will download users database from Gitlab
"""
import json
from globals import *

USR_KEYS = ["username", "name", "email"]
PJT_KEYS = ["path_with_namespace"]
USR_FILTER = {
    "bot": True,
    "using_license_seat": True,
    "state": "active",
    # "state": "blocked",
    # "state": "deactivated",
    "can_create_group": True,
    "can_create_project": True,
    "external": True,
    "is_admin": True,
}
PJT_FILTER = {
    "empty_repo": True,
    "archived": True,
    "issues_enabled": True,
    "ci_default_git_depth": 50,
    "only_allow_merge_if_pipeline_succeeds": True,
}


def count_records(filename: str, filter: dict) -> dict:
    """Return total count for first lvl records"""
    with open(filename, "r", encoding="utf-8") as file:
        file_contents = json.load(file)

    total = 0
    result = {}
    for key in filter.keys():
        result.update({key: 0})
    for record in file_contents:
        total += 1
        for key in filter.keys():
            if (key in record) and (filter[key] == record[key]):
                result.update(
                    {
                        key: result[key] + 1,
                    }
                )
    result.update(
        {
            "total": total,
        }
    )
    return result


def get_data_from_files(file_list: list, f_filter: dict) -> dict:
    """get data from file list"""
    report = {"total": 0}
    for key in f_filter.keys():
        report.update({key: 0})

    for file in file_list:
        tmp_report = count_records(file, f_filter)
        for key in report.keys():
            report.update({key: report[key] + tmp_report[key]})
    return report


def compare_data(dir_1: str, dir_2: str, f_filter: list) -> list:
    """Compare data in folders"""
    file_list_dir_1 = get_files(dir_1)
    file_list_dir_2 = get_files(dir_2)
    report = []
    for file_f in file_list_dir_1:
        with open(file_f, "r", encoding="utf-8") as file:
            file_contents = json.load(file)
            for record in file_contents:
                keys_dict = {}
                for key in f_filter:
                    keys_dict.update(
                        {
                            f"{key}": f"{record[key]}",
                        }
                    )
                find_stat = False
                for file_c in file_list_dir_2:
                    if search_record(file_c, keys_dict) is True:
                        find_stat = True
                        break
                if find_stat is False:
                    report.append(keys_dict)
    return report


def search_record(json_file: str, keys_dict: dict) -> bool:
    """
    Search for record with keys.
    Return True if record exists and False if does not
    """
    keys = list(keys_dict.keys())
    with open(json_file, "r", encoding="utf-8") as file:
        file_contents = json.load(file)
        for record in file_contents:
            if record[keys[0]] == keys_dict[keys[0]]:
                return True

    # return False if item was not found
    return False


if __name__ == "__main__":
    print("\n\tCompare Users metrics")
    f_list = get_files(PROD_USR_DIR)
    print("For production:", get_data_from_files(f_list, USR_FILTER))

    f_list = get_files(RESTORED_USR_DIR)
    print("For restored:  ", get_data_from_files(f_list, USR_FILTER))

    report = compare_data(PROD_USR_DIR, RESTORED_USR_DIR, USR_KEYS)
    print(f"\n\tmissing users: \n{report}")

    print("\n\tCompare Projects metrics")
    f_list = get_files(PROD_PROJECT_DIR)
    print("For production:", get_data_from_files(f_list, PJT_FILTER))

    f_list = get_files(RESTORED_PROJECT_DIR)
    print("For restored:  ", get_data_from_files(f_list, PJT_FILTER))

    report = compare_data(PROD_PROJECT_DIR, RESTORED_PROJECT_DIR, PJT_KEYS)
    print(f"\n\tmissing projects: \n{report}")

    print("\n\tCompare Test metrics to check script, nothing should be in the output")
    report = compare_data(PROD_USR_DIR, PROD_USR_DIR, USR_KEYS)
    print(f"\n\tmissing users: \n{report}")
