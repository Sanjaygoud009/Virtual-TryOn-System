from src.detect_pose import detect_pose
import cv2

# Use a sample image (replace with a real path)
img_path = "static/uploads/test.jpg"
output_path = "static/uploads/test_pose.jpg"
keypoints = detect_pose(img_path, output_path)
print(f"Keypoints: {len(keypoints)}")