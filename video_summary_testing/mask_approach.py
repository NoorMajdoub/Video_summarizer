import cv2
import numpy as np

def create_vscode_layout_mask(width=800, height=600):
    mask = np.zeros((height, width), dtype=np.uint8)

    cv2.rectangle(mask, (0, 0), (60, height), 255, -1)

    cv2.rectangle(mask, (0, 0), (width, 50), 255, -1)

    cv2.rectangle(mask, (60, 50), (90, height), 255, -1)

    cv2.rectangle(mask, (width - 60, 50), (width, height), 255, -1)

    return mask

mask = create_vscode_layout_mask()
cv2.imshow("VS Code Layout Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("vscode_layout_mask.png", mask)
