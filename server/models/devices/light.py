from models.devices.devices import Device

class Light(Device):
    name = 'Light'

    def __init__(self, prefix):
        self.name = f"{prefix} {self.name}"