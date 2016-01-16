# Builtins
import csv

# Internals
import Appointer.WorkerShiftPreference
import Appointer.ShiftAppointer
import Schedule.Worker
import Schedule.WorkWeek
import Schedule.WorkDay
import Schedule.Shift

WORKER_PREFERENCE_FILE_PATH = "workerPreference.csv"


def main():
    work_week = init_default_week()
    workers = init_workers_csv()
    shiftAppointer = Appointer.ShiftAppointer.ShiftAppointer(workers, work_week)
    shiftAppointer.appoint_week()
    print_work_week(work_week)


def init_default_week():
    days_in_week = [init_default_day(day_identifier) for day_identifier in xrange(1, 6)]
    return Schedule.WorkWeek.WorkWeek(days_in_week)


def init_default_day(day_identifier):
    shift_mapping = {Schedule.Shift.MORNING_SHIFT: Schedule.Shift.Shift(Schedule.Shift.MORNING_SHIFT),
                     Schedule.Shift.NOON_SHIFT: Schedule.Shift.Shift(Schedule.Shift.NOON_SHIFT),
                     Schedule.Shift.NIGHT_SHIFT: Schedule.Shift.Shift(Schedule.Shift.NIGHT_SHIFT)}
    return Schedule.WorkDay.WorkDay(shift_mapping, day_identifier)


def init_workers_csv():
    workers = []
    with open(WORKER_PREFERENCE_FILE_PATH) as worker_preference_file:
        worker_preference_csv_reader = csv.reader(worker_preference_file)
        for worker_row in worker_preference_csv_reader:
            workers.append(Schedule.Worker.Worker(worker_row[0],
                                                  Appointer.WorkerShiftPreference.WorkerShiftPreference(
                                                      {day_identifier: worker_row[day_identifier] for day_identifier in
                                                       xrange(1, len(worker_row))})))
    return workers


def print_work_week(work_week_to_print):
    for day in work_week_to_print:
        print_work_day(day)
        print "\r\n"


def print_work_day(day):
    print "Schedule for workday %(day_identifier)s" % {"day_identifier": day.identifier}
    for shift_type, shift in day.shift_type_to_shift_mapping.iteritems():
        workers_in_shift = [worker.full_name for worker in shift.workers_in_shift]
        workers_in_shift_stringified = ",".join(workers_in_shift)
        print "%(shiftType)s: %(workers)s" % {"shiftType": shift_type, "workers": workers_in_shift_stringified}


if __name__ == "__main__":
    main()