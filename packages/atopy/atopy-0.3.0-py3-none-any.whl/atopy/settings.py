from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    BaseSettings,
)


class IModel(BaseModel):  # pylint: disable=too-few-public-methods
    pass


class ISettings(BaseSettings):  # pylint: disable=too-few-public-methods
    class Config:  # pylint: disable=too-few-public-methods
        env_file = ".env"
        env_file_encoding = "utf-8"
