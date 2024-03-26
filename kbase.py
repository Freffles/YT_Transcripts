import os
import re

def sort_key(filename):
    # Extract the tutorial number from the filename
    match = re.search(r'Tutorial (\d+)', filename)
    if match:
        return int(match.group(1))
    return 0  # Default if no number is found

input_folder = 'D:\\Working\\RL_Scripts\\OUT'
output_file = 'D:\\Working\\RL_Scripts\\vba-kb.txt'

# Get all transcript text files
transcript_files = [f for f in os.listdir(input_folder) if f.endswith('_transcript.txt')]
# Sort files in numerical order based on tutorial number
transcript_files.sort(key=sort_key)

with open(output_file, 'w') as outfile:
    for file in transcript_files:
        # Extract the descriptive part of the filename
        description = file.split('-')[1].strip().replace('_transcript.txt', '')
        outfile.write(description + '\n')

        # Write the content of the transcript file
        with open(os.path.join(input_folder, file), 'r') as infile:
            outfile.write(infile.read() + '\n\n')

print("Consolidation complete. Output is saved in 'vba-kb.txt'")
