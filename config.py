import torch

# --- Model & Data ---
# "t5-small", "t5-base", "t5-large"
# Start with "t5-small" as it's the fastest to train.
MODEL_NAME = "t5-small"

# The file we created in the last step
TRAINING_FILE = "recipes_training.jsonl"

# Where the final, trained model will be saved
OUTPUT_DIR = "t5-recipe-generator"

# --- Tokenization ---
# T5's max length is 512, but we can set lower
# to save memory if our inputs/outputs are shorter.
MAX_INPUT_LENGTH = 512
MAX_TARGET_LENGTH = 512

# --- Training ---
# Batch size: How many recipes to process at once.
# 4 or 8 is good for most consumer GPUs.
# Lower this if you get "Out of Memory" errors.
BATCH_SIZE = 4
NUM_EPOCHS = 3
LEARNING_RATE = 5e-5

# --- Hardware ---
# Use CUDA (NVIDIA GPU) if available, otherwise CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"