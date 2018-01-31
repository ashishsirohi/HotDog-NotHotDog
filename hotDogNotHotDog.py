import tensorflow as tf
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

image_path = sys.argv[1]

image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line in tf.gfile.GFile("hot_dog_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

	# Sort to show labels of first prediction in order of confidence
	top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
	for type in top_k:
		hot_dog_or_not = label_lines[type]
		score = predictions[0][type]
		print('%-20s : %.5f' % (hot_dog_or_not, score))