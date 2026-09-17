import json
import os

class ConfigReader:
    """Read and cache shared JSON files used by the test framework."""
    _configs = {}

    # config_reader.py -> utils/ -> my_automation_project/ (project root)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def load_file(file_key, folder_name, file_name):
        """Read one JSON file, cache it by file_key, and raise clear errors."""
        if file_key not in ConfigReader._configs:
            file_path = os.path.join(ConfigReader.BASE_DIR, folder_name, file_name)

            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ConfigReader._configs[file_key] = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"File '{file_path}' is not valid JSON: {e}")

        return ConfigReader._configs[file_key]

    # --- Data access methods ---

    @staticmethod
    def get_config():
        return ConfigReader.load_file("config", "config", "config.json")
    
    @staticmethod
    def get_users():
        """Return users from users.json."""
        users_data = ConfigReader.load_file("users", "data", "users.json")
        return users_data.get("users", {})
    
    @staticmethod
    def get_products():
        """Return all products from test_data.json."""
        data = ConfigReader.load_file("products", "data", "test_data.json")
        return data.get("products", {})

    # --- Convenience accessors ---

    @staticmethod
    def is_headless():
        return ConfigReader.get_config().get("isHeadless")

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
    def get_timeout(timeout_type):
        """Get a timeout from config (implicit_wait or explicit_wait)."""
        timeouts = ConfigReader.get_config().get("timeout", {})
        return timeouts.get(timeout_type)
    
    @staticmethod
    def get_implicit_wait():
        return ConfigReader.get_timeout("implicit_wait")
    
    @staticmethod
    def get_explicit_wait():
        return ConfigReader.get_timeout("explicit_wait")
    
    @staticmethod
    def get_user(user_type):
        """Get user data by user_type."""
        user = ConfigReader.get_users().get(user_type)
        if user is None:
            raise KeyError(f"User type '{user_type}' not found in users.json")
        return user
    
    @staticmethod
    def get_product(product_key):
        """Get product data by key."""
        products = ConfigReader.get_products()
        return products.get(product_key)
    
    @staticmethod
    def get_product_name(product_key):
        product = ConfigReader.get_product(product_key)
        if product is None:
            raise KeyError(f"Product key '{product_key}' not found in test_data.json")
        return product.get("name")
    
    @staticmethod
    def get_product_price(product_key):
        product = ConfigReader.get_product(product_key)
        if product is None:
            raise KeyError(f"Product key '{product_key}' not found in test_data.json")
        return product.get("price")

    # --- Cache management ---

    @staticmethod
    def reload():
        """Clear the cache so the next call reloads JSON files from disk."""
        ConfigReader._configs.clear()
