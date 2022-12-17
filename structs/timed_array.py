from datetime import datetime


class TimedArray(list):

    def __init__(self):
        super().__init__()
        # PyCharm has issues with Python overrides
        self.append = self._append

    def _append(self, __object) -> None:
        # Add current time
        super().append(f"{datetime.today().strftime('%H:%M')} {__object}")
