#from xml.etree.ElementTree import Element, SubElement, tostring
from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString
from PIL import Image
import os

def write_to_xml(path, folder, filename, obj_class, x1, y1, x2, y2, img_w, img_h, img_d):
    
    node_root = Element('annotation')
 
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = folder
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = filename+'.jpg'
    node_path = SubElement(node_root, 'path')
    node_path.text = path

    # Source from Japan UEC food 256 dataset
    node_source = SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = 'UECfood256'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = img_w
    node_height = SubElement(node_size, 'height')
    node_height.text = img_h
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = img_d

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'

    
    node_object = SubElement(node_root, 'object')
    node_name = SubElement(node_object, 'name')
    node_name.text = obj_class
    
    node_pose = SubElement(node_object, 'pose')
    node_pose.text = 'Unspecified'
    node_truncated = SubElement(node_object, 'truncated')
    node_truncated.text = '0'
    node_difficult = SubElement(node_object, 'difficult')
    node_difficult.text = '0'


    node_bndbox = SubElement(node_object, 'bndbox')
    node_xmin = SubElement(node_bndbox, 'xmin')
    node_xmin.text = x1
    node_ymin = SubElement(node_bndbox, 'ymin')
    node_ymin.text = y1
    node_xmax = SubElement(node_bndbox, 'xmax')
    node_xmax.text = x2
    node_ymax = SubElement(node_bndbox, 'ymax')
    node_ymax.text = y2
 
    xml = tostring(node_root, pretty_print=False)  #格式化显示，该换行的换行
    dom = parseString(xml)


    directory =  "annotations/" + folder + '/'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
   
    filename =  directory +filename + ".xml" 
    f = open(filename, "wb")
    f.write(dom.toprettyxml(indent='\t', encoding='utf-8'))
    f.close()

def find_category(current):
    category = open('category.txt', "r")

    lines = category.readlines()

    for i in lines:
        i = i.strip()
        id = i.split('\t')[0]
        name = i.split('\t')[1]
        if(id == str(current)):
            return str(name);    

# Iterate 256 class, i.e., folder
for current in range(1,257):
    
    bb_path = 'original_image/' + str(current) + '/bb_info.txt'
    print("Now read bb_info.txt in directory: " + bb_path)
    bb = open( bb_path, "r")
    lines = bb.readlines()
    
    # obj_class, for example, rice
    obj_class = find_category(current)    
    print("class: " + obj_class + "is now processing. ")

    for line in lines:
        line = line.strip()
        name=line.split(' ')[0]
        x1=line.split(' ')[1]
        y1=line.split(' ')[2]
        x2=line.split(' ')[3]
        y2=line.split(' ')[4]

    
        folder = str(current)
        # path of image that write in xml
        path = '/home/wayne/workspace/food_data/original_image/' + folder + '/' + name + '.jpg'
        # folder of class, Now should be all point to images ?
        # This should be checked later
        # folder = str(current)
        # folder = 'iamges'
        # filename, for example, 1.jpg
        filename = name

        if(name!="img"):
            img = Image.open( 'original_image/' + str(current) + '/' + name + '.jpg')
            img_w, img_h = img.size
            img_d = 3
            write_to_xml(path, folder, filename, obj_class, x1, y1, x2, y2, str(img_w), str(img_h), str(img_d) )
    
    print("class: " + obj_class + '... Done.')

print("Transfer to xml Done with 1~256 category")
