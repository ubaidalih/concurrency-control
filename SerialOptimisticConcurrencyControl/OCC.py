from collections import deque

lock = []
records = []

filename = input("Enter the name of the file: ")
# filename = "test1.txt"
file = open(filename, "r")
text = list(file)
records = [s.strip() for s in text]
original = ""
for i in range (len(records)):
    original += records[i] + ";"
records.reverse()

transactions = {1:{"start": 1, "validation": 0, 
            "finish": 0, "result":None, "read":[], "write":[]}}

def intersect(arr1, arr2):
    res = []
    for i in range(len(arr1)):
        for j in range (len(arr2)):
            if arr1[i] == arr2[j]:
                res.append(arr1[i])
    return res

time = 1
while (len(records) > 0) :
    current = (records.pop())
    msg = ""
    trx = int(current[1])
    currComponent = ["", "", ""]
    currComponent[0] = trx
    currComponent[1] = current[0]

    if trx not in transactions.keys() :
        transactions[trx] = {"start": time, "validation": 0, 
                    "finish": 0, "result":None, "read":[], "write":[]}

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
    if (currComponent[1] == "C"):
        transactions[currComponent[0]]["validation"] = time
        result = "berhasil"
        for key in transactions.keys():
            transaction = transactions[key]
            if (transaction["validation"] != 0) and (transaction["validation"] < transactions[currComponent[0]]["validation"]):
                if transaction["finish"] < transactions[currComponent[0]]["start"] :
                    result = "berhasil"
                else :
                    Intersect = intersect(transaction["write"], transactions[currComponent[0]]["read"])
                    if (transaction["finish"] < time) and (len(Intersect) == 0):
                            result = "berhasil"
                    else :
                        result = f"terjadi intersect antara transaksi {currComponent[0]} dengan transaksi {key} yaitu saat pembacaan data {Intersect}"
                        break
        transactions[currComponent[0]]["result"] = result
        
        # finish phase
        transactions[currComponent[0]]["finish"] = time if transactions[currComponent[0]]["result"] == "berhasil" else -1

    time += 1

print(f"\nTransaksi : {original}")
print("\nHasil :\n")
for key in transactions.keys():
    transaction = transactions[key]
    msg = transaction["result"]
    success = "- start = " + str(transaction["start"]) + "\n- validation = " + str(transaction["validation"]) + "\n- finish = " + str(transaction["finish"])
    hasil = f"berhasil : \n{success}" if transaction["result"] == "berhasil" else f"gagal karena {msg}"
    print(f"Transaksi {key} {hasil}")
    print()