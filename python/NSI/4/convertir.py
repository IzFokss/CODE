def convertir(tab):
    conversion = 0
    for i in range(len(tab)):
        conversion = conversion * 2 + tab[i]

    return conversion


print(convertir([1,0,1,0,0]))
