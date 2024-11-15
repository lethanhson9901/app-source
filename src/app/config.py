from pydantic_settings import BaseSettings
from typing import List
import json
import os
from pathlib import Path

def find_env_file():
    """Find the .env file by walking up the directory tree"""
    current_dir = Path.cwd()
    while current_dir != current_dir.parent:
        env_file = current_dir / '.env'
        if env_file.exists():
            return str(env_file)
        current_dir = current_dir.parent
    return '.env'  # fallback to default

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Python Application"
    APP_VERSION: str = "1.0.0"
    API_KEY: str = "dev-secret-key"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_PORT: int = 8080
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # Docker Settings
    DOCKER_REGISTRY: str = "local"
    IMAGE_TAG: str = "latest"
    BUILD_VERSION: str = "latest"
    
    # Database Settings
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "db"
    DATABASE_URL: str | None = None
    
    # Redis Settings
    REDIS_PASSWORD: str = "redis"
    REDIS_URL: str | None = None
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Monitoring Settings
    ENABLE_METRICS: bool = True
    GRAFANA_USER: str = "admin"
    GRAFANA_PASSWORD: str = "admin"
    
    # Resource Limits
    APP_CPU_LIMIT: str = "1"
    APP_MEMORY_LIMIT: str = "512M"
    APP_CPU_RESERVATION: str = "0.25"
    APP_MEMORY_RESERVATION: str = "256M"

    class Config:
        env_file = find_env_file()
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "ALLOWED_ORIGINS":
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    if raw_val == "*":
                        return ["*"]
                    return [origin.strip() for origin in raw_val.split(",")]
            elif field_name == "DEBUG":
                return str(raw_val).lower() in ('true', '1', 't', 'y', 'yes')
            return raw_val

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set PORT to match APP_PORT if different
        if self.APP_PORT != self.PORT:
            self.PORT = self.APP_PORT
            
        # Construct DATABASE_URL if not explicitly set
        if self.DATABASE_URL is None:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@postgres:5432/{self.POSTGRES_DB}"
            )
        
        # Construct REDIS_URL if not explicitly set
        if self.REDIS_URL is None:
            self.REDIS_URL = f"redis://:{self.REDIS_PASSWORD}@redis:6379/0"

settings = Settings()

if __name__ == "__main__":
    env_file_path = Settings.Config.env_file
    print(f"\nUsing .env file: {env_file_path}")
    print(f"File exists: {os.path.exists(env_file_path)}")
    
    print("\nSettings loaded:")
    # for field in settings.__fields__:
    #     value = getattr(settings, field)
    #     print(f"{field}: {value}")
    
    # # Print environment variables for debugging
    # print("\nEnvironment variables:")
    # env_vars = {key: value for key, value in os.environ.items() 
    #             if key in settings.__fields__}
    # for key, value in env_vars.items():
    #     print(f"{key}: {value}")