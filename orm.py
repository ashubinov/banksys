from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from database import engine, Base
from models import ClientORM, DepositORM, AccountORM, UserORM, UserRole
from schemas import UserCreateSchema, DepositAddShema, DepositPatchShema, ClientAddShema, ClientPatchShema, \
    AccountPatchShema, AccountAddShema
from password import hash_password, verify_password

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_new_deposit(data: DepositAddShema, session ):

        deposit = DepositORM(
            deposit_name=data.deposit_name,
            shelf_life=data.shelf_life,
            rate=data.rate,
        )
        session.add(deposit)
        await session.commit()

    @staticmethod
    async def insert_admin_data(session):
        admin_data = UserCreateSchema(
            username="first",
            password="1234",
            role=UserRole.admin,
        )
        await AsyncORM.create_user(session, admin_data)

    @staticmethod
    async def insert_data():

        deposits = [
                {"deposit_name": "Накопительный", "shelf_life": "13", "rate": "10"},
                {"deposit_name": "Победа", "shelf_life": "12", "rate": "2"},
                {"deposit_name": "Накопительный", "shelf_life": "36", "rate": "18"},
                {"deposit_name": "Капитал", "shelf_life": "18", "rate": "7"},
                {"deposit_name": "Отпуск", "shelf_life": "12", "rate": "1"}
            ]

        clients = [
                {"client_name": "Михаил", "client_patronymic": "Петрович","client_surname": "Сидоров", "passport_numb": "8475847382", "city": "Москва", "phone_numb": "+79445676666"},
                {"client_name": "Иван","client_patronymic": "Иванович","client_surname": "Иванов", "passport_numb": "9485746373", "city": "Казань", "phone_numb": "+79843657634"},
                {"client_name": "Павел","client_patronymic": "Сергеевич", "client_surname": "Петров", "passport_numb": "33333333333", "city": "Омск", "phone_numb": "+79123456789"}
            ]

        accounts = [
                {"amount_invested": "500000", "deposit_id": "1", "client_id": "1"},
                {"amount_invested": "1500000", "deposit_id": "2", "client_id": "2"},
                {"amount_invested": "2000000", "deposit_id": "3", "client_id": "3"}
            ]

        async with engine.begin() as conn:
            insert_deposits = insert(DepositORM).values(deposits)
            insert_clients = insert(ClientORM).values(clients)
            insert_accounts = insert(AccountORM).values(accounts)

            await conn.execute(insert_deposits)
            await conn.execute(insert_clients)
            await conn.execute(insert_accounts)

            await conn.commit()

    @staticmethod
    async def create_user(session, data: UserCreateSchema) ->UserORM:
        existing = await session.scalar(
            select(UserORM).where(UserORM.user_name == data.username)
        )
        if existing:
            raise HTTPException(status_code=409, detail="user_name already exists")

        user = UserORM(
            user_name=data.username,
            password_hash=hash_password(data.password),
            role = data.role
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def authenticate_user(session, username: str, password: str):
        user = await session.scalar(
            select(UserORM).where(UserORM.user_name == username)
        )
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def get_user_by_id(session, user_id: int) -> UserORM | None:
        user = await session.scalar(
            select(UserORM).where(UserORM.user_id == user_id)
        )
        return user

    @staticmethod
    async def get_all_deposits(session):
        query = (select(DepositORM).order_by(DepositORM.deposit_id))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_deposit_by_id(session, deposit_id: int):
        query = (
            select(DepositORM)
            .where(DepositORM.deposit_id == deposit_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_deposit(session, deposit_id: int):
        try:
            query = delete(DepositORM).where(DepositORM.deposit_id==deposit_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Нельзя удалить депозит привязаны активные счета")

    @staticmethod
    async def update_deposit(session, deposit_id: int, data: DepositPatchShema):
        update_data = data.model_dump(exclude_unset = True)
        if not update_data:
            return None

        query = (
            update(DepositORM)
            .where(DepositORM.deposit_id==deposit_id)
            .values(update_data)
            .returning(DepositORM)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def add_client(session, data: ClientAddShema):
        client = ClientORM(
            client_name=data.client_name,
            client_patronymic=data.client_patronymic,
            client_surname=data.client_surname,
            phone_numb=data.phone_numb,
            passport_numb=data.passport_numb,
            city=data.city,
        )
        session.add(client)
        await session.commit()
        await session.refresh(client)

    @staticmethod
    async def get_client_by_id(session, client_id: int):
        query = (select(ClientORM)
                 .where(ClientORM.client_id == client_id))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_client(session):
        query = (select(ClientORM).order_by(ClientORM.client_id))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_client(session, client_id: int, data: ClientPatchShema):
        update_data = data.model_dump(exclude_unset = True)
        if not update_data:
            return None
        query = (
            update(ClientORM)
            .where(ClientORM.client_id == client_id)
            .values(update_data)
            .returning(ClientORM)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_client(session, client_id: int):
        try:
            query = delete(ClientORM).where(ClientORM.client_id == client_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Нельзя удалить данные клиента привязаны активные счета")

    @staticmethod
    async def add_account(session, data: AccountAddShema):
        account = AccountORM(
            opening_date = data.opening_date,
            closing_date = data.closing_date,
            amount_invested = data.amount_invested,
            deposit_id = data.deposit_id,
            client_id = data.client_id,
        )
        session.add(account)
        await session.commit()
        await session.refresh(account)

    @staticmethod
    async def get_account_by_numb(session, account_numb: int):
        query = (select(AccountORM)
                 .where(AccountORM.account_numb == account_numb ))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_account_all(session):
        query = (select(AccountORM).order_by(AccountORM.account_numb))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_account(session, account_numb: int, data: AccountPatchShema):
        update_data = data.model_dump(exclude_unset = True)
        if not update_data:
            return None
        query = (
            update(AccountORM)
            .where(AccountORM.account_numb == account_numb)
            .values(update_data)
            .returning(AccountORM)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_account(session, account_numb: int):
        try:
            query = delete(AccountORM).where(AccountORM.account_numb == account_numb)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Нельзя удалить данные клиента привязаны активные счета")