f = "readme.txt"

with open(fn, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            r.append(row)
    return r