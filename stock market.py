from CuckooHash import CuckooHash


def stocks(name, ch):
    with open(name, "r") as a:
        for i in a:
            sign, cid, stks = i.split(":")
            cid = int(cid)
            stks = int(stks)
            if ch.lookup(cid):
                ch.update(sign, cid, stks)
            elif sign == '+':
                ch.insert([cid, stks])


def display(ch):
    for i in ch.hashtable:
        for j in i:
            if j is not None:
                print("CID: ", j[0], "\tStocks: ", j[1])
    if ch.stash.population > 0:
        display(ch.stash)


def main():
    ch = CuckooHash()
    name = input("Enter the name of the file containing the required data: ")
    stocks(name, ch)
    display(ch)


if __name__ == '__main__':
    main()
