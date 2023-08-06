#!/usr/bin/env python
import ssl

import aiomysql

from rss.auth import auth as Accounts
from codefast.asyncio import async_render
from codefast.exception import get_exception_str
import codefast as cf

"""
CREATE TABLE `rss` (
	`id` int NOT NULL AUTO_INCREMENT,
	`title` text NOT NULL,
	`content` text NOT NULL,
	`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (`id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;
"""
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_cert = [f for f in Accounts.ssl_cert if cf.io.exists(f)].pop()
ctx.load_verify_locations(cafile=ssl_cert)
dbname = "rss"

async def create_pool():
    return await aiomysql.create_pool(
        host=Accounts.host,
        port=3306,
        user=Accounts.username,
        password=Accounts.password,
        db=Accounts.database,
        ssl=ctx,
    )

async def load_all():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM {}".format(dbname))
            resp = await cur.fetchall()
            return resp 
    

async def load_data(key:str, limits:int=10000):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM {} WHERE `title` = '{}' ORDER BY `id` DESC LIMIT {}".format(dbname, key, limits))
            resp = await cur.fetchall() 
            return resp


async def insert_once(key: str, value: str):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            cmd = 'INSERT INTO {} (`title`, `content`) VALUES ("{}", "{}") ON DUPLICATE KEY UPDATE `title` = "{}"'.format(dbname, key, value, value)
            resp = await cur.execute(cmd)
            await conn.commit()
            return resp

async def insert_many(data: dict):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            cmd = 'INSERT INTO {} (`title`, `content`) VALUES '.format(dbname)
            for k, v in data.items():
                cmd += '("{}", "{}"),'.format(k, v)
            cmd = cmd[:-1]
            try:
                resp = await cur.execute(cmd)
                await conn.commit()
                return resp
            except Exception as e:
                error = get_exception_str(e)
                msg = {'cmd': cmd, 'error': error}
                await async_render(cf.info, msg)
                return None
                

