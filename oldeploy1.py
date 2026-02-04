import cv2
from ultralytics import YOLO

# 1. Load your custom model
model = YOLO("best.pt")

# 2. Set source to webcam
source = "0" 

# Helper function to update the text file
def save_detection(value):
    try:
        # 'w' mode overwrites the file completely
        with open("detect.txt", "w") as f:
            f.write(str(value))
    except Exception as e:
        print(f"Error writing file: {e}")

print("Starting Inference... (detect.txt will be updated automatically)")

# 3. Run inference
results = model.predict(source, stream=True)

# 4. Process results
for result in results:
    # --- NEW LOGIC STARTS HERE ---
    # Check if there are any detections in this frame
    if result.boxes:
        # Get the class ID of the first detection (highest confidence usually comes first)
        cls_id = int(result.boxes.cls[0])
        
        # Get the name (e.g., '100', '500') from the model's names dictionary
        detected_name = model.names[cls_id]
        
        # Save to file
        save_detection(detected_name)
        
        # Optional: Print to console so you can see it working
        print(f"Detected: {detected_name} -> Saved to detect.txt")
    else:
        # Optional: If nothing is detected, do you want to clear the file?
        # If yes, uncomment the line below. If no, the last detected note remains in the file.
        # save_detection("0")
        pass
    # --- NEW LOGIC ENDS HERE ---

    # Get the image with detections
    frame = result.plot()

    cv2.imshow("YOLOv11 Inference", frame)
    
    # Press 'Esc' to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()