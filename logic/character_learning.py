from .character_auto_generator import load_data

# Pobiera z bazy danych pełną, posortowaną listę wszystkich dostępnych w grze umiejętności i zdolności.
def get_all_learnable_abilities(game_data: dict) -> dict:
    if not game_data:
        return {"skills": [], "talents": []}

    # Tworzy 2 listy zawierającą tylko nazwy wszystkich umiejętności i zdolonsci z bazy danych.
    all_skills = [skill["name"] for skill in game_data.get("skills", [])]
    all_talents = [talent["name"] for talent in game_data.get("talents", [])]

    return {"skills": sorted(all_skills), "talents": sorted(all_talents)}

# Obsługuje proces nauki nowej umiejętności lub zdolności przez postać
# Sprawdza czy ma wystarczajaco pd oraz sprawdza czy postac nie psiada juz umiejetnosci
def learn_ability(character: "Character", ability_name: str, ability_type: str) -> bool:
    COST = 100
    if not character or character.xp < COST:
        return False

    if ability_type == "skill":
        if ability_name in character.umiejetnosci:
            return False
        character.umiejetnosci.append(ability_name)
        character.umiejetnosci.sort()
    elif ability_type == "talent":
        if ability_name in character.zdolnosci:
            return False
        character.zdolnosci.append(ability_name)
        character.zdolnosci.sort()
    else:
        return False

    character.xp -= COST
    print(f"Postać {character.imie} nauczyła się '{ability_name}' za {COST} PD.")

    return True
