# -*- coding: utf-8 -*-
"""
Created on 14/06/13 15.21

@author: FrancoB

This module supplies some conversion functions

"""
__author__ = 'FrancoB'


def listToStr(intList):
    """
    Receives as input a list of integers, each of which in range 0:255 and
    returns a string representing all the integers in hexadecimal form

    Examples:
    >>> listToStr([0x30,0x31,0x32,0x33,0xAB])
    '30313233AB'
    >>> listToStr(bytearray(b"\x30\x31\x32\x33\xAB"))
    '30313233AB'
    """
    data = "".join(map((lambda x: "%2.2X" % x), intList))
    return data


def strTolist(string):
    """
    Given a string as input, it returns a list of ascii codes

    Examples:
    >>> strTolist("30313233AB")
    [51, 48, 51, 49, 51, 50, 51, 51, 65, 66]
    >>> strTolist("30313233AB5")
    [51, 48, 51, 49, 51, 50, 51, 51, 65, 66, 53]
    """
    l = map(lambda x: ord(x), list(string))
    return l


def invertHexStr(message):
    """
    Inverts the content of a string representing hexadecimal numbers.

    Examples:
    >>> invertHexStr("30313233AB")
    'AB33323130'
    >>> invertHexStr("30313233AB2")
    'AB33323130'
    """
    newMsg = ""
    for i in range(len(message) / 2):
        newMsg = message[i * 2:i * 2 + 2] + newMsg
    return newMsg


def strToHex(string):
    """
    Receives as input a string representing hexadecimal numbers and
    returns a list of integers (each in range 0:255)
    Examples:
    >>> strToHex("30313233AB")
    [48, 49, 50, 51, 171]
    >>> strToHex("30313233AB5")
    [48, 49, 50, 51, 171, 5]
    """
    intList = []
    if string is not None:
        for i in range(0, len(string), 2):
            intList.append(int(string[i:i + 2], 16))
    return intList


def removeSpaces(string):
    """
    Removes any blank character from the received text.

    Example:
    >>> removeSpaces("abc def\tghi")
    'abcdefghi'
    """
    return string.replace(" ", "").replace("\t", "")


# #############################################################################
##############################################################################
####           altre funzioni ancora da mettere a posto                   ####
##############################################################################
##############################################################################
#------------------------------------------------------ in ZveiCrypto.py
def int2bigEndian_1(number, size):
    result = int2littleEndian_1(number, size)
    result.reverse()
    return result


def int2littleEndian_1(number, size):
    data = number
    result = []
    for i in range(size):
        result.append(data & 0xFF)
        data >>= 8
    return result


def textToBit64(text):
    """
    Receives as input a string and returns the same base 64 encoded

    Example:
    >>> textToBit64("MTS"), hex(textToBit64("MTS"))
    (13971, '0x3693')
    """
    text = str(text)
    number = 0
    for i in range(len(text)):
        number = number * 32 + ord(text[i]) - 64
    return number


def bit64ToText(number, maxTextLen=3):  # #########################
    """
    Receives as input a number and decodes as a string 64 bit encoded

    Example:
    >>> bit64ToText(13971)
    'MTS'
    >>> bit64ToText(13971, 2)
    'TS'
    """
    s = ""
    for i in range(maxTextLen):
        c = chr(64 + (number & 0x1F))
        number >>= 5
        s = c + s
    return s


#------------------------------------------------------ in Cipher.py
def crc16_4(self, dataList):
    """Calculates a 16 bits crc on the received data

    Arguments:
    dataList: a list of bytes. If its length is odd, it is padded with default char.

    Returns: the crc as a list of two bytes
    """
    crc = [0, 0]
    for i in range(0, len(dataList) - 1, 2):
        crc[0] ^= dataList[i]
        crc[1] ^= dataList[i + 1]
    if len(dataList) & 1:
        crc[0] ^= dataList[len(dataList) - 1]
        crc[1] ^= ord(self.paddingChar)
    return crc


#------------------------------------------------------ in DbDecode.py
def __checkData_5(dataList, chkList):
    sum_ = 0
    for i in dataList:
        sum_ += i
    if chkList[0] != (chkList[1] ^ 0xFF):
        return False
    if chkList[0] != (sum_ % 256):
        return False
    return True


#------------------------------------------------------ in DecodeLog.py
def uint32ToStr_6(value):
    s = ""
    for i in range(4):
        s = chr(value & 0xFF) + s
        value >>= 8
    return s


#------------------------------------------------------ in MBus.py
def iToHex_7(value, digit):
    """
    Converts a numeric value to a string of fixed length
    representing an hex number

    >>> iToHex_7(5, 4)
    '0005'
    >>> "%4.4X" % 5
    '0005'
    >>> iToHex_7(18446744073709551615L,16)
    'FFFFFFFFFFFFFFFF'
    >>> iToHex_7(16446744073709551615L,17)
    '0E43E9298B137FFFF'
    >>> iToHex_7(16446744073709551615L,6)
    'E43E9298B137FFFF'
    """
    return ("%%%d.%dX" % (digit, digit)) % value
    # s = hex(value)[2:]
    # if s[-1] == 'L' or s[-1] == 'l':
    #     s = s[:-1]
    # if len(s) < digit:
    #     s = "0" * (digit-len(s)) + s
    #return s


#------------------------------------------------------ in Utility.py
def hexStr2list_8(text):
    dataList = bytearray(len(text) / 2)
    for i in range(len(text) / 2):
        o = i * 2  # offset
        dataList[i] = int(text[o:o + 2], 16)
    return dataList


if __name__ == "__main__":
    #-------------------------
    s = "30313233AB"
    print "hexStr2list_8:", s, "-->", hexStr2list_8(s)
    s = "30313233AB5"
    print "hexStr2list_8:", s, "-->", hexStr2list_8(s)
    #-------------------------
    i = 13971
    print "uint32ToStr_6:", i, "-->", uint32ToStr_6(i)

    #if __name__ == "__main__":
    import doctest

    doctest.testmod()
