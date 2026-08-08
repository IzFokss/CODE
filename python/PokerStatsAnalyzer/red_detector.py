import time
import os
from datetime import datetime

import mss
import numpy as np
from PIL import Image, ImageDraw


# ============================================================
# CONFIGURATION
# ============================================================

LOBBY_FILE = "lobby.png"
TABLE_FILE = "table.png"

# Taille des petites zones analysées
ZONE_WIDTH = 120
ZONE_HEIGHT = 60

# Espacement entre les zones
STEP_X = 60
STEP_Y = 30

# Nombre de zones utilisées pour le vote
TOP_ZONES = 10

# Seuil de rouge nécessaire
# Une zone sera considérée "rouge" si son pourcentage
# de pixels rouges dépasse ce seuil.
RED_THRESHOLD = 0.18

# Nombre de secondes pendant lesquelles une nouvelle
# détection doit rester présente avant validation.
CONFIRM_TIME = 2.5

# Intervalle entre deux captures
INTERVAL = 0.5

LOG_FILE = "states.log"

CANDIDATES_IMAGE = "red_candidates.png"


# ============================================================
# DETECTION DU ROUGE
# ============================================================

def red_percentage(image):
    """
    Retourne le pourcentage de pixels rouges dans une image.

    On cherche principalement le rouge du tapis.
    """

    arr = np.array(image).astype(np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # Conditions pour considérer un pixel comme rouge.
    red_mask = (
        (r > 100)
        & (r > g * 1.35)
        & (r > b * 1.35)
        & ((r - g) > 35)
    )

    return np.mean(red_mask)


# ============================================================
# CHARGEMENT
# ============================================================

if not os.path.exists(LOBBY_FILE):
    print(f"ERREUR : {LOBBY_FILE} introuvable.")
    raise SystemExit

if not os.path.exists(TABLE_FILE):
    print(f"ERREUR : {TABLE_FILE} introuvable.")
    raise SystemExit


lobby = Image.open(LOBBY_FILE).convert("RGB")
table = Image.open(TABLE_FILE).convert("RGB")


if lobby.size != table.size:

    print("ERREUR : les images n'ont pas la même résolution.")
    print("Lobby :", lobby.size)
    print("Table :", table.size)

    raise SystemExit


width, height = lobby.size

print(f"Résolution : {width}x{height}")
print()
print("Analyse des zones rouges...")
print()


# ============================================================
# ANALYSE DES CANDIDATES
# ============================================================

candidates = []

for y in range(
    0,
    height - ZONE_HEIGHT + 1,
    STEP_Y
):

    for x in range(
        0,
        width - ZONE_WIDTH + 1,
        STEP_X
    ):

        lobby_crop = lobby.crop((
            x,
            y,
            x + ZONE_WIDTH,
            y + ZONE_HEIGHT
        ))

        table_crop = table.crop((
            x,
            y,
            x + ZONE_WIDTH,
            y + ZONE_HEIGHT
        ))

        lobby_red = red_percentage(lobby_crop)
        table_red = red_percentage(table_crop)

        # On veut :
        #
        # lobby rouge faible
        # table rouge fort
        #
        # Donc le score est :
        # table_red - lobby_red

        score = table_red - lobby_red

        candidates.append({
            "x": x,
            "y": y,
            "width": ZONE_WIDTH,
            "height": ZONE_HEIGHT,
            "lobby_red": lobby_red,
            "table_red": table_red,
            "score": score
        })


# Trier du meilleur score au moins bon
candidates.sort(
    key=lambda c: c["score"],
    reverse=True
)


# ============================================================
# AFFICHAGE
# ============================================================

print("=" * 75)
print("             MEILLEURES ZONES ROUGES")
print("=" * 75)
print()

for i, c in enumerate(candidates[:TOP_ZONES], 1):

    print(
        f"#{i:2} "
        f"x={c['x']:4} "
        f"y={c['y']:4} | "
        f"Lobby={c['lobby_red']*100:5.1f}% | "
        f"Table={c['table_red']*100:5.1f}% | "
        f"Score={c['score']*100:5.1f}%"
    )


# ============================================================
# IMAGE DES CANDIDATES
# ============================================================

result = lobby.copy()
draw = ImageDraw.Draw(result)

for i, c in enumerate(candidates[:TOP_ZONES], 1):

    x = c["x"]
    y = c["y"]

    draw.rectangle(
        [
            x,
            y,
            x + ZONE_WIDTH,
            y + ZONE_HEIGHT
        ],
        outline="red",
        width=3
    )

    draw.text(
        (x + 5, y + 5),
        f"#{i}",
        fill="red"
    )


result.save(CANDIDATES_IMAGE)

print()
print(f"Image créée : {CANDIDATES_IMAGE}")
print()


# ============================================================
# SELECTION DES ZONES
# ============================================================

selected_zones = candidates[:TOP_ZONES]

print("Zones sélectionnées pour le vote :")

for i, c in enumerate(selected_zones, 1):

    print(
        f"#{i}: "
        f"x={c['x']} "
        f"y={c['y']} "
        f""
        f"Lobby={c['lobby_red']*100:.1f}% "
        f""
        f"Table={c['table_red']*100:.1f}%"
    )


# ============================================================
# SEUILS INDIVIDUELS
# ============================================================

# Pour chaque zone, on crée un seuil entre :
#
# quantité de rouge dans le lobby
# quantité de rouge à table
#
# Exemple :
#
# Lobby = 2%
# Table = 35%
# Seuil = 18.5%

for c in selected_zones:

    c["threshold"] = (
        c["lobby_red"] +
        c["table_red"]
    ) / 2


# ============================================================
# LOG
# ============================================================

def log_state(state, vote, total):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = (
        f"[{timestamp}] "
        f"STATE = {state} | "
        f"Vote = {vote}/{total}"
    )

    print(message)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")


# Nouveau fichier log
with open(
    LOG_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "=== ZYNGA RED TABLE DETECTOR ===\n"
    )


# ============================================================
# DETECTION D'UNE CAPTURE
# ============================================================

def detect_current_screen(sct):

    votes_table = 0

    total = len(selected_zones)

    for c in selected_zones:

        screenshot = sct.grab({
            "left": c["x"],
            "top": c["y"],
            "width": c["width"],
            "height": c["height"]
        })

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        current_red = red_percentage(image)

        if current_red > c["threshold"]:

            votes_table += 1

    # Majorité des zones
    if votes_table >= (total // 2 + 1):

        return "TABLE", votes_table, total

    else:

        return "LOBBY", votes_table, total


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

print()
print("=" * 75)
print("             DETECTION EN TEMPS REEL")
print("=" * 75)
print()
print("Le programme va maintenant surveiller l'écran.")
print()
print("Passe de :")
print("  LOBBY -> TABLE -> COUCHÉ -> LOBBY")
print()
print("Les changements seront enregistrés dans states.log")
print()
print("CTRL+C pour arrêter.")
print()


current_state = None

candidate_state = None
candidate_since = None


with mss.mss() as sct:

    while True:

        try:

            detected_state, vote, total = (
                detect_current_screen(sct)
            )

            # Première détection
            if current_state is None:

                current_state = detected_state

                log_state(
                    current_state,
                    vote,
                    total
                )

            # Même état que précédemment
            elif detected_state == current_state:

                candidate_state = None
                candidate_since = None

            # Nouveau état détecté
            else:

                # Première apparition du nouvel état
                if candidate_state != detected_state:

                    candidate_state = detected_state
                    candidate_since = time.time()

                # Le nouvel état persiste
                else:

                    elapsed = (
                        time.time()
                        - candidate_since
                    )

                    if elapsed >= CONFIRM_TIME:

                        current_state = detected_state

                        log_state(
                            current_state,
                            vote,
                            total
                        )

                        candidate_state = None
                        candidate_since = None

            time.sleep(INTERVAL)

        except KeyboardInterrupt:

            print()
            print("Arrêt du détecteur.")
            break

        except Exception as e:

            print()
            print("Erreur :", e)
            time.sleep(1)