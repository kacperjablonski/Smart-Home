from models.devices.devices import Device


class Fan(Device):
     def __init__(self,name,method,address):
        Device.__init__(self,name,method,address)
