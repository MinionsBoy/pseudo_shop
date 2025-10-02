# Dodatkowe scenariusze testowe – pseudo_shop

## API

- Test odpowiedzi na żądania z bardzo dużymi liczbami (`product_id`, ilość).
- Test odpowiedzi na żądania z nietypowymi znakami w polach (np. `name`, `description`).
- Test odpowiedzi na żądania bez wymaganych nagłówków (np. brak `Content-Type`).
- Test odpowiedzi na żądania z nieautoryzowanego źródła (jeśli dotyczy).
- Test odpowiedzi na żądania z nieprawidłową metodą HTTP (np. PUT na endpoint POST).

## E2E

- Próba wejścia na nieistniejącą stronę produktu – oczekiwany kod 404 i komunikat.
- Odświeżenie koszyka po usunięciu produktu – sprawdzenie, czy stan się zgadza.
- Cofnięcie w przeglądarce po dodaniu produktu do koszyka – sprawdzenie spójności stanu.
- Próba dodania produktu do koszyka bez zalogowania (jeśli dotyczy autoryzacji).

## Wydajność

- Test długotrwałego obciążenia (np. 1 godzina, stała liczba użytkowników).
- Test z bardzo dużą liczbą użytkowników (np. 1000+), aż do przeciążenia serwera.
- Test odporności na awarie – restart serwera w trakcie testu i sprawdzenie reakcji klientów.

## Jednostkowe

- Test niezmienności danych wejściowych (funkcje nie modyfikują argumentów).
- Testy na bardzo duże dane wejściowe (np. lista 10 000 produktów).
- Testy na nieprawidłowe typy danych (np. `None`, lista zamiast liczby).

---
