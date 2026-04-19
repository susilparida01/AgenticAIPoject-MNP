import os
from configparser import ConfigParser

class ConfigReader:
    """
    A utility class to read properties from config.properties file.
    """
    _config = None

    @classmethod
    def _get_config(cls):
        if cls._config is None:
            cls._config = ConfigParser(interpolation=None)
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.properties'))
            
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = '[DEFAULT]\n' + f.read()
                    cls._config.read_string(content)
                except Exception as e:
                    print(f"[ConfigReader] Error reading config file {config_path}: {e}")
            else:
                print(f"[ConfigReader] Config file not found: {config_path}")
                
        return cls._config

    @classmethod
    def get_property(cls, key, default=None):
        """
        Get a property value by key.
        """
        config = cls._get_config()
        val = config.get('DEFAULT', key, fallback=default)
        if (val is None or val == '') and default is not None:
            return default
        return val

    @classmethod
    def get_bool_property(cls, key, default=False):
        """Get a boolean property by key."""
        raw = cls.get_property(key, None)
        if raw is None or raw == '':
            return default
        normalized = str(raw).strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
        return default

    @classmethod
    def get_openai_api_key(cls):
        return cls.get_property("OPENAI_API_KEY")

    @classmethod
    def get_model_name(cls):
        return cls.get_property("MODEL_NAME", "gpt-4o")

    @classmethod
    def get_postgres_url(cls):
        return cls.get_property("POSTGRES_URL", "postgresql://user:password@localhost:5432/database")

    @classmethod
    def get_rest_base_url(cls):
        return cls.get_property("REST_BASE_URL", "")

    @classmethod
    def get_soap_wsdl_url(cls):
        return cls.get_property("SOAP_WSDL_URL", "")

    @classmethod
    def get_soap_endpoint_url(cls):
        return cls.get_property("SOAP_ENDPOINT_URL", "")

    @classmethod
    def get_soap_payload(cls):
        return cls.get_property("SOAP_PAYLOAD", "")

    @classmethod
    def get_browser_url(cls):
        return cls.get_property("BROWSER_URL", "")

    @classmethod
    def get_browser_username(cls):
        return cls.get_property("BROWSER_USERNAME", "")

    @classmethod
    def get_browser_password(cls):
        return cls.get_property("BROWSER_PASSWORD", "")

    @classmethod
    def get_playwright_headless(cls):
        return cls.get_bool_property("PLAYWRIGHT_HEADLESS", True)

    @classmethod
    def get_uv_path(cls):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if os.name == 'nt':
            path = os.path.join(project_root, ".venv", "Scripts", "uv.exe")
        else:
            path = os.path.join(project_root, ".venv", "bin", "uv")
        return path if os.path.exists(path) else cls.get_property("UV_PATH", default="uv")

    @classmethod
    def get_site_packages_path(cls):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        path = None
        if os.name == 'nt':
            path = os.path.join(project_root, ".venv", "Lib", "site-packages")
        else:
            lib_dir = os.path.join(project_root, ".venv", "lib")
            if os.path.exists(lib_dir):
                for item in os.listdir(lib_dir):
                    if item.startswith("python"):
                        candidate = os.path.join(lib_dir, item, "site-packages")
                        if os.path.exists(candidate):
                            path = candidate
                            break
        return path if path and os.path.exists(path) else cls.get_property("SITE_PACKAGES_PATH")

    @classmethod
    def load_to_environ(cls, keys=None):
        config = cls._get_config()
        items = config.items('DEFAULT')
        for key, value in items:
            if keys is None or key.upper() in [k.upper() for k in keys]:
                if value:
                    os.environ[key.upper()] = value


#########################################################################################
# cr = ConfigReader()
# print(cr.get_openai_api_key())

