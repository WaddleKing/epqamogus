import time
import numpy as np
from PIL import Image
import cv2
import pyautogui

def numpy_subimage_search(img1, img2):
    """Your NumPy-based search implementation (modified for benchmarking)."""
    img1 = np.asarray(img1)
    img2 = np.asarray(img2)
    img1y, img1x = img1.shape[:2]
    img2y, img2x = img2.shape[:2]
    stopy = img2y - img1y + 1
    stopx = img2x - img1x + 1

    for x1 in range(stopx):
        for y1 in range(stopy):
            x2 = x1 + img1x
            y2 = y1 + img1y
            pic = img2[y1:y2, x1:x2]
            if np.array_equal(pic, img1):
                return (x1, y1)
    return None

def opencv_template_match(img1, img2):
    """OpenCV's optimized template matching."""
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    return max_loc

def benchmark(small_img_path, big_img_path):
    # Load images
    small_img = cv2.imread(small_img_path)
    big_img = cv2.imread(big_img_path)
    
    if small_img is None or big_img is None:
        raise ValueError("Could not load one or both image files")
    
    # Convert to PIL for PyAutoGUI (needs RGB format)
    small_pil = Image.fromarray(cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB))
    big_pil = Image.fromarray(cv2.cvtColor(big_img, cv2.COLOR_BGR2RGB))

    # numpy
    start = time.time()
    numpy_pos = numpy_subimage_search(small_img, big_img)
    numpy_time = time.time() - start

    # pyautogui
    start = time.time()
    pyautogui_pos = pyautogui.locate(small_pil, big_pil, confidence=0.99)
    pyautogui_time = time.time() - start

    # opencv
    start = time.time()
    opencv_pos = opencv_template_match(small_img, big_img)
    opencv_time = time.time() - start

    print(f"numpy: found at {numpy_pos} in {numpy_time:.4f}s")
    print(f"pyautogui: found at {pyautogui_pos} in {pyautogui_time:.4f}s")
    print(f"opencv: found at {opencv_pos} in {opencv_time:.4f}s")
    return [numpy_time, pyautogui_time, opencv_time]

if __name__ == "__main__":
    # Replace these paths with your actual image files
    SMALL_IMG_PATH = "other/map.png"  # The template image to search for
    BIG_IMG_PATH = "screen.png"      # The larger image to search within
    
    n, p, c = [], [], []
    for j in range(10):  # Reduced from 100 to 10 for practical testing
        try:
            a = benchmark(SMALL_IMG_PATH, BIG_IMG_PATH)
            n.append(a[0])
            p.append(a[1])
            c.append(a[2])
        except Exception as e:
            print(f"Error in benchmark run {j+1}: {str(e)}")
            break
    
    if n and p and c:  # Only print results if we have data
        print("\nAverage Results:")
        print("numpy:    " + str(sum(n)/len(n)))
        print("pyautogui: " + str(sum(p)/len(p)))
        print("opencv:   " + str(sum(c)/len(c)))