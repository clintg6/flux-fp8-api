#!/bin/bash

# Output file for saving results
output_file="benchmark_results.txt"

# Clear the output file if it already exists
> "$output_file"

# Define an array of resolutions to test
resolutions=("1024x1024" "1024x768" "4096x2048")

# Loop over the resolutions
for resolution in "${resolutions[@]}"; do
    # Extract width and height from the resolution string
    width=$(echo $resolution | cut -d 'x' -f 1)
    height=$(echo $resolution | cut -d 'x' -f 2)
    
    # Print the current resolution to the output file
    echo "Running benchmark for resolution: $resolution" >> "$output_file"
    
    # Call your Python benchmarking script with the given width and height
    avg_time=$(python bench.py --width $width --height $height --num_steps 50)
    
    # Save the result to the output file with the resolution and average time
    echo "Resolution: $resolution, Average Time: $avg_time ms" >> "$output_file"
    echo "" >> "$output_file"  # Add an empty line for better readability
    
    echo "Completed benchmark for $resolution."
done

echo "Benchmarking complete. Results saved in $output_file."
