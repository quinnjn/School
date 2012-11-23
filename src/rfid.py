########################
# IMPORTS
########################
from Phidgets.Devices.RFID import RFID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, OutputChangeEventArgs, TagEventArgs


"""
RFID tags:
    Executive cards:
        single stripe 01022ea8f2
        Double stripe 1000033b7f
    Member card:
        01022fa703
"""

class csss_rfid:
	onTagCallback = None
	rfid = None
	rfid_tags = {
    	'01022EA8F2':'execA',
    	'1000033B7F':'execB',
    	'01022FA703':'member'
	}	
	def __init__(self):
		print("INIT: RFID")
		try:
		    self.rfid = RFID()
		except RuntimeError as e:
		    print("Runtime Exception: %s" % e.details)
		    print("Exiting....")
		    exit(1)

		try:
		    self.rfid.setOnAttachHandler(self.rfidAttached)
		    self.rfid.setOnDetachHandler(self.rfidDetached)
		    self.rfid.setOnErrorhandler(self.rfidError)
		    self.rfid.setOnOutputChangeHandler(self.rfidOutputChanged)
		    self.rfid.setOnTagHandler(self.rfidTagGained)
		    self.rfid.setOnTagLostHandler(self.rfidTagLost)
		except PhidgetException as e:
		    print("Phidget Exception %i: %s" % (e.code, e.details))
		    print("Exiting....")
		    exit(1)

		#print("Opening phidget object....")
		try:
		    self.rfid.openPhidget()
		except PhidgetException as e:
		    print("Phidget Exception %i: %s" % (e.code, e.details))
		    print("Exiting....")
		    exit(1)

		#print("Waiting for attach....")

		try:
		    self.rfid.waitForAttach(100000)
		except PhidgetException as e:
		    print("Phidget Exception %i: %s" % (e.code, e.details))
		    try:
		        self.rfid.closePhidget()
		    except PhidgetException as e:
		        print("Phidget Exception %i: %s" % (e.code, e.details))
		        print("Exiting....")
		        exit(1)
		    print("Exiting....")
		    exit(1)
	def setOnTagCallback(self, func):
		self.onTagCallback = func
	def displayDeviceInfo():
	    print("|------------|----------------------------------|--------------|------------|")
	    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
	    print("|------------|----------------------------------|--------------|------------|")
	    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (rfid.isAttached(), rfid.getDeviceName(), rfid.getSerialNum(), rfid.getDeviceVersion()))
	    print("|------------|----------------------------------|--------------|------------|")
	    print("Antenna Status: %s " % (rfid.getAntennaOn()))

	#Event Handler Callback Functions
	def rfidAttached(self, e):
	    attached = e.device
	    print("RFID %i Attached!" % (attached.getSerialNum()))

	def rfidDetached(self, e):
	    detached = e.device
	    print("RFID %i Detached!" % (detached.getSerialNum()))

	def rfidError(self, e):
	    try:
	        source = e.device
	        print("RFID %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
	    except PhidgetException as e:
	        print("Phidget Exception %i: %s" % (e.code, e.details))

	def rfidOutputChanged(self, e):
	    source = e.device
	    print("RFID %i: Output %i State: %s" % (source.getSerialNum(), e.index, e.state))

	def rfidTagGained(self, e):
	    source = e.device
	    id = e.tag
	    if id in self.rfid_tags:
	        id = self.rfid_tags[id]
	    self.onTagCallback(id)

	def rfidTagLost(self, e):
	    source = e.device

	def close(self):
		try:
			self.rfid.closePhidget()
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting....")
			exit(1)