num = 2

with open("sentence.txt") as f:
    with open("preprocess.txt", "r+") as out:
        for i in f.readlines():
            num += 1
            i = i[len(str(num))+1:]
            i = i[:-1]
            i = i + " "
            out.write(i)
            print(num)
