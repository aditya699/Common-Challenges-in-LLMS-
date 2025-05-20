# Common Challenges in LLMs

This repository explores common challenges in working with Large Language Models (LLMs) and provides practical solutions.

## Challenges

| Challenge | Description | Solution |
|-----------|-------------|----------|
| **Behavior Alignment** | Adding specific behaviors to LLMs without changing their underlying intelligence | Fine-tuning with techniques like LoRA, SFT, DPO and GRPO |
| **Parallel Processing** | Efficiently handling multiple LLM API calls and computations | ThreadPoolExecutor for IO-bound tasks, ProcessPoolExecutor for CPU-bound tasks |
| **MCP** | Standardized interface for AI agents to dynamically discover, select, and orchestrate tools based on context |

## Behavior in LLMs

The `behavior_in_llms` folder explores how to add specific behaviors to Large Language Models (LLMs) without changing their underlying intelligence.

### Contents

- **behavior_in_llms.md**: Overview of behavior alignment techniques, explaining the difference between behavior and intelligence in LLMs, when prompt engineering falls short, and methods like SFT, DPO, and LoRA.

- **unsloth_guide.ipynb**: Practical implementation of behavior alignment using the Unsloth library to fine-tune Qwen2.5 7B with LoRA, creating a CBT (Cognitive Behavioral Therapy) coach. This notebook demonstrates how to:
  - Set up the environment
  - Prepare a dataset of CBT-style interactions
  - Configure LoRA parameters
  - Train the model efficiently
  - Compare base model vs. fine-tuned model responses

### Key Takeaways

- Behavior tuning is about reliability and consistency, not intelligence
- Fine-tuning with LoRA allows efficient behavior alignment on consumer hardware
- Small, high-quality datasets (50-100 examples) can significantly change model behavior
- The techniques shown work across various LLM applications beyond therapy

### Getting Started

Open the Jupyter notebook to see a complete walkthrough of the behavior alignment process using Unsloth.