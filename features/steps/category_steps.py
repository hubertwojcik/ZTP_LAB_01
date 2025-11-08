"""
Definicje kroków dla testów zarządzania kategoriami
"""
import requests
from behave import given, when, then


@when('tworzę kategorię o nazwie "{name}" opisie "{description}" min_cenie {min_price:f} max_cenie {max_price:f}')
def step_create_category(context, name, description, min_price, max_price):
    """Utworzenie kategorii przez API"""
    url = f"{context.base_url}/api/v1/categories"
    data = {
        "name": name,
        "description": description,
        "min_price": min_price,
        "max_price": max_price
    }
    context.response = context.session.post(url, json=data)
    if context.response.status_code == 201:
        context.category = context.response.json()
        context.category_id = context.category['id']
        context.created_categories = getattr(context, 'created_categories', [])
        context.created_categories.append(context.category)


@when('tworzę kategorię o nazwie "" opisie "{description}" min_cenie {min_price:f} max_cenie {max_price:f}')
def step_create_category_empty_name(context, description, min_price, max_price):
    """Utworzenie kategorii z pustą nazwą przez API"""
    url = f"{context.base_url}/api/v1/categories"
    data = {
        "name": "",
        "description": description,
        "min_price": min_price,
        "max_price": max_price
    }
    context.response = context.session.post(url, json=data)
    if context.response.status_code == 201:
        context.category = context.response.json()
        context.category_id = context.category['id']
        context.created_categories = getattr(context, 'created_categories', [])
        context.created_categories.append(context.category)


@when('pobieram wszystkie kategorie')
def step_get_all_categories(context):
    """Pobranie wszystkich kategorii przez API"""
    url = f"{context.base_url}/api/v1/categories"
    context.response = context.session.get(url)


@when('pobieram kategorię po id z poprzedniej kategorii')
def step_get_category_by_id(context):
    """Pobranie kategorii po ID z poprzedniej kategorii"""
    category_id = getattr(context, 'category_id', None)
    if category_id:
        url = f"{context.base_url}/api/v1/categories/{category_id}"
        context.response = context.session.get(url)


@when('pobieram kategorię po id {category_id:d}')
def step_get_category_by_id_number(context, category_id):
    """Pobranie kategorii po konkretnym ID"""
    url = f"{context.base_url}/api/v1/categories/{category_id}"
    context.response = context.session.get(url)


@then('odpowiedź powinna zawierać nazwę kategorii "{name}"')
def step_check_category_name(context, name):
    """Sprawdzenie nazwy kategorii w odpowiedzi"""
    data = context.response.json()
    assert data['name'] == name, f"Oczekiwano nazwy '{name}', otrzymano '{data.get('name')}'"


@then('odpowiedź powinna zawierać min_cenę {min_price:f}')
def step_check_min_price(context, min_price):
    """Sprawdzenie min_ceny w odpowiedzi"""
    data = context.response.json()
    assert abs(data['min_price'] - min_price) < 0.01, \
        f"Oczekiwano min_ceny {min_price}, otrzymano {data.get('min_price')}"


@then('odpowiedź powinna zawierać max_cenę {max_price:f}')
def step_check_max_price(context, max_price):
    """Sprawdzenie max_ceny w odpowiedzi"""
    data = context.response.json()
    assert abs(data['max_price'] - max_price) < 0.01, \
        f"Oczekiwano max_ceny {max_price}, otrzymano {data.get('max_price')}"


@then('kategoria powinna mieć id')
def step_check_category_has_id(context):
    """Sprawdzenie czy kategoria ma ID"""
    data = context.response.json()
    assert 'id' in data, "Kategoria powinna mieć id"
    assert isinstance(data['id'], int), "Id kategorii powinno być liczbą całkowitą"


@then('odpowiedź powinna zawierać komunikat błędu o duplikującej się nazwie kategorii')
def step_check_duplicate_category_error(context):
    """Sprawdzenie błędu duplikującej się nazwy kategorii"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'already exists' in error_msg.lower() or 'duplicate' in error_msg.lower() or 'już istnieje' in error_msg.lower(), \
        f"Oczekiwano błędu duplikującej się nazwy kategorii, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać co najmniej {count:d} kategorie')
def step_check_categories_count(context, count):
    """Sprawdzenie liczby kategorii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) >= count, f"Oczekiwano co najmniej {count} kategorii, otrzymano {len(data)}"
