import datetime

day = datetime.datetime.now().weekday()

def get_sunday():
    return "Today it's Sunday"
def get_monday():
    return "Today it's Monday"
def get_tuesday():
    return "Today it's Tuesday"
def get_wednesday():
    return "Today it's Wednesday"
def get_thursday():
    return "Today it's Thursday"
def get_friday():
    return "Today it's Friday"
def get_saturday():
    return "Today it's Saturday"
def get_default():
    return "Looking forward to the Weekend"

switcher = {
    0:get_sunday,
    1:get_monday,
    2:get_tuesday,
    3:get_wednesday,
    4:get_thursday,
    5:get_friday,
    6:get_default
}

dayName = switcher.get(day,get_default)()
print(dayName)