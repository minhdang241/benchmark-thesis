"""
Prompt suite for thesis benchmarking.
Each prompt has: id, text, n_predict, input_category, output_category
"""

PROMPTS = [
    {
        "id": "P01",
        "name": "Factual Recall",
        "input_category": "short",
        "output_category": "short",
        "n_predict": 50,
        "text": ("What is edge computing? Answer in exactly two sentences."),
    },
    {
        "id": "P02",
        "name": "Comparative Analysis",
        "input_category": "short",
        "output_category": "long",
        "n_predict": 525,
        "text": (
            "Compare pipeline parallelism and tensor parallelism for distributed "
            "inference on resource-constrained edge devices. Discuss the trade-offs "
            "in terms of communication overhead, latency, and scalability. Write "
            "approximately three to four paragraphs."
        ),
    },
    {
        "id": "P03",
        "name": "Critical Analysis",
        "input_category": "long",
        "output_category": "short",
        "n_predict": 50,
        "text": (
            "Task assignment is the process of deciding upfront whether an edge SLM "
            "or a cloud LLM should handle a specific request. To achieve the right "
            "balance between saving energy, reducing lag, and keeping quality high, "
            "researchers usually use tools like lightweight scorers or bandit-based "
            "controllers to make routing choices on the fly. Some approaches use smaller "
            "models for easy tasks and larger ones only when needed. Tasks can be "
            "categorized by measuring cost effectiveness. Another scalable approach "
            "is Mixture-of-Experts, where systems route queries to specific cloud experts "
            "through a lightweight local gatekeeper. Agent-based methods extend this "
            "further by using planning agents to break down complex instructions and "
            "delegate subtasks to specialized agents. Task division allows Small "
            "Language Models and Large Language Models to collaborate on complementary "
            "subtasks by breaking down modular or hierarchical tasks into smaller "
            "components. This approach relies on three main strategies: routing, "
            "computation offloading, and early exit. Routing and forwarding techniques "
            "choose the most appropriate model on the fly during inference. Computation "
            "offloading distributes the inference workload between edge devices and cloud "
            "servers depending on live runtime conditions. Early-exit mechanisms give "
            "the system the ability to stop processing at middle layers if the model "
            "is confident enough. Critically evaluate which of these collaborative "
            "inference strategies would be most appropriate for a Raspberry Pi 5 cluster "
            "running IoT sensor data processing. Justify your answer in approximately "
            "five to seven sentences."
        ),
    },
    {
        "id": "P04",
        "name": "Comprehensive Summarisation",
        "input_category": "long",
        "output_category": "long",
        "n_predict": 450,
        "text": (
            "Deploying LLMs on edge devices presents numerous challenges due to their "
            "resource-constrained nature. Edge devices are limited by computational "
            "memory resources, which prevents them from storing and executing LLMs "
            "directly. For example, GPT-3 contains billions of parameters and requires "
            "high-performance hardware such as GPUs or TPUs, which are mostly absent "
            "in edge devices. The gap between the rapid increase in computational "
            "complexity of LLMs and the slow growth in edge device capabilities is "
            "widening yearly. LLMs are characterized by substantial energy consumption "
            "during training and inference. Significant computational power is required "
            "to process large amounts of data and execute complex tasks, which contrasts "
            "with the strict energy constraints of edge environments. Even though edge "
            "computing reduces data privacy risks by processing data locally, it still "
            "requires rigorous security measures including robust encryption. Also, "
            "since edge environments consist of heterogeneous devices, standardizing "
            "protocols across devices is challenging. To tackle deployment issues, one "
            "approach is to compact the architecture to produce Small Language Models "
            "that operate in constrained environments. Compared to LLMs with hundreds of "
            "billions of parameters, SLMs only have millions to billions of parameters. "
            "Quantization is the most widely adopted technique, converting high-precision "
            "floating-point values into lower-precision formats. Knowledge Distillation "
            "transfers reasoning capabilities from large teacher models into smaller "
            "student models. Pruning removes redundant weights and connections that "
            "contribute little to the overall output. Write a comprehensive summary "
            "of the challenges and solutions described above. Organise your response "
            "into two sections: first the challenges, then the solutions. Write "
            "approximately three to four paragraphs total."
        ),
    },
]
