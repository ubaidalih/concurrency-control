from collections import deque

lock = []
queue = []

filename = input("Enter the name of the file: ")
file = open(filename, "r")
text = list(file)
queue = [s.strip() for s in text]
queue.reverse()
original = queue.copy()
original.reverse()

while (len(queue) != 0):
    current = (queue.pop())
    
    currComponent = ["", ""]
    currComponent[0] = "T"+current[1]
    if (current[0] != "C"):
        currComponent[1] = current[3]
    
    print(current)
    if (current[0] == 'R'):
        R = currComponent
        
        if (R in lock):
            print('*'+R[0], "already has exclusive lock for", R[1])
            print("[>]"+R[0], "READ" , R[1])
        else:
            print(R[0], "request lock for", R[1])
            lockNow = False
            for transaction in (lock):
                if (transaction[1] == R[1]):
                    lockNow = transaction[0]

            if (lockNow != False):
                print("[X]Deny request,", lockNow, "has the lock")

                currQueue = []
                for i in range (len(original)):
                    if (original[i][0] == "C" and original[i][1] == lockNow[1]):
                        break
                    if (original[i][1] == current[1]):
                        currQueue.append(original[i])
                currQueue.reverse()

                i = len(queue) - 1
                while i >= 0:
                    if queue[i][0] == "C" and queue[i][1] == lockNow[1] :
                        break
                    if (queue[i][1] == current[1]):
                        queue.remove(queue[i])
                    i -= 1
                        
                for i in range (len(queue)):
                    if (queue[i][0] == "C" and queue[i][1] == lockNow):
                        for j in range (len(currQueue)):
                            queue.insert(i+j, currQueue[j])
                        break
                
                i = 0
                while i < len(lock):
                    if (lock[i][0][1] == current[1]):
                        print("[>]"+lock[i][0], "UNLOCKS", lock[i][1])
                        lock.remove(lock[i])
                    else:
                        i += 1

                print("Put", "T"+current[1], "after", lockNow, "commit")
                    
            else:
                print("lock request approved")
                print("[>]"+R[0], "LOCK", R[1])
                lock.append([R[0],R[1]])
                print("[>]"+R[0], "READ" , R[1])
        
    elif (current[0] == 'W'):
        W = currComponent
        
        if ([W[0],W[1]] in lock):
            print('*'+W[0], "already has exclusive lock for", W[1])
            print("[>]"+W[0], "WRITE" , W[1])
        else:
            print(W[0], "request lock for", W[1])
            lockNow = False
            for transaction in (lock):
                if (transaction[1] == W[1]):
                    lockNow = transaction[0]
            if (lockNow):
                print("[X]Deny request,", lockNow, "has the lock")

                currQueue = []
                for i in range (len(original)):
                    if (original[i][0] == "C" and original[i][1] == lockNow[1]):
                        break
                    if (original[i][1] == current[1]):
                        currQueue.append(original[i])
                currQueue.reverse()

                i = len(queue) - 1
                while i >= 0:
                    if queue[i][0] == "C" and queue[i][1] == lockNow[1] :
                        break
                    if (queue[i][1] == current[1]):
                        queue.remove(queue[i])
                    i -= 1
                
                for i in range (len(queue)):
                    if (queue[i][0] == "C" and queue[i][1] == lockNow[1]):
                        for j in range (len(currQueue)):
                            queue.insert(i+j, currQueue[j])
                        break
                
                i = 0
                while i < len(lock):
                    if (lock[i][0][1] == current[1]):
                        print("[>]"+lock[i][0], "UNLOCKS", lock[i][1])
                        lock.remove(lock[i])
                    else:
                        i += 1

                print("Put", "T"+current[1], "after", lockNow, "commit")
                    
            else:
                print("lock request approved")
                print("[>]"+W[0], "LOCK", W[1])
                lock.append([W[0],W[1]])
                print("[>]"+W[0], "WRITE" , W[1])
        
    elif (current[0] == 'C'):
        trx = "T"+current.strip('C')
        i = 0
        while i < len(lock):
            if (lock[i][0] == trx):
                print("[>]"+lock[i][0], "UNLOCKS", lock[i][1])
                lock.remove(lock[i])
            else:
                i += 1
    else:
        print("File tidak sesuai format.")
    print()