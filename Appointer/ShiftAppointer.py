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
        # todo: implement
        available_workers = self.filter_unavailable_workers_for_day(self.workers_to_use, day.identifier)
        if Schedule.Shift.NIGHT_SHIFT in day:
            appointed_workers = self.appoint_night_shift(day, available_workers)
            available_workers = self.__class__.calculate_available_workers(available_workers, appointed_workers)
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
        workers_appointed = []
        for worker in available_workers:
            if worker.worker_preference[day.identifier] == Schedule.Shift.NIGHT_SHIFT:
                day[Schedule.Shift.NIGHT_SHIFT].add_worker(worker)
                workers_appointed.append(worker)
        return workers_appointed

    @staticmethod
    def calculate_available_workers(orignaly_available_workers, unavailable_workers):
        return list(set(orignaly_available_workers) - set(unavailable_workers))

    def appoint_morning_and_noon_shifts(self, day, available_workers):
        """
        Appoints the morning and noon shift.

        :param day: The day we're currently appointing
        :param available_workers: The list of available workers
        """
        # TODO: implement
        pass