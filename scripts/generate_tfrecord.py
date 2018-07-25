"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'rice':
        return 1
    elif row_label == 'eels on rice':
        return 2
    elif row_label == 'pilaf':
        return 3
    elif row_label == 'chicken-egg on rice':
        return 4
    elif row_label == 'pork cutlet on rice':
        return 5
    elif row_label == 'beef curry':
        return 6
    elif row_label == 'sushi':
        return 7
    elif row_label == 'chicken rice':
        return 8
    elif row_label == 'fried rice':
        return 9
    elif row_label == 'tempura bowl':
        return 10
    elif row_label == 'bibimbap':
        return 11
    elif row_label == 'toast':
        return 12
    elif row_label == 'croissant':
        return 13
    elif row_label == 'roll bread':
        return 14
    elif row_label == 'raisin bread':
        return 15
    elif row_label == 'chip butty':
        return 16
    elif row_label == 'hamburger':
        return 17
    elif row_label == 'pizza':
        return 18
    elif row_label == 'sandwiches':
        return 19
    elif row_label == 'udon noodle':
        return 20
    elif row_label == 'tempura udon':
        return 21
    elif row_label == 'soba noodle':
        return 22
    elif row_label == 'ramen noodle':
        return 23
    elif row_label == 'beef noodle':
        return 24
    elif row_label == 'tensin noodle':
        return 25
    elif row_label == 'fried noodle':
        return 26
    elif row_label == 'spaghetti':
        return 27
    elif row_label == 'Japanese-style pancake':
        return 28
    elif row_label == 'takoyaki':
        return 29
    elif row_label == 'gratin':
        return 30
    elif row_label == 'sauteed vegetables':
        return 31
    elif row_label == 'croquette':
        return 32
    elif row_label == 'grilled eggplant':
        return 33
    elif row_label == 'sauteed spinach':
        return 34
    elif row_label == 'vegetable tempura':
        return 35
    elif row_label == 'miso soup':
        return 36
    elif row_label == 'potage':
        return 37
    elif row_label == 'sausage':
        return 38
    elif row_label == 'oden':
        return 39
    elif row_label == 'omelet':
        return 40
    elif row_label == 'ganmodoki':
        return 41
    elif row_label == 'jiaozi':
        return 42
    elif row_label == 'stew':
        return 43
    elif row_label == 'teriyaki grilled fish':
        return 44
    elif row_label == 'fried fish':
        return 45
    elif row_label == 'grilled salmon':
        return 46
    elif row_label == 'salmon meuniere':
        return 47
    elif row_label == 'sashimi':
        return 48
    elif row_label == 'grilled pacific saury':
        return 49
    elif row_label == 'sukiyaki':
        return 50
    elif row_label == 'sweet and sour pork':
        return 51
    elif row_label == 'lightly roasted fish':
        return 52
    elif row_label == 'steamed egg hotchpotch':
        return 53
    elif row_label == 'tempura':
        return 54
    elif row_label == 'fried chicken':
        return 55
    elif row_label == 'sirloin cutlet':
        return 56
    elif row_label == 'nanbanzuke':
        return 57
    elif row_label == 'boiled fish':
        return 58
    elif row_label == 'seasoned beef with potatoes':
        return 59
    elif row_label == 'hambarg steak':
        return 60
    elif row_label == 'steak':
        return 61
    elif row_label == 'dried fish':
        return 62
    elif row_label == 'ginger pork saute':
        return 63
    elif row_label == 'spicy chili-flavored tofu':
        return 64
    elif row_label == 'yakitori':
        return 65
    elif row_label == 'cabbage roll':
        return 66
    elif row_label == 'omelet':
        return 67
    elif row_label == 'egg sunny-side up':
        return 68
    elif row_label == 'natto':
        return 69
    elif row_label == 'cold tofu':
        return 70
    elif row_label == 'egg roll':
        return 71
    elif row_label == 'chilled noodle':
        return 72
    elif row_label == 'stir-fried beef and peppers':
        return 73
    elif row_label == 'simmered pork':
        return 74
    elif row_label == 'boiled chicken and vegetables':
        return 75
    elif row_label == 'sashimi bowl':
        return 76
    elif row_label == 'sushi bowl':
        return 77
    elif row_label == 'fish-shaped pancake with bean jam':
        return 78
    elif row_label == 'shrimp with chill source':
        return 79
    elif row_label == 'roast chicken':
        return 80
    elif row_label == 'steamed meat dumpling':
        return 81
    elif row_label == 'omelet with fried rice':
        return 82
    elif row_label == 'cutlet curry':
        return 83
    elif row_label == 'spaghetti meat sauce':
        return 84
    elif row_label == 'fried shrimp':
        return 85
    elif row_label == 'potato salad':
        return 86
    elif row_label == 'green salad':
        return 87
    elif row_label == 'macaroni salad':
        return 88
    elif row_label == 'Japanese tofu and vegetable chowder':
        return 89
    elif row_label == 'pork miso soup':
        return 90
    elif row_label == 'chinese soup':
        return 91
    elif row_label == 'beef bowl':
        return 92
    elif row_label == 'kinpira-style sauteed burdock':
        return 93
    elif row_label == 'rice ball':
        return 94
    elif row_label == 'pizza toast':
        return 95
    elif row_label == 'dipping noodles':
        return 96
    elif row_label == 'hot dog':
        return 97
    elif row_label == 'french fries':
        return 98
    elif row_label == 'mixed rice':
        return 99
    elif row_label == 'goya chanpuru':
        return 100
    elif row_label == 'green curry':
        return 101
    elif row_label == 'okinawa soba':
        return 102
    elif row_label == 'mango pudding':
        return 103
    elif row_label == 'almond jelly':
        return 104
    elif row_label == 'jjigae':
        return 105
    elif row_label == 'dak galbi':
        return 106
    elif row_label == 'dry curry':
        return 107
    elif row_label == 'kamameshi':
        return 108
    elif row_label == 'rice vermicelli':
        return 109
    elif row_label == 'paella':
        return 110
    elif row_label == 'tanmen':
        return 111
    elif row_label == 'kushikatu':
        return 112
    elif row_label == 'yellow curry':
        return 113
    elif row_label == 'pancake':
        return 114
    elif row_label == 'champon':
        return 115
    elif row_label == 'crape':
        return 116
    elif row_label == 'tiramisu':
        return 117
    elif row_label == 'waffle':
        return 118
    elif row_label == 'rare cheese cake':
        return 119
    elif row_label == 'shortcake':
        return 120
    elif row_label == 'chop suey':
        return 121
    elif row_label == 'twice cooked pork':
        return 122
    elif row_label == 'mushroom risotto':
        return 123
    elif row_label == 'samul':
        return 124
    elif row_label == 'zoni':
        return 125
    elif row_label == 'french toast':
        return 126
    elif row_label == 'fine white noodles':
        return 127
    elif row_label == 'minestrone':
        return 128
    elif row_label == 'pot au feu':
        return 129
    elif row_label == 'chicken nugget':
        return 130
    elif row_label == 'namero':
        return 131
    elif row_label == 'french bread':
        return 132
    elif row_label == 'rice gruel':
        return 133
    elif row_label == 'broiled eel bowl':
        return 134
    elif row_label == 'clear soup':
        return 135
    elif row_label == 'yudofu':
        return 136
    elif row_label == 'mozuku':
        return 137
    elif row_label == 'inarizushi':
        return 138
    elif row_label == 'pork loin cutlet':
        return 139
    elif row_label == 'pork fillet cutlet':
        return 140
    elif row_label == 'chicken cutlet':
        return 141
    elif row_label == 'ham cutlet':
        return 142
    elif row_label == 'minced meat cutlet':
        return 143
    elif row_label == 'thinly sliced raw horsemeat':
        return 144
    elif row_label == 'bagel':
        return 145
    elif row_label == 'scone':
        return 146
    elif row_label == 'tortilla':
        return 147
    elif row_label == 'tacos':
        return 148
    elif row_label == 'nachos':
        return 149
    elif row_label == 'meat loaf':
        return 150
    elif row_label == 'scrambled egg':
        return 151
    elif row_label == 'rice gratin':
        return 152
    elif row_label == 'lasagna':
        return 153
    elif row_label == 'Caesar salad':
        return 154
    elif row_label == 'oatmeal':
        return 155
    elif row_label == 'fried pork dumplings served in soup':
        return 156
    elif row_label == 'oshiruko':
        return 157
    elif row_label == 'muffin':
        return 158
    elif row_label == 'popcorn':
        return 159
    elif row_label == 'cream puff':
        return 160
    elif row_label == 'doughnut':
        return 161
    elif row_label == 'apple pie':
        return 162
    elif row_label == 'parfait':
        return 163
    elif row_label == 'fried pork in scoop':
        return 164
    elif row_label == 'lamb kebabs':
        return 165
    elif row_label == 'dish consisting of stir-fried potato eggplant and green pepper':
        return 166
    elif row_label == 'roast duck':
        return 167
    elif row_label == 'hot pot':
        return 168
    elif row_label == 'pork belly':
        return 169
    elif row_label == 'xiao long bao':
        return 170
    elif row_label == 'moon cake':
        return 171
    elif row_label == 'custard tart':
        return 172
    elif row_label == 'beef noodle soup':
        return 173
    elif row_label == 'pork cutlet':
        return 174
    elif row_label == 'minced pork rice':
        return 175
    elif row_label == 'fish ball soup':
        return 176
    elif row_label == 'oyster omelette':
        return 177
    elif row_label == 'glutinous oil rice':
        return 178
    elif row_label == 'trunip pudding':
        return 179
    elif row_label == 'stinky tofu':
        return 180
    elif row_label == 'lemon fig jelly':
        return 181
    elif row_label == 'khao soi':
        return 182
    elif row_label == 'Sour prawn soup':
        return 183
    elif row_label == 'Thai papaya salad':
        return 184
    elif row_label == 'boned sliced Hainan-style chicken with marinated rice':
        return 185
    elif row_label == 'hot and sour fish and vegetable ragout':
        return 186
    elif row_label == 'stir-fried mixed vegetables':
        return 187
    elif row_label == 'beef in oyster sauce':
        return 188
    elif row_label == 'pork satay':
        return 189
    elif row_label == 'spicy chicken salad':
        return 190
    elif row_label == 'noodles with fish curry':
        return 191
    elif row_label == 'Pork Sticky Noodles':
        return 192
    elif row_label == 'Pork with lemon':
        return 193
    elif row_label == 'stewed pork leg':
        return 194
    elif row_label == 'charcoal-boiled pork neck':
        return 195
    elif row_label == 'fried mussel pancakes':
        return 196
    elif row_label == 'Deep Fried Chicken Wing':
        return 197
    elif row_label == 'Barbecued red pork in sauce with rice':
        return 198
    elif row_label == 'Rice with roast duck':
        return 199
    elif row_label == 'Rice crispy pork':
        return 200
    elif row_label == 'Wonton soup':
        return 201
    elif row_label == 'Chicken Rice Curry With Coconut':
        return 202
    elif row_label == 'Crispy Noodles':
        return 203
    elif row_label == 'Egg Noodle In Chicken Yellow Curry':
        return 204
    elif row_label == 'coconut milk soup':
        return 205
    elif row_label == 'pho':
        return 206
    elif row_label == 'Hue beef rice vermicelli soup':
        return 207
    elif row_label == 'Vermicelli noodles with snails':
        return 208
    elif row_label == 'Fried spring rolls':
        return 209
    elif row_label == 'Steamed rice roll':
        return 210
    elif row_label == 'Shrimp patties':
        return 211
    elif row_label == 'ball shaped bun with pork':
        return 212
    elif row_label == 'Coconut milk-flavored crepes with shrimp and beef':
        return 213
    elif row_label == 'Small steamed savory rice pancake':
        return 214
    elif row_label == 'Glutinous Rice Balls':
        return 215
    elif row_label == 'loco moco':
        return 216
    elif row_label == 'haupia':
        return 217
    elif row_label == 'malasada':
        return 218
    elif row_label == 'laulau':
        return 219
    elif row_label == 'spam musubi':
        return 220
    elif row_label == 'oxtail soup':
        return 221
    elif row_label == 'adobo':
        return 222
    elif row_label == 'lumpia':
        return 223
    elif row_label == 'brownie':
        return 224
    elif row_label == 'churro':
        return 225
    elif row_label == 'jambalaya':
        return 226
    elif row_label == 'nasi goreng':
        return 227
    elif row_label == 'ayam goreng':
        return 228
    elif row_label == 'ayam bakar':
        return 229
    elif row_label == 'bubur ayam':
        return 230
    elif row_label == 'gulai':
        return 231
    elif row_label == 'laksa':
        return 232
    elif row_label == 'mie ayam':
        return 233
    elif row_label == 'mie goreng':
        return 234
    elif row_label == 'nasi campur':
        return 235
    elif row_label == 'nasi padang':
        return 236
    elif row_label == 'nasi uduk':
        return 237
    elif row_label == 'babi guling':
        return 238
    elif row_label == 'kaya toast':
        return 239
    elif row_label == 'bak kut teh':
        return 240
    elif row_label == 'curry puff':
        return 241
    elif row_label == 'chow mein':
        return 242
    elif row_label == 'zha jiang mian':
        return 243
    elif row_label == 'kung pao chicken':
        return 244
    elif row_label == 'crullers':
        return 245
    elif row_label == 'eggplant with garlic sauce':
        return 246
    elif row_label == 'three cup chicken':
        return 247
    elif row_label == 'bean curd family style':
        return 248
    elif row_label == 'salt & pepper fried shrimp with shell':
        return 249
    elif row_label == 'baked salmon':
        return 250
    elif row_label == 'braised pork meat ball with napa cabbage':
        return 251
    elif row_label == 'winter melon soup':
        return 252
    elif row_label == 'steamed spareribs':
        return 253
    elif row_label == 'chinese pumpkin pie':
        return 254
    elif row_label == 'eight treasure rice':
        return 255
    elif row_label == 'hot & sour soup':
        return 256
    else:
        return 0


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    print(filename)
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), 'original_image')
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
