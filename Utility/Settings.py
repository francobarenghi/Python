# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 23:37:39 2010

@author: Proprietario
"""


from xml.etree.ElementTree import Element, ElementTree


class Settings():

    class NonexistentNodeException(Exception):
        def __init__(self, nodePathName):
            Exception.__init__(self, "Settings", "Node '%s' doesn't exist" % nodePathName)

    class NonexistentFileException(Exception):
        def __init__(self, filePathName):
            Exception.__init__(self, "Settings", "The file '%s' doesn't exist" % filePathName)

    def __init__(self, filePathName, createIfNonexistent=True, rootNodeName="DataSet"):
        """
        Opens and parse the xml file with the given path and name.

        :param filePathName: file name complete with path
        :type filePathName: str
        :param createIfNonexistent: if true and the file doesn't exist, the file will be created
        :type createIfNonexistent: bool
        :param rootNodeName: if a new file is created this is the root node name
        :type rootNodeName: str

        :returns: list of found Elements (or empty if none)

        :raises: NonexistentFileException if the file doesn't exist and createIfNonexistent is false

        Example:
          s = Settings("C:/temp/test.xml", True)

        """
        self.filename = filePathName
        self.xmlTree = ElementTree()
        self.separator = "/"
        try:
            self.xmlTree.parse(filePathName)
        except:
            if createIfNonexistent:
                elem = self.__createNode(rootNodeName)
                self.xmlTree._setroot(elem)
            else:
                raise self.__class__.NonexistentFileException(filePathName)

    def getXmlTree(self):
        """
        :returns the xml tree of the instance
        """
        return self.xmlTree

    def setPathSeparator(self, separator):
        """
        Specifies the separator used to write path-tree in string format

        :param separator: single char or string
        :type separator: str
        """
        self.separator = separator

    def searchNodes(self, name=None, path=None, startNode=None):
        """
        Searches all the nodes with the given name and path
........
        :param name: the name of the node
        :type name: str
        :param path: path to the node
        :type path: see __normalizePath method for more information
        :param startNode: node use as root; if None the document root is used
        :type startNode: Element
        :returns: list of found Elements (or empty if none)
        """
        pathList = self.__normalizePath(path)
        collectedNodes = []
        if startNode is None:
            startNode = self.xmlTree.getroot()
        if name is None:
            if len(pathList) > 0:
                name = pathList[-1]
                pathList.pop(-1)
            else:
                return [startNode]
        self.__search(name, pathList, startNode, collectedNodes)
        return collectedNodes

    def getNodeText(self, name=None, path=None, startNode=None):
        """
        Searches a node with the given name and path and returns its text

        The search stops at the first node found.
......... modificare
        :param name: the name of the node
        :type name: str
        :param path: path to the node
        :type path: see __normalizePath method for more information
        :param startNode: node use as root; if None the document root is used
        :type startNode: Element
        :returns: str the text of the node
        :raises: NonexistentNodeException if any node has been found
        """
        found = self.searchNodes(name, path, startNode)
        if len(found) == 0:
            raise self.__class__.NonexistentNodeException(path + self.separator + name)
        return found[0].text

    def setNodeText(self, name, text, path=None, startNode=None, create=True):
        """
        Searches a node with the given name and path and returns its text

        The search stops at the first node found.
.......
        :param name: the name of the node
        :type name: str
        :param path: path to the node
        :type path: see __normalizePath method for more information
        :param startNode: node use as root; if None the document root is used
        :type startNode: Element
        :returns: str the text of the node
        :raises: NonexistentNodeException if any node has been found
        """
        pathList = self.__normalizePath(path)
        if startNode is None:
            startNode = self.xmlTree.getroot()
        if name is None:
            if len(pathList) > 0:
                name = pathList[-1]
                pathList.pop(-1)
            else:
                raise Exception("Invalid node name and path")
        node = self.__getOrCreate(name, pathList, startNode, create)
        if node is None:
            raise self.__class__.NonexistentNodeException(path + self.separator + name)
        if text is not None:
            node.text = text

    #    def getXmlTree(self):
#        """
#        Returns the xml tree of the instance
#        """
#        return self.xmlTree

    def save(self):
        """
        Saves the xml tree changes into the source file
        """
        self.xmlTree.write(self.filename)

    def getNodeName(self, node):
        return node.tag

    def getRootNode(self):
        return self.xmlTree.getroot()

    def getNodeChildren(self, node=None, path=None):
        if node is None:
            if path is not None:
                nodes = self.searchNodes(None, path)
                if len(nodes) > 0:
                    node = nodes[0]
            if node is None:
                raise self.__class__.NonexistentNodeException("" + path)
        return list(node)
        #return node._children

