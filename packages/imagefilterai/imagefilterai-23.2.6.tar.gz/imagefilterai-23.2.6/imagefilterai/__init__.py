import cv2 # pip install opencv-python
from numpy import* # pip install numpy

def bw(path):

    image = cv2.imread(path)

    bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite('bwimage.png', bw)

def removebackground(path):

    image = cv2.imread(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
    mask = 255 - mask

    kernel = ones((3,3), uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = (2*(mask.astype(float32))-255).clip(0, 255).astype(uint8)

    result = image.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    cv2.imwrite('imagewithoutbackground.png', result)

def blur(path, stage):

    image = cv2.imread(path)

    if stage == 'extra':
        blur = cv2.GaussianBlur(image, (99, 99), 0)
    if stage == 'meddium':
        blur = cv2.GaussianBlur(image, (75, 75), 0)
    else:
        blur = cv2.GaussianBlur(image, (51, 51), 0)

    cv2.imwrite('blurredimage.png', blur)

def cartoon(path):

    image = cv2.imread(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    color = cv2.bilateralFilter(image, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, image, mask = edges)
    cv2.imwrite('cartoonimage.png', cartoon)

def rotate(path, gradus):

    image = cv2.imread(path)

    (height, weight, d) = image.shape
    center = (weight // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, gradus, 1.0)
    rotate = cv2.warpAffine(image, matrix, (weight, height))
    cv2.imwrite('rotatedimage.png', rotate)
    