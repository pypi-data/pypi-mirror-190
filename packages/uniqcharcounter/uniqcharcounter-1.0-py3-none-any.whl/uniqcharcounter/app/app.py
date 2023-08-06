import os
from argparse import ArgumentParser, Namespace
from typing import List, Union

from ..utils.exceptions import (CommandLineArgumentsException,
                                CustomFileNotFoundException,
                                CustomTypeErrorException)
from ..utils.functions import (count_uniq_chars_in_list,
                               count_uniq_chars_in_string)


def main() -> Union[List[int], int]:
    """
    Function for parsing command line arguments
    """
    parser = ArgumentParser(description="Function for parsing command line strings")
    parser.add_argument("--string", help="string value as args")
    parser.add_argument("--data", help="file_path as args")
    namespace_args = parser.parse_args()
    return execution_arguments_priority(namespace_args)


def execution_arguments_priority(namespace_args: Namespace) -> Union[List[int], int]:
    """
    If 2 arguments was passed - only "--data" will be executed
    """
    if not isinstance(namespace_args, Namespace):
        raise CustomTypeErrorException(
            f"Wrong data type {type(namespace_args)}, must be a {Namespace}"
        )
    data, string = namespace_args.data, namespace_args.string
    if not data and not string:
        raise CommandLineArgumentsException(
            f"Required argument '--string' or '--data' is missing"
        )
    if data:
        return count_uniq_chars_in_list(read_file(data))
    elif string:
        return count_uniq_chars_in_string(string)


def read_file(file_path: str) -> List[str]:
    """Reading and preparing file before well be used by function"""
    if not os.path.exists(file_path):
        raise CustomFileNotFoundException(
            f"No such file or directory: '{file_path}'"
        )
    else:
        with open(file_path) as file:
            return [line.strip("\n") for line in file.readlines()]
