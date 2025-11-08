Feature: Zarządzanie kategoriami
  Jako użytkownik systemu
  Chcę zarządzać kategoriami produktów
  Aby móc organizować produkty z ograniczeniami cenowymi

  Background:
    Given API jest dostępne pod adresem "http://localhost:8000"

  Scenario: Utworzenie poprawnej kategorii
    When tworzę kategorię o nazwie "KategoriaTest1_1762595027" opisie "Urządzenia elektroniczne" min_cenie 10.0 max_cenie 5000.0
    Then status odpowiedzi powinien być 201
    And odpowiedź powinna zawierać nazwę kategorii "KategoriaTest1_1762595027"
    And odpowiedź powinna zawierać min_cenę 10.0
    And odpowiedź powinna zawierać max_cenę 5000.0
    And kategoria powinna mieć id

  Scenario: Utworzenie kategorii z nieprawidłową nazwą - pusta
    When tworzę kategorię o nazwie "" opisie "Test" min_cenie 10.0 max_cenie 5000.0
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "name"

  Scenario: Utworzenie kategorii z max_ceną mniejszą niż min_cena
    When tworzę kategorię o nazwie "KategoriaTest3_1762595027" opisie "Test" min_cenie 1000.0 max_cenie 500.0
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "max_price"

  Scenario: Utworzenie kategorii z max_ceną równą min_cenie
    When tworzę kategorię o nazwie "KategoriaTest4_1762595027" opisie "Test" min_cenie 100.0 max_cenie 100.0
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "max_price"

  Scenario: Utworzenie kategorii z duplikującą się nazwą
    Given utworzyłem kategorię o nazwie "KategoriaTest5_1762595027" opisie "Test" min_cenie 10.0 max_cenie 5000.0
    When tworzę kategorię o nazwie "KategoriaTest5_1762595027" opisie "Inny" min_cenie 20.0 max_cenie 6000.0
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o duplikującej się nazwie kategorii

  Scenario: Pobranie wszystkich kategorii
    Given utworzyłem kategorię o nazwie "KategoriaTest7_1762595027" opisie "Test" min_cenie 10.0 max_cenie 5000.0
    And utworzyłem kategorię o nazwie "OdziezTest" opisie "Test" min_cenie 5.0 max_cenie 1000.0
    When pobieram wszystkie kategorie
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 2 kategorie

  Scenario: Pobranie kategorii po ID
    Given utworzyłem kategorię o nazwie "KategoriaTest8_1762595027" opisie "Test" min_cenie 10.0 max_cenie 5000.0
    When pobieram kategorię po id z poprzedniej kategorii
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać nazwę kategorii "KategoriaTest8_1762595027"

  Scenario: Pobranie nieistniejącej kategorii
    When pobieram kategorię po id 99999
    Then status odpowiedzi powinien być 404
