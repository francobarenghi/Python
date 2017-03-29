# -*- coding: utf-8 -*-
"""
Created on 16/04/14 10.16

@author: FrancoB
"""
__author__ = 'FrancoB'

import os
import logging
logger = logging.getLogger(__name__)


def createDir(dirName):
    """
    Creates the specified folder if it doesn't exist yet.
    If the folder is into an non existent path, it creates the path too
    """
    try:
        normalizePath(dirName)
        if os.path.exists(dirName):
            logging.debug("folder '%s' already exists", dirName)
            return
        os.mkdir(dirName)
        logging.debug("created folder '%s'", dirName)
    except OSError:
        path, folder = os.path.split(dirName)
        createDir(path)
        createDir(dirName)


def removeDir(path):
    """
    Removes a directory tree
    """
    normalizePath(path)
    if os.path.exists(path):
        os.system("rmdir /S /Q \"%s\"" % path)


def copyDir(source, dest):
    """
    Copies a directory tree into another
    """
    source = normalizePath(source)
    dest = normalizePath(dest)
    os.system("robocopy \"%s\" \"%s\" /S >nul" % (source, dest))


def normalizePath(path):
    """
    changes any occurrence of the "\\" windows path separator with the generic world-wide-used "/"
    separator into the given path
    """
    s = path.replace("\\", "/")
    return s

