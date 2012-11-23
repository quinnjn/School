#######################
# Phidget Imports
#######################
from ctypes import *
import sys
from time import sleep 
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

#Event Handler Callback Functions
def TextLCDAttached(e):
	attached = e.device
	print("TextLCD %i Attached!" % (attached.getSerialNum()))

def TextLCDDetached(e):
	detached = e.device
	print("TextLCD %i Detached!" % (detached.getSerialNum()))

def TextLCDError(e):
	try:
		source = e.device
		print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))

#LCD Text Display Object
class csss_lcd:
	str_top = ""
	str_bottom = ""
	top_len = 0
	bot_len = 0
	textLCD = None
	
	def __init__(self):
		print("INIT: LCD")
		try:
			self.textLCD = TextLCD()
		except RuntimeError as e:
			print("RuntimeExceotion: %s" % e.details)
			print("Exiting....")
			exit(1)
		
		try:
			self.textLCD.setOnAttachHandler(TextLCDAttached)
			self.textLCD.setOnDetachHandler(TextLCDDetached)
			self.textLCD.setOnErrorhandler(TextLCDError)
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting....")
			exit(1)
		
		try:
			self.textLCD.openPhidget()
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting....")
			exit(1)	
		sleep(2)		
		return

	#Information Display Function
	def display(self, row, str):
			print("Displaying %s" % str)
			if len(str) > 20:
				self.scroll(row, str)
			try:
				if self.textLCD.getDeviceID()==PhidgetID.PHIDID_TEXTLCD_ADAPTER:
						self.textLCD.setScreenIndex(0)
						self.textLCD.setScreenSize(TextLCD_ScreenSize.PHIDGET_TEXTLCD_SCREEN_2x8)
				self.textLCD.setDisplayString(row, bytes(str, 'utf-8'))
			except PhidgetException as e:
				print("Phidget Exception %i: %s" % (e.code, e.details))

	def displaySlow(self, row,str):
			self.display(row, str)
			sleep(0.75)

	def scroll(self, row, str):
			length = len(str)
			currIndex = 0
			endIndex = 20
			self.displaySlow(row, str[currIndex:endIndex])
			for currIndex in range (1,length):
				self.display(row,str[currIndex:endIndex])
				if endIndex < length:
					endIndex += 1
				sleep(0.22)
			self.clearRow(row)

	def clearRow(self, row):
			print("Clearing TextLCD")
			self.display(row, " ")

	def clearAll(self):
			self.clearRow(0)
			self.clearRow(1)

	def close(self):
		try:
			print("Closing TextLCD")
			self.textLCD.closePhidget()
		except PhidgetException as e:
			print("Phidget Exception &i: %s" % (e.code, e.details))
			print("Exiting....")
			exit(1)
