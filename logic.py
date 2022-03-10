import requests

reco=requests.get("https://api.npoint.io/14804045beafa4cbc0ec")
reco=reco.json()
listt=[]
keys=[]
for m in reco:
    listt.append(reco[m])
    keys.append(m)





        
       
