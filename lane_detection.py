import cv2
import numpy as np

def grayscale(img):
    """Applies the Grayscale transform"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    """Applies an image mask"""
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """Draws lines on the image"""
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """Applies Hough transform"""
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """Combines the lines image with the original image"""
    return cv2.addWeighted(initial_img, α, img, β, γ)

def detect_lanes(image):
    """Main function to detect lanes"""
    gray = grayscale(image)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = canny(blur, 50, 150)

    imshape = image.shape
    vertices = np.array([[(0, imshape[0]), (460, 320), (520, 320), (imshape[1], imshape[0])]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    rho = 2
    theta = np.pi / 180
    threshold = 15
    min_line_length = 40
    max_line_gap = 20
    lines_image = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

    final_image = weighted_img(lines_image, image)
    return final_image

if __name__ == '__main__':
    # Example usage
    input_image = cv2.imread('test_images/test_image.jpg')
    result = detect_lanes(input_image)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

