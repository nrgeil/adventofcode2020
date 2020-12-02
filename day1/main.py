with open('1.txt') as f:
    all_entries = [int(i) for i in f.readlines()]

# Part 1
found = False
while not found:
    # Each time we check a number, we can safely remove from the list so it isn't checked on every loop
    entry = all_entries.pop()
    for e in all_entries:
        if (e + entry) == 2020:
            print(e * entry)
            found = True
            break

# Part 2
with open('1.txt') as f:
    all_entries = [int(i) for i in f.readlines()]

e1 = all_entries.copy()
e2 = all_entries.copy()

found = False
while not found:
    entry = all_entries.pop()
    for i in e1:
        for j in e2:
            if (i + j + entry) == 2020:
                print(entry * i * j)
                found = True
                break
        if found:
            break
