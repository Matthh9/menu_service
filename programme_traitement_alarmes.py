# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:30:19 2022

@author: Matthieu
"""
 
from pandas import DataFrame

def splitAlarmes(text):
    text= text.replace("th>", "td>")
    text= text.replace("</tr>", "")
    text = text.replace("</td>", "")
    split_tr=text.split('<tr>')
    split_th=split_tr[1].replace('</th>', '').replace('</tr>', '').split('<th>')[0].split('<td>')
    index_additionnal_text = split_th.index('Additional Text')
    index_managed_onject = split_th.index('Managed Object')
    
    split_td=[]
    for element in split_tr[2:]:
        temp = element.replace('</td>', '').replace('</tr>', '').split('<td>')
        add = temp[index_additionnal_text].split("\n",1)[0]
        managed = temp[index_managed_onject]
        split_td.append([add, managed])


    return split_td
    
    
def traitementAlarmesGenerales(chaine):
    tab = splitAlarmes(chaine)
    text=""
    for element in tab:
        text = text+element[0]+"\n>>"+element[1]+"\r\n"+"\r\n"
    text = "".join(text.rsplit("\r\n", 2))
    return(text)
    
    
    
def traitementAlarmesDCM(chaine):
    tab = splitAlarmes(chaine)
    
    traitement=[]
    for element in tab:
        dcm = element[1].split(" ", 2)[1]
        port = element[0].split(" on ")[1].split(", TS")[0]
        ip = element[0].split(", TS ")[1].split(":")[0]
        traitement.append([dcm, port, ip])
    
    df = DataFrame(traitement, columns = ["a", "b", "c"])
    df = df.sort_values(["a", "b"], ascending = (True, True))
    
    traitement = df.values.tolist()
    
    dcm=traitement[0][0]
    port=traitement[0][1]
    chaines=[]
    traitement2=[]
    for element in traitement:
        if (dcm==element[0] and port==element[1]):
            chaines.append(element[2])
        else:
            traitement2.append([dcm, port, chaines])
            dcm = element[0]
            port = element[1]
            chaines = [element[2]]
    #pour le dernier élément sinon il en manque un
    traitement2.append([dcm, port, chaines])
    
    
    text=""
    for element in traitement2:
        text+= element[0]+" : "+element[1]+"\r\n"
        text+= "\r\n".join(element[2])
        text+="\r\n"+"\r\n"
    
    text = "".join(text.rsplit("\r\n", 1))
    return(text)


# test = traitementAlarmesDCM(text)