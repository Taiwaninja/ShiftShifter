# Builtins
import math
import random

# Internals
import Appointer.WorkerShiftPreference
import Schedule.Shift


class ShiftAppointer(object):
    def __init__(self, workers_to_use, work_week_to_appoint):
        self.workers_to_use = workers_to_use
        self.work_week = work_week_to_appoint

    def appoint_week(self):
        for day in self.work_week:
            self.appoint_day(day)

    def appoint_day(self, day):
        available_workers = self.filter_unavailable_workers_for_day(self.workers_to_use, day.identifier)
        if Schedule.Shift.NIGHT_SHIFT in day:
            appointed_night_shift_workers = self.appoint_night_shift(day, available_workers)
            available_workers = self.calculate_available_workers(available_workers, appointed_night_shift_workers)
        self.appoint_morning_and_noon_shifts(day, available_workers)

    def filter_unavailable_workers_for_day(self, workers, day_identifier):
        return [worker for worker in workers if
                worker.worker_preference[day_identifier] != Appointer.WorkerShiftPreference.UNAVAILABLE_FOR_SHIFT]

    def appoint_night_shift(self, day, available_workers):
        """
        Appoints the night shift and returns the workers appointed

        :param day: The day we're currently appointing
        :param available_workers: The list of available workers
        :return: the list of appointed workers
        """
        workers_appointed = [worker for worker in available_workers if
                             worker.worker_preference[day.identifier] == Schedule.Shift.NIGHT_SHIFT]
        self.assign_workers_iterable_to_shift(day, workers_appointed, Schedule.Shift.NIGHT_SHIFT)
        return workers_appointed

    @classmethod
    def assign_workers_iterable_to_shift(cls, day, workers_to_assign, shift_type):
        for worker in workers_to_assign:
            cls.assign_worker_to_shift(day, worker, shift_type)

    @staticmethod
    def assign_worker_to_shift(day, worker_to_assign, shift_type):
        day[shift_type].add_worker(worker_to_assign)

    @staticmethod
    def calculate_available_workers(originally_available_workers, unavailable_workers):
        return list(set(originally_available_workers) - set(unavailable_workers))

    def appoint_morning_and_noon_shifts(self, day, available_workers):
        """
        Appoints the morning and noon shift.

        :param day: The day we're currently appointing
        :param available_workers: The list of available workers
        """
        number_of_workers_morning, number_of_workers_noon = \
            self.calculate_morning_then_noon_number_of_workers(len(available_workers))

        unassigned_workers_that_prefer_morning_shifts, unassigned_workers_that_prefer_noon_shifts, \
        unassigned_workers_with_no_preferred_shift = self.calculate_workers_by_prefference_morning_noon_no_prefference(
            available_workers, day)

        choosen_morning_workers = self.choose_random_workers(number_of_workers_morning,
                                                             unassigned_workers_that_prefer_morning_shifts)
        choosen_noon_workers = self.choose_random_workers(number_of_workers_noon,
                                                          unassigned_workers_that_prefer_noon_shifts)

        unassigned_workers_that_prefer_morning_shifts = unassigned_workers_that_prefer_morning_shifts - choosen_morning_workers
        unassigned_workers_that_prefer_noon_shifts = unassigned_workers_that_prefer_noon_shifts - choosen_noon_workers

        number_of_workers_noon_left = int(number_of_workers_noon - len(choosen_noon_workers))
        number_of_workers_morning_left = int(number_of_workers_morning - len(choosen_morning_workers))

        assigned_non_preffered_noon = self.assign_non_preffered_workers(number_of_workers_noon_left,
                                                                        unassigned_workers_that_prefer_morning_shifts.union(
                                                                            unassigned_workers_with_no_preferred_shift))
        unassigned_workers_with_no_preferred_shift = unassigned_workers_with_no_preferred_shift - assigned_non_preffered_noon

        assigned_non_preffered_morning = self.assign_non_preffered_workers(number_of_workers_morning_left,
                                                                           unassigned_workers_that_prefer_noon_shifts.union(
                                                                               unassigned_workers_with_no_preferred_shift))

        choosen_morning_workers = choosen_morning_workers.union(assigned_non_preffered_morning)
        choosen_noon_workers = choosen_noon_workers.union(assigned_non_preffered_noon)

        self.assign_workers_iterable_to_shift(day, choosen_morning_workers, Schedule.Shift.MORNING_SHIFT)
        self.assign_workers_iterable_to_shift(day, choosen_noon_workers, Schedule.Shift.NOON_SHIFT)

    def calculate_morning_then_noon_number_of_workers(self, num_of_available_workers):
        # we use float to avoid the 1/2=0 bug.
        avg_amount_of_workers = num_of_available_workers / 2.0
        amount_of_workers_morning_noon = [math.floor(avg_amount_of_workers), math.ceil(avg_amount_of_workers)]
        # this is used to prevent one shift always having more workers then the other
        random.shuffle(amount_of_workers_morning_noon)
        return amount_of_workers_morning_noon

    @staticmethod
    def calculate_workers_by_prefference_morning_noon_no_prefference(available_workers, day):
        workers_that_prefer_morning_shifts = set([worker for worker in available_workers if
                                                  worker.worker_preference[
                                                      day.identifier] == Schedule.Shift.MORNING_SHIFT])

        workers_that_prefer_noon_shifts = set([worker for worker in available_workers if
                                               worker.worker_preference[
                                                   day.identifier] == Schedule.Shift.NOON_SHIFT])

        workers_with_no_preffered_shift = set([worker for worker in available_workers if
                                               worker.worker_preference[day.identifier] ==
                                               Appointer.WorkerShiftPreference.NO_PREFERENCE])
        return workers_that_prefer_morning_shifts, workers_that_prefer_noon_shifts, workers_with_no_preffered_shift

    def assign_non_preffered_workers(self, amount_of_workers_to_assign, set_of_workers_to_assign_from):
        return set(random.sample(set_of_workers_to_assign_from, amount_of_workers_to_assign))

    def choose_random_workers(self, amount_of_workers_to_choose, workers_to_choose_from):
        # Cant allocate more workers then given!
        # Conversion to int for random.sample parameter
        real_amount_of_workers_to_choose = int(min(amount_of_workers_to_choose, len(workers_to_choose_from)))
        return set(random.sample(workers_to_choose_from, real_amount_of_workers_to_choose))