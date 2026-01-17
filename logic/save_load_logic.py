# Plik: logic/save_load_logic.py

import json
import os
from datetime import datetime
import shutil
import glob
import uuid

SAVE_DIR = "saves"

#Upewnia się, że folder na zapisy istnieje. Jeśli nie, tworzy go.
def ensure_save_directory():
    os.makedirs(SAVE_DIR, exist_ok=True)

# Zapisuje dane postaci do pliku JSON. Dba również o skopiowanie portretu  oraz ikon przedmiotów do folderu z zapisami, nadając im unikalne nazwy.
def save_character(character_data: dict, filename: str) -> bool:
    ensure_save_directory()
    safe_filename = "".join(
        c for c in filename if c.isalnum() or c in (" ", "_", "-")
    ).rstrip()
    if not safe_filename:
        print("Błąd: Nazwa zapisu jest nieprawidłowa.")
        return False

    portrait_source_path = character_data.get("portrait_path")
    if portrait_source_path and os.path.exists(portrait_source_path):
        try:
            _, ext = os.path.splitext(portrait_source_path)
            portrait_dest_path = os.path.join(SAVE_DIR, f"{safe_filename}{ext}")
            shutil.copy2(portrait_source_path, portrait_dest_path)
            character_data["portrait_ext"] = ext
            print(f"Zapisano portret w: {portrait_dest_path}")
        except Exception as e:
            print(f"Błąd podczas kopiowania portretu: {e}")
    if "portrait_path" in character_data:
        del character_data["portrait_path"]

    if "ekwipunek" in character_data:
        for item in character_data["ekwipunek"]:
            icon_source_path = item.get("icon_path")
            if (
                icon_source_path
                and os.path.exists(icon_source_path)
                and not icon_source_path.startswith(safe_filename)
            ):
                try:
                    _, ext = os.path.splitext(icon_source_path)
                    unique_id = uuid.uuid4().hex[:8]
                    icon_dest_filename = f"{safe_filename}_item_{unique_id}{ext}"
                    icon_dest_path = os.path.join(SAVE_DIR, icon_dest_filename)
                    shutil.copy2(icon_source_path, icon_dest_path)
                    item["icon_path"] = icon_dest_filename
                    print(f"Zapisano ikonę przedmiotu w: {icon_dest_path}")
                except Exception as e:
                    print(f"Błąd podczas kopiowania ikony przedmiotu: {e}")

    filepath = os.path.join(SAVE_DIR, f"{safe_filename}.json")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(character_data, f, indent=4, ensure_ascii=False)
        print(f"Zapisano postać w pliku: {filepath}")
        return True
    except IOError as e:
        print(f"Błąd zapisu do pliku: {e}")
        return False

# Przeszukuje folder z zapisami, sortuje pliki JSON od najnowszego  i zwraca listę z nazwami zapisów oraz ich datami modyfikacji.
def list_saves() -> list[dict]:
    ensure_save_directory()
    saves_with_dates = []
    try:
        files = os.listdir(SAVE_DIR)
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(SAVE_DIR, filename)
                mod_time = os.path.getmtime(filepath)
                saves_with_dates.append((mod_time, os.path.splitext(filename)[0]))

        saves_with_dates.sort(key=lambda x: x[0], reverse=True)

        formatted_saves = []
        for mod_time, name in saves_with_dates:
            date_str = datetime.fromtimestamp(mod_time).strftime("%d.%m.%Y %H:%M")
            formatted_saves.append({"name": name, "date": date_str})

        return formatted_saves
    except IOError as e:
        print(f"Błąd odczytu folderu z zapisami: {e}")
        return []

#słuzy do załadowania sava
def load_character_data(filename: str) -> dict | None:
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "portrait_ext" in data and data["portrait_ext"]:
            img_path = os.path.join(SAVE_DIR, f"{filename}{data['portrait_ext']}")
            if os.path.exists(img_path):
                data["portrait_path"] = img_path

        if "ekwipunek" in data:
            for item in data["ekwipunek"]:
                icon_filename = item.get("icon_path")
                if icon_filename:
                    full_path = os.path.join(SAVE_DIR, icon_filename)
                    item["icon_path"] = full_path if os.path.exists(full_path) else ""

        print(f"Wczytano postać z pliku: {filepath}")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd wczytywania pliku {filepath}: {e}")
        return None

#usuwanie savów
def delete_save(filename: str) -> bool:
    try:
        pattern = os.path.join(SAVE_DIR, f"{filename}*")
        files_to_delete = glob.glob(pattern)

        if not files_to_delete:
            return False

        for filepath in files_to_delete:
            os.remove(filepath)
            print(f"Usunięto plik: {filepath}")
        return True
    except IOError as e:
        print(f"Błąd podczas usuwania plików dla zapisu '{filename}': {e}")
        return False
