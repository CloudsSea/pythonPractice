
import tensorFlow as tf
from .import input_data



mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# x = tf.placeholder("float",[None,784])
#
# W = tf.Variable(tf.zeros([784,10]))
# b = tf.Variable(tf.zeros[10])
#
# y = tf.nn.softmax(tf.matmul(x,W) + b)
#
# y_ = tf.placeholder("float",[None,10])
# cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
#
# train_step = tf.train.GrandientDescentOptimizer(0.01).minimize(cross_entropy)
#
# init = tf.initialize_all_variables()
#
# sess = tf.Session()
# sess.run(init)
#
# for i in range(1000):
#     batch_xs,batch_ys = mnist.train.next_batch(100)
