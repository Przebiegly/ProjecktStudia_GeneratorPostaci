from .character_auto_generator import load_data, generate_human_birthplace

# Zwraca listę wszystkich dostępnych ras postaci z bazy danych i zwraca je w liscie
def get_race_options():
    game_data = load_data()
    return list(game_data["races"].keys()) if game_data else []

# Zwraca  listę profesji dostępnych dla wybranej rasy
def get_professions_for_race(race_name: str):
    game_data = load_data()
    if not game_data or race_name not in game_data.get("race_profession_tables", {}):
        return []
    professions = {
        entry["profession"] for entry in game_data["race_profession_tables"][race_name]
    }
    return sorted(list(professions))

# Zwraca listę imion odpowiednich dla wybranej rasy i płci.
def get_names_for_race_and_gender(race_name: str, gender: str):
    game_data = load_data()
    race_data = game_data["races"].get(race_name)
    if not race_data:
        return []
    gender_key = "male" if gender == "Mężczyzna" else "female"
    return sorted(
        list({entry["name"] for entry in race_data["names"].get(gender_key, [])})
    )

# Zwraca dostępne kolory włosów i oczu dla wybranej rasy.
def get_appearance_options_for_race(race_name: str):
    game_data = load_data()
    if not game_data or race_name not in game_data["races"]:
        return {}
    race_details = game_data["races"][race_name]["physical_details"]
    return {
        "hair_colors": [item["color"] for item in race_details.get("hair_colors", [])],
        "eye_colors": [item["color"] for item in race_details.get("eye_colors", [])],
    }

# Zwraca listę możliwych miejsc urodzenia dla wybranej rasy.
def get_birthplaces_for_race(race_name: str):
    game_data = load_data()
    race_data = game_data["races"].get(race_name)
    if (
        not race_data
        or "personal_details" not in race_data
        or "birthplaces_table" not in race_data["personal_details"]
    ):
        return ["Losowe miejsce w Imperium"] if race_name == "Człowiek" else []
    places = {
        entry["place"] for entry in race_data["personal_details"]["birthplaces_table"]
    }
    return sorted(list(places))


def get_list_options_for_race(race_name: str, gender: str):
    game_data = load_data()
    if not game_data or race_name not in game_data["races"]:
        return {}
    race_data = game_data["races"][race_name]
    age_values = sorted(
        list(
            {str(item["value"]) for item in race_data["personal_details"]["age_table"]}
        )
    )
    height_base = race_data["physical_details"]["height"].get(
        "male_base" if gender == "Mężczyzna" else "female_base", 150
    )
    height_values = [str(height_base + i) for i in range(1, 21)]
    weight_values = sorted(
        list(
            {
                str(item["value"])
                for item in race_data["physical_details"]["weight_table"]
            }
        )
    )
    sibling_values = sorted(
        list(
            {
                str(item["value"])
                for item in race_data["personal_details"]["siblings_table"]
            }
        )
    )
    appearance_options = get_appearance_options_for_race(race_name)
    birthplace_options = get_birthplaces_for_race(race_name)
    return {
        "age": age_values,
        "height": height_values,
        "weight": weight_values,
        "siblings": sibling_values,
        "hair_color": appearance_options.get("hair_colors", []),
        "eye_color": appearance_options.get("eye_colors", []),
        "birthplace": birthplace_options,
    }

# daj nam znaki gwiezdne i cechy szczegolne
def get_general_options():
    game_data = load_data()
    if not game_data:
        return {}
    return {
        "star_signs": [
            item["sign"] for item in game_data["general_tables"].get("star_signs", [])
        ],
        "distinguishing_marks": [
            item["mark"]
            for item in game_data["general_tables"].get("distinguishing_marks", [])
        ],
    }

