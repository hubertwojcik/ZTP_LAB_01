Feature: Przykładowa funkcjonalność
  Jako programista
  Chcę przetestować aplikację
  Aby móc zweryfikować że działa poprawnie

  Scenario: Sprawdzenie zdrowia aplikacji
    Given API jest dostępne pod adresem "http://localhost:8000"
    When sprawdzam endpoint health
    Then status odpowiedzi powinien być 200
    And odpowiedź powinna zawierać "healthy"
