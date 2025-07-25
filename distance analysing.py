"""

This code analises the picture provided by the user, then by pointing out the 
2 points, it calculates the distance them, in unit of pixels.
After this, the user enters the reciprocal lattice parameter,
the code calculates the the real lattice parameter in unit of Anstrom.

Attention, the formula used here for converting pixels to lattice parameter 
is only for hexagone lattice, if you want to get other lattice parameter,
change the fromula.

"""

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
import os


image_file_before = "beforeanea.jpg"
image_file_after = "afteranea.jpg"

def get_distance_from_image(image_path, title_prompt):
    """
    Displays an image, lets the user click 2 points, and returns the
    annotated image, points, and horizontal distance.

    Args:
        image_path (str): The file path to the image.
        title_prompt (str): The title for the image selection window.

    Returns:
        tuple: A tuple containing (annotated_image, points, distance)
               or (None, None, None) if input is cancelled.
    """
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: Could not load image from path: {image_path}")
        return None, None, None

    print("-" * 50)
    print(f"--- Analyzing '{os.path.basename(image_path)}' ---")
    print("An image window has opened. Please click on the 2 points of interest.")
    print("After the 2nd click, the window will close automatically.")
    

    fig = plt.figure(figsize=(12, 9))
    plt.imshow(img)
    plt.title(title_prompt, fontsize=16)
    plt.xlabel("The window will close after the 2nd click.", fontsize=10)
    
    points = plt.ginput(2, timeout=0)
    plt.close(fig)

    if len(points) < 2:
        print("\nInput cancelled. Less than 2 points were selected.")
        return None, None, None

    centroids = sorted([(int(x), int(y)) for x, y in points], key=lambda p: p[0])
    p1, p2 = centroids
    distance = p2[0] - p1[0]


    output_image = img.convert("RGB")
    draw = ImageDraw.Draw(output_image)
    
  
    draw.ellipse([p1[0] - 10, p1[1] - 10, p1[0] + 10, p1[1] + 10], outline="lime", width=3)
    draw.ellipse([p2[0] - 10, p2[1] - 10, p2[0] + 10, p2[1] + 10], outline="cyan", width=3)
    

    line_y = int((p1[1] + p2[1]) / 2) 
    draw.line([(p1[0], line_y), (p2[0], line_y)], fill="yellow", width=2)

    return output_image, centroids, distance

def analyze_annealing_effect(bef_anea_path, aft_anea_path):
    """
    Analyzes two images (before and after annealing) to calculate the real lattice parameter.
    """

    bef_img, bef_points, p_1 = get_distance_from_image(
        bef_anea_path, "Click 2 points on the 'Before Annealing' image"
    )
    if p_1 is None:
        print("Analysis stopped.")
        return


    aft_img, aft_points, p_2 = get_distance_from_image(
        aft_anea_path, "Click 2 points on the 'After Annealing' image"
    )
    if p_2 is None:
        print("Analysis stopped.")
        return

 
    print("-" * 50)
    try:
        a_input = input("Please enter the reciprocal lattice parameter (a) in Å⁻¹: ")
        a = float(a_input)
    except ValueError:
        print("Invalid input. Please enter a number. Exiting.")
        return


    d_1 = (p_2 * a) / p_1
    d_2 = (4 * np.pi) / (d_1 * np.sqrt(3))

    print("\n--- Analysis Results ---")
    print(f"Distance (Before Annealing): p_1 = {p_1} pixels")
    print(f"Distance (After Annealing):  p_2 = {p_2} pixels")
    print(f"Calculated Reciprocal Distance: d₁ = {d_1:.4f} Å⁻¹")
    print(f"Real Lattice Parameter: d₂ = {d_2:.4f} Å")
    print("-" * 26)


    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    

    axes[0].imshow(bef_img)
    axes[0].set_title("Before Annealing", fontsize=16)
    axes[0].set_xticks([])
    axes[0].set_yticks([])


    axes[1].imshow(aft_img)
    axes[1].set_title("After Annealing", fontsize=16)
    axes[1].set_xticks([])
    axes[1].set_yticks([])

   
    plt.subplots_adjust(bottom=0.2)
    
    text_coords = (f"Before Coords: {bef_points[0]}, {bef_points[1]}  |  "
                   f"After Coords: {aft_points[0]}, {aft_points[1]}")
    text_dists = f"Pixel Distance (Before): {p_1} px  |  Pixel Distance (After): {p_2} px"
    text_result = f"Real Lattice Parameter (d₂): {d_2:.4f} Å"

    plt.figtext(0.5, 0.12, text_coords, ha="center", fontsize=10, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    plt.figtext(0.5, 0.07, text_dists, ha="center", fontsize=10, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    plt.figtext(0.5, 0.02, text_result, ha="center", fontsize=12, weight='bold', bbox={"facecolor":"gold", "alpha":0.6, "pad":5})

 
    new_filename = f"{os.path.splitext(bef_anea_path)[0]}_comparison_analised.png"
    plt.savefig(new_filename)
    print(f"Analysis complete. Result saved to: '{new_filename}'")
    
    plt.show()


if __name__ == '__main__':
    analyze_annealing_effect(image_file_before, image_file_after)