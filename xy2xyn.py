import os
import json

js_path = '../data/BDD100K/labels/valid/6a0b1172-6ce71a69.json'
out_labels_path = './'
main_dir = 'xy2xyn'
all_images = list()
js_path = os.path.join(main_dir, js_path)
out_labels_path = os.path.join(main_dir, out_labels_path)

if not os.path.exists(out_labels_path):
    os.makedirs(out_labels_path)

js = json.load(open(js_path, 'r'))

annotations_by_image_id = {}
annotations_by_id = {}
for ann in js['annotations']:
    ann_id = ann['id']
    assert (ann_id not in annotations_by_id), 'error ,annotation id already in annotations_by_id'
    annotations_by_id[ann_id] = ann
    image_id = ann['image_id']
    if image_id not in annotations_by_image_id:
        annotations_by_image_id[image_id] = list()
    annotations_by_image_id[image_id].append(ann_id)

for im in js['images']:
    im_id = im['id']
    fname = os.path.basename(im['file_name']).split('.')[0]
    all_images.append(im['file_name'])
    w = im['width']
    h = im['height']
    label_name = fname + '.txt'
    with open(os.path.join(out_labels_path, label_name), 'w') as out_labels:
        if im_id in annotations_by_image_id:
            for ann_id in annotations_by_image_id[im_id]:
                ann = annotations_by_id[ann_id]
                category_id = ann['category_id'] - 1  # coco category id start with 1, and yolo category id start with 0
                out_seg = []
                for seg in ann['segmentation']:
                    for i in range(int(len(seg)/2)):
                        x = seg[i*2] / w
                        y = seg[i*2 + 1] / h
                        out_seg.append(x)
                        out_seg.append(y)
                line = str(category_id)
                for coord in out_seg:
                    line += ' ' + str(coord)
                out_labels.write(line)
                out_labels.write('\n')

with open(os.path.join(main_dir, js_path.split('.')[0] + '.txt'), 'w') as f:
    for im_name in all_images:
        f.write(im_name)
        f.write('\n')