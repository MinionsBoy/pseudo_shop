### 1. GET `/api/products`
- **Scenariusz:** Odpowiedź dla pustej listy produktów (jeśli aplikacja to obsługuje).
  - Oczekiwany rezultat: kod 200, odpowiedź JSON zawiera pustą listę.

### 2. GET `/api/products/<id>`
- **Scenariusz:** Przekazanie nieprawidłowego typu identyfikatora (np. tekst zamiast liczby).
  - Oczekiwany rezultat: kod 404 lub 400, odpowiedź JSON z informacją o błędzie.

### 3. POST `/api/cart`
- **Scenariusz:** Dodanie produktu do koszyka wielokrotnie (sprawdzenie zwiększania ilości).
  - Oczekiwany rezultat: kod 201, ilość produktu w koszyku zwiększa się przy każdym dodaniu.
- **Scenariusz:** Dodanie produktu z nadmiarowymi polami w JSON.
  - Oczekiwany rezultat: kod 201, nadmiarowe pola są ignorowane, produkt dodany poprawnie.
- **Scenariusz:** Dodanie produktu z pustym ciałem żądania.
  - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.

### 4. GET `/api/cart`
- **Scenariusz:** Pobranie koszyka, gdy jest pusty.
  - Oczekiwany rezultat: kod 200, odpowiedź JSON zawiera pustą listę produktów i `total` równy 0.

### 5. DELETE `/api/cart/<product_id>` (jeśli API obsługuje)
- **Scenariusz:** Usunięcie produktu z pustego koszyka.
  - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.
- **Scenariusz:** Usunięcie produktu z koszyka, gdy występuje wielokrotnie (sprawdzenie czy ilość się zmniejsza lub produkt jest usuwany całkowicie).

---

**Dodatkowe uwagi:**
- Sprawdzaj poprawność obsługi nietypowych danych wejściowych (np. bardzo duże liczby, znaki specjalne).
- Testuj zachowanie sesji (czy koszyk jest unikalny dla każdej sesji testowej).
- Sprawdzaj, czy odpowiedzi nie zawierają zbędnych lub poufnych danych.