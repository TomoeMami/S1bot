from time import sleep
import os

def run_child():
    os.system('python check.py')


def run_parent():
    count = 0
    while True:
        os.system('python bili-check.py')
        count = count + 1
        # if(count == 8):
        #     os.system('python dy-check.py')
        #     count = 0
        sleep(20)

if __name__ == '__main__':
    run_parent()

