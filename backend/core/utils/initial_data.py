"""Стартовые данные, которые заливаются в пустую БД при запуске приложения."""

DEPOSITS = [
    {"deposit_name": "Накопительный", "shelf_life": 13, "rate": 10},
    {"deposit_name": "Победа", "shelf_life": 12, "rate": 2},
    {"deposit_name": "Накопительный", "shelf_life": 36, "rate": 18},
    {"deposit_name": "Капитал", "shelf_life": 18, "rate": 7},
    {"deposit_name": "Отпуск", "shelf_life": 12, "rate": 1},
]

CLIENTS = [
    {"client_name": "Михаил", "client_patronymic": "Петрович", "client_surname": "Сидоров",
     "passport_numb": "8475847382", "city": "Москва", "phone_numb": "+79445676666"},
    {"client_name": "Иван", "client_patronymic": "Иванович", "client_surname": "Иванов",
     "passport_numb": "9485746373", "city": "Казань", "phone_numb": "+79843657634"},
    {"client_name": "Павел", "client_patronymic": "Сергеевич", "client_surname": "Петров",
     "passport_numb": "33333333333", "city": "Омск", "phone_numb": "+79123456789"},
]

ACCOUNTS = [
    {"amount_invested": 500000, "deposit_id": 1, "client_id": 1},
    {"amount_invested": 1500000, "deposit_id": 2, "client_id": 2},
    {"amount_invested": 2000000, "deposit_id": 3, "client_id": 3},
]
