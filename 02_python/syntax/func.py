#code....
a = 1
b = 2
c = 3
s = a + b + c
r = s / 3
print(r)
#code....

'''
def average():
    a = 1
    b = 2
    c = 3
    s = a + b + c
    r = s / 3
    print(r)
'''

def average(*args):
    x = 0
    for number in args:
        x += number
    return(x / len(args))
    

average()