# Odpowiada by byl podglad w UI ( odpowiada miedzy innymi za to ze laczy zdolosci clasowe jak i te z profesji)
def get_combined_data_for_ui(race_name: str, profession_name: str):
    game_data = load_data()
    if not game_data or race_name not in game_data["races"]:
        return {}
    skill_map = {s["id"]: s["name"] for s in game_data["skills"]}
    talent_map = {t["id"]: t["name"] for t in game_data["talents"]}
    item_map = {i["id"]: i["name"] for i in game_data["items"]}
    race_data = game_data["races"][race_name]
    race_abilities = race_data["skills_and_talents"]
    main_stats = race_data["base_stats"].copy()
    sec_stats = race_data["secondary_stats"].copy()
    base_skills = {
        skill_map.get(sid)
        for sid in race_abilities.get("skills", [])
        if sid in skill_map
    }
    base_talents = {
        talent_map.get(tid)
        for tid in race_abilities.get("talents", [])
        if tid in talent_map
    }
    skill_choices = [
        [skill_map.get(sid) for sid in group if sid in skill_map]
        for group in race_abilities.get("skill_choices", [])
    ]
    talent_choices = [
        [talent_map.get(tid) for tid in group if tid in talent_map]
        for group in race_abilities.get("talent_choices", [])
    ]
    base_equipment = set()
    equipment_choices = []
    if profession_name and profession_name in game_data["base_class"]:
        prof_details = game_data["base_class"][profession_name]
        for stat, value_list in prof_details.get("advances", {}).items():
            value = sum(value_list)
            if stat in main_stats:
                main_stats[stat] += value
            elif stat in sec_stats:
                sec_stats[stat] += value
        base_skills.update(
            {
                skill_map.get(sid)
                for sid in prof_details.get("skills", [])
                if sid in skill_map
            }
        )
        base_talents.update(
            {
                talent_map.get(tid)
                for tid in prof_details.get("talents", [])
                if tid in talent_map
            }
        )
        skill_choices.extend(
            [
                [skill_map.get(sid) for sid in group if sid in skill_map]
                for group in prof_details.get("skill_choices", [])
            ]
        )
        talent_choices.extend(
            [
                [talent_map.get(tid) for tid in group if tid in talent_map]
                for group in prof_details.get("talent_choices", [])
            ]
        )
        base_equipment.update(
            {
                item_map.get(iid)
                for iid in prof_details.get("equipment", [])
                if iid in item_map
            }
        )
        equipment_choices.extend(
            [
                [item_map.get(iid) for iid in group if iid in item_map]
                for group in prof_details.get("equipment_choices", [])
            ]
        )
    return {
        "main_stats": main_stats,
        "sec_stats": sec_stats,
        "base_skills": sorted(list(base_skills)),
        "skill_choices": skill_choices,
        "base_talents": sorted(list(base_talents)),
        "talent_choices": talent_choices,
        "base_equipment": sorted(list(base_equipment)),
        "equipment_choices": equipment_choices,
    }

# Zbiera wszystkie wybory użytkownika z interfejsu i tworzy finalny słownik danych postaci.
def finalize_character(user_selections: dict):
    game_data = load_data()
    if not game_data:
        return None

    race_name = user_selections.get("rasa")
    profession_name = user_selections.get("profesja")

    preview_data = get_combined_data_for_ui(race_name, profession_name)
    final_skills = set(preview_data.get("base_skills", []))
    final_skills.update(user_selections.get("chosen_skills", []))
    final_talents = set(preview_data.get("base_talents", []))
    final_talents.update(user_selections.get("chosen_talents", []))
    final_equipment_names = set(preview_data.get("base_equipment", []))
    final_equipment_names.update(user_selections.get("chosen_equipment", []))

    birthplace = user_selections.get("miejsce_urodzenia")
    if birthplace == "Losowe miejsce w Imperium":
        birthplace = generate_human_birthplace(
            game_data["general_tables"]["human_birthplaces"]
        )

    profession_details = game_data["base_class"].get(profession_name, {})
    advances_schema = profession_details.get("advances", {})

    final_equipment = sorted(
        [{"name": name, "icon_path": ""} for name in final_equipment_names],
        key=lambda x: x["name"],
    )

    character_data = {
        "rasa": race_name,
        "plec": user_selections.get("plec"),
        "profesja": profession_name,
        "cechy_glowne": user_selections.get("cechy_glowne", {}),
        "cechy_drugorzedne": user_selections.get("cechy_drugorzedne", {}),
        "wyglad": {
            k: v
            for k, v in user_selections.items()
            if k in ["wzrost", "waga", "kolor_wlosow", "kolor_oczu", "znak_szczegolny"]
        },
        "szczegoly_osobiste": {
            "imie": user_selections.get("imie"),
            "miejsce_urodzenia": birthplace,
            "wiek": user_selections.get("wiek"),
            "rodzenstwo": user_selections.get("rodzenstwo"),
            "znak_gwiezdny": user_selections.get("znak_gwiezdny"),
        },
        "schemat_rozwoju": advances_schema,
        "umiejetnosci": sorted(list(final_skills)),
        "zdolnosci": sorted(list(final_talents)),
        "ekwipunek": final_equipment,
        "xp": 0,
        "gold": 0,
        "purchased_advances": {},
    }
    return character_data
