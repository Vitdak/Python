import os

def main():
    i = 0
    path = "C:/Mokymai/Py/pics/"
    for filename in os.listdir(path):
        dst = "img" + str(i) + ".jpg"
        source = path + filename
        dst = path + dst
        os.rename(source,dst)
        i = i + 1

main()
