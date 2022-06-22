from models.device import Device


class Fan(Device):
    def __init__(self, name: str) -> None:
        Device.__init__(self, name)
        self.fan_power = 0
        self.type = 'fan'
        self.rotation = False
        self.available_options = {'on/off': self.change_state,
                                  'zmień moc': self.give_me_more_power,
                                  'rotacja': self.change_rotation}

    @property
    def get_option(self) -> dict:
        available_options = {'on/off': self.state,
                             'zmień moc': self.fan_power,
                             'rotacja': self.rotation}
        return available_options

    def __call__(self, select_option: str):
        return self.available_options[select_option]()

    def change_state(self) -> bool:
        super().change_state()
        self.fan_power = 1 if self.state else 0
        self.rotation = False
        return self.message(self.state, self.type)

    def give_me_more_power(self, power: int) -> str:
        self.fan_power = power
        return f'Zmieniono moc wiatraka {power}'

    def change_rotation(self) -> str:
        if self.rotation:
            self.rotation = False
            return 'Wyłączam obracanie'
        else:
            self.rotation = True
            return self.message(self.rotation)

    def message(self, state: bool, option: str):
        return f"{'Włączono' if state else 'Wyłączono'} {option}"
