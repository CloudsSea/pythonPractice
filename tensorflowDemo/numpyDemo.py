import numpy as np


def arrayDemo():
    a = np.array([1,2,3])
    print(a)

    b = np.array([1,2,3,4],ndmin=2)
    print(b)

    c = np.array([1,2,3], dtype=complex)

    print(c)
def dtypeDemo():
    dt = np.dtype(np.int32)
    print(dt)

    dt2 = np.dtype([('age',np.int8)])
    print(dt2)

    a = np.array([(10,),(20,)],dtype=dt2)
    print(a)
    print(a['age'])

def arrayProperties():
    #形状
    a = np.arange(24)
    print(a.ndim)
    #更改形状
    b = a.reshape(2,4,3)
    print(b.ndim)

    x  = np.array([1,2,3,4,5], dtype=np.float64)
    # 内存
    print(x.itemsize)
    # 内存信息
    print(x.flags)

def createArray():
    # empty  数组元素为随机值，因为它们未初始化
    x = np.empty([3,2], dtype=int)
    print(x)
    # zeros
    y = np.zeros(5)
    print(y)
    # ones
    z = np.ones(5)
    print(z)

def createArrayFromArray():
    #列表
    x = [1,2,3]
    a = np.asarray(x)
    print(a)
    #元组
    y = (1,2,3)
    b = np.asarray(y)
    print(b)
    #元组列表
    z = [(1,2,3),(4,5)]
    c = np.asarray(z)
    print(z)

    # 设置了 dtype 参数
    x1 = [1,2,3]
    a1 = np.asarray(x,dtype = float)
    print(a1)

    # frombuffer 动态数组;以流的形式读入转化成 ndarray 对象
    s = b'Hello World'
    a2 = np.frombuffer(s, dtype= 'S1')
    print (a2)

    # 可迭代对象中建立
    list = range(5)
    it= iter(list)
    x2 = np.fromiter(it,dtype=float
                     )
    print(x)







if __name__ == "__main__":
    #arrayProperties()
    # createArray()
    # createArrayFromArray()
    createArrayFromArray()