import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


def demo1():
    v1 = tf.constant([1, 2, 3, 4])
    v2 = tf.constant([1, 2, 3, 4])
    v_add = tf.matmul(v1, v2)
    with tf.Session() as sess:
        print(sess.run(v_add))


def demo2():
    zeros_s = tf.zeros([2,3],tf.int32)
    ones_t = tf.ones([2,3],tf.int32)

    range_t = tf.lin_space(2.0,5.0,5)
    range_t2 = tf.range(10)

    #创}建一个具有一定均值（默认值 = 0.0）和标准差（默认值 = 1.0）、形状为[M，N] 的正态分布随机数组：
    #正态分布
    t_random = tf.random_normal([2,3],mean=2.0,stddev=4,seed=12)


def demo3():
    sess = tf.InteractiveSession()

    I_matrix = tf.eye(5)
    print(I_matrix.eval())
    X = tf.Variable(tf.eye(10))
    X.initializer.run()
    print(X.eval())

    A = tf.Variable(tf.random_normal([5,10]))
    A.initializer.run()

    produt = tf.matmul(A,X)

    print(produt.eval())

    b  = tf.Variable(tf.random_uniform([5,10],0,2,dtype=tf.int32))
    b.initializer.run()
    print(b.eval())

    b_new = tf.cast(b,dtype=tf.float32)

    t_sum = tf.add(produt, b_new)

    t_sub = produt - b_new
    print("A*X _b\n", t_sum.eval())
    print("A*X - b\n", t_sub.eval())




if __name__ == "__main__":
    demo3()