***

# Dokumentacja Projektu: Generator Postaci Warhammer

## 1. Instalacja i Uruchomienie

Aby rozpocząć pracę z generatorem, postępuj zgodnie z poniższymi krokami:

1.  **Pobierz aplikację**
    Upewnij się, że masz wszystkie pliki projektu na swoim komputerze.

2.  **Zainstaluj środowisko Python**
    Aplikacja wymaga zainstalowanego Pythona do poprawnego działania.

3.  **Zainstaluj wymaganą bibliotekę**
    Otwórz terminal lub wiersz poleceń i zainstaluj bibliotekę `PyQt6` za pomocą menedżera pakietów pip:
    ```bash
    pip install PyQt6
    ```

4.  **Uruchom aplikację**
    W głównym folderze projektu wykonaj następującą komendę:
    ```bash
    python main.py
    ```

## 2. Przewodnik Użytkownika

### Główne Okno: Kreator Postaci

Po uruchomieniu aplikacji wita Cię okno kreatora postaci, które jest centralnym punktem programu.

![Okno Kreatora Postaci](photos/First_window.png)

Z tego poziomu masz dostęp do trzech głównych funkcji, które pozwalają rozpocząć nową przygodę lub kontynuować poprzednią.

#### 1. Tworzenie Ręczne

Ta opcja daje Ci pełną kontrolę nad procesem kreacji bohatera. Możesz samodzielnie wybrać rasę, płeć, imię oraz profesję. Formularz jest w pełni interaktywny – po wybraniu rasy i profesji podgląd cech, umiejętności i zdolności na dole okna natychmiast się zaktualizuje. Jest to idealne rozwiązanie dla graczy, którzy mają już sprecyzowaną wizję swojej postaci. Aby zakończyć, uzupełnij wszystkie pola i kliknij przycisk **"Stwórz Postać"**.

#### 2. Wczytanie Postaci

Jeśli posiadasz już bohatera zapisanego z poprzedniej sesji, możesz bez problemu wrócić do rozgrywki. Użyj przycisku **"Wczytaj Postać"**, aby otworzyć listę zapisanych plików i kontynuować swoją przygodę dokładnie tam, gdzie ją przerwałeś.

#### 3. Generowanie w Pełni Losowe

Szukasz inspiracji lub chcesz jak najszybciej rozpocząć grę? Kliknij przycisk **"Wygeneruj w Pełni Losową Postać"**. Aplikacja w jednym kroku stworzy dla Ciebie kompletną, gotową do gry postać – losując wszystko, od rasy i imienia, po statystyki i ekwipunek.

