#!/usr/bin/env python
########################
# IMPORTS
########################
#Basic imports
from ctypes import *
import sys
#Phidet specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, OutputChangeEventArgs, TagEventArgs

#Our imports
import rfid

########################
# Twitter Functions 
########################
def twitUserLogin(user):
    print ("%s" % user)

########################
# MAIN
########################
csss_rfid = rfid.csss_rfid()
csss_rfid.setOnTagCallback(twitUserLogin)


chr = sys.stdin.read(1)


########################
# CLOSE
########################
csss_rfid.close()
########################
# RFID
########################
exit(0)