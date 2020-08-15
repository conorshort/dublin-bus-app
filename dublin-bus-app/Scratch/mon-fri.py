days =  [[0, 0,	1,	0,	0,	0,	0],
 [0, 0,	0,	1,	0,	0,	0],
 [0, 0,	0,	0,	1,	0,	0],
 [0, 0,	0,	0,	0,	1,	0],
 [0, 0,	0,	0,	0,	0,	1],
 [1, 0,	0,	0,	0,	0,	0],
 [1, 1,	1,	1,	1,	0,	0],
 [1, 1,	1,	1,	1,	0,	0],
 [0, 0,	0,	0,	0,	1,	0],
 [0, 0,	0,	0,	0,	1,	0],
 [0, 0,	0,	0,	0,	0,	1],
 [1, 1,	1,	1,	1,	0,	0],
 [1, 0,	0,	0,	0,	0,	1],
 [0, 0,	0,	0,	0,	1,	0],
 [0, 1,	1,	1,	1,	0,	0],
 [1, 0,	0,	0,	0,	0,	1],
 [0, 0,	0,	0,	0,	1,	0]]
 

def day_bools_to_string(day_bool_list):
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday (and bank holidays)"]
    for day in day_bool_list:
        day_string = ""
        consecutive = False
        for i, day in enumerate(d):
            if day == 0:
                consecutive = False
            elif day == 1 and not consecutive:
                day_string += ", " + day_names[i][:3]
                consecutive = True
            elif i + 1 >= len(day_bool_list):
                break
            elif day == 1 and day_bool_list[i + 1] == 0:
                day_string += "-" + day_names[i][:3]
                consecutive = False
    return day_string[2:]


for d in days:
    print(day_bools_to_string(d))
