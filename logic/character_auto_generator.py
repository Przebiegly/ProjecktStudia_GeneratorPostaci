import json
import os
import random
import sys

#To jest potrzebne by odpowiedno zwracal sciezke jak generuje gotowy program z .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Wczytuje i zwraca dane z pliku JSON
def load_data(filename="database/database.json"):
    correct_path = resource_path(filename)
    try:
        with open(correct_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"BŁĄD: Plik '{correct_path}' nie został znaleziony.")
        return None
    except json.JSONDecodeError as e:
        print(f"BŁĄD: Plik '{correct_path}' zawiera błąd w formacie JSON: {e}")
        return None

#Symuluje rzut kosicią (zakres kosci od 1 do 10)
def roll_d10():
    return random.randint(1, 10)

#Symuluje rzut dwiema kosicmi i zwraca ich sume (zakres kosci od 1 do 10)
def roll_2d10():
    return random.randint(1, 10) + random.randint(1, 10)

#Symuluje rzut kosicią (zakres kosci od 1 do 100)
def roll_d100():
    return random.randint(1, 100)

# Słuzy by odnalesc odpowiedni elementy np jezeli roll bedzie przyjmowal 8 to bedzie szukac elementu dla range rownego 8
def find_in_range_table(table, roll):
    for entry in table:
        if entry["range"][0] <= roll <= entry["range"][1]:
            return entry
    return None

#Losowo wybiera jedną rasę z dostępnej puli
def choose_race(races_data):
    return random.choice(list(races_data.keys()))

# Generuje początkowe cechy główne postaci na podstawie wartości rasowych i sumy 2 rzutów koscia z zakresu od 1 do 10
def generate_primary_stats(race_data):
    base_stats = race_data["base_stats"]
    return {stat: base + roll_2d10() for stat, base in base_stats.items()}

# Oblicza cechy drugorzędne na podstawie cech głównych i danych zaspisanych w database
def generate_secondary_stats(race_data, primary_stats):
    secondary_stats = race_data["secondary_stats"].copy()
    secondary_stats["Żyw"] = find_in_range_table(race_data["vitality_table"], roll_d10())["value"]
    secondary_stats["PP"] = find_in_range_table(race_data["destination_points_table"], roll_d10())["value"]
    secondary_stats["S"] = primary_stats["K"] // 10
    secondary_stats["Wt"] = primary_stats["Odp"] // 10
    return secondary_stats

# Losuje szczegóły wyglądu postaci, takie jak wzrost, waga, kolor oczu i włosów
def generate_appearance(race_data, gender, general_tables):
    details = race_data["physical_details"]
    base_height = (details["height"]["male_base"] if gender == "Mężczyzna" else details["height"]["female_base"])
    hair_list = details.get("hair_colors", [{"roll": 1, "color": "Brak danych"}])
    eye_list = details.get("eye_colors", [{"roll": 1, "color": "Brak danych"}])
    return {
        "wzrost": base_height + roll_d10(),
        "waga": find_in_range_table(details["weight_table"], roll_d100())["value"],
        "kolor_wlosow": next((item["color"] for item in hair_list if item["roll"] == roll_d10()),hair_list[0]["color"],),
        "kolor_oczu": next((item["color"] for item in eye_list if item["roll"] == roll_d10()),eye_list[0]["color"],),
        "znak_szczegolny": find_in_range_table(general_tables["distinguishing_marks"], roll_d100())["mark"],
    }

# Losuje szczegóły  postaci, w tym imię, wiek i miejsce urodzenia
def generate_personal_details(race_data, gender, general_tables):
    gender_key = "male" if gender == "Mężczyzna" else "female"
    return {
        "imie": find_in_range_table(race_data["names"][gender_key], roll_d100())["name"],
        "miejsce_urodzenia": generate_birthplace(race_data, general_tables),
        "wiek": find_in_range_table(race_data["personal_details"]["age_table"], roll_d100())["value"],
        "liczba_rodzenstwa": find_in_range_table(race_data["personal_details"]["siblings_table"], roll_d10())["value"],
        "znak_gwiezdny": find_in_range_table(general_tables["star_signs"], roll_d100())["sign"],
    }

# Tworzy losowe miejsce urodzenia dla człowieka, łącząc typ osady z prowincją (funkcja pomocnicza)
def generate_human_birthplace(human_birthplaces_data):
    provinces = human_birthplaces_data.get("provinces", [{"roll": 0, "name": "Nieznana Prowincja"}])
    settlements = human_birthplaces_data.get("settlements", [{"roll": 0, "type": "Nieznana Osada"}])
    province = next((p["name"] for p in provinces if p["roll"] == roll_d10() % 10),provinces[0]["name"],)
    settlement = next((s["type"] for s in settlements if s["roll"] == roll_d10() % 10),settlements[0]["type"],)
    return f"{settlement} w prowincji {province}"

