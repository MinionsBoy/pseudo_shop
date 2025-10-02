# Pseudo Shop – Dokumentacja i zakładany zakres testów

## O aplikacji

Pseudo Shop to minimalistyczna aplikacja sklepu internetowego napisana w
[Flask](https://flask.palletsprojects.com/).  Umożliwia ona przeglądanie
listy produktów, podgląd szczegółów, dodawanie do koszyka oraz
usuwanie z koszyka.  Wszystkie dane są przechowywane w pamięci,
dzięki czemu aplikację można uruchomić bez konfiguracji bazy danych.
Ponadto udostępnione są **interfejsy API** (`/api/products`,
`/api/cart`), które zwracają dane w formacie JSON i pozwalają na
manipulowanie koszykiem z poziomu zapytań HTTP.

Ta struktura stanowi dobrą podstawę do nauki automatyzacji testów.

## Instrukcja uruchomienia aplikacji

1. **Utwórz i aktywuj wirtualne środowisko.**  Dzięki temu
   zależności nie będą kolidowały z innymi projektami.  W systemach
   Unix/Linux/OS X wykonaj:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   W systemie Windows użyj polecenia `venv\Scripts\activate`.

2. **Zainstaluj zależności.**  Lista niezbędnych pakietów znajduje się w
   pliku `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację.**  Możesz uruchomić serwer Flask bezpośrednio
   poleceniem:

   ```bash
   python app.py
   ```

   lub korzystając z wbudowanego narzędzia `flask`:

   ```bash
   export FLASK_APP=app.py  # w systemie Windows: set FLASK_APP=app.py
   flask run
   ```

4. Otwórz przeglądarkę i przejdź pod adres `http://127.0.0.1:5000/` aby
   zobaczyć stronę główną sklepu.  Interfejs API dostępny jest pod
   ścieżkami `/api/products` i `/api/cart`.

5. Aby przeprowadzić testy wydajnościowe z użyciem **Locust**,
   zainstaluj dodatkowo pakiet `locust` (`pip install locust`) i
   uruchom w katalogu projektu polecenie `locust`.  Szczegóły
   znajdziesz w pliku `locustfile.py` oraz w dokumentacji
   Locusta【287612495241309†L45-L74】.

## Struktura projektu

```
pseudo_shop/
├── app.py            # główny plik aplikacji Flask
├── locustfile.py     # skrypt do testów wydajnościowych (Locust)
├── requirements.txt  # zależności Pythona
├── templates/        # pliki szablonów HTML
├── static/           # pliki statyczne (CSS)
├── tests/            # pozostawione puste miejsce na Twoje testy PyTest
└── README.md         # niniejsza dokumentacja
```

## Zakres testów automatycznych

Poniżej przedstawiono przykładowy zakres testów, które warto
zaimplementować.  Lista jest długa, ale pojedyncze przypadki są
proste – celem jest objęcie testami jak największej części
funkcjonalności.

### 1. Testy jednostkowe (unit tests)

Testy jednostkowe sprawdzają pojedyncze funkcje i metody w izolacji
od reszty systemu【742723500898335†L87-L100】.  W projekcie testy
można napisać w bibliotekach `pytest` lub `unittest`【487443277442423†L102-L113】; pliki z testami powinny
rozpoczynać się od `test_` i znajdować się w katalogu `tests/`【930677016118185†L23-L27】.

Propozycje prostych testów jednostkowych:

| Funkcja/metoda | Co sprawdzamy? |
|---|---|
| `get_product_by_id` | Zwraca odpowiedni produkt dla istniejącego `id`; zwraca `None` dla `id`, którego nie ma. |
| `get_cart` | Tworzy nowy koszyk, jeśli nie istnieje; ponowne wywołanie zwraca ten sam koszyk (persistencja w sesji). |
| `calculate_cart_total` | Poprawnie sumuje ceny w koszyku dla różnych ilości produktów. |
| Widoki Flask (`index`, `product_detail`, `cart`) | Zwracają kod 200 (lub 404, jeśli produkt nie istnieje) i zawierają oczekowane elementy w `response.data`. |
| API (`/api/products`, `/api/products/<id>`, `/api/cart`) | Zwracają kod HTTP 200 oraz JSON z odpowiednią strukturą; błędne żądania zwracają kod 400/404. |

Przy pisaniu testów API skorzystaj z wbudowanego **klienta testowego**
Flaska.  Klient pozwala wysyłać żądania GET/POST bez uruchamiania
prawdziwego serwera【930677016118185†L75-L89】.  Dane form i pliki można
przekazywać poprzez parametr `data`, a JSON poprzez parametr
`json`【930677016118185†L79-L101】.

Testy jednostkowe można podzielić na dwa podkatalogi, np. `tests/unit` i
`tests/api`, co ułatwi uruchamianie tylko wybranego zestawu【742723500898335†L195-L203】.

### 2. Testy API

Chociaż testy API są częściowo pokryte testami jednostkowymi, warto
wydzielić dedykowany zestaw scenariuszy odwzorowujących prawdziwe
wywołania REST‑owe:

* **Lista produktów:** żądanie GET `/api/products` zwraca listę
  produktów w formacie JSON; liczba elementów odpowiada
  wielkości listy `products` w aplikacji.

* **Szczegóły produktu:** żądanie GET `/api/products/2` zwraca dane
  produktu o identyfikatorze 2; żądanie z nieistniejącym id
  zwraca kod 404 i komunikat o błędzie.

* **Dodawanie do koszyka:** żądanie POST `/api/cart` z ciałem
  `{'product_id': 3}` zwraca kod 201 i komunikat o dodaniu; po
  dodaniu kilku produktów `GET /api/cart` powinno zwrócić listę
  elementów z odpowiednimi ilościami i polem `total` równym sumie
  cen.

* **Błędne żądania:** żądanie POST `/api/cart` bez pola
  `product_id` lub z nieprawidłowym typem powinno zwracać kod 400,
  natomiast z id spoza listy produktów – kod 404.

W testach API warto korzystać z parametrów `follow_redirects` i
`json` klienta testowego【930677016118185†L75-L90】 oraz sprawdzać
nagłówki odpowiedzi.

### 3. Testy Selenium / end‑to‑end (E2E)

Testy E2E symulują zachowania prawdziwego użytkownika i obejmują całą
ścieżkę aplikacji【796096092115764†L243-L266】.  Wykorzystują przeglądarkę (np.
Chrome lub Firefox) sterowaną przez **Selenium** albo nowoczesne
narzędzia E2E.  Takie testy powinny potwierdzić, że wszystkie
komponenty – od szablonów HTML po logikę serwerową – współdziałają
poprawnie【487443277442423†L164-L186】.

Poniżej lista sugerowanych scenariuszy E2E (przykładowe; w razie
potrzeby można dodać kolejne):

* **Wyświetlanie strony głównej:** otworzenie adresu głównego
  `http://localhost:5000/`, sprawdzenie tytułu strony i liczby
  wyświetlonych produktów.

* **Przegląd produktu:** kliknięcie w link „Szczegóły” na liście
  produktów; sprawdzenie, że otwarta została strona produktu z
  prawidłowym opisem i ceną.

* **Dodawanie do koszyka:** na stronie produktu kliknięcie przycisku
  „Dodaj do koszyka” powinno przenieść użytkownika do koszyka; liczba
  pozycji w koszyku powinna się zwiększyć.

* **Usuwanie z koszyka:** na stronie koszyka kliknięcie przycisku
  „Usuń” powinno zmniejszyć ilość danego produktu lub całkowicie go
  usunąć.

* **Nawigacja:** sprawdzenie, że link „Kontynuuj zakupy” z koszyka
  prowadzi z powrotem na stronę główną.

Podczas pisania testów Selenium należy pamiętać o kilku dobrych
praktykach:

* **Używaj explicit waits.**  Zamiast statycznych `sleep()` stosuj
  mechanizmy oczekiwania, które czekają tylko do momentu pojawienia
  się elementu na stronie; dzięki temu testy będą bardziej stabilne【314694163589468†L332-L339】.

* **Dobieraj wytrzymałe selektory.**  Preferuj identyfikatory (`id`)
  lub atrybuty `name`, unikaj złożonych selektorów `xpath` czy
  `cssSelector`, ponieważ są podatne na zmiany w układzie strony【314694163589468†L341-L345】.

* **Stosuj asercje.**  Każdy scenariusz powinien weryfikować stan
  aplikacji, np. tytuł strony, obecność elementu czy zmianę adresu
  URL【314694163589468†L347-L353】.

* **Parametryzuj testy i porządkuj je w zestawy.**  Ułatwia to
  uruchamianie tych samych scenariuszy z różnymi danymi i poprawia
  organizację projektu【314694163589468†L360-L377】.

* **Dbaj o cleanup.**  Zamykaj przeglądarkę po każdym teście, aby
  zwolnić zasoby【314694163589468†L385-L391】.

### 4. Testy wydajnościowe

Testy wydajnościowe badają, jak aplikacja reaguje na duże obciążenie.
W projekcie załączono plik `locustfile.py` z przykładowym scenariuszem
używającym narzędzia **Locust**.  Scenariusz polega na losowym
wywoływaniu API produktów oraz dodawaniu produktów do koszyka przez
wielu równoległych użytkowników.  Możesz go uruchomić poleceniem
`locust` i skonfigurować liczbę użytkowników oraz tempo przyrostu w
interfejsie webowym (domyślnie pod adresem `http://localhost:8089`).

Kilka wskazówek do przygotowania własnych testów wydajnościowych:

* **Określ użytkowników i scenariusze.**  Zdefiniuj klasy użytkowników
  z metodami odwzorowującymi typowe ścieżki (przegląd produktów,
  dodawanie do koszyka).  Każda metoda powinna korzystać z API
  aplikacji【287612495241309†L45-L74】.

* **Stopniowo zwiększaj obciążenie.**  Rozpocznij test od małej liczby
  użytkowników (np. 5–10), a następnie zwiększaj ją aż do momentu,
  gdy czas odpowiedzi zacznie rosnąć, co pozwoli znaleźć wąskie gardła
  serwera.

* **Mierz kluczowe metryki.**  Monitoruj średnie i maksymalne czasy
  odpowiedzi, liczbę żądań na sekundę oraz wskaźniki błędów.  Locust
  udostępnia te statystyki w zakładce **Charts** interfejsu webowego.

* **Przygotuj osobne środowisko testowe.**  Testy wydajnościowe mogą
  znacząco obciążyć aplikację; najlepiej uruchamiać je w izolacji,
  korzystając np. z dockerowego kontenera lub środowiska stagingowego.

### 5. Inne uwagi

* **Testy w osobnej konfiguracji.**  Dobrym zwyczajem jest
  skonfigurowanie aplikacji w trybie testowym (`TESTING = True`) oraz
  używanie oddzielnej bazy danych.  Dzięki temu
  testy nie będą ingerować w dane produkcyjne.

* **Pokrycie kodu.**  Narzędzie `coverage.py` pozwala zmierzyć, która
  część kodu została przetestowana.  Dąż do wysokiego pokrycia (np.
  ≥80 %)【796096092115764†L243-L266】, ale pamiętaj, że jakość testów jest ważniejsza
  niż sama liczba.

## Podpis

Mikołaj Mikołajczak 2025