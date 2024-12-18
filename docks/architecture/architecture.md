# Warstwa Kontekstu

Użytkownik za pomocą aplikacji może otrzymać dane o pomiarach jakości powietrza pobrane z GIOS api.

# Warstwa Kontenerów

W ramach aplikacji wyróżniamy 3 kontenery
- Aplikację przeglądarkową która służy jako interfejs użytkownika
- Django Api obsługujące zapytania z przeglądarki i dostarczające dane do wyświetlenia
- Baza danych służąca do zapisu i odczytu danych historycznych

# Warstwa Komponentów

Warstwa komponentów opisuje 2 z wyżej wymienionych kontenerów: Aplikację przeglądarkową i Backend w django


## Aplikacja przeglądarkowa

Składa się z 4 komponentów:

- strony głównej - wyświetlanie pod rooterm url. Docelowo zawierać będzie przywitanie i odnośnik do listy stacji pomiarowych
- strona z listą stacji pomiarowych. Będzie zawierać listę dostępnych stacji pomiarowych, podstawowe informacje o nich i odnośniki do strony z ich detalami
- strona z detalami stacji. Tu docelowo wyświetlane będą obecne odczyty jakości powietrza. Odczyty będą uwzględniać wyniki pomiarów wielu elementów
- podstrona z danymi historycznymi. Tu wyświetlany będzie wykres historycznych wyników pomiarów.


## Backend

- URL-s komponent frameworku Django odpowiadający za serwowanie odpowiednich danych po wejściu na określone url. Każde url strony ma przypisaną metodę w komponencie tworzenia widoków
- Komponent tworzenia widoków. Zawiera metody odpowiedzialne za przygotowanie strony i danych na niej wyświetlanych.

Poszczególne metody korzystają z wzorców stron HTML i mogą korzystać z komponentów odpowiedzialnych za pobieranie najnowszych danych lub agregacji danych historycznych
- Wzorce HTML. Wzorce określające ogólny wygląd strony internetowej z dynamicznymi elementami do wyświetlania danych.
- Komponent zbierania danych o stacji. Jest wywoływany w przypadku potrzeby pobrania najnowszych odczytów jakości powietrza lub w przypadku braku danych o stacji w lokalnej bazie danych. Wysyła zapytania do GIOS API
- Komponent agregacji danych. Służy do wczytywania informacji o historycznych pomiarach z danej stacji. Wywołuje zapytania na bazie danych i przetwarza dane tak by metody w komponencie tworzenia widoków mogły łatwo na nich operować.
