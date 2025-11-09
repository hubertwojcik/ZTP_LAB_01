# ZTP LAB 01 - System Zarządzania Produktami

## 📋 O Projekcie

System zarządzania produktami zbudowany w **FastAPI** z bazą danych **PostgreSQL**. Projekt implementuje pełny CRUD dla produktów i kategorii, z automatycznym śledzeniem zmian (audit trail) oraz walidacją zawartości (zakazane frazy).

### Główne Funkcjonalności

✅ **Zarządzanie Produktami** - CRUD z walidacją nazwy, ceny, ilości  
✅ **Zarządzanie Kategoriami** - Kategorie z zakresami cenowymi  
✅ **Zakazane Frazy** - Moderacja treści w nazwach produktów  
✅ **Audit Trail** - Automatyczne logowanie wszystkich zmian produktów  
✅ **Walidacja Biznesowa** - Sprawdzanie zakresów cenowych, unikalności, formatów  
✅ **Testy BDD** - Kompleksowe testy integracyjne z frameworkiem Behave

---

## 🏗️ Struktura Projektu

```
.
├── src/                          # Kod źródłowy aplikacji
│   ├── api/                      # Endpointy REST API
│   │   ├── products.py          # Endpointy produktów
│   │   ├── product_category.py  # Endpointy kategorii
│   │   ├── forbidden_phrases.py # Endpointy zakazanych fraz
│   │   └── product_audit.py     # Endpointy historii zmian
│   ├── models/                   # Modele SQLAlchemy (baza danych)
│   │   ├── product.py
│   │   ├── product_category.py
│   │   ├── forbidden_phrase.py
│   │   └── product_audit.py
│   ├── schemas/                  # Schematy Pydantic (walidacja)
│   ├── repositories/             # Warstwa dostępu do danych
│   ├── services/                 # Logika biznesowa
│   ├── main.py                   # Punkt wejścia FastAPI
│   ├── config.py                 # Konfiguracja
│   └── database.py               # Połączenie z bazą danych
│
├── features/                      # Testy BDD (Behave)
│   ├── product_management.feature
│   ├── category_management.feature
│   ├── forbidden_phrases.feature
│   ├── audit_trail.feature
│   └── steps/                    # Implementacje kroków testowych
│
├── alembic/                      # Migracje bazy danych
├── docker-compose.yml            # Konfiguracja Docker Compose
├── Dockerfile                    # Obraz Docker dla aplikacji
├── Makefile                      # Przydatne komendy
└── requirements.txt              # Zależności Python
```

---

## 🚀 Szybki Start

### Pierwsza Instalacja

```bash
# 1. Pełna inicjalizacja (czyści, buduje, uruchamia, migruje)
make init

# 2. Uruchom testy
make test
```

### Podstawowe Komendy

```bash
make up      # Uruchom serwisy (PostgreSQL + FastAPI)
make down    # Zatrzymaj serwisy
make logs    # Zobacz logi
make test    # Uruchom testy integracyjne
make clean   # Wyczyść wszystko (wolumeny, cache)
```

### Dostęp do Aplikacji

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📍 Gdzie Co Znajduje Się?

### **API Endpointy** (`src/api/`)

- `products.py` - Operacje na produktach (GET, POST, PUT, DELETE)
- `product_category.py` - Operacje na kategoriach
- `forbidden_phrases.py` - Zarządzanie zakazanymi frazami
- `product_audit.py` - Historia zmian produktów

### **Modele Bazy Danych** (`src/models/`)

- `product.py` - Tabela produktów (id, name, price, quantity, category_id)
- `product_category.py` - Tabela kategorii (name, min_price, max_price)
- `forbidden_phrase.py` - Tabela zakazanych fraz
- `product_audit.py` - Tabela historii zmian (audit trail)

### **Logika Biznesowa** (`src/services/`)

