class SettingsService:

    _settings = {

        "theme": "light",

        "notifications": True,

        "auto_migration": True,

        "risk_threshold": "HIGH",

        "default_algorithm": "ML-KEM-768",

        "dashboard_refresh": 5

    }


    @classmethod
    def get_settings(cls):

        return cls._settings


    @classmethod
    def update_settings(cls, data):

        cls._settings.update(data)

        return cls._settings
