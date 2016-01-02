class Worker(object):
    def __init__(self, full_name, worker_preference):
        self.full_name = full_name
        self.shifts = []
        self.worker_preference = worker_preference

    def add_shift(self, shift):
        self.shifts.append(shift)