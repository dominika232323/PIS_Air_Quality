# Air Quality - System Monitorowania Jakości Powietrza

## Cel projektu
Celem projektu jest stworzenie systemu informatycznego do przechowywania, przetwarzania i wizualizacji danych o jakości powietrza na podstawie publicznie dostępnego API (https://powietrze.gios.gov.pl/pjp/content/api). System ma wspierać analizę danych historycznych, ich agregację oraz umożliwiać interaktywne wizualizacje w przystępnej formie dla użytkowników.

---

## Kluczowe funkcjonalności
### 1. Wyświetlanie stacji pomiarowych
- Lista wszystkich dostępnych stacji z możliwością filtrowania po:
  - nazwie,
  - lokalizacji (gmina, powiat, województwo),
  - mierzonych parametrach.

### 2. Informacje szczegółowe o stacji
- Wyświetlanie listy stanowisk na wybranej stacji oraz parametrów, które mierzą.

### 3. Wyświetlanie najnowszych danych pomiarowych
- Wizualizacja najnowszych i historycznych granicznych (najniższa i najwyższa wartość) pomiarów dla każdego stanowiska na stacji.

### 4. Wspieranie danych historycznych
- Wyświetlanie wykresu historii wartości parametrów na wybranej stacji w formie wykresu z róznymi przedziałami czasowymi (dla ostatniego dnia, tygodnia, miesiąca, roku i całej historii) i oznaczonymi wartościami najmniejszymi, największymi i przekraczającymi normy

### 5. Agregacja danych
- Wyświetlanie zagregowanych wartości parametrów dla różnych poziomów administracyjnych:
  - dla ostatniego pomiaru,
  - dla wybranego przedziału czasowego.

### 6. Monitorowanie norm jakości powietrza
- Wyświetlanie aktualnych ostrzeżeń o przekroczonych normach jakości powietrza.
- Wyświetlanie chronologicznej listy przeszłych ostrzeżeń o przekroczonych normach z możliwością filtrowania po czasie i lokalizacji.

### 7. Interaktywne wizualizacje
- Interaktywne wykresy.
- Kolorowanie stacji w zależności od poziomu jakości powietrza (np. bardzo dobry – zielony, zły – czerwony).

### Ewentualne rozszerzenia
- Wyświetlanie stacji i pomiarów na interaktywnej mapie
- Znajdowanie najbliższej stacji na podstawie współrzędnych geografizcznych

---

## Użytkowanie

### Uruchamianie aplikacji

- Przejdź do głównego katalogu repozytorium (tam gdzie znajduje się Makefile).
- Uruchom aplikacje poleceniem `make up`.
- Zatrzymaj aplikację (bazę danych) poleceniem `make down`.

### Testowanie

- Przejdź do głównego katalogu repozytorium (tam gdzie znajduje się Makefile).
- Zainstaluj zależności poleceniem `make requirements`.
- Uruchom testy poleceniem `make tests`.
- Sprawdz coverage testów poleceniem `make coverage`.
- Usuń pozostałości po testowaniu pokrycia `make clean`.

### Lista pozostałych poleceń
- `make migrations` - stosuje migracje (po dodaniu/ zmienieniu modelu)
- `make start_db` - uruchamia kontener z bazą danych
- `make stop_db` - zatrzymuje kontener z bazą danych
- `make run` - uruchamia serwer Django

---

## Endpointy

- `.../` - wyświetla stronę powitalną
- `.../all/` - wyświetla listę wszystkich stacji i ich położenie
- `.../<nr_stacji>/` - wyświetla listę sensorów na stacji o podanym numerze

---

## Technologie

### Backend
- **Python**: język programowania do przetwarzania danych.
- **Django**: framework do zarządzania bazą danych i obsługi API.
- **PostgreSQL**: baza danych do przechowywania danych pomiarowych.
- **Docker**: konteneryzacja aplikacji i bazy danych.

### Frontend
- Interaktywne wizualizacje z wykorzystaniem:
  - **Plotly**,
- **Streamlit**.

### CI/CD:
- **Jira**: system zarządzania zadaniami.
- **GitHub**: repozytorium kodu.
- **Pytest**: framework do testowania.
- **Jenkins**: automatyczne budowanie, testowanie i wdrażanie aplikacji.
- **Nexus**: repozytorium artefaktów.

---
