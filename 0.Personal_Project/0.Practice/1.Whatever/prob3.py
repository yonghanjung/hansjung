from random import shuffle 
def main():
    x = [[i] for i in range(1,47)]
    shuffle(x)
    print sorted(x[0:6])

if __name__ == '__main__':
    main()