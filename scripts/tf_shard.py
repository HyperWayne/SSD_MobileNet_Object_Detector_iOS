import contextlib2
from google3.third_party.tensorflow_models.object_detection.dataset_tools import tf_record_creation_util

num_shards=10
output_filebase='/data/train_dataset.record'

with contextlib2.ExitStack() as tf_record_close_stack:
  output_tfrecords = tf_record_creation_util.open_sharded_output_tfrecords(
      tf_record_close_stack, output_filebase, num_shards)
  for index, example in examples:
    tf_example = create_tf_example(example)
    output_shard_index = index % num_shards
    output_tfrecords[output_shard_index].write(tf_example.SerializeToString())
