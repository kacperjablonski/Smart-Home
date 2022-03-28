from models.device import Device


class Fan(Device):
    def __init__(self, name):
        self.power_willmill = 0
        self.type = 'fan'
        self.rotation = False
        Device.__init__(self, name)

    def change_status(self):
        super().change_status()
        if self.status:
            self.power_willmill = 1
            return 'Włączono wiatrak'
        else:
            self.power_willmill = 0
            return 'Wyłączono wiatrak'

    def give_me_more_power(self, power):
        self.power_willmill = power
        return f'Zmieniono moc wiatraka {power}'

    def change_rotation(self):
        if self.rotation:
            self.rotation = False
            return 'Wyłączam obracanie'
        else:
            self.rotation = True
            return 'Włączam obracanie'
