import torch
import argparse
from flux_pipeline import FluxPipeline

# Setup the argument parser to take width, height, and num_steps as command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Generate images with specified parameters.")
    parser.add_argument("--width", type=int, default=1024, help="Width of the generated image.")
    parser.add_argument("--height", type=int, default=1024, help="Height of the generated image.")
    parser.add_argument("--num_steps", type=int, default=50, help="Number of inference steps.")
    return parser.parse_args()

# Load the pipeline
pipe = FluxPipeline.load_pipeline_from_config_path("./configs/config-dev-rocm.json")

def generate_image(width, height, num_steps):
    # Replace this with your actual pipeline call
    result = pipe.generate(
        prompt="ghibli style, a fantasy landscape with castles",
        width=width,
        height=height,
        num_steps=num_steps,
        guidance=3.5,
        seed=13456,
        strength=0.8,
    )
    return result

def benchmark_generate_image(num_repeats=1, width=1024, height=1024, num_steps=50):
    # Warm-up the GPU by running a few iterations of the generation
    for _ in range(1):
        _ = generate_image(width, height, num_steps)  # Run the generate image call 4 times to warm up
        torch.cuda.synchronize()  # Synchronize to ensure GPU operations complete
    
    # Start the timer
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    
    start.record()
    
    # Run the benchmark for the specified number of repeats
    for _ in range(num_repeats):
        _ = generate_image(width, height, num_steps)  # Benchmark the image generation
        torch.cuda.synchronize()  # Synchronize to ensure the timing is accurate
    
    end.record()
    
    # Wait for all GPU operations to complete
    torch.cuda.synchronize()
    
    # Calculate and return the average time per run
    elapsed_time = start.elapsed_time(end) / num_repeats
    return elapsed_time

if __name__ == "__main__":
    # Parse the command line arguments
    args = parse_args()
    
    # Run the benchmark with the provided command line arguments
    print(f"Benchmarking with width={args.width}, height={args.height}, num_steps={args.num_steps}")
    avg_time = benchmark_generate_image(num_repeats=1, width=args.width, height=args.height, num_steps=args.num_steps)
    
    print(f"Average time per image generation: {avg_time} ms")
