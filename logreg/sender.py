import re


def use_sender():
    try:
        file = open(r'use_sender.dat', 'r')
        cnt = int(file.readline())
        use = int(file.readline())
        times = int(file.readline())
        file.close()
        file = open(r'use_sender.dat', 'w')
        file.write(str(cnt)+'\n')
        if(times == 2):
            use = (use + 1) % cnt
            file.write(str(use)+'\n')
            file.write(str(0)+'\n')
        else:
            file.write(str(use)+'\n')
            times = times + 1
            file.write(str(times)+'\n')
        file.close()
        return use
    except FileNotFoundError:
        return 0


def sender(num):
    num = int(num) + 1
    file = open(r'sender_list.dat', 'r')
    handle = ""
    for i in range(0, num):
        handle = str(file.readline())
    file.close()
    return handle
