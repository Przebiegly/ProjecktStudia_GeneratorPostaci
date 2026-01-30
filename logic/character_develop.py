

def get_profession_details(profession_name: str, game_data: dict):
    if profession_name in game_data.get("base_class", {}):
        return game_data["base_class"][profession_name]
    if profession_name in game_data.get("advanced_class", {}):
        return game_data["advanced_class"][profession_name]
    return {}

# Tłumaczy identyfikatory (ID) z danych profesji na pełne, czytelne nazwy umiejętności, zdolności i ekwipunku ( sa one tez w .json tylko w osobnym miejscu).
def get_full_profession_data(profession_name: str, game_data: dict):

    skill_map = {s["id"]: s["name"] for s in game_data["skills"]}
    talent_map = {t["id"]: t["name"] for t in game_data["talents"]}
    item_map = {i["id"]: i["name"] for i in game_data["items"]}

    prof_details = get_profession_details(profession_name, game_data)

    skills = {
        skill_map.get(sid) for sid in prof_details.get("skills", []) if sid in skill_map
    }
    talents = {
        talent_map.get(tid)
        for tid in prof_details.get("talents", [])
        if tid in talent_map
    }
    equipment = {
        item_map.get(iid)
        for iid in prof_details.get("equipment", [])
        if iid in item_map
    }

    skill_choices = [
        [skill_map.get(sid) for sid in group if sid in skill_map]
        for group in prof_details.get("skill_choices", [])
    ]
    talent_choices = [
        [talent_map.get(tid) for tid in group if tid in talent_map]
        for group in prof_details.get("talent_choices", [])
    ]
    equipment_choices = [
        [item_map.get(iid) for iid in group if iid in item_map]
        for group in prof_details.get("equipment_choices", [])
    ]

    return {
        "skills": skills,
        "talents": talents,
        "equipment": equipment,
        "skill_choices": skill_choices,
        "talent_choices": talent_choices,
        "equipment_choices": equipment_choices,
    }

# Porównuje posiadane przez postać atrybuty z nową profesją, aby wyliczyć tylko te, które postać zyska.
def get_profession_preview_data(
    character: "Character", new_profession_name: str, game_data: dict):

    if not character or not new_profession_name:
        return {}

    new_prof_details = get_profession_details(new_profession_name, game_data)
    advances = new_prof_details.get("advances", {})
    total_advances = {stat: sum(values) for stat, values in advances.items()}

    new_prof_data = get_full_profession_data(new_profession_name, game_data)

    char_skills = set(character.umiejetnosci)
    char_talents = set(character.zdolnosci)
    char_equipment = {item["name"] for item in character.ekwipunek}

    new_base_skills = sorted(list(new_prof_data["skills"] - char_skills))
    new_base_talents = sorted(list(new_prof_data["talents"] - char_talents))
    new_base_equipment = sorted(list(new_prof_data["equipment"] - char_equipment))

    return {
        "total_advances": total_advances,
        "new_base_skills": new_base_skills,
        "new_skill_choices": new_prof_data["skill_choices"],
        "new_base_talents": new_base_talents,
        "new_talent_choices": new_prof_data["talent_choices"],
        "new_base_equipment": new_base_equipment,
        "new_equipment_choices": new_prof_data["equipment_choices"],
    }

# Obsługuje logikę wydawania 100 PD na wykupienie jednego rozwinięcia cechy ze schematu profesji.
def purchase_advance(character: "Character", stat_key: str):
    if not character or character.xp < 100:
        return False

    schema = character.schemat_rozwoju.get(stat_key, [])
    purchased_count = character.purchased_advances.get(stat_key, 0)

    if purchased_count >= len(schema):
        return False

    advance_value = schema[purchased_count]
    character.xp -= 100
    character.purchased_advances[stat_key] = purchased_count + 1

    if stat_key in character.cechy_glowne:
        character.cechy_glowne[stat_key] += advance_value
    elif stat_key in character.cechy_drugorzedne:
        character.cechy_drugorzedne[stat_key] += advance_value
    elif stat_key.lower() == "po":
        if "Po" in character.cechy_drugorzedne:
            character.cechy_drugorzedne["Po"] += advance_value
        if "PO" in character.cechy_drugorzedne:
            character.cechy_drugorzedne["PO"] += advance_value

    return True

# Sprawdza, czy postać wykupiła wszystkie dostępne rozwinięcia (jest to warunkiem zmiany profesji.)
def are_all_advances_purchased(character: "Character"):
    if not character:
        return False
    for stat, values in character.schemat_rozwoju.items():
        if character.purchased_advances.get(stat, 0) < len(values):
            return False
    return True

# Finalizuje proces zmiany profesji postaci, aktualizując jej atrybuty, odejmując PD i resetując schemat rozwoju.
def change_character_profession(
    character: "Character", new_profession: str, game_data: dict, choices: dict):

    if not character or not are_all_advances_purchased(character) or character.xp < 500:
        return False

    current_prof_data = get_profession_details(character.profesja, game_data)
    exit_professions = current_prof_data.get("profesja_wyjsciowa", [])

    if new_profession not in exit_professions:
        return False

    preview_data = get_profession_preview_data(character, new_profession, game_data)

    gained_skills = set(preview_data["new_base_skills"])
    gained_skills.update(choices.get("skills", []))
    gained_talents = set(preview_data["new_base_talents"])
    gained_talents.update(choices.get("talents", []))
    gained_equipment = set(preview_data["new_base_equipment"])
    gained_equipment.update(choices.get("equipment", []))

    character.umiejetnosci.extend(list(gained_skills))
    character.zdolnosci.extend(list(gained_talents))
    new_equipment_items = [{"name": name, "icon_path": ""} for name in gained_equipment]
    character.ekwipunek.extend(new_equipment_items)

    character.umiejetnosci.sort()
    character.zdolnosci.sort()
    character.ekwipunek.sort(key=lambda x: x["name"])

    character.xp -= 500
    character.profesja = new_profession

    new_prof_details = get_profession_details(new_profession, game_data)
    character.schemat_rozwoju = new_prof_details.get("advances", {})
    character.purchased_advances = {}

    return True
