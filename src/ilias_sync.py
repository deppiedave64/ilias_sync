#!/usr/bin/env python3

import argparse
from pathlib import Path, PurePath

from PFERD import Pferd
from PFERD.ilias import IliasElementType
from PFERD.transform import (
    attempt,
    do,
    glob,
    keep,
    move,
    move_dir,
    optionally,
    rename,
    re_move,
    re_rename,
)

OUTPUT_PATH = "/home/david/Studium/"

tf_ws_2020_la1 = attempt(
    do(
        move_dir("Tutoriumsblätter/", "Tutorium/"),
        optionally(re_rename(r"Tutorium_([0-9]{2})\.pdf", "LA1_Tut {1}.pdf")),
    ),
    do(
        move_dir("Vorlesungsmaterial/", "Vorlesung/"),
        optionally(re_rename(r"LA1_([0-9]{2})\.pdf", "Skript v{1}.pdf")),
        re_rename(r"(.*)", "LA1_{1}"),
    ),
    do(
        move_dir("Übungen/", "Blätter/"),
        optionally(re_rename(r"Übungsblatt ([0-9]+).*\.pdf", "ÜB {1}.pdf")),
        optionally(re_rename(r"Lösung zu Blatt ([0-9]+)\.pdf", "ÜB {1} Lösung.pdf")),
        re_rename(r"(.*)", "LA1_{1}"),
    ),
    re_move(r"Tutorien/Tutorium 21: Muhammed Öz/Übungen/\D*(\d+)\D*/.*\.pdf", "Blätter/LA1_ÜB {1} Abgabe korrigiert.pdf"),
    keep,
)

tf_ws_2020_hm1 = attempt(
    re_move(r"Tutorien/Tutorium_03/Übungsblattabgabe/Übungsblatt_([0-9]+)/.*\.pdf", "Blätter/HM1_ÜB {1} Abgabe korrigiert.pdf"),
    move("Vorlesungsmaterial/Skript Höhere Mathematik 1.pdf", "HM1_Skript.pdf"),
    do(
        move_dir("Übungen/", "Übung/"),
        optionally(re_rename(r"Übung_([0-9]{2})\.pdf", "HM1_Übung {1}.pdf")),
    ),
    do(
        optionally(move("Übungsblätter/Lösungsvorschläge/Lösungsvorschlag_Tutoriumsblatt.pdf",
                        "Blätter/HM1_Tutoriumsblatt Lösung.pdf")),
        optionally(re_move(r"Übungsblätter/Lösungsvorschläge/Lösungsvorschlag_ÜB_([0-9]{2})\.pdf",
                           "Blätter/HM1_ÜB {1} Lösung.pdf")),
        optionally(move("Übungsblätter/Tutoriumsblatt.pdf", "Blätter/HM1_Tutoriumsblatt.pdf")),
        optionally(re_move(r"Übungsblätter/Übungsblatt_([0-9]{2})\.pdf", "Blätter/HM1_ÜB {1}.pdf")),
    ),
    keep,
)

tf_ws_2020_proggen = attempt(
    keep,
)

tf_ws_2020_gbi = attempt(
    do(
        move_dir("Vorlesung: Skript/", "Skript/"),
        optionally(re_rename(r"([0-9]+)\. (.*)\.pdf", "GBI_Skript {1} - {2}.pdf")),
    ),
    re_move(r"Vorlesung: Folien/([0-9]+)\. (.*)\.pdf", "Vorlesung/GBI_Vorlesung {1} - {2}.pdf"),
    do(
        move_dir("Große Übung: Folien/", "Übung/"),
        optionally(re_rename(r"([0-9]+)\-uebung\.pdf", "GBI_Übung {1}.pdf")),
    ),
    attempt(
        re_move(r"Aufgabenblätter/Aufgabenblatt ([0-9]+)/.*aufgaben.pdf", "Blätter/GBI_ÜB {1}.pdf"),
        re_move(r"Aufgabenblätter/Aufgabenblatt ([0-9]+)/loesungen.pdf", "Blätter/GBI_ÜB {1} Lösung.pdf"),
        re_move(r"Aufgabenblätter/Aufgabenblatt ([0-9]+)/.*\.pdf", "Blätter/GBI_ÜB {1} Abgabe korrigiert.pdf"),
    ),
    keep,
)

tf_ss_2021_hm2 = attempt(
    glob("*.pdf"),
)

tf_ss_2021_la2 = attempt(
    glob("*.pdf"),
)

tf_ss_2021_swt1 = attempt(
    glob("*.pdf"),
    glob("*.zip"),
    glob("*.jpg"),
    glob("*.png"),
    glob("*.java"),
)

tf_ss_2021_algo1 = attempt(
    keep,
)

tf_ss_2021_dt = attempt(
    glob("*.pdf"),
)

tf_ss_2021_jap2 = attempt(
    keep,
)

tf_ss_2021_icpc = attempt(
    keep,
)


