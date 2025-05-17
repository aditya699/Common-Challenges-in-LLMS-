# Behavior in LLMs

This folder explores how to add specific behaviors to Large Language Models (LLMs) without changing their underlying intelligence.

## Contents

- **behavior_in_llms.md**: Overview of behavior alignment techniques, explaining the difference between behavior and intelligence in LLMs, when prompt engineering falls short, and methods like SFT, DPO, and LoRA.

- **unsloth_guide.ipynb**: Practical implementation of behavior alignment using the Unsloth library to fine-tune Qwen2.5 7B with LoRA, creating a CBT (Cognitive Behavioral Therapy) coach. This notebook demonstrates how to:
  - Set up the environment
  - Prepare a dataset of CBT-style interactions
  - Configure LoRA parameters
  - Train the model efficiently
  - Compare base model vs. fine-tuned model responses

## Key Takeaways

- Behavior tuning is about reliability and consistency, not intelligence
- Fine-tuning with LoRA allows efficient behavior alignment on consumer hardware
- Small, high-quality datasets (50-100 examples) can significantly change model behavior
- The techniques shown work across various LLM applications beyond therapy

## Getting Started

Open the Jupyter notebook to see a complete walkthrough of the behavior alignment process using Unsloth.
