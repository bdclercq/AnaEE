class Config:

    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return "{0}-{1}-{2} {3}:{4}:{5}".format(self.day, self.month, self.year,
                                                self.hour, self.minute, self.second)
