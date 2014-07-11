def main():
    a = "python python python"
    a = a.split()
    for i in a:
        print i,"=",a.count(i)

if __name__ == "__main__" :
    main()