import os

path = input('Please input xml files path like: \'D:/xml/\'\n')

f = os.listdir(path)

for i in f:

    f1 = open(path + i, 'r+')
    infos = f1.readlines()
    f1.seek(0, 0)

    for line in infos:
        # Change origin xml path in the first part and goal path in the second
        line_new = line.replace('D:\\img\\', 'C:\\image\\')
        f1.write(line_new)

    f1.close()
