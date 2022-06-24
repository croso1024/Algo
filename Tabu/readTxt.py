# -*- coding: utf-8 -*-
import csv 
columnName = ["縣市","經度","緯度"]
csvfile = "city.csv" 

# with open("city.csv","w+") as f: 
#     csvwriter = csv.writer(f)
#     csvwriter.writerow(columnName)

with open("city.txt","r") as f:
    for line in f.readlines():
        line = line.split(",")
        with open("city.csv","a+") as f2:
            writer = csv.writer(f2)
            writer.writerow(line)