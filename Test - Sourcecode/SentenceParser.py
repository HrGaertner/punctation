

with open('sentence.txt', 'r') as f:
    N = 2010839
    N = 3
    for k in range(0, N):
        line = f.readline()

    print(line.split('\t')[1])
