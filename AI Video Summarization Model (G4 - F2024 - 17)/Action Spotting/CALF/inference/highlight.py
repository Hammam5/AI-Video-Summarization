import json
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def create_highlights(video_path, json_path, output_folder, include_labels, confidence_threshold):
    try:
        # Extract the base name from the video path and create a new output filename
        base_name = os.path.basename(video_path)
        base_name_without_ext = os.path.splitext(base_name)[0]
        output_path = os.path.join(output_folder, f"{base_name_without_ext}_highlights.mp4")

        # Load JSON data
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Load the video file
        video = VideoFileClip(video_path)

        clips = []
        print("Processing events...")

        # Process each event in the JSON file
        for event in data['predictions']:
            if event['label'] in include_labels and float(event['confidence']) >= confidence_threshold:
                start_time = max(0, int(event['position']) / 1000 - 15)  # Start 15 seconds before the event
                end_time = min(video.duration, int(event['position']) / 1000 + 15)  # End 15 seconds after the event
                print(f"Adding clip: {start_time}-{end_time} for {event['label']}")

                # Extract the clip and add to the list of clips
                clip = video.subclip(start_time, end_time)
                clips.append(clip)

        # Concatenate all clips to make a highlight reel
        if clips:
            final_clip = concatenate_videoclips(clips)
            final_clip.write_videofile(output_path, codec='libx264', fps=24)
            final_clip.close()  # Explicitly close the final clip
            video.close()  # Explicitly close the original video clip
            print("Highlights video created successfully.")

            # Open the highlight video using the default media player
            os.startfile(output_path)
        else:
            video.close()  # Explicitly close the original video clip
            print("No clips meet the criteria.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the labels to include and the minimum confidence threshold
labels_to_include = ['Goal']  # Change labels as needed
confidence_thresh = 0.15  # Change confidence threshold as needed

# Define the output folder
output_folder = 'outputs/highlights'

# Example video file
video_file = '2015-11-21 - 20-30 Manchester City 1 - 4 Liverpool.mkv'
path=os.path.splitext(os.path.basename(video_file))[0]
# Call the function with appropriate paths and parameters
#create_highlights(video_file, f'outputs/{path}/Predictions-v2.json', output_folder, labels_to_include, confidence_thresh)
create_highlights(video_file, f'outputs/Predictions-v2.json', output_folder, labels_to_include, confidence_thresh)
