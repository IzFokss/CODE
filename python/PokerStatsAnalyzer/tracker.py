import time
import os
import re
import csv
from datetime import datetime

import mss
import numpy as np
import pytesseract
from PIL import Image


# ============================================================
# TESSERACT
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# CONFIGURATION
# ============================================================

# Zone de la BANKROLL en haut de l'écran
BANKROLL_REGION = {
    "left": 680,
    "top": 5,
    "width": 260,
    "height": 65
}


# ------------------------------------------------------------
# Zones utilisées pour détecter TABLE / LOBBY
# ------------------------------------------------------------

# Ces zones viennent de ton test précédent.
# On les conservera si elles continuent à fonctionner.

ZONES = [
    {"x": 480, "y": 450, "width": 120, "height": 60},
    {"x": 540, "y": 450, "width": 120, "height": 60},
    {"x": 480, "y": 510, "width": 120, "height": 60},
    {"x": 540, "y": 510, "width": 120, "height": 60},
    {"x": 360, "y": 450, "width": 120, "height": 60},
    {"x": 420, "y": 420, "width": 120, "height": 60},
    {"x": 540, "y": 390, "width": 120, "height": 60},
    {"x": 420, "y": 390, "width": 120, "height": 60},
    {"x": 600, "y": 330, "width": 120, "height": 60},
    {"x": 480, "y": 390, "width": 120, "height": 60},
]


RED_THRESHOLD = 0.18

INTERVAL = 0.5

CONFIRM_TIME = 2.5

CSV_FILE = "sessions.csv"

LOG_FILE = "tracker.log"


# ============================================================
# OUTILS
# ============================================================

def red_percentage(image):

    arr = np.array(image).astype(np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    red_mask = (
        (r > 100)
        & (r > g * 1.35)
        & (r > b * 1.35)
        & ((r - g) > 35)
    )

    return np.mean(red_mask)


# ============================================================
# OCR BANKROLL
# ============================================================

def read_bankroll(sct):

    screenshot = sct.grab(BANKROLL_REGION)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    # Agrandissement
    image = image.resize(
        (
            image.width * 4,
            image.height * 4
        )
    )

    from PIL import ImageEnhance, ImageFilter

    image = image.convert("L")

    image = ImageEnhance.Contrast(image).enhance(3)

    image = image.filter(
        ImageFilter.SHARPEN
    )

    text = pytesseract.image_to_string(
        image,
        config="--psm 7"
    )

    text = text.strip()

    # --------------------------------------------------------
    # DEBUG OCR
    # --------------------------------------------------------

    # Décommente cette ligne si on veut voir exactement
    # ce que Tesseract lit.
    #
    # print("OCR =", repr(text))

    # --------------------------------------------------------
    # RECHERCHE DES NOMBRES
    # --------------------------------------------------------

    matches = re.findall(
        r"\d[\d,]*",
        text
    )

    if not matches:
        return None

    valid_numbers = []

    for number in matches:

        number = number.replace(",", "")

        try:
            value = int(number)

        except ValueError:
            continue

        # ----------------------------------------------------
        # FILTRE ANTI-FAUX OCR
        # ----------------------------------------------------
        #
        # On accepte :
        #
        # 0
        # ou
        # les bankrolls >= 1 million
        #
        # Mais on ignore :
        #
        # 2
        # 3
        # 900
        # 12345
        #

        if value == 0 or value >= 1_000_000:

            valid_numbers.append(value)

    if not valid_numbers:
        return None

    # S'il y a plusieurs nombres, on prend le plus grand.
    return max(valid_numbers)


# ============================================================
# DETECTION TABLE / LOBBY
# ============================================================

def detect_state(sct):

    table_votes = 0

    for zone in ZONES:

        screenshot = sct.grab({
            "left": zone["x"],
            "top": zone["y"],
            "width": zone["width"],
            "height": zone["height"]
        })

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        red = red_percentage(image)

        if red > RED_THRESHOLD:
            table_votes += 1

    total = len(ZONES)

    if table_votes >= (total // 2 + 1):

        return "TABLE"

    return "LOBBY"


# ============================================================
# LOG
# ============================================================

def log(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    line = f"[{timestamp}] {message}"

    print(line)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(line + "\n")


# ============================================================
# CSV
# ============================================================

def create_csv():

    if not os.path.exists(CSV_FILE):

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "session",
                "start",
                "end",
                "duration_seconds",
                "bankroll_start",
                "bankroll_end",
                "profit"
            ])


def save_session(
    start_time,
    end_time,
    bankroll_start,
    bankroll_end
):

    duration = int(
        (end_time - start_time).total_seconds()
    )

    profit = None

    if (
        bankroll_start is not None
        and bankroll_end is not None
    ):

        profit = bankroll_end - bankroll_start

    # Numéro de session
    session_number = 1

    try:

        with open(
            CSV_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

            session_number = len(lines)

    except FileNotFoundError:

        pass

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            session_number,
            start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            end_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            duration,
            bankroll_start,
            bankroll_end,
            profit
        ])

    log(
        f"SESSION TERMINÉE | "
        f"Départ={bankroll_start} | "
        f"Fin={bankroll_end} | "
        f"Profit={profit}"
    )


