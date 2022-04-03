from models.devices.devices import Device


class Light(Device):

    def __init__(self,name,address):
        Device.__init__(self,name,address)
        
