# Scenariusze testów wydajnościowych (Locust) – pseudo_shop

Testy wydajnościowe pozwalają sprawdzić, jak aplikacja radzi sobie pod dużym obciążeniem. W projekcie znajduje się plik `locustfile.py` z przykładowym scenariuszem wykorzystującym narzędzie **Locust**.

---

## 1. Scenariusze użytkowników

- **Przeglądanie produktów**
  - Użytkownik wysyła żądania GET `/api/products` (lista produktów).
  - Użytkownik losowo wybiera produkt i wysyła GET `/api/products/<id>` (szczegóły produktu).

- **Dodawanie do koszyka**
  - Użytkownik wysyła żądania POST `/api/cart` z losowym `product_id`.

- **Mieszany scenariusz**
  - Użytkownik naprzemiennie przegląda produkty i dodaje je do koszyka.

---

## 2. Stopniowe zwiększanie obciążenia

- Rozpocznij test od małej liczby użytkowników (np. 5–10).
- Stopniowo zwiększaj liczbę użytkowników (np. co 10–20 sekund) aż do momentu, gdy:
  - Czas odpowiedzi zacznie wyraźnie rosnąć,
  - Wskaźnik błędów przekroczy akceptowalny poziom,
  - Serwer przestanie odpowiadać.

---

## 3. Kluczowe metryki do monitorowania

- Średni i maksymalny czas odpowiedzi (response time).
- Liczba żądań na sekundę (RPS).
- Wskaźnik błędów (procent odpowiedzi 4xx/5xx).
- Liczba użytkowników aktywnych w danym momencie.

---

## 4. Dobre praktyki

- **Testuj w osobnym środowisku** – testy wydajnościowe mogą obciążyć aplikację i bazę danych.
- **Analizuj wykresy w zakładce Charts** w interfejsie Locusta (`http://localhost:8089`).
- **Zdefiniuj różne klasy użytkowników** w pliku `locustfile.py` dla różnych ścieżek (np. tylko przeglądanie, tylko dodawanie do koszyka, scenariusz mieszany).
- **Dokumentuj wąskie gardła** – notuj, przy jakim obciążeniu pojawiają się problemy z wydajnością.

---

## 5. Przykładowy przebieg testu

1. Uruchom aplikację i Locusta: `locust`
2. W interfejsie webowym ustaw:
   - Liczbę użytkowników początkowych (np. 5)
   - Tempo przyrostu użytkowników (np. 1 użytkownik/s)
3. Obserwuj wykresy i statystyki.
4. Zwiększaj liczbę użytkowników, aż pojawią się opóźnienia lub błędy.
5. Zapisz wyniki i wnioski.