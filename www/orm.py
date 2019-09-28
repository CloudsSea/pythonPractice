import asyncio,logging,aiomysql


def log(sql,args=()):
    logging.info('SQL_%s' % sql)


async def create_pool(loop,**kw):
    logging.info('create datebase connection pool....')
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


async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            result = await cur.fetchall()
        else:
            result = await cur.fetchmany()
        await cur.close()
        logging('result len: %s' % len(result))
        return result;


async def execute(sql, args):
    log(sql,args)
    global __pool
    with (await __pool) as conn:
        try:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(sql.replace('?', '%s') % args)
            affected = cur.rowcount
            await cur.close
        except BaseException as e:
            raise
        return affected


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s,%s:%s>' % (self.__class__.__name__, self.__class__.column_type, self.__class__.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class IntegerField(Field):
    def __init__(self,name=None,primary_key=False,default=0,ddl='bigint'):
        super().__init__(name,ddl,primary_key,default)


class BooleanField(Field):
    def __init__(self,name=None,default=False,ddl='boolean'):
        super().__init__(name,ddl,default)


def FloatField(Field):
    def __init__(self,name=None,primaryKey=False,default=0.0,ddl="real"):
        super().__init__(name,ddl,primaryKey,default)

def TextField(Field):
    def __init__(self,name=None,default=None,ddl='txt'):
        super().init(name,ddl,default)


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ','.join(L)


class ModelMetaclass(type):
    # Me: 拓展/替换类的属性,拓展或替换 增,删,改,查,table,mapping,primary_key等属性
    def __init__(cls, name, bases, attrs):
        # 排除Model本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name,tableName))
        #获取所有的Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键
                    if primaryKey:
                            raise RuntimeError('Duplicate primary key for field %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found')
        for k in mappings.keys():
            # pop掉,然后后面替换?
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mapping__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)

        return type.__new__(cls,name,bases,attrs)


class Model(dict,metaclass=ModelMetaclass):

    def __init__(self,**kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s' " % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self,key):
        return getattr(self,key,None)

    def setValueOrDefault(self,key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key,str(value)))
                setattr(self,key,value)
        return value

    # classmethod修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    @classmethod
    def find(cls, pk):
        # find object by primary key
        rs = await select('%s where `%s`=?' % (cls.__select__,cls.__primary_key__, [pk], 1))
        if len(rs) == 0:
            return None
        else:
            return cls(**rs[0])

    @classmethod
    async def findAll(cls,where=None,args=None):
        sql = [cls.__select__]
        orderBy = args.get('orderBy')
        limit = args.get('limit')

        if where:
            sql.append('where')
            sql.append(where)

        if args is None:
            args = []

        if orderBy != 'a':
            sql.append('order by')
            sql.append(orderBy)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit,int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit,tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('invaid limit value: %s' % str(limit))
        rs = await select(' '.join(sql),args)
        return [cls(**r) for r in rs]

    async  def findNumber(cls, selecteField,where=None,args=None):
        sql = ['select %s _num_ from `%s` ' % (selecteField,cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql),args,1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']




    async def save(self):
        args = list(map(self.getVauleOrDefault, self.__fields__))
        #主键在参数的最后一个还得出现一次
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__,args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue(),self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__,args)
        if rows != 1:
            logging.warning('failed to update record: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove record: affected rows: %s' % rows)


