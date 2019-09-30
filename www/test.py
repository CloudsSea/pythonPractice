from models import User,Blog,Comment
import  orm
import asyncio


async def test(loop):
    await orm.create_pool(loop=loop,host='39.105.167.124',user='root',password='123456',db='yelp')

    u = User(name='Test',email='123@sina.com',passwd='123456',image='abcout:blank')
    await u.save()
    ## 网友指出添加到数据库后需要关闭连接池，否则会报错 RuntimeError: Event loop is closed
    orm.__pool.close()
    await orm.__pool.wait_closed()

    # orm.__pool.close()
    # await  orm.__pool.wait_closed()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()
