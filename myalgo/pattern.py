
def pattern(n):
    for i in range(n):
        for j in range(n):
            print("*",end="")
        print()
def pattern2(n):
    for i in range(n+1):
        for j in range(i):
            print("*",end="")
        print("")
def pattern3(n):
    for i in range(n+1):
        for j in range(i):
            print("*",end="")
        print("")

pattern2(4)