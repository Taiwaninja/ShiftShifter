class WorkDay(object):
    def __init__(self, shift_type_to_shift_mapping, day_identifier):
        self.shift_type_to_shift_mapping = shift_type_to_shift_mapping
        self.identifier = day_identifier

    def __iter__(self):
        return iter(self.shift_type_to_shift_mapping)

    def __contains__(self, item):
        return item in self.shift_type_to_shift_mapping

    def __getitem__(self, key):
        return self.shift_type_to_shift_mapping[key]

    def __setitem__(self, key, value):
        self.shift_type_to_shift_mapping[key] = value