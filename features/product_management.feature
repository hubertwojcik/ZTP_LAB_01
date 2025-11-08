Feature: Zarządzanie produktami
  Jako użytkownik systemu
  Chcę zarządzać produktami
  Aby móc utrzymywać katalog produktów z odpowiednią walidacją

  Background:
    Given API jest dostępne pod adresem "http://localhost:8000"

  Scenario: Utworzenie poprawnego produktu
    Given mam kategorię o nazwie "ElektronikaTest1" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop2024Test1" cenie 1299.99 ilości 50 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 201
    And odpowiedź powinna zawierać nazwę produktu "Laptop2024Test1"
    And odpowiedź powinna zawierać cenę produktu 1299.99
    And produkt powinien mieć id

  Scenario: Utworzenie produktu z nieprawidłową nazwą - za krótka
    Given mam kategorię o nazwie "ElektronikaTest2" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "AB" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "name"

  Scenario: Utworzenie produktu z nieprawidłową nazwą - zawiera znaki specjalne
    Given mam kategorię o nazwie "ElektronikaTest3" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop-2024" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "name"

  Scenario: Utworzenie produktu z nieprawidłową ceną - ujemna
    Given mam kategorię o nazwie "ElektronikaTest1" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop2024Test" cenie -10.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "price"

  Scenario: Utworzenie produktu z nieprawidłową ceną - zero
    Given mam kategorię o nazwie "ElektronikaTest2" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop2024Test" cenie 0.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "price"

  Scenario: Utworzenie produktu z nieprawidłową ilością - ujemna
    Given mam kategorię o nazwie "ElektronikaTest3" min_cena 10.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop2024Test" cenie 100.0 ilości -5 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "quantity"

  Scenario: Utworzenie produktu z ceną poniżej minimum kategorii
    Given mam kategorię o nazwie "ElektronikaTest4" min_cena 100.0 max_cena 5000.0
    When tworzę produkt o nazwie "Laptop2024Test" cenie 50.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o zakresie ceny

  Scenario: Utworzenie produktu z ceną powyżej maksimum kategorii
    Given mam kategorię o nazwie "ElektronikaTest5" min_cena 10.0 max_cena 1000.0
    When tworzę produkt o nazwie "Laptop2024Test" cenie 2000.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o zakresie ceny

  Scenario: Utworzenie produktu z nieistniejącą kategorią
    When tworzę produkt o nazwie "Laptop2024Test" cenie 100.0 ilości 10 id_kategorii 99999
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o nieistniejącej kategorii

  Scenario: Utworzenie produktu z duplikującą się nazwą
    Given mam kategorię o nazwie "ElektronikaTest6" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "UnikalnyProduktTest" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When tworzę produkt o nazwie "UnikalnyProduktTest" cenie 200.0 ilości 20 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o duplikującej się nazwie

  Scenario: Utworzenie produktu z zakazaną frazą w nazwie
    Given mam kategorię o nazwie "ElektronikaTest7" min_cena 10.0 max_cena 5000.0
    And utworzyłem zakazaną frazę "spam"
    When tworzę produkt o nazwie "SpamProduktTest" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o zakazanej frazie

  Scenario: Pobranie wszystkich produktów
    Given mam kategorię o nazwie "ElektronikaTest8" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    And utworzyłem produkt o nazwie "Produkt2Test" cenie 200.0 ilości 20 id_kategorii z poprzedniej kategorii
    When pobieram wszystkie produkty
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 2 produkty

  Scenario: Pobranie produktu po ID
    Given mam kategorię o nazwie "ElektronikaTest9" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When pobieram produkt po id z poprzedniego produktu
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać nazwę produktu "Produkt1Test"

  Scenario: Pobranie nieistniejącego produktu
    When pobieram produkt po id 99999
    Then status odpowiedzi powinien być 404

  Scenario: Aktualizacja produktu z powodzeniem
    Given mam kategorię o nazwie "ElektronikaTest10" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When aktualizuję produkt po id z poprzedniego produktu z ceną 150.0
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać cenę produktu 150.0

  Scenario: Aktualizacja produktu z nieprawidłowymi danymi
    Given mam kategorię o nazwie "ElektronikaTest11" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When aktualizuję produkt po id z poprzedniego produktu z ceną -10.0
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "price"

  Scenario: Aktualizacja produktu z duplikującą się nazwą
    Given mam kategorię o nazwie "ElektronikaTest12" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    And utworzyłem produkt o nazwie "Produkt2Test" cenie 200.0 ilości 20 id_kategorii z poprzedniej kategorii
    When aktualizuję produkt po id z poprzedniego produktu z nazwą "Produkt1Test"
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o duplikującej się nazwie

  Scenario: Usunięcie produktu z powodzeniem
    Given mam kategorię o nazwie "ElektronikaTest13" min_cena 10.0 max_cena 5000.0
    And utworzyłem produkt o nazwie "Produkt1Test" cenie 100.0 ilości 10 id_kategorii z poprzedniej kategorii
    When usuwam produkt po id z poprzedniego produktu
    Then status odpowiedzi powinien być 204
    And pobieram produkt po id z poprzedniego produktu
    Then status odpowiedzi powinien być 404

  Scenario: Usunięcie nieistniejącego produktu
    When usuwam produkt po id 99999
    Then status odpowiedzi powinien być 404
