urdu_chars = [
   'آ', 'ا', 'ب', 'پ', 'ت', 'ٹ', 'ث', 'ج', 'چ', 'ح', 'خ',
   'د', 'ڈ', 'ذ', 'ر', 'ڑ', 'ز', 'ژ', 'س', 'ش', 'ص',
   'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل',
   'م', 'ن', 'ں', 'و', 'ہ', 'ھ', 'ء', 'ی', 'ے', 'ئ', 'ؤ', 'ۂ', ' '
]

characters = ['-'] + urdu_chars
char_to_index = {ch: i for i, ch in enumerate(characters)}
index_to_char = {i: ch for ch, i in char_to_index.items()}
num_classes = len(characters)

def binarize_image(image, method='otsu'):
    """
    Binarize an image using different methods.
    
    Args:
        image: PIL Image object
        method: Binarization method: 'simple', 'otsu', 'adaptive', or 'sauvola'
    
    Returns:
        Binarized PIL Image
    """
    import numpy as np
    from PIL import Image, ImageFilter
    
    # Convert to grayscale if not already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to numpy array
    img_array = np.array(image)
    
    if method == 'simple':
        # Simple thresholding
        threshold = 127
        binary_array = (img_array > threshold) * 255
    
    elif method == 'otsu':
        # Otsu's method (requires cv2)
        import cv2
        img_cv = np.array(image)
        _, binary_array = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    elif method == 'adaptive':
        # Adaptive thresholding (requires cv2)
        import cv2
        img_cv = np.array(image)
        # Block size must be odd and > 1
        binary_array = cv2.adaptiveThreshold(img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
    
    elif method == 'sauvola':
        # Sauvola's method - good for document images
        from skimage.filters import threshold_sauvola
        from skimage import img_as_ubyte
        
        # Get threshold map
        window_size = 25
        thresh_sauvola = threshold_sauvola(img_array, window_size=window_size)
        
        # Apply threshold
        binary_array = img_as_ubyte(img_array > thresh_sauvola)
    
    else:
        raise ValueError(f"Unknown binarization method: {method}")
    
    # Convert back to PIL Image
    binary_image = Image.fromarray(binary_array.astype('uint8'))
    return binary_image