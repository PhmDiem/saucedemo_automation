# SauceDemo Automation Testing

Automation test project cho [saucedemo.com](https://www.saucedemo.com) sử dụng Selenium + Pytest + Allure.

---

## 🗂️ Cấu trúc project

```
saucedemo-automation/
├── config/
│   └── config.json
├── data/
│   ├── users.json
│   └── test_data.json
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── reports/                        ← Allure reports lưu theo timestamp
├── screenshots/                    ← Tự động chụp khi test fail
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_product_detail.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/
│   └── config_reader.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── run_tests.bat                   ← Chạy test (Windows)
├── run_tests.sh                    ← Chạy test (Mac/Linux)
└── view_report.bat                 ← Xem report đã lưu (Windows)
```

---

## ⚙️ Cài đặt

**1. Clone project**
```bash
git clone <repo-url>
cd saucedemo-automation
```

**2. Tạo virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Cài dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Chạy test (Windows)

Mỗi lần chạy sẽ tự động:
1. Xóa allure-results cũ
2. Chạy pytest với các tham số truyền vào
3. Copy history từ lần chạy trước (để xem trend)
4. Generate report vào `reports\<timestamp>` và mở trình duyệt

**Cú pháp**
```bat
.\run_tests.bat <tham_số>
```

**Ví dụ**

```bat
# Chạy tất cả test
.\run_tests.bat tests/

# Chạy 1 file
.\run_tests.bat tests/test_login.py

# Chạy theo marker
.\run_tests.bat -m smoke tests/
.\run_tests.bat -m login tests/
.\run_tests.bat -m "login and positive" tests/

# Chạy 1 test case cụ thể
.\run_tests.bat -k test_login_success tests/

# Chạy 1 hàm trong file
.\run_tests.bat tests/test_login.py::TestLogin::test_login_success
```

---

## 🚀 Chạy test (Mac/Linux)

```bash
chmod +x run_tests.sh
./run_tests.sh
```

---

## 📊 Xem report (Windows)

```bat
.\view_report.bat
```

Sẽ hiển thị danh sách các lần chạy theo thời gian, ví dụ:

```
========================================
  DANH SACH CAC LAN CHAY TEST
========================================
  [1]  2025-01-15_14-30
  [2]  2025-01-15_10-00
  [3]  2025-01-14_16-45
========================================
  [0]  Thoat
========================================

Chon so de xem report: 1
```

Nhập số tương ứng để mở report trong trình duyệt.

---

## 🏷️ Markers

| Marker | Mô tả |
|---|---|
| `smoke` | Các test quan trọng nhất |
| `positive` | Happy path |
| `negative` | Negative cases |
| `bug` | Known bugs (problem_user) |
| `performance` | Đo response time |
| `login` | Module login |
| `select_sort` | Module sort |
| `cart` | Module cart |

---

## 👥 Test accounts

| Username | Password | Mục đích |
|---|---|---|
| `standard_user` | `secret_sauce` | Happy path — full flow |
| `locked_out_user` | `secret_sauce` | Verify block login |
| `problem_user` | `secret_sauce` | Known bugs |
| `performance_glitch_user` | `secret_sauce` | Response time |
| `error_user` | `secret_sauce` | Error handling |
| `visual_user` | `secret_sauce` | UI regression |

---

## 📋 Test coverage

| Module | Positive | Negative | Bug | Performance |
|---|:---:|:---:|:---:|:---:|
| Login | ✅ | ✅ | - | - |
| Inventory - Sort | ✅ | - | ✅ | - |
| Inventory - Cart | ✅ | ✅ | ✅ | ✅ |
| Product Detail | ✅ | - | - | - |
| Cart | ✅ | ✅ | - | - |
| Checkout | ✅ | ✅ | - | - |

---

## 🛠️ Tech stack

- **Language:** Python 3.x
- **Framework:** Selenium WebDriver
- **Test runner:** Pytest
- **Report:** Allure
- **Browser:** Chrome