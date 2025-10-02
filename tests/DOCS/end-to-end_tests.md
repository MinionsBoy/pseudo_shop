# Scenariusze testów E2E (end-to-end) – pseudo_shop

Poniższe scenariusze można zaimplementować np. w Selenium lub innym narzędziu E2E. Każdy z nich symuluje zachowanie prawdziwego użytkownika w przeglądarce.

---

## 1. Wyświetlanie strony głównej

- Otwórz stronę główną `http://localhost:5000/`.
- Sprawdź, czy tytuł strony jest zgodny z oczekiwanym.
- Sprawdź, czy na stronie wyświetlana jest lista produktów.
- Zweryfikuj, czy liczba produktów odpowiada liczbie w bazie/aplikacji.

## 2. Przegląd produktu

- Na stronie głównej kliknij w link „Szczegóły” przy wybranym produkcie.
- Sprawdź, czy otwarta została strona szczegółów produktu.
- Zweryfikuj, czy wyświetlany jest prawidłowy opis i cena produktu.

## 3. Dodawanie do koszyka

- Na stronie szczegółów produktu kliknij przycisk „Dodaj do koszyka”.
- Sprawdź, czy nastąpiło przekierowanie do koszyka.
- Zweryfikuj, czy liczba pozycji w koszyku zwiększyła się o 1.

## 4. Usuwanie z koszyka

- W koszyku kliknij przycisk „Usuń” przy wybranym produkcie.
- Sprawdź, czy ilość danego produktu w koszyku się zmniejszyła lub produkt został całkowicie usunięty (jeśli ilość spadła do zera).

## 5. Nawigacja

- W koszyku kliknij link „Kontynuuj zakupy”.
- Sprawdź, czy nastąpiło przekierowanie z powrotem na stronę główną.

---

## Dobre praktyki przy pisaniu testów E2E

- **Używaj explicit waits** – czekaj na pojawienie się elementów zamiast używać `sleep()`.
- **Stosuj wytrzymałe selektory** – preferuj `id` lub `name`, unikaj złożonych `xpath`/`cssSelector`.
- **Stosuj asercje** – weryfikuj tytuły stron, obecność elementów, zmiany adresu URL.
- **Parametryzuj testy i porządkuj je w zestawy** – ułatwia to uruchamianie różnych wariantów.
- **Dbaj o cleanup** – zamykaj przeglądarkę po każdym teście.
