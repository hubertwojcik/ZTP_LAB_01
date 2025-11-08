"""
Definicje kroków dla testów historii zmian
"""
import requests
from behave import when, then, given


@given('pobieram id produktu z poprzedniego produktu')
def step_store_product_id(context):
    """Zapisanie ID produktu do późniejszego użycia"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        context.stored_product_id = product_id


@when('pobieram historię produktu dla id z poprzedniego produktu')
def step_get_product_history(context):
    """Pobranie historii zmian produktu"""
    product_id = getattr(context, 'product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}/history"
        context.response = context.session.get(url)


@when('pobieram historię produktu dla id {product_id:d}')
def step_get_product_history_by_id(context, product_id):
    """Pobranie historii zmian produktu po konkretnym ID"""
    url = f"{context.base_url}/api/v1/products/{product_id}/history"
    context.response = context.session.get(url)


@when('pobieram historię produktu dla id z zapisanego id produktu')
def step_get_product_history_stored(context):
    """Pobranie historii zmian produktu używając zapisanego ID produktu"""
    product_id = getattr(context, 'stored_product_id', None)
    if product_id:
        url = f"{context.base_url}/api/v1/products/{product_id}/history"
        context.response = context.session.get(url)


@then('odpowiedź powinna zawierać co najmniej {count:d} wpis w historii')
def step_check_audit_records_count(context, count):
    """Sprawdzenie liczby wpisów w historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) >= count, f"Oczekiwano co najmniej {count} wpisów w historii, otrzymano {len(data)}"


@then('wpis w historii powinien mieć typ_zmiany "{change_type}"')
def step_check_audit_change_type(context, change_type):
    """Sprawdzenie typu zmiany w wpisie historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) > 0, "Nie znaleziono wpisów w historii"
    
    change_types = [record.get('change_type') for record in data]
    assert change_type in change_types, \
        f"Oczekiwano typ_zmiany '{change_type}', znaleziono: {change_types}"


@then('odpowiedź powinna zawierać co najmniej {count:d} wpis w historii z typem_zmiany "{change_type}"')
def step_check_audit_records_with_type(context, count, change_type):
    """Sprawdzenie liczby wpisów w historii z konkretnym typem zmiany"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    
    matching_records = [r for r in data if r.get('change_type') == change_type]
    assert len(matching_records) >= count, \
        f"Oczekiwano co najmniej {count} wpisów z typem_zmiany '{change_type}', otrzymano {len(matching_records)}"


@then('wpis w historii powinien mieć nazwę_pola "{field_name}"')
def step_check_audit_field_name(context, field_name):
    """Sprawdzenie nazwy pola w wpisie historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    
    field_names = [record.get('field_name') for record in data]
    assert field_name in field_names, \
        f"Oczekiwano nazwy_pola '{field_name}', znaleziono: {field_names}"


@then('wpis w historii powinien mieć starą_wartość "{old_value}"')
def step_check_audit_old_value(context, old_value):
    """Sprawdzenie starej wartości w wpisie historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    
    old_values = [str(record.get('old_value', '')) for record in data]
    assert old_value in old_values, \
        f"Oczekiwano starej_wartości '{old_value}', znaleziono: {old_values}"


@then('wpis w historii powinien mieć nową_wartość "{new_value}"')
def step_check_audit_new_value(context, new_value):
    """Sprawdzenie nowej wartości w wpisie historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    
    new_values = [str(record.get('new_value', '')) for record in data]
    assert new_value in new_values, \
        f"Oczekiwano nowej_wartości '{new_value}', znaleziono: {new_values}"


@then('odpowiedź powinna zawierać co najmniej {count:d} wpisy w historii')
def step_check_multiple_audit_records(context, count):
    """Sprawdzenie wielu wpisów w historii"""
    data = context.response.json()
    assert isinstance(data, list), "Odpowiedź powinna być listą"
    assert len(data) >= count, f"Oczekiwano co najmniej {count} wpisów w historii, otrzymano {len(data)}"
