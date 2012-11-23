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
import lcd

########################
# Twitter Functions 
########################
def twitUserLogin(user):
    print ("%s" % user)

########################
# MAIN
########################
#csss_rfid = rfid.csss_rfid()
#csss_rfid.setOnTagCallback(twitUserLogin)

csss_lcd = lcd.csss_lcd()
csss_lcd.displaySlow(0,"OPEN")
csss_lcd.displaySlow(1,"CLOSED")
csss_lcd.clearRow(1)
csss_lcd.displaySlow(1,"Hello")
csss_lcd.clearAll()
csss_lcd.display(1,"Herp derp derp, I'm scrollllinngg!!!")

chr = sys.stdin.read(1)


########################
# CLOSE
########################
#csss_rfid.close()
csss_lcd.close()

########################
# RFID
########################
exit(0)
