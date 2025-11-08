"""
Definicje kroków dla testów zarządzania produktami
"""
import requests
from behave import given, when, then
from behave import use_step_matcher
use_step_matcher("parse")
import json


@given('API jest dostępne pod adresem "{url}"')
@given('Zakładając że API jest dostępne pod adresem "{url}"')
def step_api_available(context, url):
    """Ustawienie podstawowego URL dla żądań API"""
    context.base_url = url
    if not hasattr(context, 'session'):
        context.session = requests.Session()


@given('mam kategorię o nazwie "{name}" min_cena {min_price:f} max_cena {max_price:f}')
@given('Zakładając że mam kategorię o nazwie "{name}" min_cena {min_price:f} max_cena {max_price:f}')
def step_create_category(context, name, min_price, max_price):
    """Utworzenie kategorii i zapisanie w kontekście"""
    url = f"{context.base_url}/api/v1/categories"
    data = {
        "name": name,
        "description": f"Opis dla {name}",
        "min_price": min_price,
        "max_price": max_price
    }
    response = context.session.post(url, json=data)
    if response.status_code == 201:
        context.category = response.json()
        context.category_id = context.category['id']
        context.created_categories = getattr(context, 'created_categories', [])
        context.created_categories.append(context.category)
    elif response.status_code == 400 and "already exists" in response.text:
        get_response = context.session.get(f"{context.base_url}/api/v1/categories")
        if get_response.status_code == 200:
            categories = get_response.json()
            for cat in categories:
                if cat['name'] == name:
                    context.category = cat
                    context.category_id = cat['id']
                    break
    else:
        context.response = response


@given('utworzyłem produkt o nazwie "{name}" cenie {price:f} ilości {quantity:d} id_kategorii z poprzedniej kategorii')
def step_create_product_background(context, name, price, quantity):
    """Utworzenie produktu w kroku tła"""
    step_create_product(context, name, price, quantity)
    if hasattr(context, 'product'):
        context.created_products = getattr(context, 'created_products', [])
        context.created_products.append(context.product)


@given('utworzyłem kategorię o nazwie "{name}" opisie "{description}" min_cenie {min_price:f} max_cenie {max_price:f}')
def step_create_category_background(context, name, description, min_price, max_price):
    """Utworzenie kategorii w kroku tła"""
    url = f"{context.base_url}/api/v1/categories"
    data = {
        "name": name,
        "description": description,
        "min_price": min_price,
        "max_price": max_price
    }
    response = context.session.post(url, json=data)
    if response.status_code == 201:
        context.category = response.json()
        context.category_id = context.category['id']
    else:
        get_response = context.session.get(f"{context.base_url}/api/v1/categories")
        if get_response.status_code == 200:
            categories = get_response.json()
            for cat in categories:
                if cat['name'] == name:
                    context.category = cat
                    context.category_id = cat['id']
                    break


@when('tworzę produkt o nazwie "{name}" cenie {price:f} ilości {quantity:d} id_kategorii z poprzedniej kategorii')
def step_create_product(context, name, price, quantity):
    """Utworzenie produktu przez API"""
    url = f"{context.base_url}/api/v1/products"
    category_id = getattr(context, 'category_id', 1)
    data = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "category_id": category_id
    }
    context.response = context.session.post(url, json=data)
    if context.response.status_code == 201:
        context.product = context.response.json()
        context.product_id = context.product['id']


@when('tworzę produkt o nazwie "{name}" cenie {price:f} ilości {quantity:d} id_kategorii {category_id:d}')
def step_create_product_with_category_id(context, name, price, quantity, category_id):
    """Utworzenie produktu z konkretnym ID kategorii"""
    url = f"{context.base_url}/api/v1/products"
    data = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "category_id": category_id
    }
    context.response = context.session.post(url, json=data)


@when('pobieram wszystkie produkty')
def step_get_all_products(context):
    """Pobranie wszystkich produktów przez API"""
    url = f"{context.base_url}/api/v1/products"
    context.response = context.session.get(url)


@when('pobieram produkt po id z poprzedniego produktu')
@then('pobieram produkt po id z poprzedniego produktu')
@given('pobieram produkt po id z poprzedniego produktu')
def step_get_product_by_id(context):
    """Pobranie produktu po ID z poprzedniego produktu"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}"
        context.response = context.session.get(url)


@when('pobieram produkt po id {product_id:d}')
def step_get_product_by_id_number(context, product_id):
    """Pobranie produktu po konkretnym ID"""
    url = f"{context.base_url}/api/v1/products/{product_id}"
    context.response = context.session.get(url)


@when('aktualizuję produkt po id z poprzedniego produktu z ceną {price:f}')
def step_update_product_price(context, price):
    """Aktualizacja ceny produktu"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}"
        data = {"price": price}
        context.response = context.session.put(url, json=data)
        if context.response.status_code == 200:
            context.product = context.response.json()


