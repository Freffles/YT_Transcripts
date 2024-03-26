import argparse
import os
import re

# Function to clean a line from the VTT file
def clean_vtt_line(line):
    # Remove HTML-like tags (e.g., <c>, <00:00:02.310>)
    line = re.sub(r'<[^>]+>', '', line)
    # Replace multiple spaces with a single space
    line = re.sub(r' {2,}', ' ', line)
    return line.strip()

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_folder', help='the input folder containing .vtt and .srt files')
parser.add_argument('output_folder', help='the output folder to save the processed files')
args = parser.parse_args()

# Get a list of all .vtt and .srt files in the input folder
subtitle_files = [os.path.join(args.input_folder, f) for f in os.listdir(args.input_folder) if f.endswith('.vtt') or f.endswith('.srt')]

# Loop through the list of subtitle files
for input_file in subtitle_files:
    # Get the base filename (without the path or extension)
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
	# Remove '.en' from the filename
    filez = base_filename.replace('.en', '')
    #filez = re.sub('\.', '', base_filename)

    # Extract the subtitle paragraphs
    paragraphs = ""
    previous_line = ""  # Keep track of the previous line
    header_passed = False  # Flag to skip the header for VTT files
    with open(input_file, 'r') as file:
        if input_file.endswith('.vtt'):
            lines = file.readlines()
            for line in lines:
                # Skip the header
                if not header_passed:
                    if line.strip() == "":
                        header_passed = True
                    continue

                # Skip lines that are timecodes or empty
                if '-->' in line or line.strip() == '':
                    continue

                cleaned_line = clean_vtt_line(line)
                # Skip adding the line if it's a duplicate
                if cleaned_line != previous_line:
                    paragraphs += cleaned_line + " "
                    previous_line = cleaned_line
        elif input_file.endswith('.srt'):
            for line in file:
                if line.strip().isdigit() or '-->' in line or line.strip() == '':
                    continue
                paragraphs += clean_vtt_line(line) + " "

    # Construct the output filename
    output_file = os.path.join(args.output_folder, filez + '_transcript.txt')

    # Save the resulting string to the output file
    with open(output_file, 'w') as f:
        f.write(paragraphs)
