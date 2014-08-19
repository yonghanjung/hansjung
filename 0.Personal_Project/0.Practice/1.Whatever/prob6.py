from collections import Counter

def countWords(a_list):
    words = {}
    for i in range(len(a_list)):
        item = a_list[i]
        count = a_list.count(item)
        words[item] = count
    return sorted(words.items(), key = lambda item: item[1], reverse=True)

def main():
    a = "python python python"
    print countWords(a.split())

if __name__ == "__main__":
    main()