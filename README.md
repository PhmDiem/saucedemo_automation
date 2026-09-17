# SauceDemo Automation Testing

> UI test automation for [SauceDemo](https://www.saucedemo.com/) using Selenium, Pytest, and Allure.

## Technology

- Python 3.10+
- Selenium WebDriver
- Pytest
- Allure Report
- Chrome/Chromium in headless or headed mode

## Project structure

```text
saucedemo_automation/
├── .github/workflows/       # GitHub Actions
├── config/config.json       # URL, browser, and timeout settings
├── data/                    # Test accounts and product data
├── pages/                   # Page Object Model classes
├── tests/                   # Test cases
├── utils/config_reader.py   # Configuration and test data reader
├── conftest.py              # Fixtures and failure screenshots
├── pytest.ini               # Pytest options and markers
├── requirements.txt
├── run_tests.bat            # Run tests on Windows
├── run_tests.sh             # Run tests on macOS/Linux
└── view_report.bat          # Open a report on Windows
```

The `allure-results/`, `reports/`, `allure-reports/`, and `screenshots/` directories contain generated output and are ignored by Git.

## Installation

```bash
git clone <repo-url>
cd saucedemo_automation
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The test machine must have Chrome/Chromium installed. Selenium Manager will locate or download a compatible ChromeDriver. If network access is restricted, install ChromeDriver manually and add it to PATH.

## Configuration

Edit [`config/config.json`](config/config.json). Tests run headlessly by default:

```json
{
  "base_url": "https://www.saucedemo.com/",
  "products_url": "https://www.saucedemo.com/inventory.html",
  "isHeadless": true,
  "browser": "chrome",
  "timeout": {
    "implicit_wait": 10,
    "explicit_wait": 30
  }
}
```

Set `isHeadless` to `false` to display the browser.

## Running tests

### Windows

```powershell
# Run all tests and generate an Allure report
.\run_tests.bat tests/

# Run one file or one test
.\run_tests.bat tests/test_login.py
.\run_tests.bat tests/test_login.py::TestLogin::test_login_success

# Run by marker or keyword
.\run_tests.bat -m smoke tests/
.\run_tests.bat -k test_login_success tests/
```

### macOS/Linux

Install the Allure Commandline before generating reports.

```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Direct Pytest commands

```bash
python -m pytest tests/ -v
python -m pytest --collect-only -q
```

Pytest writes raw results to `allure-results/` according to `pytest.ini`.

## Allure reports

Windows and macOS/Linux store reports in `reports/<timestamp>/`. On Windows, the test script opens the generated report automatically:

```powershell
.\view_report.bat
```

Or use the Allure CLI:

```bash
allure open reports/<timestamp>
```

## Test accounts

| User type | Username | Purpose |
|---|---|---|
| `standard` | `standard_user` | Happy path |
| `locked_out` | `locked_out_user` | Locked account |
| `problem` | `problem_user` | Known application bugs |
| `performance` | `performance_glitch_user` | Response-time checks |
| `error` | `error_user` | Error handling |
| `visual` | `visual_user` | UI checks |

Additional negative-test users are defined in [`data/users.json`](data/users.json), including `wrong_username`, `wrong_password`, and `empty_both`.

## Markers

| Marker | Meaning |
|---|---|
| `smoke` | Critical flows |
| `login` | Login module |
| `positive` | Happy-path cases |
| `negative` | Negative cases |
| `bug` | Known application bugs |
| `performance` | Response-time checks |
| `select_sort` | Inventory sorting |
| `cart` | Cart module |
| `add_to_cart` | Add-to-cart cases |
| `remove_from_cart` | Remove-from-cart cases |
| `edge_cases` | Edge cases |

Examples:

```bash
python -m pytest -m "login and positive" tests/
python -m pytest -m smoke tests/
```

## Test scope

- Successful and failed login.
- Inventory display, sorting, cart actions, and refresh persistence.
- Product detail information, cart actions, and navigation.
- Cart display, item name/price, removal, continue shopping, and checkout navigation.
- Checkout validation, cancellation, order summary, totals, and order completion.
- Scenarios for `problem_user`, `error_user`, and `performance_glitch_user`.

The project currently collects **59 test cases**. Pass/fail results depend on the browser, ChromeDriver, and access to SauceDemo from the execution environment.

## CI

The [`Run_all_test.yml`](.github/workflows/Run_all_test.yml) workflow runs on pushes and pull requests targeting `main` or `master`, and supports manual `workflow_dispatch` runs.

CI will:

1. Install Python 3.10.
2. Install dependencies from `requirements.txt`.
3. Run `pytest`.
4. Upload `allure-results/` as an artifact.
