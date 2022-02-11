from pydantic import BaseModel, BaseSettings


class DataBase(BaseModel):
    host: str
    port: int
    db: str
    user: str
    password: str

    def get_sql_url(self):
        return f'{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class Setting(BaseSettings):
    database: DataBase

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


settings = Setting()
