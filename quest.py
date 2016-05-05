from os import listdir
import csv
files = listdir("./quest")

mytxt = list(filter(lambda x: x.endswith('.txt'), files))
res = {}
doubles = 0
sug = []
with open('suggest.txt','r',errors='ignore') as f:
    for line in f:
        sug.append(str.lower(line))
with open('suggest-страны.txt','r') as f:
    for line in f:
        sug.append(str.lower(line))
suggests = 0
print("Suggest file strings: %s"%len(sug))
for name in mytxt:
    with open("./quest/"+name,'r') as f:
        for line in f:
            city = name.split(' ')[-1][0:-4]
            if line not in res.keys():
                if line not in sug:
                    res[line] = city
                else:
                    suggests = suggests + 1
                    print("Suggests: %s"%suggests)
            else:
                doubles = doubles + 1
                print("Doubles: %s"%doubles)
print("Unique: %s"%len(res))
print("Doubles: %s"%doubles)
print("Suggests: %s"%suggests)                
with open('question.csv','w') as result:
    writer = csv.writer(result,delimiter=',')
    for (line,city) in res.items():
        writer.writerow([city,line])