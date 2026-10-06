import cv2
import os
import uuid
import numpy as np
from .face_detection import detect_faces_in_image

def process_video_file(video_path, upload_folder, sample_frame_count=24):
    """
    Extracts frames from video, detects faces in sampled frames,
    returns aggregated statistics and representative images.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {
            'success': False,
            'error': 'Unable to open video file.',
            'frames_analyzed': 0,
            'total_faces': 0,
            'annotated_filename': None,
            'face_crops': [],
            'frame_mats': []
        }

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    duration_sec = total_frames / fps if fps > 0 else 0

    if total_frames <= 0:
        total_frames = 100 # Fallback default if stream property fails

    # Determine frame indices to sample
    sample_count = min(sample_frame_count, max(1, total_frames))
    indices = np.linspace(0, total_frames - 1, sample_count, dtype=int)

    sampled_frames = []
    all_face_crops = []
    total_faces_count = 0
    best_annotated_filename = None
    best_face_count_in_frame = -1

    for frame_idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        sampled_frames.append(frame)

        # Detect faces in this sampled frame
        num_faces, ann_filename, crops, _ = detect_faces_in_image(frame, upload_folder)
        total_faces_count += num_faces
        
        for crop in crops:
            if crop not in all_face_crops and len(all_face_crops) < 12:
                all_face_crops.append(crop)

        if num_faces > best_face_count_in_frame or best_annotated_filename is None:
            best_face_count_in_frame = num_faces
            best_annotated_filename = ann_filename

    cap.release()

    # If no annotated filename was generated (e.g. zero faces detected in any frame), create one from middle frame
    if best_annotated_filename is None and len(sampled_frames) > 0:
        mid_idx = len(sampled_frames) // 2
        _, best_annotated_filename, _, _ = detect_faces_in_image(sampled_frames[mid_idx], upload_folder)

    return {
        'success': True,
        'frames_analyzed': len(sampled_frames),
        'total_frames': total_frames,
        'fps': round(fps, 1),
        'duration_sec': round(duration_sec, 2),
        'total_faces': total_faces_count,
        'annotated_filename': best_annotated_filename,
        'face_crops': all_face_crops,
        'frame_mats': sampled_frames
    }
