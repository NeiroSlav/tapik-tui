from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    BACKEND_HOST: str

    @property
    def backend_url(self) -> str:
        return f"http://{self.BACKEND_HOST}"


def get_settings() -> Settings:
    return Settings()  # type: ignore