- `product_service.py` - Walidacja, tworzenie, aktualizacja produktów
  - Sprawdzanie zakazanych fraz w nazwach
  - Walidacja zakresów cenowych kategorii
  - Automatyczne logowanie zmian do audit trail

### **Testy** (`features/`)

- `product_management.feature` - Testy CRUD produktów
- `category_management.feature` - Testy kategorii
- `forbidden_phrases.feature` - Testy moderacji treści
- `audit_trail.feature` - Testy historii zmian

### **Migracje** (`alembic/`)

- `versions/` - Pliki migracji bazy danych
- `env.py` - Konfiguracja Alembic

---

## 🔑 Kluczowe Funkcjonalności do Opisania

### 1. **Walidacja Produktów**

- Nazwa: 3-100 znaków, unikalna, bez zakazanych fraz
- Cena: dodatnia, w zakresie kategorii (min_price - max_price)
- Ilość: nieujemna liczba całkowita
- Kategoria: musi istnieć w bazie

### 2. **Audit Trail**

- Automatyczne logowanie: CREATE, UPDATE, DELETE
- Przechowywanie: stara wartość, nowa wartość, timestamp, typ operacji
- Dostęp przez API: `/api/v1/products/{id}/history`

### 3. **Zakazane Frazy**

- Lista fraz niedozwolonych w nazwach produktów
- Sprawdzanie przy tworzeniu i aktualizacji
- Zwraca błąd 400 z informacją o znalezionej frazie

### 4. **Architektura**

- **3-warstwowa**: API → Service → Repository
- **Repository Pattern** - izolacja dostępu do danych
- **Service Layer** - logika biznesowa i walidacja
- **Dependency Injection** - FastAPI Depends()

---

## 🧪 Testy

Projekt zawiera kompleksowe testy integracyjne używające **Behave (BDD)**:

```bash
make test  # Uruchom wszystkie testy
```

Testy sprawdzają:

- ✅ Wszystkie operacje CRUD
- ✅ Walidację danych wejściowych
- ✅ Działanie zakazanych fraz
- ✅ Audit trail (historia zmian)
- ✅ Walidację zakresów cenowych

---

## 🛠️ Technologie

- **FastAPI** - Framework webowy
- **PostgreSQL** - Baza danych
- **SQLAlchemy** - ORM
- **Pydantic** - Walidacja danych
- **Alembic** - Migracje bazy danych
- **Docker & Docker Compose** - Konteneryzacja
- **Behave** - Testy BDD

---

## 📝 Przykłady Użycia API

### Utworzenie Kategorii

```bash
POST /api/v1/categories
{
  "name": "Elektronika",
  "description": "Urządzenia elektroniczne",
  "min_price": 10.0,
  "max_price": 5000.0
}
```

### Utworzenie Produktu

```bash
POST /api/v1/products
{
  "name": "Laptop2024",
  "price": 1299.99,
  "quantity": 50,
  "category_id": 1
}
```

### Historia Zmian Produktu

```bash
GET /api/v1/products/1/history
```

---

## 💡 Jak Opowiedzieć o Projekcie?

1. **Co to jest?** - System zarządzania produktami z REST API
2. **Architektura** - 3-warstwowa (API, Service, Repository), FastAPI + PostgreSQL
3. **Funkcjonalności** - CRUD, walidacja, audit trail, moderacja treści
4. **Testy** - Kompleksowe testy BDD pokrywające wszystkie wymagania
5. **Docker** - Pełna konteneryzacja, łatwe uruchomienie jednym poleceniem
6. **Jakość kodu** - Separacja odpowiedzialności, dependency injection, wzorce projektowe

---

## 🔧 Rozwiązywanie Problemów

```bash
# Aplikacja nie startuje
make logs      # Sprawdź logi
make restart   # Zrestartuj

# Problemy z bazą danych
make down      # Zatrzymaj wszystko
make up        # Uruchom od nowa

# Pełny reset
make clean     # Usuń wolumeny i cache
make build     # Przebuduj obrazy
make up        # Uruchom
```
