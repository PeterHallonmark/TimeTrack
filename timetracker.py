

import argparse
from datetime import datetime, timedelta
import json
import sys


TIMEDELTA_END_OF_DAY = timedelta(hours=23, minutes=59, seconds=59)
TIMEDELTA_ZERO = timedelta(0)


class ActivityHeader:
    def __init__(self, name):
        self.name = name
        self.__activities = []

    def __repr__(self):
        return "class ActivityHeader(name=" + self.name + ")"

    def append(self, activity):
        self.__activities.append(activity)
        activity._header = self

    def accept(self, visitor):
        visitor.visit_activity_header(self)


class Activity:
    def __init__(self, date, start, end):
        self._header = None
        self.date = date
        self.start = start
        self.end = end
        
    def duration(self):
        if self.start and self.end:
            return self.end - self.start
        else:
            return TIMEDELTA_ZERO
    
    def accept(self, visitor):
        visitor.visit_activity(self)


class Away(Activity):
    def __init__(self, date, start, end, name):
        Activity.__init__(self, date, start, end)
        self.name = name

    def accept(self, visitor):
        visitor.visit_away(self)


class Reported:
    def __init__(self):
        pass
        

class Weeks:
    def __init__(self, weeks=[]):
        self.weeks = weeks

    def __repr__(self):
        return "class Weeks()"

    def days(self):
        for week in self.weeks:
            for day in week:
                yield day

    def __iter__(self):
        for week in self.weeks:
            yield week

    def accept(self, visitor):
        visitor.visit_weeks(self)


class Week:
    def __init__(self, number, days=[]):
        self.number = number
        self.days = days

    def __repr__(self):
        return "class Week(number=" + str(self.number) + ")"

    def __iter__(self):
        for day in self.days:
            yield day

    def accept(self, visitor):
        visitor.visit_week(self)


class Day:
    def __init__(self, date, activities, reported):
        self.date = date
        self.activities = activities
        self.reported = reported
        self.year, self.week, self.weekday = self.date.isocalendar()

    def __repr__(self):
        return "class Day(date=" + str(self.date) + ")"

    def __iter__(self):
        for activity in self.activities:
            yield activity

    def accept(self, visitor):
        visitor.visit_day(self)


class Period:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.__days = []

    def append(self, day):
        self.__days.append(day)

    def days(self):
        for day in self.__days:
            yield day

    def __repr__(self):
        return "class Period(name=" + self.name + ", " \
                            "start=" + str(self.start) + ", " \
                            "end=" + str(self.end) + ")"

    def accept(self, visitor):
        visitor.visit_period(self)


