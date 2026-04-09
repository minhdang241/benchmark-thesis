"""
Configuration for C1 and C2 benchmark experiments.

Adjust paths below to match your Raspberry Pi setup.
"""

# ============================================================
# Paths — edit these to match your environment
# ============================================================
FOLDER_PATH = "../"
LLAMA_CPP_BIN = f"{FOLDER_PATH}/llama.cpp/build/bin/llama-completion"
DLLAMA_BIN = f"{FOLDER_PATH}/distributed-llama/dllama"
MODEL_DIR = "models/"
OUTPUT_DIR = "logs/"

# ============================================================
# Distributed Environment (C3 / C4)
# ============================================================
WORKER_IP = "192.168.1.110"
# WORKER_IP = "192.168.1.104"
RPC_PORT = "50052"  # Default llama.cpp RPC server port
DLLAMA_PORT = "9999"  # Default dllama worker port

# ============================================================
# Models — Tier A (small) and Tier B (medium)
# ============================================================
MODELS_LLAMA = {
    # Tier A: Small models
    "qwen3-1.7b-q4_0": {
        "tier": "A",
        "filename": "llama/tierA/qwen3-1.7B/qwen3-1.7b-q4_0.gguf",
        "description": "Qwen3 1.7B Q4_0",
        "approx_size_gb": 1.1,
    },
    "llama-3.2-1b-instruct-q4_0": {
        "tier": "A",
        "filename": "llama/tierA/llama-3.2-1B/llama-3.2-1b-instruct-q4_0.gguf",
        "description": "Llama 3.2 1B Instruct Q4_0",
        "approx_size_gb": 3.4,
    },
    # Tier B: Medium models
    "llama-3.1-8b-instruct-q4_0": {
        "tier": "B",
        "filename": "llama/tierB/meta-llama-3.1-8B/meta-llama-3.1-8b-instruct-q4_0.gguf",
        "description": "Llama 3.1 8B Instruct Q4_0",
        "approx_size_gb": 6.3,
    },
    "qwen3-8b-q4_0": {
        "tier": "B",
        "filename": "llama/tierB/qwen3-8B/qwen3-8b-q4_0.gguf",
        "description": "Qwen3 8B Q4_0",
        "approx_size_gb": 6.7,
    },
    # Tier C: Large models
    "qwen3-14b-q4_0": {
        "tier": "C",
        "filename": "llama/tierC/qwen3-14B/qwen3-14b-q4_0.gguf",
        "description": "Qwen3 14B Q4_0",
        "approx_size_gb": 10,
    },
    # "qwen3-30b-q4_0": {
    # "tier": "C",
    # "filename": "llama/tierC/qwen3-30B-A3B/qwen3-30b-a3b-instruct-2507-q4_0.gguf",
    # "description": "Qwen3 30B Q4_0",
    # "approx_size_gb": 16,
    # },
}


MODELS_DLLAMA = {
    # Tier A: Small models
    "qwen3-1.7b-q4_0": {
        "tier": "A",
        "filename": "dllama/tierA/qwen3-1.7B/dllama_model_qwen3_1.7b_q40.m",
        "tokenizer_name": "dllama/tierA/qwen3-1.7B/dllama_tokenizer_qwen3_1.7b.t",
        "description": "Qwen3 1.7B Q4_0",
        "approx_size_gb": 2.2,
    },
    "llama-3.2-3b-instruct-q4_0": {
        "tier": "A",
        "filename": "dllama/tierA/llama-3.2-1B/dllama_model_llama3.2-1b-instruct_q40.m",
        "tokenizer_name": "dllama/tierA/llama-3.2-1B/dllama_tokenizer_llama3_2.t",
        "description": "Llama 3.2 1B Instruct Q4_0",
        "approx_size_gb": 3.4,
    },
    # Tier B: Medium models
    "llama-3.1-8b-instruct-q4_0": {
        "tier": "B",
        "filename": "dllama/tierB/meta-llama-3.1-8B/dllama_model_llama3.1_instruct_q40.m",
        "tokenizer_name": "dllama/tierB/meta-llama-3.1-8B/dllama_tokenizer_llama_3_1.t",
        "description": "Llama 3.1 8B Instruct Q4_0",
        "approx_size_gb": 6.3,
    },
    "qwen3-8b-q4_0": {
        "tier": "B",
        "filename": "dllama/tierB/qwen3-8B/dllama_model_qwen3_8b_q40.m",
        "tokenizer_name": "dllama/tierB/qwen3-8B/dllama_tokenizer_qwen3_8b.t",
        "description": "Qwen3 8B Q4_0",
        "approx_size_gb": 6.7,
    },
    # Tier C: Large models
    "qwen3-14b-q4_0": {
        "tier": "C",
        "filename": "dllama/tierC/qwen3-14B/dllama_model_qwen3_14b_q40.m",
        "tokenizer_name": "dllama/tierC/qwen3-14B/dllama_tokenizer_qwen3_14b_q40.t",
        "description": "Qwen3 14B Q4_0",
        "approx_size_gb": 10,
    },
    # "qwen3-30b-q4_0": {
    # "tier": "C",
    # "filename": "dllama/tierC/qwen3-30B-A3B/dllama_model_qwen3_30b_a3b_q40.m",
    # "tokenizer_name": "dllama/tierC/qwen3-30B-A3B/dllama_tokenizer_qwen3_30b_a3b.t",
    # "description": "Qwen3 30B Q4_0",
    # "approx_size_gb": 17,
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
    "C3": {
        "name": "llama.cpp 2-node (RPC)",
        "framework": "llama.cpp",
        "binary": LLAMA_CPP_BIN,
        "distributed": True,
        "rpc_servers": f"{WORKER_IP}:{RPC_PORT},127.0.0.1:50052",
    },
    "C4": {
        "name": "Distributed Llama 2-node",
        "framework": "distributed_llama",
        "binary": DLLAMA_BIN,
        "distributed": True,
        "workers": f"{WORKER_IP}:{DLLAMA_PORT}",
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
