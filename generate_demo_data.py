import os
import cv2
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_media():
    uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    # 1. Create a sample face image
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (0, 0), (400, 400), (20, 30, 45), -1)
    
    # Draw simple facial outline
    cv2.ellipse(img, (200, 200), (80, 105), 0, 0, 360, (200, 215, 230), -1)
    # Eyes
    cv2.circle(img, (170, 175), 10, (40, 40, 40), -1)
    cv2.circle(img, (230, 175), 10, (40, 40, 40), -1)
    # Mouth
    cv2.ellipse(img, (200, 235), (25, 12), 0, 0, 180, (50, 50, 50), 3)

    sample_img_path = os.path.join(uploads_dir, 'sample_portrait.jpg')
    cv2.imwrite(sample_img_path, img)

    print("[DeepGuard AI Seed] Created sample portrait media.")

def seed_demo_detections():
    from app import create_app
    from models import db
    from models.user import User
    from models.detection import Detection

    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email='user@deepguard.ai').first()
        if not user:
            print("[Seed Warning] Demo user not found.")
            return

        if Detection.query.count() > 0:
            print("[Seed Info] Detection records already present.")
            return

        print("[DeepGuard AI Seed] Generating sample detection records...")

        samples = [
            ('portrait_analysis_01.jpg', 'Image', 'LIKELY REAL', 94.2, 1, 1, 0.38, False),
            ('synthetic_deepfake_face.png', 'Image', 'POSSIBLY FAKE', 91.7, 1, 1, 0.45, False),
            ('interview_stream_clip.mp4', 'Video', 'POSSIBLY FAKE', 88.4, 18, 24, 2.15, False),
            ('security_cam_verif.mp4', 'Video', 'LIKELY REAL', 96.1, 12, 24, 1.84, False),
            ('social_media_avatar.jpeg', 'Image', 'POSSIBLY FAKE', 85.9, 1, 1, 0.41, True),
        ]

        now = datetime.utcnow()

        for i, (fname, mtype, pred, conf, faces, frames, ptime, is_demo) in enumerate(samples):
            det = Detection(
                user_id=user.id,
                filename=f"demo_{i}_{fname}",
                original_filename=fname,
                media_type=mtype,
                prediction=pred,
                confidence=conf,
                faces_detected=faces,
                frames_analyzed=frames,
                processing_time=ptime,
                annotated_filename='sample_portrait.jpg',
                is_demo_mode=is_demo,
                created_at=now - timedelta(days=(5 - i), hours=i * 2)
            )
            det.set_sample_faces(['sample_portrait.jpg'])
            det.set_details({
                'spatial_score': round(conf, 1),
                'fft_ratio': 0.824,
                'fft_score': round(conf - 2, 1),
                'laplacian_blur_var': 142.0,
                'color_variance': 38.5,
                'model_info': 'PyTorch DeepGuard Neural Model'
            })
            db.session.add(det)

        db.session.commit()
        print("[DeepGuard AI Seed] Successfully seeded sample detection records.")

if __name__ == '__main__':
    create_sample_media()
    seed_demo_detections()
