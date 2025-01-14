#"d01": "161693FA83F973FA5BF9CFC607F96FFCA3FABFE003E0030000800F8C0EFF180B1515140CFE00FF00FF00FFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000009EF6",
#"d02": "1616910800FA83180B151514FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000000EFFFFFFFFFFFFFFFFFFFFFC9FFABFE003E003FFFF000C30333632FFFFFFFF7720",
#"d03": "161681F973FA5FF9D3C60FF96FFFFFFFFFFFFFFFFFFFFF00800F8C533933303039494434363957323430330059E9",
#"d04": "1616C502F973F88BC937FA2F3035FFF103405454542B2A2A5C343005000E000E020000000E00AA000500000AAD02010100FA5FFFFF2C36",

str = "F973F88BC937FA2F3035FFF103405454542B2A2A5C343005000E000E020000000E00AA000500000AAD02010100FA5FFFFF2C36"
str = "FA83F973FA5BF9CFC607F96FFCA3FABFE003E0030000800F8C0EFF180B1515140CFE00FF00FF00FFFFFFFFFFFFFFFFFFFFFFFF"
str = "F9C3F983F9C7FA03C4C7F973E003E003E003E0030000B40A5D0EA3180C0105040CFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000000000000000000000000000000000000000000000000000000416091600002E12"

def Get_Number(vector,index,Bytes):
    length = len(vector)
    index = index - 1
    index = index * 2
    Bytes = Bytes * 2
    Cnt_Bytes = 0
    numero = 0
    for i in range(0,length):
        if(i >= index):
            if(Cnt_Bytes < Bytes):
                numero = numero << 4
                numero = numero | Caracter_Hex(vector[i])
                Cnt_Bytes = Cnt_Bytes + 1
    return numero

def Caracter_Hex(val):
    if val == '0':
        return 0x0
    if val == '1':
        return 0x1
    if val == '2':
        return 0x2
    if val == '3':
        return 0x3
    if val == '4':
        return 0x4
    if val == '5':
        return 0x5
    if val == '6':
        return 0x6
    if val == '7':
        return 0x7
    if val == '8':
        return 0x8
    if val == '9':
        return 0x9    
    if val == 'a' or val == 'A':
        return 0xA
    if val == 'b' or val == 'B':
        return 0xB
    if val == 'c' or val == 'C':
        return 0xC
    if val == 'd' or val == 'D':
        return 0xD
    if val == 'e' or val == 'E':
        return 0xE
    if val == 'f' or val == 'F':
        return 0xF

def Valor_Convertido(valve):
    if(valve <= 0xFF):
        valve = 0xC000 | valve
    aux = valve
    signo = 0
    aux = aux & 0xF000
    if(aux == 0xF000):
        print("Es negativo")
        signo = 1
        valve = valve - 0xF000
    else:
        valve = valve - 0xC000
    valve = valve & 0xFFFF
    valve = valve >> 4
    if(signo==1):
        valve = 0x100 - valve
    valve = valve / 4.0
    if(signo == 1):
        valve = -valve
    return valve

print("Valor de setpoint: ")
numero = Get_Number(str,1,2)
numero = Valor_Convertido(numero)
print(numero)

print("Valor de suministro: ")
numero = Get_Number(str,3,2)
numero = Valor_Convertido(numero)
print(numero)

print("Valor de retorno: ")
numero = Get_Number(str,5,2)
numero = Valor_Convertido(numero)
print(numero)

print("Valor de retorno: ")
numero = Get_Number(str,7,2)
numero = Valor_Convertido(numero)
print(numero)

print("Valor de retorno: ")
numero = Get_Number(str,9,2)
numero = Valor_Convertido(numero)
print(numero)