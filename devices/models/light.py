from models.device import Device

avinable_color = ['white', 'green', 'red', 'blue', 'yellow']


class Light(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.power_light = 0
        self.color = 'white'
        self.type = 'light'
        self.method = {'on/off': self.change_status,
                        'zmień moc': self.give_me_more_power,
                        'kolor': self.change_color}

    def change_status(self):
        super().change_status()
        if self.status:
            self.power_light = 1
            return 'Włączono lampę'
        else:
            self.power_light = 0
            return "wyłączono lampę"

    def give_me_more_power(self, power):
        self.power_light = power
        return f'zmieniono moc {power}'

    def change_color(self, color):
        if color is avinable_color:
            self.color = color
            return f'Zmieniono kolor na {color}'
        return f'Nie można zmienić koloru na {color}'