#    def addElement(self, path, name, text, attr={}):
#        """
#        Given a path to a tree node, creates a node with the received
#        name, text and attributes.
#        If the path doesn't exists, it creates each node necessary to
#        create the complete path
#        ATTENTION: even if a node with the same path and name exists, a new
#                   node is created. Anyway
#        """
#        parent = self.__search(path, True)
#        elem = self.__createNode(name, text, attr)
#        parent._children.append(elem)
#        return elem

    def deleteNodeChildren(self, node=None, path=None):
        if node is None:
            if path is not None:
                nodes = self.searchNodes(None, path)
                if len(nodes) > 0:
                    node = nodes[0]
            if node is None:
                raise self.__class__.NonexistentNodeException("" + path)
        node._children = []

    def deleteNode(self, node, path=None, startNode=None):
        if node is None:
            return
        pathList = self.__normalizePath(path)
        if startNode is None:
            startNode = self.xmlTree.getroot()
        return self.__delete(node, startNode)

    def __delete(self, node, parent):
        success = False
        for index in range(len(parent._children)):
            if node == parent._children[index]:
                parent._children.pop(index)
                success = True
            else:
                success = self.__delete(node, parent._children[index])
            if success:
                return True
        return False

    def __normalizePath(self, path):
        """
        Convert supported path encoding into a list of string
        :param path: path to convert in canonical format
        :type path: - str : single string with items separated by a separator
                    - tuple : tuple of strings
                    - list : list of strings
        :returns: list of str
        """
        if isinstance(path, str):
            pathList = path.split(self.separator)
            i = 0
            while True:
                try:
                    if len(pathList[i]) == 0:
                        pathList.pop(i)
                    else:
                        i += 1
                except:
                    break
        elif isinstance(path, list):
            pathList = path
        elif isinstance(path, tuple):
            pathList = list(path)
        else:
            pathList = []
        return pathList

    def __search(self, name, pathList, parentNode, collectedNodes):
        """
        Recursive private search method
        """
        for child in list(parentNode):
            if len(pathList) == 0:
                if child.tag == name:
                    collectedNodes.append(child)
            elif child.tag == pathList[0]:
                self.__search(name, pathList[1:], child, collectedNodes)

    def __getOrCreate(self, name, pathList, parentNode, create):
        """
        Recursive private search method
        """
        if len(pathList) == 0:
            target = name
        else:
            target = pathList[0]
        for child in list(parentNode):
            if child.tag == target:
                if len(pathList) == 0:
                    return child
                else:
                    return self.__getOrCreate(name, pathList[1:], child, create)
        #node not found
        if create:
            child = self.__createNode(target)
            parentNode.append(child)
            if len(pathList) == 0:
                return child
            else:
                return self.__getOrCreate(name, pathList[1:], child, create)
        else:
            return None

#        if len(pathList) == 0:
#            elem = self.__createNode(name)
#            parentNode.append(elem)
#            return elem
#        for child in list(parentNode):
#            if len(pathList) == 0:
#                elem = self.__createNode(name)
#                parentNode.append(elem)
#                return elem
#            elif child.tag == pathList[0]:
#                return self.__getOrCreate(name, pathList[1:], child)
#        # the parent has not the searched child, create it and continue
#        elem = self.__createNode(pathList[0])
#        parentNode.append(elem)
#        return self.__getOrCreate(name, pathList[1:], elem)

    def __createNode(self, name, text="", attr={}):
        """
        Creates and returns a node with the given name, text and attributes
        """
        elem = Element( name, attr)
        elem.text = text
        elem.tail = "\n"
        return elem


#-------------------------------------------------------------------
def printList(l):
    print "list=", l
    if l is not None: print "    has length=", len(l)

if __name__ == "__main__":
    import os
    path = os.path.abspath(os.path.curdir)
    filename = os.path.join(path, "Settings.xml")
    set = Settings(filename)
    print "Versioni supportate 1 -----------------------------"
    l = set.searchNodes("supportedVersions")
    printList(l)
    print "Versioni supportate 2 -----------------------------"
    l = set.searchNodes("version","supportedVersions")
    printList(l)
    for e in l:
        l = set.searchNodes("display", startNode=e)
        printList(l)
        print set.getNodeText("display", startNode=e)," <-> ", set.getNodeText("number", startNode=e)
    print "Formato dei Dati 1 --------------------------------"
    l = set.searchNodes("nvmDataFormat")
    printList(l)
    l = set.getNodeChildren(l[0])
    for e in l:
        print set.getNodeName(e)
    print "Classi di prodotto --------------------------------"
    l = set.searchNodes("classes", "products")
    printList(l)
    l = set.getNodeChildren(l[0])
    for e in l:
        print set.getNodeText("description", startNode=e)," <-> ", set.getNodeText("value", startNode=e)
    print "Tipi di comunicazione -----------------------------"
    l = set.searchNodes("rfTypes", "products")
    printList(l)
    l = set.getNodeChildren(l[0])
    for e in l:
        print set.getNodeText("description", startNode=e)," <-> ", set.getNodeText("value", startNode=e)
    print "Versioni hardware ---------------------------------"
    l = set.searchNodes("hwVersions", "products")
    printList(l)
    l = set.getNodeChildren(l[0])
    for e in l:
        print set.getNodeText("description", startNode=e)," <-> ", set.getNodeText("value", startNode=e)







        