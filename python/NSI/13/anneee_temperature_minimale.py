t_moy = [14.9, 13.3, 13.1, 12.5, 13.0, 13.6, 13.7]
annees = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

def annee_temperature_minimale(t_moy, annees):
    t_min = t_moy[0]
    annee_la_plus_froide = annees[0]
    for i in range(1, len(t_moy)):
        if t_moy[i] < t_min:
            t_min = t_moy[i]
            annee_la_plus_froide = annees[i]
    return f"L'année la plus froide est {annee_la_plus_froide}, avec une moyenne de {t_min} °c"

print(annee_temperature_minimale(t_moy, annees))