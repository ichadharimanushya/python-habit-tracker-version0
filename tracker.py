from pathlib import Path
import json
from datetime import datetime, timedelta, date




# filepaths and extra variables
BASE_DIR = Path(__file__).parent
json_path = BASE_DIR/"habits.json"




class HabitTracker():
    def __init__(self, name):
        self.name = name.strip().lower()
        self.database = self.loadjson()
        self.data = self.database["users"][self.name]
        self.habits = self.data["habits"]

    def loadjson(self):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                if self.name in data["users"]:
                    return data
                else:
                    data["users"][self.name] = {
                                                "habits": []
                                                }
                print("-----New User Created----")
                self.database = data
                self.savejson()
                return data
        except Exception as e:
            self.database = {
                "users": {
                    self.name : {
                        "habits": []
                    }
                }
            }
            self.savejson()
            print("-----New User Created----")
            return self.database

    def savejson(self):
        with open(json_path, 'w') as f:
            json.dump(self.database, f, indent = 4)

    def addhabit(self, arg = ""):
        if not arg:
            print("--Usage: addhabit <name_habit>--")
            return
        for habits in self.habits:
            if habits["name"] == arg:
                print("--Entered habit already exist--")
                return
        habit = {
            "name": arg,
            "created": f"{datetime.now().date()}",
            "completed_dates": []
            }
        self.habits.append(habit)
        self.savejson()
        print("--Habit added successfully--")

    def allhabits(self, arg = ""):
        for index, habits in enumerate(self.habits, start = 0):
            print(f"{index+1}. {habits['name']}")

    def deletehabit(self, arg = ""):
        if not arg:
            print("--Usage: deletehabit <number_habit>--")
            return
        try:
            arg = int(arg)
            if arg <= 0 or arg > len(self.habits):
                print("--There is no habit at entered number--")
                return
        except ValueError as e:
            print("--Entered argument should be a number--")
            return
        self.habits.pop(arg-1)
        self.savejson()

    def complete(self, arg = ""):
        datetoday = f"{datetime.now().date()}"
        for habits in self.habits:
            if arg == habits["name"]:
                if datetoday not in habits["completed_dates"]:
                    habits["completed_dates"].append(datetoday)
                    self.savejson()
                    return
                else:
                    print("--Habit already completed for the day--")
                    return
        print("--No such habit found--")

    def history(self, arg = ""):
        if not arg:
            print("--Usgae: history <name_habit>--")
            return
        for habits in self.habits:
            if arg == habits["name"]:
                if not habits["completed_dates"]:
                    print("--Habit not completed once--")
                    return
                for date in habits["completed_dates"]:
                    print(date)
                return
        print("--No such habit found--")

    def currentstreak(self, arg = "") -> None | int:
        if not arg:
            print("--Usage: currentstreak <name_habit>--")
            return
        dates = []
        for habit in self.habits:
            if habit["name"] == arg:
                dates = habit["completed_dates"]
                break
        dates = sorted(dates)
        if not dates:
            print("--No data/streak for entered habit--")
            return 
        today = str(datetime.now().date())
        streak = 1
        if today not in dates:
            print("--Streak pending, habit is not completed today--")
            return
        for i in range(-1, -(len(dates)), -1):
            if datetime.strptime(dates[i],
                                 "%Y-%m-%d") - timedelta(days = 1) == datetime.strptime(dates[i-1],
                                                                                               "%Y-%m-%d"):
                streak += 1
            else: break
        print(f"--Current streak : {streak}--")
        
    def longeststreak(self, arg = ""):
        arg  = arg.lower().strip()
        if not arg:
            print("--Usage: currentstreak <name_habit>--")
            return
        dates = []
        for habit in self.habits:
            if habit["name"] == arg:
                dates = habit["completed_dates"]
                break
        dates = sorted(dates)
        if not dates:
            print("--No data/streak for entered habit--")
            return
        streak = []
        count = 1
        prev_date = datetime.strptime(dates[0], "%Y-%m-%d")
        for date in dates[1:]:
            date = datetime.strptime(date, "%Y-%m-%d")
            if date == prev_date + timedelta(days = 1):
                count += 1
            else:
                streak.append(count)
                count = 1
            prev_date = date
        streak.append(count)
        print(f"--Longest streak : {max(streak)}--")

    def today(self, arg = ""):
        datetoday = str(datetime.now().date())
        habits = self.habits
        print("--Habits remaining--")
        found = False
        for habit in habits:
            if datetoday not in habit["completed_dates"]:
                found = True
                print(habit["name"])
        if not found:
            print("--No data found--")
        print()
        print("--Habits completed--")
        found = False
        for habit in habits:
            if datetoday in habit["completed_dates"]:
                found = True
                print(habit["name"])
        if not found:
            print("--No data found--")

    def stats(self, arg = ""):
        arg = arg.strip().lower()
        if not arg:
            print("--Usage: stats <name_habit>--")
            return
        found = False
        for habit in self.habits:
            if habit["name"] == arg:
                activedays = 1 + (datetime.now().date().__sub__(datetime.strptime(habit["created"], "%Y-%m-%d").date())).days
                completeddays = len(habit["completed_dates"])
                found = True
                break
        if found:
            print(f"Active days: {activedays}")
            print(f"Completed: {completeddays}")
            print(f"Completion rate: {(completeddays/activedays)*100}%")
            self.currentstreak(arg)
            self.longeststreak(arg)
        else:print("--No record found--")

    def weeklyreport(self, arg = ""):
        arg = arg.strip().lower()
        if not arg:
            print("--Usage: weeklyreport <name_habit>--")
            return
        habits = self.habits
        today = datetime.now().date()
        for habit in habits:
            if habit["name"] == arg:
                print("--Weekly report--")
                for i in range(6, -1, -1):
                    date = str(today - timedelta(days = i))
                    print(f"{date} ->", end = " ")
                    print("✅" if date in habit["completed_dates"] else "❌")
                return
        print("--No such habit found--")






# habit(dict) inside of habits(list) :

{
    "name": "dsa",
    "created": "2026-06-19",
    "completed_dates": []
    }

{
    "users": {
        "defaultuser": {
            "habits": [],
            "history": {}
        }
    }
}

'''
datetime
timedelta
data

addhabit -
allhabits
deletehabit -
complete -
history -
current streak -
longest streak -
today(completed and not completed)
stats -
weeklyreport -
'''