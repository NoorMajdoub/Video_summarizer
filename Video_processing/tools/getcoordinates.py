import cv2

# Load your image
image = cv2.imread('backend/framet__7.jpg')

if image is None:
    print("Error: Image not loaded. Check the path.")
    exit()

# Mouse callback function
def show_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        img_copy = image.copy()
        cv2.putText(img_copy, f'X: {x}, Y: {y}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Image", img_copy)

# Create a window and bind the function to mouse events
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", show_coordinates)

# Display the image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
