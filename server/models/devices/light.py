from models.devices.devices import Device


class Light(Device):

    def __init__(self,name,method,address):
        Device.__init__(self,name,method,address)
        