def filter_ws_2020_la1(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Tutorien")(path):
        return True
    if glob("Tutorien/Tutorium 21: Muhammed Öz/")(path):
        return True
    if glob("Tutorien/Tutorium 21: Muhammed Öz/Übungen")(path):
        return True
    if glob("Tutorien/Tutorium 21: Muhammed Öz/*")(path):
        return False
    if glob("Tutorien/*")(path):
        return False
    if glob("Vorlesungsmaterial/Videos")(path):
        return False
    if glob("Übungen/Übungsblatt *")(path):
        return True
    if glob("Übungen/Lösung *")(path):
        return True
    if glob("Übungen/*")(path):
        return False
    return True


def filter_ws_2020_hm1(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Informationen")(path):
        return False
    if glob("Tutorien")(path):
        return True
    if glob("Tutorien/Tutorium_03")(path):
        return True
    if glob("Tutorien/Tutorium_03/Übungsblattabgabe")(path):
        return True
    if glob("Tutorien/Tutorium_03/*")(path):
        return False
    if glob("Tutorien/*")(path):
        return False
    if glob("Vorlesung")(path):
        return False
    if glob("Übung")(path):
        return False
    return True


def filter_ws_2020_proggen(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Tutorien")(path):
        return False
    return True


def filter_ws_2020_gbi(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Informationen von Hochschulgruppen")(path):
        return False
    if glob("Tutorien")(path):
        return False
    return True


def filter_ss_2021_hm2(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Tutorien")(path):
        return False
    if glob("Vorlesung")(path):
        return False
    return True


def filter_ss_2021_la2(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Vorlesungsmaterial/Videos")(path):
        return False
    return True


def filter_ss_2021_swt1(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Tutorien")(path):
        return False
    if glob("HaDiKo")(path):
        return False
    if glob("linkit")(path):
        return False
    return True


def filter_ss_2021_algo1(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Tutorien")(path):
        return False
    if glob("Vorlesungsmaterial")(path):
        return True
    if glob("Vorlesungsmaterial/Videos - Initiativen")(path):
        return False
    if glob("Vorlesungsmaterial/Aufzeichnungen der Vorlesung")(path):
        return False
    return True

def filter_ss_2021_dt(path: PurePath, _type: IliasElementType) -> bool:
    if glob("Werbung für Hochschulgruppen")(path):
        return False
    if glob("Vorlesungsmaterial/Vorlesungsaufzeichnungen")(path):
        return False
    return True

def filter_ss_2021_jap2(path: PurePath, _type: IliasElementType) -> bool:
    return True

def filter_ss_2021_icpc(path: PurePath, _type: IliasElementType) -> bool:
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-run", action="store_true")
    parser.add_argument("synchronizers", nargs="*")
    args = parser.parse_args()

    pferd = Pferd(Path(OUTPUT_PATH), test_run=args.test_run)
    pferd.enable_logging()

    if "la1" in args.synchronizers:
        pferd.ilias_kit(
            target="LA1",
            course_id="1258056",
            dir_filter=filter_ws_2020_la1,
            transform=tf_ws_2020_la1,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    if "hm1" in args.synchronizers:
        pferd.ilias_kit(
            target="HM1",
            course_id="1253943",
            dir_filter=filter_ws_2020_hm1,
            transform=tf_ws_2020_hm1,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    if "proggen" in args.synchronizers:
        pferd.ilias_kit(
            target="Proggen",
            course_id="1255116",
            dir_filter=filter_ws_2020_proggen,
            transform=tf_ws_2020_proggen,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    if "gbi" in args.synchronizers:
        pferd.ilias_kit(
            target="GBI",
            course_id="1281984",
            dir_filter=filter_ws_2020_gbi,
            transform=tf_ws_2020_gbi,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    if not args.synchronizers or "hm2" in args.synchronizers:
        pferd.ilias_kit(
            target="HM2",
            course_id="1460343",
            dir_filter=filter_ss_2021_hm2,
            transform=tf_ss_2021_hm2,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )
    
    if not args.synchronizers or "la2" in args.synchronizers:
        pferd.ilias_kit(
            target="LA2",
            course_id="1471707",
            dir_filter=filter_ss_2021_la2,
            transform=tf_ss_2021_la2,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    if not args.synchronizers or "swt1" in args.synchronizers:
        pferd.ilias_kit(
            target="SWT1",
            course_id="1468007",
            dir_filter=filter_ss_2021_swt1,
            transform=tf_ss_2021_swt1,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )
    
    if not args.synchronizers or "algo1" in args.synchronizers:
        pferd.ilias_kit(
            target="Algo1",
            course_id="1470307",
            dir_filter=filter_ss_2021_algo1,
            transform=tf_ss_2021_algo1,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt"
        )

    if not args.synchronizers or "dt" in args.synchronizers:
        pferd.ilias_kit(
            target="DT",
            course_id="1479423",
            dir_filter=filter_ss_2021_dt,
            transform=tf_ss_2021_dt,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt"
        )

    if not args.synchronizers or "jap2" in args.synchronizers:
        pferd.ilias_kit(
            target="Japanisch",
            course_id="1447952",
            dir_filter=filter_ss_2021_jap2,
            transform=tf_ss_2021_jap2,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt"
        )
    
    if not args.synchronizers or "icpc" in args.synchronizers:
        pferd.ilias_kit(
            target="ICPC",
            course_id="1430957",
            dir_filter=filter_ss_2021_icpc,
            transform=tf_ss_2021_icpc,
            cookies=f"{OUTPUT_PATH}.ilias_cookies.txt",
        )

    pferd.print_summary()


if __name__ == "__main__":
    main()
