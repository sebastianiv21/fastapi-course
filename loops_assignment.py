my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

counter = 1

while counter <= 3:
    for day in my_list:
        if day == "Monday":
            continue
        print(day)
    counter += 1