@when('aktualizuję produkt po id z poprzedniego produktu z nazwą "{name}"')
def step_update_product_name(context, name):
    """Aktualizacja nazwy produktu"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}"
        data = {"name": name}
        context.response = context.session.put(url, json=data)


@when('aktualizuję produkt po id z poprzedniego produktu z ilością {quantity:d}')
def step_update_product_quantity(context, quantity):
    """Aktualizacja ilości produktu"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}"
        data = {"quantity": quantity}
        context.response = context.session.put(url, json=data)
        if context.response.status_code == 200:
            context.product = context.response.json()


@when('usuwam produkt po id z poprzedniego produktu')
def step_delete_product(context):
    """Usunięcie produktu po ID"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}"
        context.response = context.session.delete(url)


@when('usuwam produkt po id {product_id:d}')
def step_delete_product_by_id(context, product_id):
    """Usunięcie produktu po konkretnym ID"""
    url = f"{context.base_url}/api/v1/products/{product_id}"
    context.response = context.session.delete(url)


@then('status odpowiedzi powinien być {status_code:d}')
@then('Wtedy status odpowiedzi powinien być {status_code:d}')
def step_check_status_code(context, status_code):
    """Sprawdzenie kodu statusu HTTP"""
    assert context.response.status_code == status_code, \
        f"Oczekiwano statusu {status_code}, otrzymano {context.response.status_code}. Odpowiedź: {context.response.text}"


@then('odpowiedź powinna zawierać nazwę produktu "{name}"')
def step_check_product_name(context, name):
    """Sprawdzenie nazwy produktu w odpowiedzi"""
    data = context.response.json()
    assert data['name'] == name, f"Oczekiwano nazwy '{name}', otrzymano '{data.get('name')}'"


@then('odpowiedź powinna zawierać cenę produktu {price:f}')
def step_check_product_price(context, price):
    """Sprawdzenie ceny produktu w odpowiedzi"""
    data = context.response.json()
    assert abs(data['price'] - price) < 0.01, f"Oczekiwano ceny {price}, otrzymano {data.get('price')}"


@then('produkt powinien mieć id')
def step_check_product_has_id(context):
    """Sprawdzenie czy produkt ma ID"""
    data = context.response.json()
    assert 'id' in data, "Produkt powinien mieć id"
    assert isinstance(data['id'], int), "Id produktu powinno być liczbą całkowitą"


@then('odpowiedź powinna zawierać błąd pola "{field}"')
def step_check_field_error(context, field):
    """Sprawdzenie błędu walidacji pola"""
    data = context.response.json()
    assert 'detail' in data, "Odpowiedź powinna zawierać pole 'detail'"
    errors = data['detail']
    assert isinstance(errors, list), "Detail powinno być listą"
    
    field_errors = [e for e in errors if 'loc' in e and field in e.get('loc', [])]
    assert len(field_errors) > 0, f"Nie znaleziono błędu dla pola '{field}'. Błędy: {errors}"


@then('odpowiedź powinna zawierać komunikat błędu o zakresie ceny')
def step_check_price_range_error(context):
    """Sprawdzenie błędu walidacji zakresu ceny"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'price' in error_msg.lower() or 'range' in error_msg.lower() or 'between' in error_msg.lower() or 'między' in error_msg.lower(), \
        f"Oczekiwano błędu zakresu ceny, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać komunikat błędu o nieistniejącej kategorii')
def step_check_category_not_found_error(context):
    """Sprawdzenie błędu nieistniejącej kategorii"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'category' in error_msg.lower() and ('not found' in error_msg.lower() or 'not exist' in error_msg.lower() or 'nie znaleziono' in error_msg.lower()), \
        f"Oczekiwano błędu nieistniejącej kategorii, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać komunikat błędu o duplikującej się nazwie')
def step_check_duplicate_name_error(context):
    """Sprawdzenie błędu duplikującej się nazwy"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'already exists' in error_msg.lower() or 'duplicate' in error_msg.lower() or 'już istnieje' in error_msg.lower(), \
        f"Oczekiwano błędu duplikującej się nazwy, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać komunikat błędu o zakazanej frazie')
def step_check_forbidden_phrase_error(context):
    """Sprawdzenie błędu zakazanej frazy"""
    data = context.response.json()
    error_msg = data.get('detail', '')
    assert 'forbidden' in error_msg.lower() or 'zakazana' in error_msg.lower(), \
        f"Oczekiwano błędu zakazanej frazy, otrzymano: {error_msg}"


@then('odpowiedź powinna zawierać co najmniej {count:d} produkty')
def step_check_products_count(context, count):
    """Sprawdzenie liczby produktów"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) >= count, f"Oczekiwano co najmniej {count} produktów, otrzymano {len(data)}"


@when('sprawdzam endpoint health')
@when('Gdy sprawdzam endpoint health')
def step_check_health(context):
    """Sprawdzenie endpointu health aplikacji"""
    url = f"{context.base_url}/health"
    context.response = context.session.get(url)


@then('odpowiedź powinna zawierać "{text}"')
@then('Wtedy odpowiedź powinna zawierać "{text}"')
@then('I odpowiedź powinna zawierać "{text}"')
def step_check_response_contains(context, text):
    """Sprawdzenie czy odpowiedź zawiera tekst"""
    response_text = context.response.text
    assert text in response_text, f"Oczekiwano '{text}' w odpowiedzi, otrzymano: {response_text}"
