import numpy as np
import cv2
import time

DEGREE = 45

def rotate(image, degree):
    t = degree / 180 * 3.1415926
    sint = np.sin(t)
    cost = np.cos(t)
    ret = np.ndarray(originalImage.shape, np.uint8)
    (H, W, C) = originalImage.shape
    ox = W / 2
    oy = H / 2
    print(ox, oy)
    for c in range(C):
        for y in range(H):
            for x in range(W):
                x1 = x - ox
                y1 = y - oy
                xr = int(x1 * cost - y1 * sint + ox)
                yr = int(x1 * sint + y1 * cost + oy)
                if (xr > 0 and xr < W and yr > 0 and yr < H):
                    ret[yr,xr,c] = image[y,x,c]
                #ret[y,x,c] = image[y,x,c]
    return ret

originalImage = cv2.imread('landscape.jpg', cv2.IMREAD_COLOR)
begin = time.time()
cv2.imshow('original image', originalImage)
end = time.time()
print('show image: {:.3f} s'.format(end-begin))

begin = time.time()
rotatedImage = rotate(originalImage, DEGREE)
end = time.time()
print('rotate image: {:.3f} s'.format(end-begin))

cv2.imshow('rotated image', rotatedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
