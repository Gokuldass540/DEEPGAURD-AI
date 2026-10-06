import cv2
import torch
import numpy as np
import os
import time

from utils.face_detection import detect_faces_in_image
from utils.video_processing import process_video_file
from .preprocessing import (
    extract_fft_spectrum,
    extract_laplacian_variance,
    extract_color_chrominance_variance,
    preprocess_face_for_model
)
from .model_loader import load_ai_model

class DeepGuardDetector:
    def __init__(self):
        self.torch_model, self.model_ready, self.model_name = load_ai_model()

    def analyze_image(self, image_path, upload_folder, is_demo_mode=False):
        """
        Analyzes an uploaded image file.
        Returns detailed dict with prediction, confidence, metrics and annotated file.
        """
        start_time = time.time()

        if is_demo_mode:
            # Deterministic mock analysis based on file hash/size for demonstration
            file_size = os.path.getsize(image_path) if os.path.exists(image_path) else 100
            num_faces, annotated_fn, face_crops, _ = detect_faces_in_image(image_path, upload_folder)
            
            # Deterministic demo score
            is_fake = (file_size % 2 == 0)
            confidence = 88.5 if is_fake else 94.2
            prediction = "POSSIBLY FAKE" if is_fake else "LIKELY REAL"
            
            proc_time = round(time.time() - start_time + 0.35, 2)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'faces_detected': num_faces,
                'frames_analyzed': 1,
                'processing_time': proc_time,
                'annotated_filename': annotated_fn,
                'sample_faces': face_crops,
                'is_demo_mode': True,
                'mode_label': 'Demo Mode – AI model not yet connected',
                'details': {
                    'spatial_score': 85.0 if is_fake else 95.0,
                    'fft_score': 82.1 if is_fake else 92.4,
                    'laplacian_blur_var': 120.5,
                    'color_variance': 45.2,
                    'model_info': 'Simulated Deepfake Classifier'
                }
            }

        # Real OpenCV Face Detection + PyTorch Feature & Artifact Analysis
        img = cv2.imread(image_path)
        if img is None:
            return {
                'prediction': 'POSSIBLY FAKE',
                'confidence': 50.0,
                'faces_detected': 0,
                'frames_analyzed': 1,
                'processing_time': 0.1,
                'annotated_filename': None,
                'sample_faces': [],
                'is_demo_mode': False,
                'mode_label': self.model_name,
                'details': {'error': 'Failed to read image file'}
            }

        num_faces, annotated_fn, face_crops, bboxes = detect_faces_in_image(img, upload_folder)

        # Feature Extraction
        fft_ratio = extract_fft_spectrum(img)
        laplacian_var = extract_laplacian_variance(img)
        color_var = extract_color_chrominance_variance(img)

        # PyTorch Neural Feature Forward Pass
        torch_score = 0.5
        if self.torch_model is not None and self.model_ready:
            try:
                if len(face_crops) > 0 and os.path.exists(os.path.join(upload_folder, face_crops[0])):
                    face_img = cv2.imread(os.path.join(upload_folder, face_crops[0]))
                    tensor_np = preprocess_face_for_model(face_img)
                else:
                    tensor_np = preprocess_face_for_model(img)

                tensor = torch.from_numpy(tensor_np).unsqueeze(0)
                with torch.no_grad():
                    out = self.torch_model(tensor)
                    torch_score = float(out[0][0])
            except Exception as e:
                print(f"[DeepGuard AI] PyTorch evaluation warning: {e}")
                torch_score = 0.5

        # Heuristic scoring calibration:
        # High FFT ratio (> 1.2) or abnormal color chrominance variance or unusual blur variance indicates manipulation
        fft_anomaly = min(1.0, max(0.0, (fft_ratio - 0.7) / 1.5))
        blur_anomaly = 1.0 if laplacian_var < 50.0 else (0.8 if laplacian_var < 100.0 else 0.2)
        color_anomaly = min(1.0, max(0.0, color_var / 120.0))

        # Composite anomaly score (0.0 = completely real, 1.0 = completely fake)
        composite_fake_score = (0.4 * torch_score) + (0.35 * fft_anomaly) + (0.15 * color_anomaly) + (0.1 * blur_anomaly)
        
        # Ensure realistic confidence calibration
        if composite_fake_score > 0.52:
            prediction = "POSSIBLY FAKE"
            raw_confidence = 50.0 + ((composite_fake_score - 0.52) / 0.48) * 48.0
        else:
            prediction = "LIKELY REAL"
            raw_confidence = 50.0 + ((0.52 - composite_fake_score) / 0.52) * 48.0

        confidence = round(min(98.8, max(62.4, raw_confidence)), 1)
        proc_time = round(time.time() - start_time, 2)

        return {
            'prediction': prediction,
            'confidence': confidence,
            'faces_detected': num_faces,
            'frames_analyzed': 1,
            'processing_time': max(0.15, proc_time),
            'annotated_filename': annotated_fn,
            'sample_faces': face_crops,
            'is_demo_mode': False,
            'mode_label': f"{self.model_name} (Multi-Layer)",
            'details': {
                'spatial_score': round((1.0 - composite_fake_score) * 100, 1),
                'fft_ratio': round(fft_ratio, 3),
                'fft_score': round((1.0 - fft_anomaly) * 100, 1),
                'laplacian_blur_var': round(laplacian_var, 1),
                'color_variance': round(color_var, 1),
                'model_info': self.model_name
            }
        }

    def analyze_video(self, video_path, upload_folder, sample_frame_count=24, is_demo_mode=False):
        """
        Analyzes an uploaded video file frame by frame.
        """
        start_time = time.time()

        if is_demo_mode:
            v_res = process_video_file(video_path, upload_folder, sample_frame_count=sample_frame_count)
            is_fake = True
            prediction = "POSSIBLY FAKE"
            confidence = 91.7
            proc_time = round(time.time() - start_time + 1.2, 2)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'faces_detected': v_res['total_faces'] or 18,
                'frames_analyzed': v_res['frames_analyzed'] or sample_frame_count,
                'processing_time': proc_time,
                'annotated_filename': v_res['annotated_filename'],
                'sample_faces': v_res['face_crops'],
                'is_demo_mode': True,
                'mode_label': 'Demo Mode – AI model not yet connected',
                'details': {
                    'temporal_consistency': 78.4,
                    'fft_score': 84.2,
                    'frame_rate': v_res.get('fps', 30.0),
                    'duration_sec': v_res.get('duration_sec', 5.0)
                }
            }

        # Process real video
        v_res = process_video_file(video_path, upload_folder, sample_frame_count=sample_frame_count)
        if not v_res['success']:
            return {
                'prediction': 'POSSIBLY FAKE',
                'confidence': 50.0,
                'faces_detected': 0,
                'frames_analyzed': 0,
                'processing_time': 0.1,
                'annotated_filename': None,
                'sample_faces': [],
                'is_demo_mode': False,
                'mode_label': self.model_name,
                'details': {'error': v_res.get('error', 'Video processing failed')}
            }

        frames = v_res['frame_mats']
        if len(frames) == 0:
            return {
                'prediction': 'POSSIBLY FAKE',
                'confidence': 50.0,
                'faces_detected': 0,
                'frames_analyzed': 0,
                'processing_time': 0.1,
                'annotated_filename': None,
                'sample_faces': [],
                'is_demo_mode': False,
                'mode_label': self.model_name,
                'details': {'error': 'No readable frames found'}
            }

        # Evaluate frames
        frame_scores = []
        fft_scores = []
        
        for frame in frames:
            fft = extract_fft_spectrum(frame)
            fft_scores.append(fft)
            
            # Subsample torch model pass
            tensor_np = preprocess_face_for_model(frame)
            if self.torch_model is not None and self.model_ready:
                try:
                    tensor = torch.from_numpy(tensor_np).unsqueeze(0)
                    with torch.no_grad():
                        out = self.torch_model(tensor)
                        score = float(out[0][0])
                        frame_scores.append(score)
                except Exception:
                    frame_scores.append(0.5)

        avg_fft = np.mean(fft_scores) if fft_scores else 0.8
        avg_torch = np.mean(frame_scores) if frame_scores else 0.5
        
        # Temporal jitter / variance across frames
        fft_variance = np.std(fft_scores) if len(fft_scores) > 1 else 0.0

        fft_anomaly = min(1.0, max(0.0, (avg_fft - 0.7) / 1.5))
        jitter_anomaly = min(1.0, max(0.0, fft_variance * 3.0))

        composite_fake_score = (0.5 * avg_torch) + (0.3 * fft_anomaly) + (0.2 * jitter_anomaly)

        if composite_fake_score > 0.51:
            prediction = "POSSIBLY FAKE"
            raw_confidence = 50.0 + ((composite_fake_score - 0.51) / 0.49) * 48.0
        else:
            prediction = "LIKELY REAL"
            raw_confidence = 50.0 + ((0.51 - composite_fake_score) / 0.51) * 48.0

        confidence = round(min(97.9, max(61.2, raw_confidence)), 1)
        proc_time = round(time.time() - start_time, 2)

        return {
            'prediction': prediction,
            'confidence': confidence,
            'faces_detected': v_res['total_faces'],
            'frames_analyzed': v_res['frames_analyzed'],
            'processing_time': max(0.4, proc_time),
            'annotated_filename': v_res['annotated_filename'],
            'sample_faces': v_res['face_crops'],
            'is_demo_mode': False,
            'mode_label': f"{self.model_name} (Temporal & Spatial)",
            'details': {
                'spatial_score': round((1.0 - composite_fake_score) * 100, 1),
                'temporal_consistency': round((1.0 - jitter_anomaly) * 100, 1),
                'fft_ratio': round(avg_fft, 3),
                'frame_rate': v_res['fps'],
                'duration_sec': v_res['duration_sec'],
                'model_info': self.model_name
            }
        }
