from .character_auto_generator import load_data

# słuy do kategori sklepu
CATEGORIES = {
    "Broń Biała": [
        "broń jednoręczna",
        "broń dwuręczna",
        "rapier",
        "szpada",
        "kij",
        "kopia",
        "lanca",
        "włócznia",
        "pałka",
        "młot",
        "topór",
        "miecz",
        "bicz",
        "kastet",
        "lewak",
        "nóż",
        "sztylet",
        "korbacz",
        "morgensztern",
        "halabarda",
    ],
    "Broń Dystansowa": [
        "łuk",
        "kusza",
        "proca",
        "pistolet",
        "garłacz",
        "rusznica",
        "muszkiet",
        "bolas",
        "gwiazdka",
        "oszczep",
        "sieć",
    ],
    "Amunicja": ["amunicja", "bełt", "kula", "proch", "strzała"],
    "Zbroje i Pancerze": [
        "zbroja",
        "pancerz",
        "hełm",
        "czepiec",
        "kaftan",
        "koszula kolcza",
        "kurta",
        "napierśnik",
        "naramienniki",
        "nogawice",
        "skórznia",
    ],
    "Tarcze": ["tarcza", "puklerz"],
    "Ubrania": [
        "ubranie",
        "odzienie",
        "strój",
        "szata",
        "liberia",
        "mundur",
        "uniform",
        "kapelusz",
        "kaptur",
        "płaszcz",
        "peleryna",
        "rękawica",
        "łachy",
    ],
    "Narzędzia i Ekwipunek": [
        "narzędzia",
        "wytrychy",
        "lina",
        "latarnia",
        "drąg",
        "plecak",
        "sakiewka",
        "mieszek",
        "worek",
        "namiot",
        "łopata",
        "kilof",
        "łom",
        "krzesiwo",
        "hubka",
        "kajdany",
        "kotwiczka",
    ],
    "Pojemniki i Naczynia": [
        "bukłak",
        "manierka",
        "butelka",
        "skrzynia",
        "tuba na mapy",
    ],
    "Przedmioty Różne": [
        "księga",
        "przybory do pisania",
        "talia kart",
        "kości do gry",
        "instrument",
        "symbol",
        "biżuteria",
        "liczydełko",
    ],
}

# Przetwarza listę wszystkich przedmiotów z bazy danych, kategoryzuje je na podstawie zdefiniowanych słów kluczowych
def get_categorized_items() -> dict:
    game_data = load_data()
    if not game_data or "items" not in game_data:
        return {}

    categorized_items = {name: [] for name in CATEGORIES.keys()}
    categorized_items["Inne"] = []

    for item in game_data["items"]:
        price = item.get("price")
        if price is None:
            continue

        item_name = item.get("name", "Bezimienny przedmiot")
        item_name_lower = item_name.lower()

        assigned = False
        for category, keywords in CATEGORIES.items():
            for keyword in keywords:
                if keyword in item_name_lower:
                    categorized_items[category].append(
                        {"name": item_name, "cost": price}
                    )
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            categorized_items["Inne"].append({"name": item_name, "cost": price})

    final_categories = {}
    for category, items in categorized_items.items():
        if items:
            final_categories[category] = sorted(items, key=lambda x: x["name"])

    return final_categories

# Funkcja realizująca zakup przedmiotu: sprawdza, czy postać ma wystarczająco złota, odejmuje koszt i dodaje przedmiot do ekwipunku postaci.
def buy_item(character: "Character", item_name: str, item_cost: int) -> bool:
    if not character or float(character.gold) < item_cost:
        return False

    character.gold -= item_cost
    character.ekwipunek.append({"name": item_name, "icon_path": ""})
    character.ekwipunek.sort(key=lambda x: x["name"])

    print(f"Postać {character.imie} kupiła '{item_name}' za {item_cost} ZK.")
    return True
