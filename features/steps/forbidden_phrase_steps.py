"""
Definicje kroków dla testów zakazanych fraz
"""
import requests
from behave import given, when, then


@given('utworzyłem zakazaną frazę "{phrase}"')
def step_create_forbidden_phrase_background(context, phrase):
    """Utworzenie zakazanej frazy w kroku tła"""
    step_create_forbidden_phrase(context, phrase)


@when('tworzę zakazaną frazę "{phrase}"')
def step_create_forbidden_phrase(context, phrase):
    """Utworzenie zakazanej frazy przez API"""
    url = f"{context.base_url}/api/v1/forbidden-phrases"
    data = {"phrase": phrase}
    context.response = context.session.post(url, json=data)
    if context.response.status_code == 201:
        context.forbidden_phrase = context.response.json()
        context.forbidden_phrase_id = context.forbidden_phrase['id']
        context.created_forbidden_phrases = getattr(context, 'created_forbidden_phrases', [])
        context.created_forbidden_phrases.append(context.forbidden_phrase)


@when('tworzę zakazaną frazę ""')
def step_create_forbidden_phrase_empty(context):
    """Utworzenie zakazanej frazy z pustym stringiem przez API"""
    url = f"{context.base_url}/api/v1/forbidden-phrases"
    data = {"phrase": ""}
    context.response = context.session.post(url, json=data)
    if context.response.status_code == 201:
        context.forbidden_phrase = context.response.json()
        context.forbidden_phrase_id = context.forbidden_phrase['id']
        context.created_forbidden_phrases = getattr(context, 'created_forbidden_phrases', [])
        context.created_forbidden_phrases.append(context.forbidden_phrase)


@when('pobieram wszystkie zakazane frazy')
def step_get_all_forbidden_phrases(context):
    """Pobranie wszystkich zakazanych fraz przez API"""
    url = f"{context.base_url}/api/v1/forbidden-phrases"
    context.response = context.session.get(url)


@then('odpowiedź powinna zawierać frazę "{phrase}"')
def step_check_phrase(context, phrase):
    """Sprawdzenie frazy w odpowiedzi"""
    data = context.response.json()
    assert data['phrase'] == phrase.strip(), f"Oczekiwano frazy '{phrase}', otrzymano '{data.get('phrase')}'"


@then('zakazana fraza powinna mieć id')
def step_check_forbidden_phrase_has_id(context):
    """Sprawdzenie czy zakazana fraza ma ID"""
    data = context.response.json()
    assert 'id' in data, "Zakazana fraza powinna mieć id"
    assert isinstance(data['id'], int), "Id zakazanej frazy powinno być liczbą całkowitą"


@then('odpowiedź powinna zawierać komunikat błędu o duplikującej się frazie')
def step_check_duplicate_phrase_error(context):
    """Sprawdzenie błędu duplikującej się frazy"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'already exists' in error_msg.lower() or 'duplicate' in error_msg.lower() or 'już istnieje' in error_msg.lower(), \
        f"Oczekiwano błędu duplikującej się frazy, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać co najmniej {count:d} frazy')
def step_check_phrases_count(context, count):
    """Sprawdzenie liczby fraz"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) >= count, f"Oczekiwano co najmniej {count} fraz, otrzymano {len(data)}"
