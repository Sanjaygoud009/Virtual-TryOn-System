import cv2
import numpy as np
from scipy.interpolate import Rbf

def tps_warp(source_img, source_points, target_points, target_shape):
    h, w = target_shape[:2]
    source_img = cv2.resize(source_img, (int(np.max(source_points[:, 0])), int(np.max(source_points[:, 1]))))
    warp_img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Normalize points
    source_points = source_points.astype(float)
    target_points = target_points.astype(float)
    source_points[:, 0] /= source_img.shape[1]
    source_points[:, 1] /= source_img.shape[0]
    target_points[:, 0] /= w
    target_points[:, 1] /= h

    # Thin Plate Spline interpolation
    rbf_x = Rbf(source_points[:, 0], source_points[:, 1], target_points[:, 0], function='thin_plate')
    rbf_y = Rbf(source_points[:, 0], source_points[:, 1], target_points[:, 1], function='thin_plate')

    for y in range(h):
        for x in range(w):
            sx = x / w
            sy = y / h
            tx = rbf_x(sx, sy) * source_img.shape[1]
            ty = rbf_y(sx, sy) * source_img.shape[0]
            if 0 <= tx < source_img.shape[1] and 0 <= ty < source_img.shape[0]:
                warp_img[y, x] = cv2.getRectSubPix(source_img, (1, 1), (tx, ty)) * 255

    # Create mask
    mask = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            sx = x / w
            sy = y / h
            tx = rbf_x(sx, sy) * source_img.shape[1]
            ty = rbf_y(sx, sy) * source_img.shape[0]
            if 0 <= tx < source_img.shape[1] and 0 <= ty < source_img.shape[0]:
                mask[y, x] = 255

    return warp_img, mask

def blend_clothing(user_img, warped_cloth, warped_mask, center):
    # Ensure mask is binary
    _, mask = cv2.threshold(warped_mask, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Blend images
    user_bg = cv2.bitwise_and(user_img, user_img, mask=mask_inv)
    cloth_fg = cv2.bitwise_and(warped_cloth, warped_cloth, mask=mask)

    # Seamless cloning for natural blend
    result = cv2.seamlessClone(cloth_fg, user_img, mask, center, cv2.NORMAL_CLONE)
    return result

def warp_clothing(user_image_path, clothing_image_path, output_path):
    # Load images
    user_img = cv2.imread(user_image_path)
    cloth_img = cv2.imread(clothing_image_path)

    if user_img is None or cloth_img is None:
        raise ValueError("Failed to load images")

    # Load keypoints (assuming saved from detect_pose)
    keypoints = np.load('static/uploads/user_keypoints.npy')
    if keypoints.size == 0:
        raise ValueError("No keypoints found")

    # Define key points for warping
    cloth_points = np.array([
        [0, 0], [cloth_img.shape[1]-1, 0], [0, cloth_img.shape[0]-1]
    ])
    user_points = np.array([keypoints[11], keypoints[12], keypoints[24]])  # Shoulders and hip

    # Warp clothing
    warped_cloth, warped_mask = tps_warp(cloth_img, cloth_points, user_points, user_img.shape[:2])
    center = (int((keypoints[11][0] + keypoints[12][0]) / 2), int(keypoints[23][1]))
    blended_img = blend_clothing(user_img, warped_cloth, warped_mask, center)

    # Save result
    cv2.imwrite(output_path, blended_img)
    return output_path

if __name__ == "__main__":
    user_path = "static/uploads/user.jpg"
    cloth_path = "static/uploads/cloth_0_clothing.jpg"
    output_path = "static/uploads/tryon_result.jpg"
    warp_clothing(user_path, cloth_path, output_path)