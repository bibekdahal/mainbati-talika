import xml.etree.ElementTree as ET
import CursesWindow
import datetime

def GetTimeString(group, day, timeId):
    if not day in group:
        return "not found"
    times = group[day]
    if timeId >= len(times):
        return ""
    time = times[timeId]
    string = str(time["start"]["hr"]).zfill(2) + ":" + str(time["start"]["min"]).zfill(2) \
            + " - " + \
            str(time["end"]["hr"]).zfill(2) + ":" + str(time["end"]["min"]).zfill(2)
    return string

def ParseTimeStr(string):
    time = {}
    strings = string.split(':')
    if (strings[0]!=''):
        time["hr"] = int(strings[0])
    else:
        time["hr"] = 0
    if len(strings) == 2:
        time["min"] = int(strings[1])
    else:
        time["min"] = 0
    return time
    

class RoutineReader:
    def __init__(self):
        self.tables = []

    def ReadFile(self, filename):
        tree = ET.parse(filename)
        routineX = tree.getroot()
        if routineX.tag != 'Routine':
            return

        self.tables = []
        for tableX in routineX:
            if tableX.tag != 'Table':
                continue
            table = {}
            for groupX in tableX:
                if groupX.tag != 'Group' or not 'id' in groupX.attrib:
                    continue
                group = {}
                for dayX in groupX:
                    day = []
                    for timeX in dayX:
                        if timeX.tag != 'Time' or not 'start' in timeX.attrib or not 'end' in timeX.attrib:
                            continue
                        time = {}
                        time["start"] = ParseTimeStr(timeX.attrib['start'])
                        time["end"] = ParseTimeStr(timeX.attrib['end'])
                        day.append(time)
                    group[dayX.tag] = day
                table[int(groupX.attrib['id'])] = group
            self.tables.append(table)

    def GetRoutine(self):
        tableId=1
        padding = 17
        strings = []
        for table in self.tables:
            strings.append([""])
            strings.append(["Table #"+str(tableId)+":"])
            strings.append(["Group".center(6), "Sunday".center(padding), "Monday".center(padding), "Tuesday".center(padding), \
                    "Wednesday".center(padding), "Thursday".center(padding), "Friday".center(padding), "Saturday".center(padding)])
            #strings.append([""])
            for groupId, group in table.items():
                temp = str(groupId)
                timeId = 0
                while True:
                    substr = [temp.center(6),\
                        GetTimeString(group, "Sunday", timeId).center(padding), \
                        GetTimeString(group, "Monday", timeId).center(padding), \
                        GetTimeString(group, "Tuesday", timeId).center(padding), \
                        GetTimeString(group, "Wednesday", timeId).center(padding), \
                        GetTimeString(group, "Thursday", timeId).center(padding), \
                        GetTimeString(group, "Friday", timeId).center(padding), \
                        GetTimeString(group, "Saturday", timeId).center(padding)]
                    if not any(':' in string for string in substr):
                        break
                    strings.append(substr)
                    timeId += 1
                    temp = " "
            tableId += 1
        return strings

def main():
    reader = RoutineReader()
    reader.ReadFile('test.xml')

    strings = reader.GetRoutine()
    width = 126
    height = len(strings) + 1
    day = (datetime.datetime.today().weekday() + 1) % 7 + 1
    
    heads = []
    highlightCells = []
    for i in range(0, len(strings)):
        if any(':' in string for string in strings[i]):
            highlightCells.append([i, day])
        elif any('Group' in string for string in strings[i]):
            heads.append(i);
    window = CursesWindow.CursesWindow(strings, width, height, highlightCells, heads)
        
if __name__ == "__main__":
    main()
