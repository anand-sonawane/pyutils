import os, argparse
import tensorflow as tf
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio

def freeze_graph(model_dir, output_node_names):
    """Extract the sub graph defined by the output nodes and convert 
    all its variables and wights into a .pb file
    """
    if not tf.gfile.Exists(model_dir):
        raise AssertionError(
            "Export directory doesn't exists. Please specify an export "
            "directory: %s" % model_dir)

    if not output_node_names:
    	print("You need to supply the name of a node to --output_node_names.")
    	return -1

    #first we will the checkpoint path
    checkpoint = tf.train.get_checkpoint_state(model_dir)
    input_checkpoint = model_dir + "/" + checkpoint.model_checkpoint_path.split('/')[-1]

    #lets define the name for our .pb file
    output_pb_graph = model_dir + "frozen_model.pb"

    clear_devices = True

    with tf.Session(graph=tf.Graph()) as sess:

    	#lets import the meta graph into the current default graph
    	saver = tf.train.import_meta_graph(input_checkpoint + '.meta' , clear_devices = clear_devices)

    	#now lets restore the weights
    	saver.restore(sess,input_checkpoint)

    	# We use a built-in TF helper to export variables to constants
    	output_graph_def = tf.graph_util.convert_variables_to_constants(sess,tf.get_default_graph().as_graph_def(),output_node_names.split(","))

    	# Finally we serialize and dump the output graph to the filesystem
    	with tf.gfile.GFile(output_pb_graph, "wb") as f:
    		f.write(output_graph_def.SerializeToString())
    	print("%d ops in the final graph." % len(output_graph_def.node))

    return "Model saved at : " + model_dir + "/" + output_pb_graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, default="", help="Model folder to export")
    parser.add_argument("--output_node_names", type=str, default="", help="The name of the output nodes, comma separated.")
    args = parser.parse_args()

    tf.reset_default_graph()

    print(freeze_graph(args.model_dir, args.output_node_names))