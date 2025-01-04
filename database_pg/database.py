import asyncpg
import asyncio

from typing import Optional
from asyncpg.pool import PoolConnectionProxy

from src.datamodels.database_config import DatabaseConfig
from src.datamodels.user import User, Student, Teacher
from src.datamodels.labs import Lab1Request

from src.algorithms import lab1


LABS_COUNT = 12

# TODO: change hardcoded role_id to enum
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
                await conn.execute(f'TRUNCATE TABLE {table["tablename"]} CASCADE;')
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
                CREATE TABLE IF NOT EXISTS lab1 (
                    id SERIAL PRIMARY KEY,
                    alpha INTEGER NOT NULL,
                    beta INTEGER NOT NULL,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL
                );
            '''  # create table of lab1
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER REFERENCES groups(id),
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    marks BOOLEAN[] NOT NULL,
                    lab1_id INTEGER NOT NULL REFERENCES lab1(id)
                );
            '''  # create table of students
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

    async def get_student_by_username(self, username: str) -> Optional[Student]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT students.*
                FROM students
                JOIN users ON students.user_id = users.id
                WHERE users.username = $1;
            '''
            student_row = await conn.fetchrow(sql_query, username)
            if student_row is not None:
                student_row = Student(**student_row)
            return student_row

    async def get_teacher_by_username(self, username: str) -> Optional[Teacher]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT teachers.*
                FROM teachers
                JOIN users ON teachers.user_id = users.id
                WHERE users.username = $1;
            '''
            teacher_row = await conn.fetchrow(sql_query, username)
            if teacher_row is not None:
                teacher_row = Teacher(**teacher_row)
            return teacher_row

    async def registrate_user(self, user: User):
        async def add_new_user(user: User) -> int:
            sql_query = """ 
                INSERT INTO users (name, username, password, role_id)
                VALUES
                    ($1, $2, $3, $4)
                RETURNING id;
            """
            user_row = await conn.fetchrow(sql_query, user.name, user.username, user.password, user.role_id)
            return user_row.get('id')

        async def add_new_teacher(user_id: int) -> int:
            sql_query = """ 
                INSERT INTO teachers (user_id)
                VALUES
                    ($1)
                RETURNING id;
            """
            teacher_row = await conn.fetchrow(sql_query, user_id)
            return teacher_row.get('id')

        async def add_new_student(user_id: int, lab1_id: int) -> int:
            sql_query = """ 
                INSERT INTO students (user_id, marks, lab1_id)
                VALUES
                    ($1, $2, $3)
                RETURNING id;
            """
            marks = [False for _ in range(LABS_COUNT)]
            student_row = await conn.fetchrow(sql_query, user_id, marks, lab1_id)
            return student_row.get('id')

        async def generate_lab1() -> int:
            variant = lab1.generate_variant()
            sql_query = """ 
                INSERT INTO lab1 (matrix_a, matrix_b, alpha, beta)
                VALUES
                    ($1, $2, $3, $4)
                RETURNING id;
            """
            lab1_row = await conn.fetchrow(sql_query, variant.matrix_a, variant.matrix_b, variant.alpha, variant.beta)
            return lab1_row.get('id')

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                user_id = await add_new_user(user)
                if user.role_id == 1:
                    teacher_id = await add_new_teacher(user_id)
                elif user.role_id in (2, 3):
                    lab1_id = await generate_lab1()
                    student_id = await add_new_student(user_id, lab1_id)

    async def update_marks_by_username(self, username: str, new_marks: list[bool]) -> None:
        async with self._pool.acquire() as conn:
            sql_query = '''
               UPDATE students
               SET marks = $1
               WHERE user_id = (
                   SELECT id
                   FROM users
                   WHERE username = $2
               );
            '''
            await conn.execute(sql_query, new_marks, username)

    async def load_lab1_variant(self, student_id: int) -> Optional[Lab1Request]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT lab1.*
                FROM students
                JOIN lab1 ON lab1.id = students.lab1_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = Lab1Request(**variant_row)
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant


async def main():
    db = Database()
    await db.create_pool()
    await db.drop_all_tables()
    await db.setup_tables()
    # user = User(name="bba", username="ggg", password="zzz", role_id=1)
    # print(await db.get_user_by_username("ggg"))
    print(await db.get_all_tables())


if __name__ == "__main__":
    asyncio.run(main())
