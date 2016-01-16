import Schedule.Shift

NO_PREFERENCE = "No Preference"
UNAVAILABLE_FOR_SHIFT = "Unavailable"
POSSIBLE_PREFERENCES = Schedule.Shift.LEGAL_SHIFT_TYPES + [UNAVAILABLE_FOR_SHIFT, NO_PREFERENCE]


class WorkerShiftPreference(object):
    def __init__(self, day_to_shift_preference_dict):
        self.validate_shift_preference_list(day_to_shift_preference_dict)
        self.shift_preference_dict = day_to_shift_preference_dict

    @staticmethod
    def validate_shift_preference_list(shift_prefference_dict):
        for day, preference in shift_prefference_dict.iteritems():
            if preference not in POSSIBLE_PREFERENCES:
                raise ValueError("Invalid prefference %s" % preference)

    def __getitem__(self, key):
        return self.shift_preference_dict[key]

    def __setitem__(self, key, value):
        self.shift_preference_dict[key] = value