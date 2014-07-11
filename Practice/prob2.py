def main():
    a  = input()
    for i in range(a+1):
        print '  ' * (a-i-1), 
        print '*' * (i+1)

if __name__ == '__main__':
    main()