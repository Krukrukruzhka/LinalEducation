import asyncpg
import asyncio

from src.datamodels.database_config import DatabaseConfig


class Database:
    def __init__(self):
        self.config = dict(DatabaseConfig())
        self._pool = None

    async def get_pool(self):
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
            print(tables)

    async def drop_all_tables(self):
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

    async def create_all_tables(self):
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                sql_query = ''' 
                    CREATE TABLE IF NOT EXISTS roles (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL 
                    );
                    '''  # create table of roles
                await conn.execute(sql_query)

                sql_query = ''' 
                    CREATE TABLE IF NOT EXISTS teachers (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        role_id INTEGER NOT NULL REFERENCES roles(id)
                    );
                    '''  # create table of teachers
                await conn.execute(sql_query)

                sql_query = ''' 
                    CREATE TABLE IF NOT EXISTS groups (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        teacher_id INTEGER NOT NULL REFERENCES teachers(id)
                    );
                    '''  # create table of groups
                await conn.execute(sql_query)

                sql_query = ''' 
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        group_id INTEGER NOT NULL REFERENCES groups(id),
                        role_id INTEGER NOT NULL REFERENCES roles(id)
                    );
                    '''  # create table of students
                await conn.execute(sql_query)

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
                await conn.execute(sql_query)


async def main():
    db = Database()
    await db.create_pool()
    await db.get_all_tables()

if __name__ == "__main__":
    asyncio.run(main())
