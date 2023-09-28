from genericpath import exists
import os
import json
import cv2

class Yolo2Labelme:
    def __init__(self):
        pass
    


    def _yolo_label_explaination(self, yolo_label_path, image_path):
        yolo_obj = []
        #lay w, h cua image
        img = cv2.imread(image_path, 0)
        h, w = img.shape
        #mo file data yolo
        with open(yolo_label_path, "r") as yolo_label_file:
            #doc cac dong trong file yolo txt
            lines = yolo_label_file.readlines()
            for line in lines:
                #class_id, x_center, y_center, width, height = map(float, line.strip().split())
                total_params = line.strip().split()
                class_id = int(total_params[0])
                points = [((float(total_params[i]))*(float(w)), float(total_params[i+1])*(float(h))) for i in range(1, len(total_params), 2)]
                yolo_object_data = {
                    "class_id": class_id,
                    "points" : points,
                }
                yolo_obj.append(yolo_object_data)
        return yolo_obj
    
    #tao noi dung file json labelme
    def _create_labelme_json(self, image_path, yolo_obj):
        labelme_objects = []
        #doc anh de lay thong so chieu dai va chieu rong cua anh
        img = cv2.imread(image_path, 0)
        h, w = img.shape
        #noi dung phan shapes
        for yolo_object in yolo_obj:
            labelme_object = {
                "label": str(int(yolo_object["class_id"])),
                "points": yolo_object["points"],
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            labelme_objects.append(labelme_object)
        labelme_json = {
            "version": "5.3.1",
            "flags": {},
            "shapes": labelme_objects,
            "imagePath": os.path.basename(image_path),
            "imageData": None,
            "imageHeight": h,
            "imageWidth": w
        }
        return labelme_json
    
    def run(self,yolo_imgs_root,yolo_labels_root, json_output_labels_root):
        #lay danh sach cac file trong folder labels_root

        for labels_file in os.listdir(yolo_labels_root):
            if labels_file.endswith(".txt"):
                #lay path cua moi yolo_label 
                yolo_label_path = os.path.join(yolo_labels_root, labels_file)
                image_filename = os.path.splitext(labels_file)[0] + ".jpg"
                image_path = os.path.join(yolo_imgs_root, image_filename)
                
                if os.path.exists(image_path):
                    yolo_objects = self._yolo_label_explaination(yolo_label_path, image_path)
                    labelme_json = self._create_labelme_json(image_path, yolo_objects)
                    #tao duong dan file json
                    output_json_path = os.path.join(json_output_labels_root, os.path.splitext(labels_file)[0] + ".json")
                    #write du lieu vao file json
                    with open(output_json_path, "w") as json_file:
                        json.dump(labelme_json, json_file, indent=4)
                else:
                    print("Image not found")


if __name__ == '__main__':
    yolo2labelme = Yolo2Labelme()
    yolo2labelme.run(
        yolo_imgs_root= "images",
        yolo_labels_root= "labels",
        json_output_labels_root="json"
    )