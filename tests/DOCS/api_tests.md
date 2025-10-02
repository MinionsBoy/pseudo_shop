# Scenariusze testów API – pseudo_shop

## 1. Lista produktów

- **GET `/api/products`**
  - Oczekiwany rezultat: kod 200, odpowiedź w formacie JSON.
  - Lista produktów powinna zawierać wszystkie produkty dostępne w aplikacji.
  - Każdy produkt powinien mieć pola: `id`, `name`, `price`, `description` (lub inne zgodnie z modelem).

## 2. Szczegóły produktu

- **GET `/api/products/<id>`**
  - Dla istniejącego `id`:
    - Oczekiwany rezultat: kod 200, odpowiedź JSON z danymi produktu.
    - Sprawdź poprawność pól produktu.
  - Dla nieistniejącego `id`:
    - Oczekiwany rezultat: kod 404, odpowiedź JSON z komunikatem o błędzie.

## 3. Dodawanie do koszyka

- **POST `/api/cart`**
  - Z poprawnym `product_id`:
    - Oczekiwany rezultat: kod 201, odpowiedź JSON z potwierdzeniem dodania.
    - Po dodaniu kilku produktów, GET `/api/cart` powinien zwracać listę produktów z odpowiednimi ilościami i polem `total`.
  - Bez `product_id` w żądaniu:
    - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.
  - Z nieprawidłowym typem `product_id`:
    - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.
  - Z nieistniejącym `product_id`:
    - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.

## 4. Przegląd koszyka

- **GET `/api/cart`**
  - Oczekiwany rezultat: kod 200, odpowiedź JSON z aktualnym stanem koszyka.
  - Zawiera listę produktów, ilości oraz pole `total` z sumą cen.

## 5. Usuwanie z koszyka (jeśli API obsługuje)

- **DELETE `/api/cart/<product_id>`**
  - Dla istniejącego produktu w koszyku:
    - Oczekiwany rezultat: kod 200, odpowiedź JSON z potwierdzeniem usunięcia.
  - Dla nieistniejącego produktu:
    - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.

---

## Uwagi

- Sprawdzaj nagłówki odpowiedzi (`Content-Type: application/json`).
- Testuj przypadki brzegowe (pusty koszyk, wielokrotne dodanie tego samego produktu).
- Warto używać klienta testowego Flask do wysyłania żądań i sprawdzania odpowiedzi.
