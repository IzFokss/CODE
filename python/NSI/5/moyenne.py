def moyenne(notes):
    numerateur = 0
    denominateur = 1
    for i in range(len(notes)):
        numerateur += notes[i][0] * notes[i][1]
        denominateur *= notes[i][1]
    return numerateur / denominateur

print(moyenne([(15.0,2),(10.0,5),(18.5,4)]))
