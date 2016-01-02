class WorkWeek(object):
    def __init__(self, work_days):
        self.work_days_in_week = work_days

    def __iter__(self):
        return iter(self.work_days_in_week)
