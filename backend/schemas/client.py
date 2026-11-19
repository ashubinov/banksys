from pydantic import BaseModel, ConfigDict


class ClientAddShema(BaseModel):
    client_name: str
    client_patronymic: str
    client_surname: str
    passport_numb: str
    city: str
    phone_numb: str


class ClientSchema(ClientAddShema):
    model_config = ConfigDict(from_attributes=True)

    client_id: int


class ClientPatchShema(BaseModel):
    client_name: str | None = None
    client_patronymic: str | None = None
    client_surname: str | None = None
    passport_numb: str | None = None
    city: str | None = None
    phone_numb: str | None = None
