import cv2
import numpy as np
import mediapipe as mp

def detect_pose(image_path, output_path):
    try:
        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Failed to load image")
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process pose
        results = pose.process(img_rgb)
        keypoints = []
        
        # Extract keypoints
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                h, w = img.shape[:2]
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
                keypoints.append([cx, cy])
            keypoints = np.array(keypoints)
            np.save('static/uploads/user_keypoints.npy', keypoints)
        else:
            raise ValueError("No pose detected")
        
        # Save output
        cv2.imwrite(output_path, img)
        
        # Clean up
        pose.close()
        return keypoints
    except Exception as e:
        print(f"Pose detection error: {str(e)}")
        return np.array([])