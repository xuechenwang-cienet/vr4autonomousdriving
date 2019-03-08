import cv2
import base64

image = cv2.imread("/home/xcwang/Pictures/Screenshot.png")
# cv2.imshow("image", image)
# cv2.waitKey(0)
_, buf = cv2.imencode('.png', image)
# raw_image = raw_image.copy(order='C')
print(type(base64.b64encode(buf)))
print(base64.b64encode(buf))
