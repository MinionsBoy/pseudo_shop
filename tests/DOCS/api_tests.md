## 1. Lista produktów

- **GET `/api/products`**
  - Oczekiwany rezultat: kod 200, odpowiedź w formacie JSON.
  - Liczba elementów w odpowiedzi odpowiada liczbie produktów w liście `products` w aplikacji.
  - Każdy produkt ma wymagane pola (`id`, `name`, `price`, `description` ...).
  - Przykład testu: `response = client.get('/api/products')` i sprawdzenie długości listy oraz pól.

## 2. Szczegóły produktu

- **GET `/api/products/2`**
  - Oczekiwany rezultat: kod 200, odpowiedź JSON z danymi produktu o id=2.
  - Sprawdź poprawność pól produktu.
- **GET `/api/products/<nieistniejący_id>`**
  - Oczekiwany rezultat: kod 404, odpowiedź JSON z komunikatem o błędzie.

## 3. Dodawanie do koszyka

- **POST `/api/cart`** z ciałem `{'product_id': 3}`
  - Oczekiwany rezultat: kod 201, odpowiedź JSON z komunikatem o dodaniu.
  - Po dodaniu kilku produktów, `GET /api/cart` powinien zwracać listę elementów z odpowiednimi ilościami i polem `total` równym sumie cen.
- **POST `/api/cart`** bez pola `product_id`
  - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.
- **POST `/api/cart`** z nieprawidłowym typem `product_id`
  - Oczekiwany rezultat: kod 400, odpowiedź JSON z informacją o błędzie.
- **POST `/api/cart`** z id spoza listy produktów
  - Oczekiwany rezultat: kod 404, odpowiedź JSON z informacją o błędzie.

## 4. Przegląd koszyka

- **GET `/api/cart`**
  - Oczekiwany rezultat: kod 200, odpowiedź JSON z aktualnym stanem koszyka.
  - Zawiera listę produktów, ilości oraz pole `total` z sumą cen.

## Uwagi

- W testach API korzystaj z parametrów `follow_redirects` i `json` klienta testowego Flask.
- Sprawdzaj nagłówki odpowiedzi (`Content-Type: application/json`).
- Testuj przypadki brzegowe (pusty koszyk, wielokrotne dodanie tego samego produktu).
