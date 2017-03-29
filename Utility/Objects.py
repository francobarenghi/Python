# -*- coding: utf-8 -*-
"""
Created on 29/08/14 17.55

@author: FrancoB
"""
__author__ = 'FrancoB'


def createClassByName(classname, globalDict, localDict):
    """
    This function dynamically creates a class instance and returns it
    Actually it runs correctly if no parameters are required by class constructor
    """
    exec("__xxx = %s()" % classname, globalDict, localDict)
    return localDict["__xxx"]


