# E-Commerce UI & API Automation Framework

An industry-standard, GitHub-ready test automation framework engineered in Python, leveraging **Playwright** via the official **`pytest-playwright`** plugin for UI testing, **Requests** for REST API testing, and **Pytest** for test execution, CLI configuration, and fixture orchestration.

The framework is tailored for [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com/), demonstrating complete end-to-end coverage across user registration, authentication, catalog search/filter, shopping cart lifecycle, and multi-step checkout.

---

## Table of Contents
1. [Overview](#overview)
2. [Why Playwright Built-in Fixtures & API Automation?](#why-playwright-built-in-fixtures--api-automation)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Executing Tests & CLI Flags](#executing-tests--cli-flags)
7. [Framework Architecture](#framework-architecture)
8. [CI/CD Pipeline (GitHub Actions)](#cicd-pipeline-github-actions)
9. [Test Coverage Matrix](#test-coverage-matrix)
10. [Reporting, Traces & Failure Screenshots](#reporting-traces--failure-screenshots)

---

## Overview

The purpose of this framework is to provide a clean, production-grade test suite that:
- Uses the official **`pytest-playwright` built-in `page` fixture** directly, allowing standard CLI flags (`--tracing`, `--video`, `--screenshot`, `--browser`, `--headed`) to control browser behavior without touching test code.
- Automates critical customer journeys on the web application following the **Page Object Model (POM)** with a dedicated **Locators** layer.
- Validates backend REST API endpoints directly for contract, payload, and status correctness.
- Bridges UI and API layers through seamless **Integration Tests** (e.g., seeding users via API, authenticating via UI).
- Includes an automated **GitHub Actions CI/CD workflow** for continuous regression testing on every push and pull request.

---

## Why Playwright Built-in Fixtures & API Automation?

- **Why Built-in `pytest-playwright` Fixtures?**
  - **Zero Hardcoded Tracing/Browser Code:** Tracing, video, and screenshot capture are configured externally in `pytest.ini` or passed via CLI flags (e.g., `--tracing=retain-on-failure`, `--tracing=on`, `--tracing=off`), ensuring tests remain pure business logic.
  - **Native Auto-Waiting:** Playwright automatically waits for elements to become visible, enabled, and stable before performing actions, eliminating flaky `time.sleep()` calls.
  - **Automatic Browser Isolation:** Each test receives a brand new browser context and page, preventing cookie or session leaks.
- **Why Include API Automation?**
  - **Fast Feedback Loop:** API tests execute in milliseconds, validating core business logic, schema requirements, and authentication immediately.
  - **Test Setup Acceleration:** Enables rapid test data creation (such as customer accounts and shopping carts) for complex UI scenarios.

---

## Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **UI Automation** | Playwright (`pytest-playwright`) | Browser engine using built-in `page` fixture |
| **API Automation** | Requests | HTTP client for RESTful services |
| **Test Runner** | Pytest | Test discovery, parametrization, and fixtures |
| **Design Pattern** | Page Object Model (POM) | Clean separation of UI actions and selectors |
| **Selector Layer** | Dedicated Locators Package | Centralized locator definitions |
| **Reporting** | pytest-html | Self-contained HTML test execution reports |
| **CI/CD** | GitHub Actions | Automated regression pipeline on push and PR |
| **Test Data** | JSON & Dynamic Generators | Decoupled static and dynamic data payloads |

---

## Project Structure

```text
ecommerce-automation/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI/CD pipeline
├── api/                        # Specialized REST API client classes
│   ├── base_api.py             # Reusable HTTP wrapper (Session, methods, logging)
│   ├── product_api.py          # Products, search, categories, and brands API
│   ├── user_api.py             # User profile and registration API
│   ├── auth_api.py             # Authentication and JWT token API
│   └── order_api.py            # Cart and invoice management API
├── fixtures/                   # Pytest fixture definitions
│   ├── ui_fixtures.py          # POM fixtures taking the built-in page fixture
│   └── api_fixtures.py         # API client fixtures, dynamic user setup
├── locators/                   # Centralized element selectors (Separation of Concerns)
│   ├── home_locators.py        # Header, search, sort, and product cards
│   ├── login_locators.py       # Login form and error banners
│   ├── registration_locators.py# Registration form inputs and validation errors
│   ├── product_locators.py     # Product details, pricing, counter, add to cart
│   ├── cart_locators.py        # Cart table, row items, delete, quantity
│   └── checkout_locators.py    # Multi-step checkout wizard and payment
├── pages/                      # Page Object Model (POM) action classes
│   ├── base_page.py            # Base page with Playwright wrapper methods
│   ├── home_page.py            # Home page interactions and navigation
│   ├── login_page.py           # Login workflows
│   ├── registration_page.py    # User registration workflows
│   ├── product_page.py         # Product detail actions
│   ├── cart_page.py            # Cart adjustments and calculations
│   └── checkout_page.py        # Wizard steps and order placement
├── reports/                    # Execution artifacts
│   ├── report.html             # Self-contained HTML report
│   ├── execution.log           # Framework runtime log
│   └── screenshots/
│       ├── failures/           # Auto-captured screenshots on UI failures
│       └── passed/             # Optional success captures
├── test_data/                  # Static test data in JSON format
│   ├── users.json              # Credentials and user templates
│   ├── products.json           # Catalog items, search terms, and filters
│   └── test_data.json          # Application URLs and navigation routes
├── tests/                      # Test suites organized by layer
│   ├── ui/                     # UI test cases (Playwright)
│   │   ├── test_home.py        # Title, header navigation, categories
│   │   ├── test_search.py      # Search, no-results, reset, edge cases
│   │   ├── test_products.py    # Product details, quantity counters, sorting
│   │   ├── test_cart.py        # Add to cart, update quantity, delete item
│   │   ├── test_login.py       # Valid/invalid login, logout, validations
│   │   ├── test_registration.py# Registration and form validation
│   │   └── test_checkout.py    # Complete multi-step checkout
│   ├── api/                    # API test cases (Requests)
│   │   ├── test_products_api.py# Products list, search, pagination, categories
│   │   ├── test_auth_api.py    # Auth login, token validation, logout
│   │   ├── test_users_api.py   # Register user, duplicates, profile /users/me
│   │   └── test_orders_api.py  # Cart lifecycle and invoice endpoints
│   └── integration/            # UI + API Integration tests
│       └── test_ui_api_integration.py # API seed -> UI login & checkout
├── utils/                      # Utilities
│   ├── config.py               # Central environment and URL configuration
│   ├── helpers.py              # Dynamic data generator, price parser
│   └── logger.py               # Framework logging with console and file handlers
├── conftest.py                 # Root conftest: hooks, failure screenshots
├── pytest.ini                  # Pytest configuration, addopts, markers
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

---

## Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone the repository
```bash
git clone <repository-url>
cd softwaretesting
```

### 2. Create and activate a Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browser binaries
```bash
playwright install chromium
```

---

## Executing Tests & CLI Flags

The framework is configured via `pytest.ini`'s `addopts` to use Playwright's native CLI options:

```ini
[pytest]
addopts =
    -ra
    --strict-markers
    --browser chromium
    --tracing retain-on-failure
    --screenshot only-on-failure
    --html=reports/report.html
    --self-contained-html
    --base-url=https://practicesoftwaretesting.com
```

### Run all tests
```bash
pytest
```

### Control Tracing via CLI (No code changes needed)
```bash
# Keep traces only when tests fail (default via pytest.ini)
pytest --tracing retain-on-failure

# Force trace recording for every test run
pytest --tracing on

# Turn off trace recording
pytest --tracing off
```

### View Saved Playwright Traces
When a test fails (or when `--tracing on` is passed), trace zip files are saved under `test-results/`. Inspect them with:
```bash
playwright show-trace test-results/<folder-name>/trace.zip
```

### Control Screenshots and Videos via CLI
```bash
# Capture screenshots only on failure (default)
pytest --screenshot only-on-failure

# Capture full-page screenshots on failure
pytest --full-page-screenshot

# Record video on failure
pytest --video retain-on-failure
```

### Run Specific Test Suites Using Markers
```bash
# Run only UI tests
pytest -m ui

# Run only API tests
pytest -m api

# Run only Integration tests
pytest -m integration

# Run critical Smoke tests
pytest -m smoke

# Run full regression suite
pytest -m regression
```

### Run in Headed Mode (Visible Browser)
```bash
pytest --headed -m ui
```

### Run on Multiple Browsers
```bash
pytest --browser chromium --browser firefox
```

---

## Framework Architecture

1. **Official Built-in `page` Fixture:**
   - POM fixtures in `fixtures/ui_fixtures.py` receive the built-in `page` fixture from `pytest-playwright`.
   - No custom browser or context management code is needed.
   - All `addopts` flags (`--tracing`, `--video`, `--screenshot`, `--browser`) are respected seamlessly.

2. **Page Object Model (POM) with Decoupled Locators:**
   - `locators/`: Centralizes all DOM element selectors.
   - `pages/`: Exposes readable business actions (`login()`, `search_product()`, `complete_step_4_payment()`).
   - `tests/`: Pure assertion and scenario logic without raw selector strings.

3. **Dynamic & Safe Test Data:**
   - User registrations generate unique, timestamped email addresses and compliant, unbreached passwords (`PracticePassword987!`) via `utils/helpers.py`.
   - No real credentials are committed or stored in plain text.

---

## CI/CD Pipeline (GitHub Actions)

A complete continuous integration workflow is configured in `.github/workflows/tests.yml`:
- **Triggers:** Automatically on push to `main`/`master`, pull requests, and manual triggers (`workflow_dispatch`).
- **Environment:** Ubuntu Linux runner, Python 3.11 with pip caching.
- **Browser Setup:** Headless Chromium with system dependencies (`playwright install --with-deps chromium`).
- **Artifacts:** Automatically uploads `reports/report.html` and any `test-results/` traces on every run.

---

## Test Coverage Matrix

| Category | UI Tests | API Tests | Integration Tests | Total |
| :--- | :---: | :---: | :---: | :---: |
| **Home & Navigation** | 4 | - | - | **4** |
| **Search & Catalog** | 4 | 2 | - | **6** |
| **Product Details & Sorting** | 5 | 7 | 1 | **13** |
| **Shopping Cart Lifecycle** | 5 | 4 | - | **9** |
| **Authentication & Profile** | 4 | 4 | 1 | **9** |
| **User Registration** | 3 | 3 | - | **6** |
| **Checkout & Invoices** | 2 | 2 | 1 | **5** |
| **Total Test Count** | **27** | **22** | **3** | **52+ Tests** |

---

## Reporting, Traces & Failure Screenshots

- **Automated HTML Report:**
  Every test run automatically updates `reports/report.html` (configured via `pytest.ini`).
- **Trace Viewer:**
  Playwright traces saved in `test-results/` capture DOM snapshots, network calls, console logs, and action timelines:
  ```bash
  playwright show-trace test-results/<test_name>/trace.zip
  ```
- **Screenshot-On-Failure:**
  Full-page failure screenshots are captured in `reports/screenshots/failures/` and automatically embedded directly inside `reports/report.html`.
# tools-shop-demo
