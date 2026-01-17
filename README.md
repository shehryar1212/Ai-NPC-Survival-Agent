#  Generative NPC: Survival Agent Simulation
https://github.com/user-attachments/assets/31f005d5-dd3d-42f1-ad36-5bffc1a88c5e

> **An autonomous "Thinking NPC" that survives in a procedurally generated grid world using DeepSeek R1 reasoning.**

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pygame](https://img.shields.io/badge/Engine-Pygame-green?logo=sdl)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange?logo=langchain)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek_R1-purple)

##  Overview
This project demonstrates **Agentic AI** in a real-time simulation. Unlike traditional Game AI (which uses static Behavior Trees like `if health < 50: eat`), this agent uses a **Large Language Model (LLM)** to perceive, reason, and act.

The agent, **Alex**, "sees" the game world via text descriptions, formulates survival strategies (e.g., *"I see a wolf to the West, I should move North to kite it"*), and executes actions.

## ⚙️ How It Works (The Cognitive Loop)

The system separates the **Simulation Layer** (Pygame) from the **Cognitive Layer** (LLM).
```mermaid
graph TD
    World[🌍 Pygame World] -- "1. Vision Data (Text)" --> Brain[ NPC Brain Class]
    Brain -- "2. Prompt Engineering" --> LLM{DeepSeek LLM}
    LLM -- "3. JSON Reasoning" --> Brain
    Brain -- "4. Action Command" --> World
    World -- "5. Update Physics" --> Screen[🖥️ Display]
```
