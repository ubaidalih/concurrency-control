lock = []
records = []

filename = input("Enter the name of the file: ")
file = open(filename, "r")
text = list(file)
records = [s.strip() for s in text]

transactions = {}

def intersect(arr1, arr2):
    res = []
    for i in range(len(arr1)):
        for j in range (len(arr2)):
            if arr1[i] == arr2[j]:
                res.append(arr1[i])
    return res

def isEnd(transactions):
    res = True
    for i in range (1, len(transactions)+1):
        if transactions[i]["finish"] == 0:
            res = False
    return res

for i in range (len(records)):
    current = (records[i])
    trx = int(current[1])
    if trx not in transactions.keys() :
        transactions[trx] = {"start": i+1, "validation": 0, 
                    "finish": 0, "result":None, "read":[], "write":[]}

for transaction in transactions.keys() :
    msg = ""
    for i in range (len(records)):
        current = records[i]
        trx = int(current[1])
        if trx == transaction :
            time = i+1
            current = (records[i])
            currComponent = ["", "", ""]
            currComponent[0] = trx
            currComponent[1] = current[0]
            if current[0] != "C" :
                currComponent[2] = current[3]

            # start phase
            if currComponent[0] not in transactions.keys() :
                transactions[currComponent[0]] = {"start": time, "validation": 0, 
                            "finish": 0, "result":None, "read":[], "write":[]}
            if currComponent[1] == "R":
                if currComponent[2] not in transactions[currComponent[0]]["read"] :
                    transactions[currComponent[0]]["read"].append(currComponent[2])
            elif currComponent[1] == "W":
                if currComponent[2] not in transactions[currComponent[0]]["write"] :
                    transactions[currComponent[0]]["write"].append(currComponent[2])

            # validation phase
            if (currComponent[1] == "W") and (transactions[currComponent[0]]["result"] == None):
                transactions[currComponent[0]]["validation"] = time
                result = True
                if currComponent[0] == 1:
                    result = True
                for j in range (1,currComponent[0]):
                    if transactions[j]["result"] == False:
                        msg = f"transaksi {j} gagal"
                        result = False
                        break
                    if transactions[j]["finish"] < transactions[currComponent[0]]["start"] :
                        result = True
                    else :
                        if (transactions[j]["finish"] < time):
                            Intersect = intersect(transactions[j]["write"], transactions[currComponent[0]]["read"])
                            if (len(Intersect) == 0):
                                result = True
                            else :
                                msg = f"terjadi intersect antara transaksi {transaction} dengan transaksi {j} yaitu saat pembacaan data {Intersect}"
                                result = False
                                break
                        else:
                            msg = f"transaksi {transaction} melakukan write sebelum transaksi {j} selesai"
                            result = False
                            break
                transactions[currComponent[0]]["result"] = result

            # rollback
            if (transactions[currComponent[0]]["result"] == False):
                p = "rollback"

            # finish phase
            if (currComponent[1] == "W") and (transactions[currComponent[0]]["result"] == True):
                transactions[currComponent[0]]["finish"] = time

    hasil = "berhasil" if transactions[currComponent[0]]["result"] == True else f"gagal karena {msg}"
    print(f"Transaksi {transaction} {hasil}")