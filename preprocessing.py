import cv2
import numpy as np

def extract_fft_spectrum(img_mat):
    """
    Computes 2D Fast Fourier Transform power spectrum metrics.
    Deepfake face synthesis and neural blurs introduce unnatural high-frequency power distribution.
    """
    if img_mat is None or img_mat.size == 0:
        return 0.5
    
    gray = cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY) if len(img_mat.shape) == 3 else img_mat
    h, w = gray.shape
    if h < 16 or w < 16:
        return 0.5

    # 2D FFT
    f = np.fft.fft2(gray.astype(float))
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)

    # Compute high frequency vs low frequency energy ratio
    cy, cx = h // 2, w // 2
    r = min(h, w) // 6

    # Mask for low frequency core
    y_idx, x_idx = np.ogrid[:h, :w]
    mask = (x_idx - cx)**2 + (y_idx - cy)**2 <= r**2

    low_freq_energy = np.mean(magnitude_spectrum[mask])
    high_freq_energy = np.mean(magnitude_spectrum[~mask])

    ratio = high_freq_energy / (low_freq_energy + 1e-5)
    return float(ratio)

def extract_laplacian_variance(img_mat):
    """
    Measures facial texture sharpness & unnatural smoothing artifacts.
    """
    if img_mat is None or img_mat.size == 0:
        return 0.0
    gray = cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY) if len(img_mat.shape) == 3 else img_mat
    var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return float(var)

def extract_color_chrominance_variance(img_mat):
    """
    Deepfakes often show chrominance channel mismatches in YCrCb color space.
    """
    if img_mat is None or img_mat.size == 0:
        return 0.0
    ycrcb = cv2.cvtColor(img_mat, cv2.COLOR_BGR2YCrCb)
    _, cr, cb = cv2.split(ycrcb)
    std_cr = np.std(cr)
    std_cb = np.std(cb)
    return float(std_cr + std_cb)

def preprocess_face_for_model(img_mat, target_size=(224, 224)):
    """
    Resizes, normalizes and formats image for PyTorch / ML tensor input.
    """
    if img_mat is None or img_mat.size == 0:
        return np.zeros((3, target_size[0], target_size[1]), dtype=np.float32)

    resized = cv2.resize(img_mat, target_size)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # Normalize with standard ImageNet mean and std
    norm = rgb.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    norm = (norm - mean) / std

    # Transpose HWC -> CHW format
    tensor = np.transpose(norm, (2, 0, 1))
    return tensor
