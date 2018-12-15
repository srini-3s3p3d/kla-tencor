import csv
tt=['as','as','as','as']
with open('data.csv','w') as csvfile:
    writer=csv.writer(csvfile,delimiter=' ')
    for w in tt:
        writer.append(w[0])
        writer.append(w[1])