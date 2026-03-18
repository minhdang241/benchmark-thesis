"""
Configuration for C1 and C2 benchmark experiments.

Adjust paths below to match your Raspberry Pi setup.
"""

# ============================================================
# Paths — edit these to match your environment
# ============================================================
FOLDER_PATH = "/Users/minhdg241/Desktop/thesis/codebase"
LLAMA_CPP_BIN = f"{FOLDER_PATH}/llama.cpp/build/bin/llama-cli"
DLLAMA_BIN = f"{FOLDER_PATH}/distributed-llama/dllama"
MODEL_DIR = "models/"
OUTPUT_DIR = "logs/"

# ============================================================
# Models — Tier A (small) and Tier B (medium)
# ============================================================
MODELS = {
    # Tier A: Small models
    "qwen3-1.7b-q4_0": {
        "tier": "A",
        "filename": "Qwen_Qwen3-1.7B-Q4_0.gguf",
        "description": "Qwen3 1.7B Q4_0",
        "approx_size_gb": 1.1,
    },
    # "llama-3.2-3b-instruct-q4_0": {
    #     "tier": "A",
    #     "filename": "Llama-3.2-3B-Instruct-Q4_0.gguf",
    #     "description": "Llama 3.2 3B Instruct Q4_0",
    #     "approx_size_gb": 3.4,
    # },
    # # Tier B: Medium models
    # "llama-3.1-8b-instruct-q4_0": {
    #     "tier": "B",
    #     "filename": "Meta-Llama-3.1-8B-Instruct-Q4_0.gguf",
    #     "description": "Llama 3.1 8B Instruct Q4_0",
    #     "approx_size_gb": 6.3,
    # },
    # "qwen3-8b-q4_0": {
    #     "tier": "B",
    #     "filename": "Qwen3-8B-Q4_0.gguf",
    #     "description": "Qwen3 8B Q4_0",
    #     "approx_size_gb": 6.7,
    # },
}

# ============================================================
# Configurations
# ============================================================
CONFIGURATIONS = {
    "C1": {
        "name": "llama.cpp single-device",
        "framework": "llama.cpp",
        "binary": LLAMA_CPP_BIN,
        "distributed": False,
    },
    "C2": {
        "name": "Distributed Llama single-node",
        "framework": "distributed_llama",
        "binary": DLLAMA_BIN,
        "distributed": False,
    },
}

# ============================================================
# Experiment parameters
# ============================================================
NUM_RUNS = 3  # Total runs per prompt (first is warm-up)
WARMUP_RUNS = 1  # How many initial runs to discard
TEMPERATURE = 0.0
NUM_THREADS = 4  # RPi5 has 4 cores
MONITOR_INTERVAL = 0.5  # CPU/memory sampling interval in seconds
