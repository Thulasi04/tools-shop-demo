# Tools Shop Demo – UI and API Automation Testing

## Project Overview

This project focuses on UI and API automation testing of the [Practice Software Testing – Toolshop](https://practicesoftwaretesting.com/) web application using Python, Playwright, Pytest, and Requests.

## Technologies Used

- Python
- Playwright
- Pytest
- Requests
- Git and GitHub
- GitHub Actions

## Testing Scope

### UI Automation Testing
- User registration and login
- Product search and filtering
- Product details validation
- Shopping cart operations
- Checkout workflow

### API Automation Testing
- Product API testing
- User registration and authentication
- Order and cart operations
- HTTP status code validation
- Request and response validation

## Framework Features

- Page Object Model (POM)
- Reusable page objects and locators
- Pytest fixtures
- Automated HTML test reports
- Screenshot capture on test failures
- UI and API integration testing
- GitHub Actions CI/CD pipeline

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

