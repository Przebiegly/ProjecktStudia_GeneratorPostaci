class Character:
    def __init__(self, character_data: dict):
        details = character_data.get('szczegoly_osobiste', {})

        self.imie = details.get('imie', 'Bezimienny')
        self.rasa = character_data.get('rasa', 'Nieznana')
        self.plec = character_data.get('plec', 'Nieznana')
        self.wiek = details.get('wiek', 0)
        self.profesja = character_data.get('profesja', 'Brak')

        self.cechy_glowne = character_data.get('cechy_glowne', {})
        self.cechy_drugorzedne = character_data.get('cechy_drugorzedne', {})
        self.wyglad = character_data.get('wyglad', {})
        self.szczegoly_osobiste = details

        self.umiejetnosci = character_data.get('umiejetnosci', [])
        self.zdolnosci = character_data.get('zdolnosci', [])

        # ### ZMIANA: Obsługa nowego i starego formatu ekwipunku dla kompatybilności ###
        ekwipunek_data = character_data.get('ekwipunek', [])
        if ekwipunek_data and isinstance(ekwipunek_data[0], str):
            # Konwersja ze starego formatu (lista stringów) do nowego
            self.ekwipunek = [{'name': name, 'icon_path': ''} for name in ekwipunek_data]
        else:
            # Nowy format (lista słowników) jest już poprawny
            self.ekwipunek = ekwipunek_data

        self.xp = character_data.get('xp', 0)
        self.gold = character_data.get('gold', 0)

        self.schemat_rozwoju = character_data.get('schemat_rozwoju', {})
        self.purchased_advances = character_data.get('purchased_advances', {})

        self.portrait_path = character_data.get('portrait_path', '')
        self.portrait_ext = character_data.get('portrait_ext', '')


    def to_dict(self) -> dict:
        """Konwertuje obiekt postaci z powrotem na słownik w celu zapisu."""
        return {
            'rasa': self.rasa,
            'plec': self.plec,
            'profesja': self.profesja,
            'cechy_glowne': self.cechy_glowne,
            'cechy_drugorzedne': self.cechy_drugorzedne,
            'wyglad': self.wyglad,
            'szczegoly_osobiste': self.szczegoly_osobiste,
            'umiejetnosci': self.umiejetnosci,
            'zdolnosci': self.zdolnosci,
            'ekwipunek': self.ekwipunek,
            'xp': self.xp,
            'gold': self.gold,
            'schemat_rozwoju': self.schemat_rozwoju,
            'purchased_advances': self.purchased_advances,
            'portrait_path': self.portrait_path,
            'portrait_ext': self.portrait_ext
        }