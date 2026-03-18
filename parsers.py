"""
Parsers for extracting timing metrics from framework output.

llama.cpp prints timing info to stderr in a known format.
Distributed Llama has a different output format.
Both parsers return a standardised dict.
"""

import re


def parse_llama_cpp_output(
    stderr_text: str, stdout_text: str, wall_time_ms: float
) -> dict:
    """
    Parse llama.cpp stderr timing lines.

    Expected format (may vary slightly across versions):
        llama_perf_context_print:        load time =    1234.56 ms
        llama_perf_sampler_print:    sampling time =      12.34 ms /    50 runs   (...)
        llama_perf_context_print: prompt eval time =     567.89 ms /    25 tokens (   22.72 ms per token,    44.02 tokens per second)
        llama_perf_context_print:        eval time =    5678.90 ms /    49 runs   (  115.90 ms per token,     8.63 tokens per second)
        llama_perf_context_print:       total time =    6789.01 ms /    74 tokens

    Also handles older format with llama_print_timings prefix.
    """

    result = {
        "load_time_ms": 0.0,
        "prompt_eval_time_ms": 0.0,
        "prompt_tokens": 0,
        "prompt_rate_tps": 0.0,
        "eval_time_ms": 0.0,
        "eval_tokens": 0,
        "eval_rate_tps": 0.0,
        "total_time_ms": wall_time_ms,
        "total_tokens": 0,
        "ttft_ms": 0.0,  # estimated as prompt_eval_time + first token eval
        "generated_text": stdout_text.strip(),
        "parse_errors": [],
    }

    text = stderr_text

    # --- load time ---
    m = re.search(r"load time\s*=\s*([\d.]+)\s*ms", text)
    if m:
        result["load_time_ms"] = float(m.group(1))
    else:
        result["parse_errors"].append("load_time not found")

    # --- prompt eval ---
    m = re.search(
        r"prompt eval time\s*=\s*([\d.]+)\s*ms\s*/\s*(\d+)\s*tokens?\s*\(\s*([\d.]+)\s*ms per token,\s*([\d.]+)\s*tokens per second\)",
        text,
    )
    if m:
        result["prompt_eval_time_ms"] = float(m.group(1))
        result["prompt_tokens"] = int(m.group(2))
        result["prompt_rate_tps"] = float(m.group(4))
    else:
        result["parse_errors"].append("prompt_eval not found")

    # --- eval (generation) ---
    m = re.search(
        r"(?<!prompt\s)eval time\s*=\s*([\d.]+)\s*ms\s*/\s*(\d+)\s*runs?\s*\(\s*([\d.]+)\s*ms per token,\s*([\d.]+)\s*tokens per second\)",
        text,
    )
    if m:
        result["eval_time_ms"] = float(m.group(1))
        result["eval_tokens"] = int(m.group(2))
        result["eval_rate_tps"] = float(m.group(4))
    else:
        result["parse_errors"].append("eval not found")

    # --- total ---
    m = re.search(r"total time\s*=\s*([\d.]+)\s*ms\s*/\s*(\d+)\s*tokens?", text)
    if m:
        result["total_time_ms"] = float(m.group(1))
        result["total_tokens"] = int(m.group(2))
    
    # TTFT estimate: prompt processing + one token generation step
    if result["prompt_eval_time_ms"] > 0 and result["eval_tokens"] > 0:
        per_token_ms = result["eval_time_ms"] / result["eval_tokens"]
        result["ttft_ms"] = round(result["prompt_eval_time_ms"] + per_token_ms, 2)

    return result


def parse_dllama_output(
    stderr_text: str, stdout_text: str, wall_time_ms: float
) -> dict:
    """
    Parse Distributed Llama output.

    Distributed Llama output format varies by version. Common patterns:
        Generated N tokens in X.XXs (Y.YY tokens/s)
        Prompt eval: X.XX ms / N tokens (Y.YY tokens/s)

    This parser attempts multiple patterns and falls back to wall time.
    Adjust regex patterns to match your installed version.
    """
    combined = stderr_text + "\n" + stdout_text
    result = {
        "load_time_ms": 0.0,
        "prompt_eval_time_ms": 0.0,
        "prompt_tokens": 0,
        "prompt_rate_tps": 0.0,
        "eval_time_ms": 0.0,
        "eval_tokens": 0,
        "eval_rate_tps": 0.0,
        "total_time_ms": wall_time_ms,
        "total_tokens": 0,
        "ttft_ms": 0.0,
        "generated_text": "",
        "parse_errors": [],
    }

    # --- Try to find generation stats ---
    # Pattern: "Generated N tokens in X.XXs (Y.YY tokens/s)"
    m = re.search(
        r"Generated\s+(\d+)\s+tokens?\s+in\s+([\d.]+)\s*s\s*\(([\d.]+)\s*tokens?/s\)",
        combined,
    )
    if m:
        result["eval_tokens"] = int(m.group(1))
        result["eval_time_ms"] = float(m.group(2)) * 1000.0
        result["eval_rate_tps"] = float(m.group(3))
    else:
        result["parse_errors"].append(
            "generation stats not found — check dllama output format"
        )

    # --- Try to find prompt eval ---
    m = re.search(
        r"[Pp]rompt\s+eval:?\s*([\d.]+)\s*ms\s*/\s*(\d+)\s*tokens?\s*\(([\d.]+)\s*tokens?/s\)",
        combined,
    )
    if m:
        result["prompt_eval_time_ms"] = float(m.group(1))
        result["prompt_tokens"] = int(m.group(2))
        result["prompt_rate_tps"] = float(m.group(3))

    # --- Try to find load time ---
    m = re.search(
        r"[Ll]oad(?:ed|ing)?\s+(?:time|model)?:?\s*([\d.]+)\s*(?:ms|s)", combined
    )
    if m:
        val = float(m.group(1))
        # heuristic: if < 100, probably seconds
        result["load_time_ms"] = val * 1000.0 if val < 100 else val

    # --- Extract generated text (lines that aren't stats) ---
    # This is a heuristic — dllama mixes output and stats
    lines = combined.split("\n")
    text_lines = []
    stat_patterns = [
        r"Generated\s+\d+",
        r"[Pp]rompt\s+eval",
        r"[Ll]oad",
        r"tokens?/s",
        r"^\s*$",
        r"^#",
        r"^\[",
    ]
    for line in lines:
        if not any(re.search(p, line) for p in stat_patterns):
            text_lines.append(line)
    result["generated_text"] = "\n".join(text_lines).strip()

    result["total_tokens"] = result["prompt_tokens"] + result["eval_tokens"]

    # TTFT estimate
    if result["prompt_eval_time_ms"] > 0 and result["eval_tokens"] > 0:
        per_token_ms = result["eval_time_ms"] / max(result["eval_tokens"], 1)
        result["ttft_ms"] = round(result["prompt_eval_time_ms"] + per_token_ms, 2)

    return result
