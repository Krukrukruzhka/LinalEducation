import json
import logging
import random

import asyncpg
import asyncio

from typing import Optional
from asyncpg.pool import PoolConnectionProxy

from config.database_config import DatabaseConfig
from src.datamodels.user import User, Student, Teacher, StudentGroup, RolesEnum
from src.datamodels.labs import (
    LinalLab1Request, LinalLab2Request, LinalLab3Request, LinalLab4Request, LinalLab5Request, LinalLab6Request,
    LinalLab7Request, LinalLab8Request, LinalLab9Request, LinalLab10Request, LinalLab11Request, LinalLab12Request,
    LinalLab13Request, LinalLab14Request, LinalLab15Request
)
from src.datamodels.page_payload import BasicData
from src.datamodels.utils import AdditionalUserInfo, StudentWithResults, StudentMark
from src.utils.constants import LINAL_LABS_COUNT, ANGEM_LABS_COUNT

from src.algorithms import linal
from database_pg.lab_variants import linal_variants


logger = logging.getLogger()


class Database:
    def __init__(self, db_config: DatabaseConfig | dict):
        self.config = dict(db_config)
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
        async def is_exists_roles_table(connection: PoolConnectionProxy) -> bool:
            query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name = 'roles'
                );
                """
            result = await conn.fetchval(query)
            return True if result else False

        async def create_all_tables(connection: PoolConnectionProxy):
            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS roles (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL 
                );
            '''  # create table of roles
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
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
                    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id)
                );
            '''  # create table of teachers
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS groups (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    teacher_id INTEGER REFERENCES teachers(id)
                );
            '''  # create table of groups
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab1 (
                    id SERIAL PRIMARY KEY,
                    alpha INTEGER NOT NULL,
                    beta INTEGER NOT NULL,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab1
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab2 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL,
                    vector_x INTEGER[] NOT NULL,
                    vector_y INTEGER[] NOT NULL
                );
            '''  # create table of linal_lab2
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab3 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL,
                    coefficients INTEGER[] NOT NULL
                );
            '''  # create table of linal_lab3
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab4 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab4
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab5 (
                    id SERIAL PRIMARY KEY,
                    matrix_a TEXT[][] NOT NULL,
                    matrix_b TEXT[][] NOT NULL
                );
            '''  # create table of linal_lab5
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab6 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab6
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab7 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab7
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab8 (
                    id SERIAL PRIMARY KEY,
                    matrix_b INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab8
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab9 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab9
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab10 (
                    id SERIAL PRIMARY KEY,
                    equation_1_matrix_1 INTEGER[][] NOT NULL,
                    equation_1_matrix_2 INTEGER[][] NOT NULL,
                    equation_1_coefficient INTEGER NOT NULL,
                    equation_2_matrix_1 INTEGER[][] NOT NULL,
                    equation_2_matrix_2 INTEGER[][] NOT NULL,
                    equation_2_coefficient INTEGER NOT NULL,
                    equation_3_matrix_1 INTEGER[][] NOT NULL,
                    equation_3_matrix_2 INTEGER[][] NOT NULL,
                    equation_3_matrix_3 INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab10
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab11 (
                    id SERIAL PRIMARY KEY,
                    coefficients INTEGER[][] NOT NULL,
                    results INTEGER[] NOT NULL
                );
            '''  # create table of linal_lab11
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab12 (
                    id SERIAL PRIMARY KEY,
                    coefficients INTEGER[][] NOT NULL,
                    results INTEGER[] NOT NULL
                );
            '''  # create table of linal_lab12
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab13 (
                    id SERIAL PRIMARY KEY,
                    matrix_a INTEGER[][] NOT NULL,
                    matrix_b INTEGER[][] NOT NULL,
                    matrix_c INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab13
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab14 (
                    id SERIAL PRIMARY KEY,
                    coefficients INTEGER[][] NOT NULL
                );
            '''  # create table of linal_lab14
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS linal_lab15 (
                    id SERIAL PRIMARY KEY,
                    coefficients TEXT[][][] NOT NULL
                );
            '''  # create table of linal_lab15
            await connection.execute(sql_query)

            sql_query = ''' 
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER REFERENCES groups(id),
                    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
                    linal_marks JSONB NOT NULL,
                    angem_marks JSONB NOT NULL,
                    
                    linal_lab1_id INTEGER NOT NULL REFERENCES linal_lab1(id),
                    linal_lab2_id INTEGER NOT NULL REFERENCES linal_lab2(id),
                    linal_lab3_id INTEGER NOT NULL REFERENCES linal_lab3(id),
                    linal_lab4_id INTEGER NOT NULL REFERENCES linal_lab4(id),
                    linal_lab5_id INTEGER NOT NULL REFERENCES linal_lab5(id),
                    linal_lab6_id INTEGER NOT NULL REFERENCES linal_lab6(id),
                    linal_lab7_id INTEGER NOT NULL REFERENCES linal_lab7(id),
                    linal_lab8_id INTEGER NOT NULL REFERENCES linal_lab8(id),
                    linal_lab9_id INTEGER NOT NULL REFERENCES linal_lab9(id),
                    linal_lab10_id INTEGER NOT NULL REFERENCES linal_lab10(id),
                    linal_lab11_id INTEGER NOT NULL REFERENCES linal_lab11(id),
                    linal_lab12_id INTEGER NOT NULL REFERENCES linal_lab12(id),
                    linal_lab13_id INTEGER NOT NULL REFERENCES linal_lab13(id),
                    linal_lab14_id INTEGER NOT NULL REFERENCES linal_lab14(id),
                    linal_lab15_id INTEGER NOT NULL REFERENCES linal_lab15(id)
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

            sql_query = f''' 
                INSERT INTO groups (name)
                VALUES
                    ('None');
            '''
            await connection.execute(sql_query)

            sql_query = f''' 
                INSERT INTO linal_lab1 (matrix_a, matrix_b, alpha, beta)
                VALUES ($1, $2, $3, $4);
            '''
            variants = [(variant.matrix_a, variant.matrix_b, variant.alpha, variant.beta) for variant in linal_variants.LINAL_LAB1_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab2 (vector_x, vector_y, matrix_a)
                VALUES ($1, $2, $3);
            '''
            variants = [(variant.vector_x, variant.vector_y, variant.matrix_a) for variant in linal_variants.LINAL_LAB2_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab3 (matrix_a, coefficients)
                VALUES ($1, $2);
            '''
            variants = [(variant.matrix_a, variant.coefficients) for variant in linal_variants.LINAL_LAB3_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab4 (matrix_a, matrix_b)
                VALUES ($1, $2);
            '''
            variants = [(variant.matrix_a, variant.matrix_b) for variant in linal_variants.LINAL_LAB4_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab5 (matrix_a, matrix_b)
                VALUES ($1, $2);
            '''
            variants = [(variant.matrix_a, variant.matrix_b) for variant in linal_variants.LINAL_LAB5_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab6 (matrix_a)
                VALUES ($1);
            '''
            variants = [(variant.matrix_a, ) for variant in linal_variants.LINAL_LAB6_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab7 (matrix_a)
                VALUES ($1);
            '''
            variants = [(variant.matrix_a, ) for variant in linal_variants.LINAL_LAB7_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab8 (matrix_b)
                VALUES ($1);
            '''
            variants = [(variant.matrix_b, ) for variant in linal_variants.LINAL_LAB8_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab9 (matrix_a, matrix_b)
                VALUES ($1, $2);
            '''
            variants = [(variant.matrix_a, variant.matrix_b) for variant in linal_variants.LINAL_LAB9_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab10 (
                    equation_1_matrix_1, equation_1_matrix_2, equation_1_coefficient,
                    equation_2_matrix_1, equation_2_matrix_2, equation_2_coefficient,
                    equation_3_matrix_1, equation_3_matrix_2, equation_3_matrix_3
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
            '''
            variants = [(
                variant.equation_1_matrix_1, variant.equation_1_matrix_2, variant.equation_1_coefficient,
                variant.equation_2_matrix_1, variant.equation_2_matrix_2, variant.equation_2_coefficient,
                variant.equation_3_matrix_1, variant.equation_3_matrix_2, variant.equation_3_matrix_3
            ) for variant in linal_variants.LINAL_LAB10_VARIANTS]

            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab11 (coefficients, results)
                VALUES ($1, $2);
            '''
            variants = [(variant.coefficients, variant.results) for variant in linal_variants.LINAL_LAB11_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab12 (coefficients, results)
                VALUES ($1, $2);
            '''
            variants = [(variant.coefficients, variant.results) for variant in linal_variants.LINAL_LAB12_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab13 (matrix_a, matrix_b, matrix_c)
                VALUES ($1, $2, $3);
            '''
            variants = [(variant.matrix_a, variant.matrix_b, variant.matrix_c) for variant in linal_variants.LINAL_LAB13_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab14 (coefficients)
                VALUES ($1);
            '''
            variants = [(variant.coefficients, ) for variant in linal_variants.LINAL_LAB14_VARIANTS]
            await connection.executemany(sql_query, variants)

            sql_query = f''' 
                INSERT INTO linal_lab15 (coefficients)
                VALUES ($1);
            '''
            variants = [(variant.coefficients, ) for variant in linal_variants.LINAL_LAB15_VARIANTS]
            await connection.executemany(sql_query, variants)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if not await is_exists_roles_table(conn):
                    await create_all_tables(conn)
                    await fill_all_tables_by_default(conn)
                    logger.info("Tables has been created")
                else:
                    logger.info("Tables are exist")

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

            student_row = dict(student_row)
            student_row["linal_marks"] = json.loads(student_row["linal_marks"])
            student_row["angem_marks"] = json.loads(student_row["angem_marks"])
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

        async def get_all_ids_into_lab(course_name: str, lab_number: int) -> list[int]:
            sql_query = f""" 
                SELECT id FROM {course_name}_lab{lab_number};
            """
            linal_lab_rows = await conn.fetch(sql_query)
            ids = [row['id'] for row in linal_lab_rows]
            return ids

        async def add_new_user(user: User, conn: PoolConnectionProxy) -> int:
            sql_query = """ 
                INSERT INTO users (name, username, password, role_id)
                VALUES
                    ($1, $2, $3, $4)
                RETURNING id;
            """
            user_row = await conn.fetchrow(sql_query, user.name, user.username, user.password, user.role_id)
            return user_row.get('id')

        async def add_new_teacher(user_id: int, conn: PoolConnectionProxy) -> int:
            sql_query = """ 
                INSERT INTO teachers (user_id)
                VALUES
                    ($1)
                RETURNING id;
            """
            teacher_row = await conn.fetchrow(sql_query, user_id)
            return teacher_row.get('id')

        async def add_new_student(user_id: int, conn: PoolConnectionProxy) -> int:
            sql_query = """ 
                INSERT INTO students (
                    user_id, linal_marks, angem_marks, group_id,
                    linal_lab1_id, linal_lab2_id, linal_lab3_id, linal_lab4_id, linal_lab5_id,
                    linal_lab6_id, linal_lab7_id, linal_lab8_id, linal_lab9_id, linal_lab10_id,
                    linal_lab11_id, linal_lab12_id, linal_lab13_id, linal_lab14_id, linal_lab15_id
                )
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
                RETURNING id;
            """
            linal_marks = [{"result": False, "approve_date": None} for _ in range(LINAL_LABS_COUNT)]
            linal_marks = json.dumps(linal_marks)
            angem_marks = [{"result": False, "approve_date": None} for _ in range(ANGEM_LABS_COUNT)]
            angem_marks = json.dumps(angem_marks)

            linal_lab1_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=1))
            linal_lab2_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=2))
            linal_lab3_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=3))
            linal_lab4_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=4))
            linal_lab5_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=5))
            linal_lab6_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=6))
            linal_lab7_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=7))
            linal_lab8_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=8))
            linal_lab9_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=9))
            linal_lab10_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=10))
            linal_lab11_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=11))
            linal_lab12_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=12))
            linal_lab13_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=13))
            linal_lab14_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=14))
            linal_lab15_id = random.choice(await get_all_ids_into_lab(course_name="linal", lab_number=15))

            student_row = await conn.fetchrow(
                sql_query, user_id, linal_marks, angem_marks, 1,
                linal_lab1_id, linal_lab2_id, linal_lab3_id, linal_lab4_id, linal_lab5_id, linal_lab6_id, linal_lab7_id,
                linal_lab8_id, linal_lab9_id, linal_lab10_id, linal_lab11_id, linal_lab12_id, linal_lab13_id,
                linal_lab14_id, linal_lab15_id
            )
            return student_row.get('id')

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                user_id = await add_new_user(user, conn)
                if user.role_id == RolesEnum.TEACHER.id:
                    teacher_id = await add_new_teacher(user_id, conn)
                elif user.role_id in (RolesEnum.STUDENT.id, RolesEnum.LEADER.id):
                    student_id = await add_new_student(user_id, conn)

    async def update_user_linal_marks(self, username: str, new_marks: list[StudentMark]) -> None:
        new_marks = json.dumps([mark_model.model_dump() for mark_model in new_marks])
        async with self._pool.acquire() as conn:
            sql_query = '''
               UPDATE students
               SET linal_marks = $1
               WHERE user_id = (
                   SELECT id
                   FROM users
                   WHERE username = $2
               );
            '''
            await conn.execute(sql_query, new_marks, username)

    async def update_user_angem_marks(self, username: str, new_marks: list[StudentMark]) -> None:
        new_marks = json.dumps([mark_model.model_dump() for mark_model in new_marks])
        async with self._pool.acquire() as conn:
            sql_query = '''
               UPDATE students
               SET angem_marks = $1
               WHERE user_id = (
                   SELECT id
                   FROM users
                   WHERE username = $2
               );
            '''
            await conn.execute(sql_query, new_marks, username)

    async def load_linal_lab1_variant(self, student_id: int) -> Optional[LinalLab1Request]:
        lab_number = 1  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab1Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab2_variant(self, student_id: int) -> Optional[LinalLab2Request]:
        lab_number = 2  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab2Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab3_variant(self, student_id: int) -> Optional[LinalLab3Request]:
        lab_number = 3  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab3Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab4_variant(self, student_id: int) -> Optional[LinalLab4Request]:
        lab_number = 4  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab4Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab5_variant(self, student_id: int) -> Optional[LinalLab5Request]:
        lab_number = 5  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab5Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab6_variant(self, student_id: int) -> Optional[LinalLab6Request]:
        lab_number = 6  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab6Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab7_variant(self, student_id: int) -> Optional[LinalLab7Request]:
        lab_number = 7  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab7Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab8_variant(self, student_id: int) -> Optional[LinalLab8Request]:
        lab_number = 8  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab8Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab9_variant(self, student_id: int) -> Optional[LinalLab9Request]:
        lab_number = 9  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab9Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab10_variant(self, student_id: int) -> Optional[LinalLab10Request]:
        lab_number = 10  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab10Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab11_variant(self, student_id: int) -> Optional[LinalLab11Request]:
        lab_number = 11  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab11Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab12_variant(self, student_id: int) -> Optional[LinalLab12Request]:
        lab_number = 12  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab12Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab13_variant(self, student_id: int) -> Optional[LinalLab13Request]:
        lab_number = 13  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab13Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab14_variant(self, student_id: int) -> Optional[LinalLab14Request]:
        lab_number = 14  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab14Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def load_linal_lab15_variant(self, student_id: int) -> Optional[LinalLab15Request]:
        lab_number = 15  # change here
        async with self._pool.acquire() as conn:
            sql_query = f'''
                SELECT linal_lab{lab_number}.*
                FROM students
                JOIN linal_lab{lab_number} ON linal_lab{lab_number}.id = students.linal_lab{lab_number}_id
                WHERE students.id = $1;
            '''
            variant_row = await conn.fetchrow(sql_query, student_id)
            if variant_row is not None:
                variant = LinalLab15Request(**variant_row)  # change here
            else:
                raise Exception  # TODO: change to correct exception and handle it in routes
            return variant

    async def add_group(self, group: StudentGroup) -> None:
        async with self._pool.acquire() as conn:
            sql_query = """ 
                INSERT INTO groups (name, teacher_id)
                VALUES
                    ($1, $2)
                RETURNING id;
            """
            group_row = await conn.fetchrow(sql_query, group.name, group.teacher_id)
            return group_row.get('id')

    async def get_all_groups(self) -> list[StudentGroup]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT * FROM groups
                ORDER BY id DESC;
            '''
            group_rows = await conn.fetch(sql_query)
            return [StudentGroup(**group) for group in group_rows]

    async def get_all_groups_and_students(self) -> list[(str, list[StudentWithResults])]:
        groups_and_students = {}

        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT groups.name as group_name, users.name as student_name, students.linal_marks as linal_marks, students.angem_marks as angem_marks
                FROM students
                JOIN users ON students.user_id = users.id
                RIGHT JOIN groups ON students.group_id = groups.id
                ORDER BY groups.name, users.name ASC;
            '''
            rows = await conn.fetch(sql_query)

            for row in rows:
                group_name = row['group_name']
                student_name = row['student_name']
                linal_marks = row['linal_marks']
                angem_marks = row['angem_marks']
                if group_name not in groups_and_students:
                    groups_and_students[group_name] = []

                linal_marks = json.loads(linal_marks)
                angem_marks = json.loads(angem_marks)
                groups_and_students[group_name].append(
                    StudentWithResults(
                        name=student_name,
                        linal_marks=linal_marks,
                        total_linal_result=sum([1 if mark_model["result"] else 0 for mark_model in linal_marks]),
                        angem_marks=angem_marks,
                        total_angem_result=sum([1 if mark_model["result"] else 0 for mark_model in angem_marks])
                    )
                )

        groups_and_students = sorted(groups_and_students.items(), key=lambda x: x[0])[::-1]

        return groups_and_students

    async def get_group_id_by_name(self, name: str) -> Optional[int]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT id
                FROM groups
                WHERE name = $1;
            '''
            group_row = await conn.fetchrow(sql_query, name)
            if group_row is not None:
                return group_row['id']
            return None

    async def get_group_by_student_id(self, student_id: int) -> Optional[StudentGroup]:
        async with self._pool.acquire() as conn:
            sql_query = '''
                SELECT *
                FROM groups    
                WHERE id = (
                   SELECT group_id
                   FROM students
                   WHERE id = $1
                );
            '''
            group_row = await conn.fetchrow(sql_query, student_id)
            if group_row is not None:
                group_row = StudentGroup(**group_row)
            return group_row

    async def get_basic_data_by_username(self, username: str) -> BasicData:
        user = await self.get_user_by_username(username)
        role_name = RolesEnum.get_role_ru_name_by_id(user.role_id)
        all_groups = await self.get_all_groups()
        all_groups = [student_group for student_group in all_groups]

        if user.role_id in (RolesEnum.STUDENT.id, RolesEnum.LEADER.id):
            student = await self.get_student_by_username(username)
            student_group = await self.get_group_by_student_id(student_id=student.id)
            return BasicData(
                user=user,
                role_name=role_name,
                all_groups=all_groups,
                student=student,
                student_group=student_group
            )
        else:
            teacher = await self.get_teacher_by_username(username)
            return BasicData(
                user=user,
                role_name=role_name,
                all_groups=all_groups,
                teacher=teacher
            )

    async def update_name_by_username(self, username: str, new_name: str, connection: PoolConnectionProxy) -> None:
        sql_query = '''
            UPDATE users
            SET name = $1
            WHERE username = $2
        '''
        await connection.execute(sql_query, new_name, username)

    async def update_additional_teacher_info(self, username: str, additional_info: AdditionalUserInfo) -> None:
        async def update_phone(connection: PoolConnectionProxy) -> None:
            sql_query = '''
                UPDATE teachers
                SET phone = $1
                WHERE user_id = (
                    SELECT id
                    FROM users
                    WHERE username = $2
                )
            '''
            await connection.execute(sql_query, additional_info.phone, username)

        async def update_email(connection: PoolConnectionProxy) -> None:
            sql_query = '''
                UPDATE teachers
                SET email = $1
                WHERE user_id = (
                    SELECT id
                    FROM users
                    WHERE username = $2
                )
            '''
            await connection.execute(sql_query, additional_info.email, username)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if additional_info.name:
                    await self.update_name_by_username(username=username, new_name=additional_info.name, connection=conn)
                if additional_info.phone:
                    await update_phone(connection=conn)
                if additional_info.email:
                    await update_email(connection=conn)

    async def update_additional_student_info(self, username: str, additional_info: AdditionalUserInfo) -> None:
        async def update_student_group(connection: PoolConnectionProxy) -> None:
            sql_query = '''
                UPDATE students
                SET group_id = (
                    SELECT id
                    FROM groups
                    WHERE name = $1
                )
                WHERE user_id = (
                   SELECT id
                   FROM users
                   WHERE username = $2
                );
            '''
            await connection.execute(sql_query, additional_info.group_name, username)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if additional_info.name:
                    await self.update_name_by_username(username=username, new_name=additional_info.name, connection=conn)
                if additional_info.group_name:
                    await update_student_group(connection=conn)


async def main():
    db_config = {
        "user": 'krukrukruzhka',
        "password": 'password',
        "database": 'LinalEducation',
        "host": 'localhost',
        "port": '5432',
        "min_size": 20,
        "max_size": 20
    }
    db = Database(db_config=db_config)
    await db.create_pool()
    # print(await db.get_all_groups_and_students())
    await db.drop_all_tables()
    await db.setup_tables()

    # user = User(name="bba", username="ggg", password="zzz", role_id=1)
    # print(await db.get_group_id_by_name('М8О-403Б-21'))


if __name__ == "__main__":
    asyncio.run(main())
