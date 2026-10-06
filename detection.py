from datetime import datetime
import json
from . import db

class Detection(db.Model):
    __tablename__ = 'detections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(20), nullable=False) # 'Image' or 'Video'
    prediction = db.Column(db.String(50), nullable=False) # 'LIKELY REAL' or 'POSSIBLY FAKE'
    confidence = db.Column(db.Float, nullable=False)
    faces_detected = db.Column(db.Integer, default=0)
    frames_analyzed = db.Column(db.Integer, default=1)
    processing_time = db.Column(db.Float, default=0.0)
    annotated_filename = db.Column(db.String(255), nullable=True)
    sample_faces_json = db.Column(db.Text, nullable=True) # JSON list of sample crop filenames
    details_json = db.Column(db.Text, nullable=True) # JSON object with breakdown metrics
    is_demo_mode = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_sample_faces(self):
        if self.sample_faces_json:
            try:
                return json.loads(self.sample_faces_json)
            except Exception:
                return []
        return []

    def set_sample_faces(self, face_list):
        self.sample_faces_json = json.dumps(face_list)

    def get_details(self):
        if self.details_json:
            try:
                return json.loads(self.details_json)
            except Exception:
                return {}
        return {}

    def set_details(self, details_dict):
        self.details_json = json.dumps(details_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else 'Guest User',
            'filename': self.filename,
            'original_filename': self.original_filename,
            'media_type': self.media_type,
            'prediction': self.prediction,
            'confidence': round(self.confidence, 1),
            'faces_detected': self.faces_detected,
            'frames_analyzed': self.frames_analyzed,
            'processing_time': round(self.processing_time, 2),
            'annotated_filename': self.annotated_filename,
            'sample_faces': self.get_sample_faces(),
            'details': self.get_details(),
            'is_demo_mode': self.is_demo_mode,
            'created_at': self.created_at.strftime('%b %d, %Y %H:%M')
        }
