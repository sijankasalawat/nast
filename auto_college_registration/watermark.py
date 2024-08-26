# import cv2
# import numpy as np

# def detect_watermark(image_path, watermark_text):
#     # Load the image
#     image = cv2.imread(image_path)
#     if image is None:
#         return False

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Use template matching to detect the watermark
#     result = cv2.matchTemplate(gray, watermark_text, cv2.TM_CCOEFF_NORMED)

#     # Define a threshold for detection
#     threshold = 0.8
#     loc = np.where(result >= threshold)

#     # If we found a match, return True
#     if np.any(loc[0]):
#         return True
#     return False
import cv2
import numpy as np

def detect_watermark_frequency(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Failed to load image.")
        return False

    # Perform Fourier Transform
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    # Calculate the magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

    # Analyze the frequency domain for watermark patterns
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask to filter out the low frequencies (center)
    mask = np.ones((rows, cols, 2), np.uint8)
    r = 50  # Radius around the center to keep low frequencies
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 0

    # Apply the mask and inverse DFT
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    # Threshold the result to detect high-frequency patterns (potential watermarks)
    _, thresh = cv2.threshold(img_back, 120, 255, cv2.THRESH_BINARY)

    # If any high-frequency patterns are detected, assume a watermark is present
    if np.sum(thresh) > 0:
        return True
    return False
