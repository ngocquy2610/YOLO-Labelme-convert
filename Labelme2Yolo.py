import os
import pandas as pd
import json

class Labelme2Yolo:
    def __init__(self) -> None:
        pass

    def run(self, imgs_root, labels_root, labels_output_root):
        #create output folder
        if not os.path.exists(labels_output_root):
            os.makedirs(labels_output_root)

        for json_file in os.listdir(labels_root):
            with open(os.path.join(labels_root, json_file)) as f:
                data = json.load(f)
                filename = data['imagePath']
                img_width = data['imageWidth']
                img_height = data['imageHeight']

                txt_filename = os.path.splitext(json_file)[0] + ".txt"

                with open(os.path.join(labels_output_root, txt_filename), "w") as txt_file:
                    yolo_labels = []
                    for shape in data['shapes']:
                        add = []
                        if shape['label'] == '': # label
                            label = 0
                            add.append(str(label))

                        points = shape['points']

                        x1 = str(points[0][0]/img_width)
                        y1 = str(points[0][1]/img_height)
                        x2 = str(points[1][0]/img_width)
                        y2 = str(points[1][1]/img_height)

                        add.append(x1)
                        add.append(y1)
                        add.append(x1)
                        add.append(y2)
                        add.append(x2)
                        add.append(y2)
                        add.append(x2)
                        add.append(y1)

                        new_line = '\n'
                        add.append(new_line)
                        yolo_labels.append(add)

                    json_path = os.path.join(labels_root, json_file)
                    filename = os.path.splitext(os.path.basename(json_path))[0]
                    output_path = os.path.join(labels_output_root, f'{filename}.txt')

                    with open(output_path, 'a') as f:

                        for info in range(0, len(yolo_labels)):

                            f.writelines(' '.join(yolo_labels[info]))

if __name__ == '__main__':

    labelme2yolo = Labelme2Yolo()

    labelme2yolo.run(
        imgs_root = 'images', #folder imgs
        labels_root = 'json', #folder labels
        labels_output_root= 'labels' #folder output
    )