class TimeTracker:
    def __init__(self, dateformat="%Y-%m-%d", timeformat="%H.%M"):
        self.__dateformat = dateformat
        self.__timeformat = timeformat
        self.__headers = {}
        
    def parse(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        self.__headers = self.__parse_headers(data["activities"])
        period = self.__parse_period(data["period"])
        weeks = self.__parse_weeks(data["weeks"])
        for day in weeks.days():
            period.append(day)

        return period, weeks

    def __parse_headers(self, activities):
        result = {}
        for item in activities:         
            name = item["activity"]
            result[name] = ActivityHeader(name)
        return result
    
    def __get_header(self, header):
        return self.__headers[header]
    
    def __parse_period(self, period):
        name = period["name"]
        start = self.__parse_date(period["start"])
        end = self.__parse_date(period["end"], offset=TIMEDELTA_END_OF_DAY)
        return Period(name, start, end)
        
    def __parse_weeks(self, weeks):
        temp = []
        for item in weeks:
            week_number = int(item["week"])
            days = []
            for day in item["timetrack"]:
                day = self.__parse_day(day)
                days.append(day)
            temp.append(Week(week_number, days))
        return Weeks(temp)

    def __parse_day(self, day):
        date = self.__parse_date(day["date"])
        activities = self.__parse_timetrack(day["timetrack"], date)
        reported = self.__parse_reported(day)
        return Day(date, activities, reported)
        
    def __parse_timetrack(self, timetrack, date):
        activities = []
        for item in timetrack:
            start = self.__parse_time(item["start"])
            end = self.__parse_time(item["end"])
            
            if "activity" in item:
                header = self.__get_header(item["activity"])
                activity = Activity(date, start, end)
                header.append(activity)
                activities.append(activity)
            elif "away" in item:
                name = item["away"]
                away = Away(date, start, end, name)
                activities.append(away)
        return activities           

    def __parse_reported(self, day):
        try:
            return Reported()
        except:
            return Reported()

    def __parse_date(self, date, offset=timedelta()):
        try:
            return datetime.strptime(date, self.__dateformat) + offset
        except:
            return None           

    def __parse_time(self, time):
        try:
            item = datetime.strptime(time, self.__timeformat)
            return timedelta(hours=item.hour,
                             minutes=item.minute,
                             seconds=item.second)
        except:
            return None


class TimeTrackerVisitor:
    def visit_period(self, period):
        pass

    def visit_weeks(self, weeks):
        pass
        
    def visit_week(self, week):
        pass
    
    def visit_day(self, day):
        pass
        
    def visit_activity_header(self, header):
        pass

    def visit_activity(self, activity):
        pass
        
    def visit_away(self, away):
        pass              


class TimeTrackerValidateVisitor(TimeTrackerVisitor):
    def __init__(self):
        self.__warnings = []
        
    def visit_period(self, period):
        start = period.start
        end = period.end
        
        if start and end:
            if start < end:
                self.__validate_days(start, end, period.days())  
            else:
                self.__warning("Expected start of period to be less than end of period.")
                self.__trace("start date: " + self.__date(start))
                self.__trace("end date:   " + self.__date(end))
        else:
            self.__warning("Expected both start of period and end of period to be valid dates.")
            self.__trace("start date: " + self.__date(start)) 
            self.__trace("end date:   " + self.__date(end))

    def visit_weeks(self, weeks):
        self.__prev_activity = None
        self.__prev_number = None
        self.__prev_day = None
        
        for week in weeks:
            week.accept(self)
        
    def visit_week(self, week):
        if self.__prev_number:
            if week.number != (self.__prev_number+1):
                self.__warning("Expected week numbers to increase by 1.")
                self.__trace("previous week number: " + str(self.__prev_number))
                self.__trace("current week number:  " + str(week.number))

        for day in week:
            day.accept(self)
        self.__prev_number = week.number
    
    def visit_day(self, day):
        if self.__prev_day:
            if day.date < self.__prev_day.date:
                self.__warning("Expected date to increase.")
                self.__trace("previous date: " + self.__date(self.__prev_day.date)) 
                self.__trace("current date:  " + self.__date(day.date))

        self.__prev_activity = None
        for activity in day.activities:
            activity.accept(self)        
        self.__prev_day = day
        
    def visit_activity_header(self, header):
        pass

    def visit_activity(self, activity):
        if activity.start:
            if self.__is_range_invalid(activity.start, activity.end):
                self.__warning("Expected time to increase.")
                self.__trace("activity at date: " + self.__date(activity.date))
                self.__trace("start time:       " + self.__time(activity.start))
                self.__trace("end time:         " + self.__time(activity.end))
        else:
            print("Warning: Expected start time to have valid value")
        
        if self.__prev_activity:
            if self.__is_range_invalid(self.__prev_activity.end, activity.start, False):
                self.__warning("Expected time to be equal or increase for next activity.")
                self.__trace("activities at date: " + self.__date(activity.date))
                self.__trace("previous end time:  " + self.__time(self.__prev_activity.end))
                self.__trace("current start time: " + self.__time(activity.start))

        self.__prev_activity = activity
        
    def visit_away(self, away):
        self.visit_activity(away)

    def __date(self, date):
        if date:
            return str(date.date())
        else:
            return "N/A"

    def __time(self, time):
        if time:
            return str(time)
        else:
            return "N/A"

    def __warning(self, warning):
        self.__trace_info = []
        self.__warnings.append((warning, self.__trace_info))

    def __trace(self, trace):
        self.__trace_info.append(trace)

    def __validate_days(self, start, end, days):
        for day in days:
            if day.date < start:
                self.__warning("Expected date to be ...TBD")
            if end < day.date:
                self.__warning("Expected date to be ...TBD")

    def __is_range_invalid(self, start, end, equal_invalid=True):
        if start and end:
            if start == end:
                return equal_invalid
            else:
                return end < start
        return False
    
    def stdout(self):
        for warning, trace_list in self.__warnings:
            print("WARNING: " + warning)
            for trace in trace_list:
                print("    " + trace)
            print("")
        return self.__warnings
    
    def count_warnings(self):
        return len(self.__warnings)


class TimeTrackerCalculateVisitor:
    def __init__(self):
        self.__ignore_away = set()
    
    def visit_period(self, period):
        pass

    def visit_weeks(self, weeks):
        for week in weeks:
            week.accept(self)
        
    def visit_week(self, week):
        print(str(week.number) + " ----")
        for day in week:
            day.accept(self)
    
    def visit_day(self, day):
        self.__activity_summary = TIMEDELTA_ZERO
        self.__activity_list = []
        self.__away_summary = TIMEDELTA_ZERO
        self.__away_list = []
        
        print(day)
        for activity in day:
            activity.accept(self)
        print(self.__activity_list)
        print(self.__activity_summary)
        print(day)
        
    def visit_activity_header(self, header):
        pass

    def visit_activity(self, activity):
        self.__activity_list.append(activity)
        self.__activity_summary  += activity.duration()
        
    def visit_away(self, away):
        if away.name not in self.__ignore_away:
            self.__activity_list.append(away)
            self.__away_summary  += away.duration()
   
    def ignore_away(self, ignore):
        self.__ignore_away.add(ignore)


def main():
    #parser = argparse.ArgumentParser(description='Process some integers.')
    #args = parser.parse_args()    


    timetracker = TimeTracker()
    period, weeks = timetracker.parse("time_2025_september.json")

    # Validate the timetrack data
    validate = TimeTrackerValidateVisitor()
    weeks.accept(validate)
    period.accept(validate)

    if validate.count_warnings() > 0:
        validate.stdout()
        return -1
    
    calculate = TimeTrackerCalculateVisitor()
    calculate.ignore_away("lunch")
    weeks.accept(calculate)
    
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
