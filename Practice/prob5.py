import datetime 
def main():   
    today = datetime.datetime.now()
    a = str(today)[:-7]
    print "[",a,"]"

if __name__ == '__main__':
    main()