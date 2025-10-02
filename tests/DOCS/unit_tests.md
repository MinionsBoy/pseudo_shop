## 1. Funkcja `get_product_by_id`

- **Scenariusz:** Zwraca poprawny produkt dla istniejącego `id`.
- **Scenariusz:** Zwraca `None` dla nieistniejącego `id`.
- **Scenariusz:** Obsługuje nieprawidłowy typ `id` (np. tekst zamiast liczby).

## 2. Funkcja `get_cart`

- **Scenariusz:** Tworzy nowy koszyk, jeśli nie istnieje w sesji.
- **Scenariusz:** Ponowne wywołanie zwraca ten sam koszyk (persistencja w sesji).
- **Scenariusz:** Koszyk jest unikalny dla każdej sesji użytkownika.

## 3. Funkcja `calculate_cart_total`

- **Scenariusz:** Poprawnie sumuje ceny dla pojedynczego produktu.
- **Scenariusz:** Poprawnie sumuje ceny dla wielu produktów i różnych ilości.
- **Scenariusz:** Zwraca 0 dla pustego koszyka.
- **Scenariusz:** Obsługuje produkty z ceną 0 lub ujemną (jeśli takie są możliwe).

## 4. Widoki Flask (HTML)

- **Widok `index`:**
  - Zwraca kod 200 i zawiera listę produktów w treści odpowiedzi.
- **Widok `product_detail`:**
  - Zwraca kod 200 dla istniejącego produktu i zawiera jego dane.
  - Zwraca kod 404 dla nieistniejącego produktu.
- **Widok `cart`:**
  - Zwraca kod 200 i zawiera listę produktów oraz sumę w koszyku.

## 5. Inne przypadki

- **Scenariusz:** Dodanie tego samego produktu wielokrotnie do koszyka zwiększa jego ilość.
- **Scenariusz:** Usunięcie produktu z koszyka zmniejsza ilość lub usuwa produkt całkowicie, jeśli ilość spada do zera.
- **Scenariusz:** Koszyk nie zawiera duplikatów produktów – ilość jest sumowana.

---

**Dodatkowe uwagi:**
- Testuj przypadki brzegowe (np. pusta lista produktów, bardzo duże liczby).
- Sprawdzaj, czy funkcje nie modyfikują danych wejściowych (jeśli nie powinny).
- Zalecane jest użycie bibliotek `pytest` lub `unittest` do implementacji tych testów.