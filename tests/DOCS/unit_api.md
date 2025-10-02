
### 1. GET `/api/products`
- **Scenariusz:** Odpowiedź dla pustej listy produktów (jeśli aplikacja to obsługuje).
  - Oczekiwany rezultat: kod 200, odpowiedź JSON zawiera pustą listę.
- **Scenariusz:** Każdy produkt w odpowiedzi ma wymagane pola (`id`, `name`, `price`, `description` ...).
  - Oczekiwany rezultat: wszystkie produkty mają komplet wymaganych pól.


### 2. GET `/api/products/<id>`
- **Scenariusz:** Przekazanie nieprawidłowego typu identyfikatora (np. tekst zamiast liczby).
  - Oczekiwany rezultat: kod 404 lub 400, odpowiedź JSON z informacją o błędzie.
- **Scenariusz:** Sprawdzenie poprawności pól produktu w odpowiedzi dla istniejącego id.
  - Oczekiwany rezultat: kod 200, odpowiedź JSON zawiera wszystkie wymagane pola produktu.


### 3. POST `/api/cart`
- **Scenariusz:** Dodanie produktu do koszyka wielokrotnie (sprawdzenie zwiększania ilości).
  - Oczekiwany rezultat: kod 201, ilość produktu w koszyku zwiększa się przy każdym dodaniu.
- **Scenariusz:** Dodanie produktu z nadmiarowymi polami w JSON.
  - Oczekiwany rezultat: kod 201, nadmiarowe pola są ignorowane, produkt dodany poprawnie.
- **Scenariusz:** Dodanie produktu z pustym ciałem żądania.
  - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.
- **Scenariusz:** Po dodaniu kilku produktów, `GET /api/cart` zwraca listę elementów z odpowiednimi ilościami i polem `total` równym sumie cen.
  - Oczekiwany rezultat: kod 200, lista produktów i pole `total` są zgodne z oczekiwaniami.


### 4. GET `/api/cart`
- **Scenariusz:** Pobranie koszyka, gdy jest pusty.
  - Oczekiwany rezultat: kod 200, odpowiedź JSON zawiera pustą listę produktów i `total` równy 0.
- **Scenariusz:** Zawartość koszyka po dodaniu produktów – sprawdzenie ilości i sumy.
  - Oczekiwany rezultat: kod 200, lista produktów i pole `total` są zgodne z oczekiwaniami.


### 5. DELETE `/api/cart/<product_id>` (jeśli API obsługuje)
- **Scenariusz:** Usunięcie produktu z pustego koszyka.
  - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.
- **Scenariusz:** Usunięcie produktu z koszyka, gdy występuje wielokrotnie (sprawdzenie czy ilość się zmniejsza lub produkt jest usuwany całkowicie).
- **Scenariusz:** Usunięcie istniejącego produktu z koszyka.
  - Oczekiwany rezultat: kod 200, odpowiedź JSON z potwierdzeniem usunięcia.
- **Scenariusz:** Usunięcie nieistniejącego produktu z koszyka.
  - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.

---

**Dodatkowe uwagi:**
- Sprawdzaj poprawność obsługi nietypowych danych wejściowych (np. bardzo duże liczby, znaki specjalne).
- Testuj zachowanie sesji (czy koszyk jest unikalny dla każdej sesji testowej).
- Sprawdzaj, czy odpowiedzi nie zawierają zbędnych lub poufnych danych.