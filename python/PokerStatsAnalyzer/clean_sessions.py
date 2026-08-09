import argparse
import csv
import datetime
import os
from pathlib import Path

FIELDNAMES = [
    "session",
    "start",
    "end",
    "duration_seconds",
    "bankroll_start",
    "bankroll_end",
    "profit",
]

DEFAULT_MIN_DURATION = 30


def parse_int(value):
    if value is None:
        return None

    value = str(value).strip().replace(" ", "").replace(",", "")

    if value == "":
        return None

    try:
        return int(value)
    except ValueError:
        return None


def parse_timestamp(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return datetime.datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None


def load_sessions(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def make_backup(path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(path).with_name(
        f"{Path(path).stem}.backup_{timestamp}{Path(path).suffix}"
    )
    Path(path).rename(backup_path)
    return backup_path


def validate_and_fix_row(row, min_duration, remove_zero_profit):
    start = parse_timestamp(row.get("start"))
    end = parse_timestamp(row.get("end"))
    duration = parse_int(row.get("duration_seconds"))
    bankroll_start = parse_int(row.get("bankroll_start"))
    bankroll_end = parse_int(row.get("bankroll_end"))
    profit = parse_int(row.get("profit"))

    if start is None or end is None:
        return False, None, "timestamp invalide"

    actual_duration = int((end - start).total_seconds())

    if actual_duration <= 0:
        return False, None, "durée invalide"

    if bankroll_start is None or bankroll_end is None:
        return False, None, "bankroll manquante ou invalide"

    fixed_duration = duration if duration == actual_duration else actual_duration
    fixed_profit = profit if profit is not None else bankroll_end - bankroll_start

    if fixed_duration < min_duration:
        return False, None, f"trop courte ({fixed_duration}s)"

    if remove_zero_profit and fixed_profit == 0:
        return False, None, "profit nul"

    cleaned_row = {
        "session": row.get("session", ""),
        "start": row.get("start", ""),
        "end": row.get("end", ""),
        "duration_seconds": str(fixed_duration),
        "bankroll_start": str(bankroll_start),
        "bankroll_end": str(bankroll_end),
        "profit": str(fixed_profit),
    }

    reason = []

    if duration != fixed_duration:
        reason.append(f"durée réparée ({duration} -> {fixed_duration})")

    if profit is None:
        reason.append("profit recompté")

    return True, cleaned_row, "; ".join(reason) if reason else "OK"


def clean_sessions(rows, min_duration, remove_zero_profit):
    kept = []
    removed = []
    repaired = []

    for row in rows:
        valid, cleaned_row, reason = validate_and_fix_row(
            row,
            min_duration,
            remove_zero_profit,
        )

        if valid:
            kept.append(cleaned_row)
            if reason != "OK":
                repaired.append((row, reason))
        else:
            removed.append((row, reason))

    return kept, removed, repaired


def write_sessions(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(total, kept, removed, repaired, output_path, backup_path=None):
    print("Nettoyage terminé")
    print("==================")
    print(f"Total de sessions lues : {total}")
    print(f"Sessions conservées : {len(kept)}")
    print(f"Sessions supprimées : {len(removed)}")
    print(f"Sessions réparées : {len(repaired)}")
    print(f"Fichier publié : {output_path}")

    if backup_path is not None:
        print(f"Sauvegarde originale : {backup_path}")

    if removed:
        print("\nSessions supprimées :")
        for row, reason in removed:
            info = f"session={row.get('session', '')}, start={row.get('start', '')}, end={row.get('end', '')}"
            print(f" - {info} -> {reason}")

    if repaired:
        print("\nSessions réparées :")
        for row, reason in repaired:
            info = f"session={row.get('session', '')}, start={row.get('start', '')}, end={row.get('end', '')}"
            print(f" - {info} -> {reason}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Nettoie les anomalies dans sessions.csv et génère un fichier nettoyé."
    )

    parser.add_argument(
        "--input",
        default="sessions.csv",
        help="Chemin du fichier sessions.csv à analyser.",
    )
    parser.add_argument(
        "--output",
        default="sessions.cleaned.csv",
        help="Chemin du fichier de sortie nettoyé.",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Écrase le fichier source après avoir créé une sauvegarde.",
    )
    parser.add_argument(
        "--min-duration",
        type=int,
        default=DEFAULT_MIN_DURATION,
        help="Durée minimale en secondes pour conserver une session (par défaut 30).",
    )
    parser.add_argument(
        "--remove-zero-profit",
        action="store_true",
        help="Supprime aussi les sessions dont le profit est exactement zéro.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    rows = load_sessions(args.input)

    kept, removed, repaired = clean_sessions(
        rows,
        min_duration=args.min_duration,
        remove_zero_profit=args.remove_zero_profit,
    )

    output_path = args.output
    backup_path = None

    if args.inplace:
        backup_path = make_backup(args.input)
        output_path = args.input

    write_sessions(output_path, kept)
    print_summary(len(rows), kept, removed, repaired, output_path, backup_path)


if __name__ == "__main__":
    main()