# Generuje miejsce urodzenia dla odpowiedniej klasy
def generate_birthplace(race_data, general_tables):
    if race_data.get("name") == "Człowiek":
        return generate_human_birthplace(general_tables["human_birthplaces"])
    birthplaces_table = race_data.get("personal_details", {}).get("birthplaces_table")
    if not birthplaces_table:
        return "Nieznane Krainy"
    place_entry = find_in_range_table(birthplaces_table, roll_d100())
    place = place_entry["place"]
    return (
        generate_human_birthplace(general_tables["human_birthplaces"])
        if "człowieka" in place
        else place)

# Sprawdza i zapisuje umiejętności i zdolności dla postaci (wynikajace z classy postaci)
def get_racial_abilities(race_data):
    abilities = race_data["skills_and_talents"]
    skill_ids = set(abilities.get("skills", []))
    talent_ids = set(abilities.get("talents", []))
    for choice in abilities.get("skill_choices", []):
        skill_ids.add(random.choice(choice))
    for choice in abilities.get("talent_choices", []):
        talent_ids.add(random.choice(choice))
    if abilities.get("random_talents", 0) > 0 and "random_talents_table" in race_data:
        for _ in range(abilities["random_talents"]):
            entry = find_in_range_table(race_data["random_talents_table"], roll_d100())
            if entry:
                talent_ids.add(entry["talent_id"])
    return {"skill_ids": skill_ids, "talent_ids": talent_ids}

# losuje profesje startowa ( przy okazji zapisuje tez umiejętności i zdolności oraz ekwipunek)
def assign_profession(race_name, game_data):
    prof_entry = None
    profession_table = game_data["race_profession_tables"][race_name]
    while not prof_entry:
        roll = roll_d100()
        prof_entry = find_in_range_table(profession_table, roll)
    prof_name = prof_entry["profession"]
    prof_details = game_data["base_class"][prof_name]
    skill_ids = set(prof_details.get("skills", []))
    talent_ids = set(prof_details.get("talents", []))
    equipment_ids = set(prof_details.get("equipment", []))
    for choice in prof_details.get("skill_choices", []):
        skill_ids.add(random.choice(choice))
    for choice in prof_details.get("talent_choices", []):
        talent_ids.add(random.choice(choice))
    for choice in prof_details.get("equipment_choices", []):
        equipment_ids.add(random.choice(choice))

    return {
        "nazwa": prof_name,
        "advances": prof_details.get("advances", {}),
        "skill_ids": skill_ids,
        "talent_ids": talent_ids,
        "equipment_ids": equipment_ids,
    }

# Główna funkcja, która wywołuje wszystkie powyższe by stworzyc kompletna postac
def create_character():
    game_data = load_data()
    if not game_data:
        return None

    character = {}
    character["rasa"] = choose_race(game_data["races"])
    character["plec"] = random.choice(["Mężczyzna", "Kobieta"])
    race_data = game_data["races"][character["rasa"]]

    cechy_glowne = generate_primary_stats(race_data)
    cechy_drugorzedne = generate_secondary_stats(race_data, cechy_glowne)

    profession_data = assign_profession(character["rasa"], game_data)
    character["profesja"] = profession_data["nazwa"]
    character["schemat_rozwoju"] = profession_data["advances"]

    character["cechy_glowne"] = cechy_glowne
    character["cechy_drugorzedne"] = cechy_drugorzedne
    character["wyglad"] = generate_appearance(race_data, character["plec"], game_data["general_tables"])
    character["szczegoly_osobiste"] = generate_personal_details(race_data, character["plec"], game_data["general_tables"])

    racial_abilities = get_racial_abilities(race_data)
    final_skill_ids = racial_abilities["skill_ids"].union(profession_data["skill_ids"])
    final_talent_ids = racial_abilities["talent_ids"].union(profession_data["talent_ids"])

    skill_map = {s["id"]: s["name"] for s in game_data["skills"]}
    talent_map = {t["id"]: t["name"] for t in game_data["talents"]}
    item_map = {i["id"]: i["name"] for i in game_data["items"]}

    character["umiejetnosci"] = sorted([skill_map.get(sid) for sid in final_skill_ids if sid in skill_map])
    character["zdolnosci"] = sorted([talent_map.get(tid) for tid in final_talent_ids if tid in talent_map])

    equipment_names = sorted([item_map.get(iid) for iid in profession_data["equipment_ids"] if iid in item_map])

    character["ekwipunek"] = [
        {"name": name, "icon_path": ""} for name in equipment_names
    ]

    character["xp"] = 0
    character["gold"] = 0
    character["purchased_advances"] = {}

    return character
