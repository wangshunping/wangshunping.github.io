

'''
    Modify file name
'''

import re
import os

def main():
    filenamelist = os.listdir('.')
    pattern = re.compile(r'(^\d{4}-\d{2}-\d{2})-([\w\-\.]+)')
    for x in filenamelist:
         os.rename(x,pattern.sub(func,x))


def func(m):
    return m.group(1).title()+'#'+m.group(2).title()

if __name__ == "__main__":
    main()
