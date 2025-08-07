from ultralytics import YOLO

# Load a yolo1v11.n PyTorch model
model = YOLO("best_yolov12n.pt")

# export model to NCNN format
model.export(format="ncnn", imgsz=640) #creates "yolo11n_ncnn_model"
