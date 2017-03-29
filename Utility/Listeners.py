# -*- coding: utf-8 -*-
"""
Created on 10/06/14 11.24

@author: FrancoB
"""
__author__ = 'FrancoB'


import threading
import socket
import serial
import logging
import time


class Dispatcher(threading.Thread):
    """
    This class creates a task that enqueues the received messages and,
    asynchronously, calls a list of callbacks (delegates) for each message dequeued.
    The queue is handled in FIFO mode
    """
    def __init__(self, callbackList):
        threading.Thread.__init__(self)
        self.callbackList = callbackList
        self.lock = threading.RLock()
        self.msgQueue = []
        self.stop = False
        self.start()

    def push(self, msg):
        """
        Appends a message to the queue
        """
        with self.lock:
            self.msgQueue.insert(0, msg)

    def terminate(self):
        """
        Terminates the task
        """
        self.stop = True

    def run(self):
        while not self.stop:
            msg = None
            with self.lock:
                if len(self.msgQueue) > 0:
                    msg = self.msgQueue.pop()
            if msg is not None:
                for cb in self.callbackList:
                    cb(msg)
            else:
                time.sleep(.01)


class IpListener(threading.Thread):
    """
    This creates a task that listen incoming data from a tcp/ip port and enqueue
    the received messages to a dispatcher
    Each received message is completed with a timestamp.
    """
    def __init__(self, addr, port, dispatcher):
        threading.Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.stop = False
        self.dispatcher = dispatcher

    def terminate(self):
        """
        Terminates the listening task and closes the serial port
        Messages already enqueued into dispatcher are lost
        """
        self.stop = True
        self.dispatcher.terminate()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.addr, self.port))
        while not self.stop:
            logging.debug('Waiting for connection on addr %s, port %d', self.addr, self.port)
            s.listen(1)
            conn, addr = s.accept()
            logging.info("Connected by %s" % str(addr))
            while not self.stop:
                try:
                    rawData = conn.recv(2048)
                    if not rawData: break
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S") + ".%03.0f" % ((time.clock()*1000)%1000)
                    self.dispatcher.push(timestamp + " @ " + rawData)
                    #logging.debug("[%s]" % rawData)
                except:
                    logging.info("Broken connection by remote host")
                    break
            conn.close()
        logging.info("TcpIp listener terminated")


class SerialListener(threading.Thread):
    """
    This creates a task that listen incoming data from a serial port and enqueue
    the received messages to a dispatcher.
    Each received packet is completed with a timestamp.

    Use Example:
            def onReceivedMessage(msg):
                print msg
                ...

            ...
            dispatcher = Dispatcher([onReceivedMessage])
            listener = SerialListener("COM16", dispatcher)
            self.listener.open()
    """
    def __init__(self, serialPort, dispatcher, baudrate=115200):
        threading.Thread.__init__(self)
        self.serialPort = serialPort
        self.baudrate = baudrate
        self.stop = False
        self.dispatcher = dispatcher

    def open(self):
        """
        Opens the serial port and starts listening
        """
        self.uart = serial.Serial(self.serialPort, self.baudrate, timeout=3.)
        logging.info("serial port %s open", str(self.serialPort))
        self.start()

    def terminate(self):
        """
        Terminates the listening task and closes the serial port
        Messages already enqueued into dispatcher are lost
        """
        self.stop = True
        self.dispatcher.terminate()
        self.uart.close()

    def run(self):
        if not self.uart.isOpen():
            self.uart.open()
        while not self.stop:
            toRead = self.uart.inWaiting()
            if toRead > 0:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S") + ".%03.0f" % ((time.clock()*1000)%1000)
                data = bytearray()
                #self.socket.send(timestamp)
                while toRead > 0:
                    data = data + self.uart.read(toRead)
                    for retry in range(10):
                        toRead = self.uart.inWaiting()
                        if toRead > 0:  break
                        time.sleep(0.001)
                    #logging.debug("serial port received %d bytes", len(data))
                self.dispatcher.push(timestamp + " @ " + data)
                #print "received %d bytes", len(data)
            time.sleep(0.010)


__myDict = {}
def myLogger(msg):
    global __myDict
    msg = msg.strip()
    #print msg ######
    start = msg.find("@")
    if start >= 0:
        timestamp = msg[:start]
        data = msg[start+1:].strip()
        lines = data.split("\n")
        for line in lines:
            #print "->" + line.strip() + "<-" ######
            exp = "[ \t]*(?P<name>[a-zA-Z _]+)[ \t]*:[ \t]*(?P<value>[0-9]+).*"
            res = re.search(exp, line, re.DOTALL)
            try:
                #s = res.group("name") + " ; " + int(res.group("value")) + ";"
                #print res.group("name"), "=", int(res.group("value"))
                __myDict[str(res.group("name"))] = int(res.group("value"))
            except Exception, e:
                #print e.message
                pass
        if len(__myDict) == 4:
            print timestamp + "; " + \
                  __myDict.keys()[0] + "; " + str(__myDict[__myDict.keys()[0]]) + "; " +\
                  __myDict.keys()[1] + "; " + str(__myDict[__myDict.keys()[1]]) + "; " +\
                  __myDict.keys()[2] + "; " + str(__myDict[__myDict.keys()[2]]) + "; " +\
                  __myDict.keys()[3] + "; " + str(__myDict[__myDict.keys()[3]]) + "; "
            __myDict = {}



if __name__ == "__main__":
    import re
    text = """
    received 2014-06-10 11:31:24.000 @
     Ext Batt NoLoad: 03516

     Ext Batt WithLoad: 03419
    received 2014-06-10 11:31:26.474 @
     Int Batt NoLoad: 03510

     Int Batt WithLoad: 03153
    received 2014-06-10 11:31:36.807 @
     Ext Batt NoLoad: 03514

     Ext Batt WithLoad: 03419
    """
    dispatcher = Dispatcher([myLogger])
    listener = SerialListener("COM12", dispatcher, baudrate=38400)
    listener.open()
