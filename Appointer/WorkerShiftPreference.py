import Schedule.Shift

NO_PREFERENCE = None
UNAVAILABLE_FOR_SHIFT = "Unavailable"
POSSIBLE_PREFERENCES = Schedule.Shift.LEGAL_SHIFT_TYPES + UNAVAILABLE_FOR_SHIFT + NO_PREFERENCE


class WorkerShiftPreference(object):
    def __init__(self, day_to_shift_prefference_dict):
        self.validate_shift_prefference_list(day_to_shift_prefference_dict)
        self.shift_prefference_list = day_to_shift_prefference_dict

    def validate_shift_prefference_list(self, shift_prefference_list):
        for day, preference in shift_prefference_list:
            if preference not in POSSIBLE_PREFERENCES:
                raise ValueError("Invalid prefference %s" % preference)