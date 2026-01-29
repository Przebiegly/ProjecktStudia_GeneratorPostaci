# Dokumentacja Projektu: Generator Postaci Warhammer


## 1. Ogólny Opis Projektu

Aplikacja "Generator Postaci Warhammer by Lauer" słuzy zarządzania postaciami w systemie gry fabularnej Warhammer Fantasy Roleplay (WFRP). 

*   **W pełni losowe generowanie postaci:** Jednym kliknięciem tworzy kompletną postać, losując rasę, profesję, statystyki, wygląd i inne szczegóły.
*   **Manualne tworzenie postaci:** Użytkownik może krok po kroku wybrać wszystkie atrybuty swojej postaci, korzystając z list opartych na danych z gry.
*   **Zarządzanie kartą postaci:** Po stworzeniu postaci, aplikacja wyświetla kartę postaci, na której można śledzić swój rozwój.
*   **Rozwój postaci:** Umożliwia wydawanie punktów doświadczenia (PD) na rozwój cech oraz zmianę profesji po spełnieniu wymagań.
*   **Naukę umiejętności i zdolności:** Daje możliwość uczenia się nowych umiejętności i zdolności za PD.
*   **Zarządzanie ekwipunkiem:** Posiada wbudowany sklep, w którym można kupować przedmioty za złoto.
*   **Zapis i wczytywanie:** Postacie można zapisywać na dysku i wczytywać w dowolnym momencie, co pozwala na prowadzenie wielu postaci jednocześnie.

## 2. Użyte Technologie

*   **Język programowania:** Python 3
*   **Interfejs graficzny (GUI):** PyQt6 
*   **Format danych:** JSON 
*   **Czcionka:** MedievalSharp 

## 3. Instrukcja Uruchomienia
1. Pobierz kod z githuba

2.  Upewnij się, że masz zainstalowany Python 3 oraz bibliotekę PyQt6.
    ```bash
    pip install PyQt6
    ```
3.  Uruchom aplikację.
    ```bash
    python main.py
    ```
---

## 4. Struktura Projektu

*   **`main.py`**: Główny plik startowy aplikacji. Odpowiada za inicjalizację `QApplication`, wczytanie czcionek i uruchomienie głównego okna.
*   **`Character.py`**: Definicja klasy `Character`, która jest modelem danych dla postaci gracza. Przechowuje wszystkie informacje o postaci i zawiera metodę do serializacji.
*   **`database/`**: Folder zawierający plik `database.json`. Przechowuje on wszystkie dane potrzebne do generowania i rozwijania postaci.
*   **`fonts/`**: Folder w którym znajduje sie czcionka
*   **`logic/`**: Moduły zawierające logikę aplikacji.
    *   `character_auto_generator.py`: Funkcje do losowego tworzenia postaci.
    *   `character_manual_generator.py`: Funkcje które przekazuja w odpowiedni sposób dane by to użytkownik mógł wybrać samemu poszczególne obcje.
    *   `character_develop.py`: Logika rozwoju postaci (wykupowanie rozwinięć, zmiana profesji).
    *   `character_buy_items.py`: Logika sklepu i kupowania przedmiotów.
    *   `character_learning.py`: Logika do nauki nowych umiejętności i zdolności.
    *   `save_load_logic.py`: Funkcje odpowiedzialne za zapisywanie i wczytywanie plików postaci.
*   **`ui/`**: Moduły definiujące poszczególne okna i widgety interfejsu użytkownika.
    *   `window_connector.py`: Centralny hub aplikacji, zarządza przełączaniem między widokami i przechowuje stan aktualnej postaci.
    *   `main_window.py`: Główne okno aplikacji, wyświetlające kartę postaci.
    *   `generateCharacter_window.py`: Okno do tworzenia nowej postaci.
    *   `developCharacter_window.py`: Okno rozwoju postaci.
    *   `buyItems_window.py`: Okno do Interfejsu sklepu.
    *   `learn_skill_talent_window.py`: Okno do nauki umiejetności i zdolności sklepu.
    *   `addGoldAndXp_Window.py`: Okno do zwiekszenia Xp i Golda
    *   `save_character_window.py`: Okno do zapisu postaci
    *   `load_character_window.py`: Okno do wczytanai sava postaci
    *   `styles.py`: Centralny plik ze stylem
*   **`saves/`**: Domyślny folder, w którym przechowywane są zapisane postacie w formacie `.json` wraz ze zdjeciami.


