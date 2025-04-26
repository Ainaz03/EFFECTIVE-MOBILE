def func():
    i, j = 0, 1
    while True:
        yield i
        i,j = j, i+j

for _ in range(10):
    print(next(func()))