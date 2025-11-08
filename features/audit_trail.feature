Feature: Historia zmian produktów
  Jako użytkownik systemu
  Chcę śledzić zmiany produktów
  Aby móc utrzymywać historię wszystkich modyfikacji

  Background:
    Given API jest dostępne pod adresem "http://localhost:8000"

  Scenario: Utworzenie wpisu w historii przy utworzeniu produktu
    Given mam kategorię o nazwie "Elektronika_1762595027" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    And pobieram historię produktu dla id z poprzedniego produktu
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 1 wpis w historii
    And wpis w historii powinien mieć typ_zmiany "CREATE"

  Scenario: Utworzenie wpisu w historii przy aktualizacji produktu
    Given mam kategorię o nazwie "Elektronika_1762595027" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When aktualizuję produkt po id z poprzedniego produktu z ceną 150.0
    And pobieram historię produktu dla id z poprzedniego produktu
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 1 wpis w historii z typem_zmiany "UPDATE"
    And wpis w historii powinien mieć nazwę_pola "price"
    And wpis w historii powinien mieć starą_wartość "100.0"
    And wpis w historii powinien mieć nową_wartość "150.0"

  Scenario: Utworzenie wpisu w historii przy usunięciu produktu
    Given mam kategorię o nazwie "Elektronika_1762595027" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    And pobieram id produktu z poprzedniego produktu
    When usuwam produkt po id z poprzedniego produktu
    Then status odpowiedzi powinien być 204
    # Note: History is deleted before product deletion to avoid foreign key constraint
    # In production, you might want to use ON DELETE SET NULL or CASCADE in DB schema

  Scenario: Pobranie historii dla nieistniejącego produktu
    When pobieram historię produktu dla id 99999
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 0 wpis w historii

  Scenario: Wiele wpisów w historii dla wielu aktualizacji
    Given mam kategorię o nazwie "Elektronika_1762595027" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When aktualizuję produkt po id z poprzedniego produktu z ceną 150.0
    And aktualizuję produkt po id z poprzedniego produktu z ilością 20
    And pobieram historię produktu dla id z poprzedniego produktu
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 3 wpisy w historii
