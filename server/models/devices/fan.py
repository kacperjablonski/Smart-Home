from models.devices.devices import Device


class Fan(Device):
     def __init__(self,name,address):
        Device.__init__(self,name,address)
