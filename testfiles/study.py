import datetime
s="strong"
print(s[::-1])

a = [1,3,5,7]
print(str(a))
print(sum(a))
print(sum(a)/len(a))

print(datetime.datetime.now().date())
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(datetime.datetime.now().strftime('%H:%M:%S'))



    #index at 1
    #position at 1
    #current value at list[1]
    #is position > 0, && list[0] > current    is left of current > current

    #index 2, position 2, current list[index]
    #spot before list[index] > current
    #position reuces to check again


def insertSort(alist):
    for i in range(1, len(alist)):
        current = alist[i]
        position = i

        while position > 0 and alist[position-1] > current:
            alist[position] = alist [position-1]
            position = position-1
        alist[position] = current
alist = [23, 32, 12, 53453, 3, 24, 56, 76]
insertSort(alist)
print(alist)


def binarySearch(alist, item):
    begining = 0
    endoflist = len(alist) - 1
    foundit = False

    while begining <= endoflist and not foundit:
        middle = (begining + endoflist)//2
        if alist[middle] == item:
            foundit = True
        else:
            if item < alist[middle]:
                endoflist = middle -1
            else:
                begining = middle + 1
    return foundit

print(binarySearch([1, 3, 5, 7, 9], 6))
print(binarySearch([1, 3, 5, 7, 9], 5))