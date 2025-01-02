import asyncpg
import asyncio

from typing import Optional
from asyncpg.pool import PoolConnectionProxy

from src.datamodels.database_config import DatabaseConfig
from src.datamodels.user import User


class Database:
    def __init__(self):
        self.config = dict(DatabaseConfig())
        self._pool = None

    def get_pool(self):
        return self._pool

    async def create_pool(self):
        self._pool = await asyncpg.create_pool(
            **self.config
        )

    async def get_all_tables(self):
        async with self._pool.acquire() as conn:
            tables = await conn.fetch(
                '''
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public';
                '''
            )
            return tables

    async def drop_all_tables(self) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute('SET session_replication_role = replica;')

            tables = await conn.fetch(
                '''
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public';
                '''
            )

            for table in tables:
                await conn.execute(f'DROP TABLE IF EXISTS {table["tablename"]} CASCADE;')

            # Восстанавливаем временные ограничения целостности
            await conn.execute('SET session_replication_role = DEFAULT;')

    async def setup_tables(self) -> None:
        async def create_all_tables(connection: PoolConnectionProxy):
            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS roles (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL 
                );
                '''  # create table of roles
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role_id INTEGER NOT NULL REFERENCES roles(id)
                );
                '''  # create table of users
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS teachers (
                    id SERIAL PRIMARY KEY,
                    email TEXT,
                    phone TEXT,
                    user_id INTEGER NOT NULL REFERENCES users(id)
                );
                '''  # create table of teachers
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS groups (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    teacher_id INTEGER NOT NULL REFERENCES teachers(id)
                );
                '''  # create table of groups
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER NOT NULL REFERENCES groups(id),
                    user_id INTEGER NOT NULL REFERENCES users(id)
                );
                '''  # create table of students
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS lab1 (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    alpha INTEGER NOT NULL,
                    beta INTEGER NOT NULL,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL,
                    student_id INTEGER NOT NULL REFERENCES students(id),
                    mark INTEGER
                );
                '''  # create table of lab1
            await connection.execute(sql_query)

        async def fill_all_tables_by_default(connection: PoolConnectionProxy):
            sql_query = f''' 
                INSERT INTO roles (name)
                VALUES
                    ('teacher'), ('student'), ('leader'), ('developer');
                '''  # fill roles
            await connection.execute(sql_query)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                await create_all_tables(conn)
                await fill_all_tables_by_default(conn)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        async with self._pool.acquire() as conn:
            sql_query = ''' 
                SELECT * FROM users
                WHERE username = $1;
                '''
            user_row = await conn.fetchrow(sql_query, username)
            if user_row is not None:
                user_row = User(**user_row)
            return user_row

    async def registrate_user(self, user: User):
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                sql_query = """ 
                    INSERT INTO users (name, username, password, role_id)
                    VALUES
                        ($1, $2, $3, $4);
                    """
                await conn.execute(sql_query, user.name, user.username, user.password, user.role_id)


async def main():
    db = Database()
    await db.create_pool()
    # await db.drop_all_tables()
    await db.setup_tables()
    # user = User(name="bba", username="ggg", password="zzz", role_id=1)
    # print(await db.get_user_by_username("ggg"))
    print(await db.get_all_tables())


if __name__ == "__main__":
    asyncio.run(main())
