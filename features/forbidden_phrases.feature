Feature: Zarządzanie zakazanymi frazami
  Jako administrator systemu
  Chcę zarządzać zakazanymi frazami
  Aby móc zapobiegać nieodpowiednim nazwom produktów

  Background:
    Given API jest dostępne pod adresem "http://localhost:8000"

  Scenario: Utworzenie poprawnej zakazanej frazy
    When tworzę zakazaną frazę "spam"
    Then status odpowiedzi powinien być 201
    And odpowiedź powinna zawierać frazę "spam"
    And zakazana fraza powinna mieć id

  Scenario: Utworzenie zakazanej frazy z pustym stringiem
    When tworzę zakazaną frazę ""
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "phrase"

  Scenario: Utworzenie zakazanej frazy z samymi spacjami
    When tworzę zakazaną frazę "   "
    Then status odpowiedzi powinien być 422
    And odpowiedź powinna zawierać błąd pola "phrase"

  Scenario: Utworzenie duplikującej się zakazanej frazy
    Given utworzyłem zakazaną frazę "spam"
    When tworzę zakazaną frazę "spam"
    Then status odpowiedzi powinien być 400
    And odpowiedź powinna zawierać komunikat błędu o duplikującej się frazie

  Scenario: Pobranie wszystkich zakazanych fraz
    Given utworzyłem zakazaną frazę "spam"
    And utworzyłem zakazaną frazę "adult"
    When pobieram wszystkie zakazane frazy
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać co najmniej 2 frazy
