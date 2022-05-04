from models.device import Device


class Fan(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.power_willmill = 0
        self.type = 'fan'
        self.rotation = False
        self.method = {'on/off': self.change_status,
                        'zmień moc': self.give_me_more_power,
                        'rotacja': self.change_rotation}

    @property
    def get_method(self):
        method ={'on/off': self.status,
                'zmień moc': self.power_willmill,
                'rotacja': self.rotation}
        return method

    def __call__(self,chose_method):
        return self.method[chose_method]()

    def change_status(self):
        super().change_status()
        if self.status:
            self.power_willmill = 1
            return 'Włączono wiatrak'
        else:
            self.power_willmill = 0
            self.rotation = False
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

