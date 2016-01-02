MORNING_SHIFT = "Morning"
NOON_SHIFT = "Noon"
NIGHT_SHIFT = "Night"
LEGAL_SHIFT_TYPES = [NIGHT_SHIFT, NOON_SHIFT, MORNING_SHIFT]


class Shift(object):
    def __init__(self, shift_type):
        self.workers_in_shift = []
        if shift_type not in LEGAL_SHIFT_TYPES:
            raise ValueError("Invalid shift type, legal types are %s" % LEGAL_SHIFT_TYPES)

    def add_worker(self, worker_to_add):
        self.workers_in_shift.append(worker_to_add)