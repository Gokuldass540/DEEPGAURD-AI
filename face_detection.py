import cv2
import os
import uuid
import numpy as np

def get_face_cascade():
    if hasattr(cv2, 'CascadeClassifier'):
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            cascade = cv2.CascadeClassifier(cascade_path)
            if not cascade.empty():
                return cascade
        except Exception:
            pass
    return None

FACE_CASCADE = get_face_cascade()

def detect_faces_in_image(image_path_or_mat, upload_folder):
    """
    Detects faces in an image using OpenCV with fallback spatial heuristic.
    Returns:
    - faces_detected_count (int)
    - annotated_filename (str)
    - face_crops (list of relative crop file paths)
    - bounding_boxes (list of (x, y, w, h))
    """
    if isinstance(image_path_or_mat, str):
        img = cv2.imread(image_path_or_mat)
        base_name = os.path.basename(image_path_or_mat)
    else:
        img = image_path_or_mat.copy()
        base_name = f"mat_{uuid.uuid4().hex[:6]}.jpg"

    if img is None:
        return 0, None, [], []

    h_img, w_img = img.shape[:2]
    faces = []

    # Method 1: Haar Cascade if available
    cascade = get_face_cascade()
    if cascade is not None:
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
            for (x, y, w, h) in detected:
                faces.append((int(x), int(y), int(w), int(h)))
        except Exception as e:
            print(f"[Face Detection Warning] Cascade failed: {e}")

    # Method 2: Fallback Skin-tone / Facial Region Spatial Detection if no faces found
    if len(faces) == 0:
        try:
            ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            # Skin tone thresholding in YCrCb space
            min_YCrCb = np.array([0, 133, 77], np.uint8)
            max_YCrCb = np.array([255, 173, 127], np.uint8)
            skin_mask = cv2.inRange(ycrcb, min_YCrCb, max_YCrCb)

            contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > (h_img * w_img * 0.03): # At least 3% of image area
                    x, y, w, h = cv2.boundingRect(cnt)
                    aspect_ratio = float(w) / h
                    if 0.5 <= aspect_ratio <= 1.5:
                        faces.append((int(x), int(y), int(w), int(h)))
        except Exception:
            pass

    # Method 3: Fallback Central Region if still no faces found
    if len(faces) == 0:
        crop_w = int(w_img * 0.45)
        crop_h = int(h_img * 0.55)
        crop_x = int((w_img - crop_w) / 2)
        crop_y = int((h_img - crop_h) / 3)
        faces.append((crop_x, crop_y, crop_w, crop_h))

    annotated = img.copy()
    face_crops = []
    bounding_boxes = []

    os.makedirs(upload_folder, exist_ok=True)

    for i, (x, y, w, h) in enumerate(faces):
        bounding_boxes.append((x, y, w, h))
        
        # Add padding around face crop
        pad_h = int(h * 0.12)
        pad_w = int(w * 0.12)
        y1 = max(0, y - pad_h)
        y2 = min(h_img, y + h + pad_h)
        x1 = max(0, x - pad_w)
        x2 = min(w_img, x + w + pad_w)

        crop = img[y1:y2, x1:x2]
        if crop.size > 0:
            crop_resized = cv2.resize(crop, (224, 224))
            crop_filename = f"crop_{uuid.uuid4().hex[:8]}_{i}.jpg"
            crop_path = os.path.join(upload_folder, crop_filename)
            cv2.imwrite(crop_path, crop_resized)
            face_crops.append(crop_filename)

        # Draw tech-styled cyan bounding box with corner marks
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 240, 0), 2)
        
        # Corner accents
        line_len = int(min(w, h) * 0.2)
        cv2.line(annotated, (x, y), (x + line_len, y), (0, 255, 255), 3)
        cv2.line(annotated, (x, y), (x, y + line_len), (0, 255, 255), 3)
        cv2.line(annotated, (x + w, y), (x + w - line_len, y), (0, 255, 255), 3)
        cv2.line(annotated, (x + w, y), (x + w, y + line_len), (0, 255, 255), 3)

        label = f"FACE #{i+1} | AI INSPECT"
        cv2.putText(annotated, label, (x, max(18, y - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)

    # Save annotated image
    annotated_filename = f"annotated_{uuid.uuid4().hex[:8]}_{base_name}"
    if not annotated_filename.endswith('.jpg'):
        annotated_filename += '.jpg'
    annotated_path = os.path.join(upload_folder, annotated_filename)
    cv2.imwrite(annotated_path, annotated)

    return len(faces), annotated_filename, face_crops, bounding_boxes
