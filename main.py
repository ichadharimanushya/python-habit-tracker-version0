#connectivity using modules
from tracker import HabitTracker


name = input("Enter your name:\n>").strip().lower()
if not name:
    name = "defaultuser"
habit_tracker = HabitTracker(name)
print("=====WELCOME=====")


commands = {
    "addhabit" : habit_tracker.addhabit,
    "allhabits" :habit_tracker.allhabits,
    "deletehabit" : habit_tracker.deletehabit,
    "complete" : habit_tracker.complete,
    "history" : habit_tracker.history,
    "currentstreak" : habit_tracker.currentstreak,
    "longeststreak" : habit_tracker.longeststreak,
    "today" : habit_tracker.today,
    "stats" : habit_tracker.stats,
    "weeklyreport" : habit_tracker.weeklyreport
}



while 1:
    user = input('->').strip().lower()
    if not user:
        print("--Usage: <command> <supported_argument>--\n")
        continue
    command = user.split()
    n = len(command)
    if n == 1:
        arg = ""
    elif n != 2:
        print("--Usage: <command> <supported_argument>--\n")
        continue
    else:
        arg = command[1]
    method = command[0]
    if method == "exit":
        print("=====GOODBYE=====")
        break
    elif method in commands:
        commands[method](arg)
    else:
        print("--Invalid command--")
    print()
        