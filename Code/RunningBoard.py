from BusStop import BusStop
from StopSchedule import StopSchedule


class RunningBoard:
    def __init__(self):
        self.__timetable = {}
        self.__index_map = {}

    def add_entry(self, bus_stop: BusStop, schedule: StopSchedule):
        if bus_stop in self.__timetable:
            raise ValueError("This buss stop is already registered in this running board")
        elif schedule.get_order() in self.__index_map:
            raise ValueError(
                f"A bus stop with the scheduled order {schedule.get_order()}\
                 already exist int this running board"
            )
        else:
            self.__timetable[bus_stop] = schedule
            self.__index_map[schedule.get_order()] = bus_stop

    def _shift(self, start: int):
        indexes = [x for x in self.__index_map]
        indexes.sort()
        index = indexes.index(start)
        to_remap = []
        while index + 1 < len(indexes) and indexes[index] + 1 >= indexes[index + 1]:
            to_remap.append(index)
            self.get_schedule(index).set_order(indexes[index] + 1)
            index += 1

        to_remap.append(index)
        self.get_schedule(index).set_order(indexes[index] + 1)
        to_remap.reverse()

        for i in to_remap:
            self.__index_map[indexes[i] + 1] = self.__index_map[indexes[i]]

        del self.__index_map[start]

    def insert_entry(self, bus_stop: BusStop, schedule: StopSchedule):
        if bus_stop in self.__timetable:
            raise ValueError("This buss stop is already registered in this running board")
        elif schedule.get_order() in self.__index_map:
            self._shift(schedule.get_order())
        self.add_entry(bus_stop, schedule)

    def get_schedule(self, schedule_order: int):
        if schedule_order not in self.__index_map:
            raise ValueError(f"There is no schedule with order {schedule_order} registered in this running board")
        return self.__timetable[self.__index_map[schedule_order]]

    def remove_entry_by_schedule(self, schedule_order: int):
        if schedule_order not in self.__index_map:
            raise ValueError(f"Unable to remove entry related to schedule with order {schedule_order}\
             : no schedule with that order found")
        else:
            del self.__timetable[self.__index_map[schedule_order]]
            del self.__index_map[schedule_order]

    def remove_entry_by_bus_stop(self, bus_stop: BusStop):
        if bus_stop not in self.__timetable:
            raise ValueError(f"Unable to remove entry related to bus stop {str(bus_stop)}\
             : this bus stop is not registered here")
        else:
            del self.__index_map[self.__timetable[bus_stop].get_order()]
            del self.__timetable[bus_stop]

    def __str__(self):
        val = ""
        for stop in self.__timetable:
            val += stop.get_name() + ":" + str(self.__timetable[stop].get_order()) + "\n"
        return val.strip()


if __name__ == '__main__':
    runningBoard = RunningBoard()
    runningBoard.add_entry(
        BusStop("osef0", 12),
        StopSchedule(0, None)
    )
    runningBoard.add_entry(
        BusStop("osef1", 12),
        StopSchedule(1, None)
    )
    runningBoard.add_entry(
        BusStop("osef2", 12),
        StopSchedule(2, None)
    )
    runningBoard.add_entry(
        BusStop("osef3", 12),
        StopSchedule(3, None)
    )
    runningBoard.add_entry(
        BusStop("osef5", 12),
        StopSchedule(5, None)
    )
    runningBoard.insert_entry(
        BusStop("osef2_", 12),
        StopSchedule(2, None)
    )

    print(str(runningBoard))