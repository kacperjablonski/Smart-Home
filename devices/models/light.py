from models.device import Device

class Light(Device):
 
    available_color = ['white', 'green', 'red', 'blue', 'yellow']

    def __init__(self,name):
        Device.__init__(self, name)
        self.power_light = 0
        self.color = 'white'
        self.type = 'light'
        self.available_options = {'on/off': self.change_state,
                                  'zmień moc': self.change_light_power,
                                  'kolor': self.change_color}

    @property
    def get_option(self) -> dict:
        available_options = {'on/off': self.state,
                             'zmień moc': self.power_light,
                             'rotacja': self.color}
        return available_options

    def __call__(self, select_option: str):
        return self.available_options[select_option]()

    def change_state(self) -> str:
        super().change_state()
        if self.state:
            self.power_light = 1
            return 'Włączono lampę'
        else:
            self.power_light = 0
            return "wyłączono lampę"

    def change_light_power(self, power: int) -> str:
        self.power_light = power
        return f'zmieniono moc {power}'

    def change_color(self, color: str) -> str:
        if color is self.available_color:
            self.color = color
            return f'Zmieniono kolor na {color}'
        return f'Nie można zmienić koloru na {color}'

