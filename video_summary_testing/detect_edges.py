import cv2

def detect_edges(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize for easier viewing (optional)
    image = cv2.resize(image, (800, 600))

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny Edge Detection
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    cv2.imwrite("vscode_layout_mask.png", edges)
    # Show original and edges

def match():
      
            # Load the main image and mask (grayscale or binary)
            image = cv2.imread('vscode3.png', cv2.IMREAD_COLOR)
            mask = cv2.imread('vscode_layout_mask.png', cv2.IMREAD_GRAYSCALE)

            # Optional: resize mask to a region of interest
            h, w = mask.shape
            roi = image[0:h, 0:w]  # You can change the position as needed

            # Apply mask (bitwise AND)
            masked_region = cv2.bitwise_and(roi, roi, mask=mask)

            # Optional: Check if mask pattern exists in image using template matching
            # First create template by applying mask to the pattern region
            template = masked_region

            # Match template over entire image
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

            # Get the best match position
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Set a threshold for detection
            threshold = 0.8
            print(max_val)

            # Optional: Visualize the match
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.imshow("Match", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__=="__main__":
   match()