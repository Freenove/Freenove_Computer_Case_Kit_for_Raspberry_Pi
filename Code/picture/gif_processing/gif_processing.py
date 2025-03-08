import os
from PIL import Image, ImageSequence
import glob

def extract_gif_to_images(gif_path, output_folder='picture'):
    # Ensure that the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open GIF file
    with Image.open(gif_path) as img:
        # Get the frame rate of GIF
        frame_count = img.n_frames
        
        # 逐Save frame by frame as an image, named with zero padding numbers
        for i in range(frame_count):
            img.seek(i)
            frame_filename = f'frame_{i:04d}.png'  # Use a 4-digit zero filled number
            frame_path = os.path.join(output_folder, frame_filename)
            img.save(frame_path, 'PNG')
            print(f'Saved {frame_path}')

def images_to_gif(input_folder='picture', output_folder='gif', output_gif_path='output.gif'):
    # Ensure that the input folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The folder '{input_folder}' does not exist.")
    
    # Ensure that the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Use the glob module to match all image files by file name pattern and sort them accordingly
    image_files = sorted(glob.glob(os.path.join(input_folder, 'frame_*.png')))
    
    # Check if the image file has been obtained
    if not image_files:
        raise FileNotFoundError(f"No image files found in the folder '{input_folder}'.")
    
    # Open the first image as the initial frame and create a frame list
    frames = [Image.open(img_file) for img_file in image_files]
    
    # Save to a new GIF file
    output_path = os.path.join(output_folder, output_gif_path)
    frames[0].save(output_path,
                   save_all=True,
                   append_images=frames[1:],
                   duration=200,  # The duration of each frame (in milliseconds)
                   loop=0)  # 0 represents a perpetual loop
    print(f'Saved {output_path}')


if __name__ == "__main__":
    gif_path = 'example.gif'  # Please replace with your GIF file path

    # Decompose GIF into images frame by frame
    #extract_gif_to_images(gif_path)

    # Synthesize images into a GIF
    images_to_gif()