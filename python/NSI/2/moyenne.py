def moyenne (lst):
    somme =0
    for i in range(len(lst)):
        somme += lst[i]
    moyenne = somme / len(lst)
    return moyenne



print(moyenne([20,10,10,20]))