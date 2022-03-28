from models.devices.devices import Device

class Fan(Device):
    name = 'Fan'

    def __init__(self, prefix):
        self.name = f"{prefix} {self.name}"