#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

tools: tools contains the class Tools.

Classes:
    Tools: Tools contains some tools.

Methods:
        full_name(directory, file_name):
        Returns the full name of a subdirectory and a file name.
"""

import os


class Tools:
    """Tools contains some tools."""

    @staticmethod
    def full_name(directory, file_name):
        '''

        Returns the full name of a subdirectory and a file name.

            Args:
                directory (str): The subdirectory of the file.
                file_name (str): The file name.

            Returns:
                full_name (str): The full name of the file.
        '''
        working_directory = os.path.dirname(__file__)
        if directory.find("/"):
            directories = directory.split("/")
        elif directory.find("\\"):
            directories = directory.split("\\")
        directory = ""
        for subdirectory in directories:
            directory = os.path.join(directory, subdirectory)
        return os.path.join(working_directory, directory, file_name)
