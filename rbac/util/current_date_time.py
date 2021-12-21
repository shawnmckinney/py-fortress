'''
@copyright: 2022 - Symas Corporation
'''

from datetime import datetime


class CurrentDateTime:

    def __init__(
        self,
        ):
        
        now_=datetime.now()
        self.minute = str(now_.minute).zfill(2)
        self.hour = str(now_.hour).zfill(2)            
        self.month = str(now_.month).zfill(2)
        self.day = str(now_.day).zfill(2)
        self.year = str(now_.year).zfill(4)
        self.date = self.year + self.month + self.day
        self.time = self.hour + self.minute
        self.day_of_week = str(now_.weekday()+1)
        self.seconds = now_.timestamp()