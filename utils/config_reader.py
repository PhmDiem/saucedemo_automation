import json
import os

class ConfigReader:
    """Đọc và cache các file JSON dùng chung cho framework test."""
    _configs = {}

    # config_reader.py -> utils/ -> my_automation_project/ (project root)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def load_file(file_key, folder_name, file_name):
        """Đọc 1 file JSON, cache theo file_key. Raise lỗi rõ ràng nếu có vấn đề."""
        if file_key not in ConfigReader._configs:
            file_path = os.path.join(ConfigReader.BASE_DIR, folder_name, file_name)

            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ConfigReader._configs[file_key] = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"File '{file_path}' không đúng format JSON: {e}")

        return ConfigReader._configs[file_key]

    # --- Các hàm lấy dữ liệu cụ thể ---

    @staticmethod
    def get_config():
        return ConfigReader.load_file("config", "config", "config.json")

    @staticmethod
    def get_users():
        """Trả về dict các user từ users.json"""
        users_data = ConfigReader.load_file("users", "data", "users.json")
        return users_data.get("users", {})
    
    @staticmethod
    def get_products():
        """Lấy toàn bộ danh sách sản phẩm từ test_data.json"""
        data = ConfigReader.load_file("products", "data", "test_data.json")
        return data.get("products", {})

    # --- Các hàm tiện ích gọi nhanh ---

    @staticmethod
    def get_url():
        return ConfigReader.get_config().get("base_url")
    
    @staticmethod
    def get_product_url():
        return ConfigReader.get_config().get("products_url")

    @staticmethod
    def get_browser():
        return ConfigReader.get_config().get("browser")

    @staticmethod
    def get_timeout(timeout_type="implicit_wait"):
        """Lấy timeout từ config (implicit_wait hoặc explicit_wait)"""
        timeouts = ConfigReader.get_config().get("timeout", {})
        return timeouts.get(timeout_type)

    @staticmethod
    def get_user(user_type):
        """Lấy thông tin user theo user_type"""
        user = ConfigReader.get_users().get(user_type)
        if user is None:
            raise KeyError(f"Không tìm thấy user_type '{user_type}' trong users.json")
        return user
    
    @staticmethod
    def get_product(product_key):
        """Lấy thông tin của 1 sản phẩm theo key"""
        products = ConfigReader.get_products()
        return products.get(product_key)

    # --- Tiện ích quản lý cache ---

    @staticmethod
    def reload():
        """Xóa cache để lần gọi tiếp theo đọc lại file JSON từ disk."""
        ConfigReader._configs.clear()