import tensorflow as tf
import argparse
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio

#function to load the graph from .pb file
def load_graph(pb_filename):
    with tf.gfile.FastGFile(pb_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.reset_default_graph()
        tf.import_graph_def(graph_def, name='')

#print the layers present in the graph
def print_layer_names():
    with tf.Session() as sess:
        for operation in sess.graph.get_operations() :
            print(operation.name,operation.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pb_file", type=str, default="", help="Path to .pb model")
    args = parser.parse_args()

    load_graph(args.pb_file)
    print_layer_names()
