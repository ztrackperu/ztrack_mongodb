from datetime import datetime

def per_actual():
    now = datetime.now()
    mes = now.month 
    per = now.year
    day = now.day
    periodo = str(day)+"_"+str(mes)+"_"+str(per)
    return periodo


mensaje_completo =  "TUNEL_"+per_actual() +" "+str(datetime.now())
with open("programado.txt","a+") as file:
    file.write(mensaje_completo +"\n")