# ============================================================
# INITIALISATION
# ============================================================

create_csv()

with open(
    LOG_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "=== ZYNGA POKER TRACKER ===\n"
    )


print()
print("======================================")
print("       ZYNGA POKER TRACKER")
print("======================================")
print()
print("Tracker lancé.")
print("Passe sur Zynga Poker.")
print("CTRL+C pour arrêter.")
print()


# ============================================================
# VARIABLES
# ============================================================

current_state = None

candidate_state = None

candidate_since = None

last_lobby_bankroll = None

session_start = None

session_bankroll_start = None


# ============================================================
# BOUCLE
# ============================================================

with mss.MSS() as sct:

    while True:

        try:

            detected_state = detect_state(sct)

            # ------------------------------------------------
            # CHANGEMENT DE STATE
            # ------------------------------------------------

            if detected_state != current_state:

                # Première détection
                if current_state is None:

                    current_state = detected_state

                    log(
                        f"STATE = {current_state}"
                    )

                # Nouvelle détection candidate
                elif candidate_state != detected_state:

                    candidate_state = detected_state

                    candidate_since = time.time()

                # Confirmation
                else:

                    elapsed = (
                        time.time()
                        - candidate_since
                    )

                    if elapsed >= CONFIRM_TIME:

                        old_state = current_state

                        current_state = detected_state

                        candidate_state = None
                        candidate_since = None

                        log(
                            f"STATE CHANGE : "
                            f"{old_state} -> "
                            f"{current_state}"
                        )

                        # ====================================
                        # LOBBY -> TABLE
                        # ====================================

                        if (
                            old_state == "LOBBY"
                            and current_state == "TABLE"
                        ):

                            session_start = datetime.now()

                            session_bankroll_start = (
                                last_lobby_bankroll
                            )

                            log(
                                f"SESSION START | "
                                f"Bankroll="
                                f"{session_bankroll_start}"
                            )

                        # ====================================
                        # TABLE -> LOBBY
                        # ====================================

                        elif (
                            old_state == "TABLE"
                            and current_state == "LOBBY"
                        ):

                            # On attend un peu avant OCR
                            # pour laisser le lobby apparaître.

                            time.sleep(1)

                            bankroll_end = read_bankroll(
                                sct
                            )

                            if bankroll_end is not None:

                                last_lobby_bankroll = (
                                    bankroll_end
                                )

                            log(
                                f"Bankroll lobby = "
                                f"{bankroll_end}"
                            )

                            if session_start is not None:

                                save_session(
                                    session_start,
                                    datetime.now(),
                                    session_bankroll_start,
                                    bankroll_end
                                )

                                session_start = None
                                session_bankroll_start = None


            # ------------------------------------------------
            # OCR BANKROLL DANS LE LOBBY
            # ------------------------------------------------

            if current_state == "LOBBY":

                bankroll = read_bankroll(sct)

                if bankroll is not None:

                    # Si une transition candidate vers TABLE est en cours,
                    # on ne met pas à jour le bankroll du lobby : lors de
                    # l'entrée à une table le jeu peut prélever un
                    # "entry fee" qui ferait baisser temporairement la
                    # bankroll affichée. Le script doit ignorer ces
                    # variations pendant la fenêtre de confirmation.
                    if (
                        candidate_state == "TABLE"
                        and candidate_since is not None
                        and (time.time() - candidate_since) < CONFIRM_TIME
                    ):
                        # Ignorer la mise à jour pour éviter d'enregistrer
                        # un bankroll affecté par l'entry fee.
                        pass
                    else:
                        if bankroll != last_lobby_bankroll:

                            log(
                                f"BANKROLL = "
                                f"{bankroll:,}"
                            )

                            last_lobby_bankroll = bankroll


            time.sleep(INTERVAL)

        except KeyboardInterrupt:

            print()
            print("Tracker arrêté.")
            break

        except Exception as e:

            log(
                f"ERREUR : {e}"
            )

            time.sleep(1)