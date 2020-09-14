import logging; logging.basicConfig(level=logging.INFO)
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

async def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    async with __pool.get() as comm:
        async with comm.cursor() as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                #返回指定条数的数据
                rs = await cur.fetchmany(size)
            else:
                #返回全部数据
                rs = await cur.fetchall()
            logging.info('rows returned: %s' % len(rs))
            return rs

async def excute(sql,ages,aotucommit=True):
    log(sql)
    async with __pool.get() as comm:
        if not aotucommit:
            await comm.begin()
        try:
            async with comm.cursor() as cur:
                await cur.execute(sql.replace(),ages or ())
                affected = cur.rowcount
                if not aotucommit:
                    await comm.begin()
                return affected
        except BaseException as a:
            if not aotucommit:
                await comm.rollback()
                raise