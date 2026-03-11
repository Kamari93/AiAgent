AI Code Assistant Agent

A simple AI-powered coding agent built with Python and the Gemini API.
The agent can explore a codebase, read files, execute Python scripts, and write files in order to answer questions or complete coding tasks.

This project demonstrates how to build a tool-using AI agent with a feedback loop, allowing the model to iteratively reason about problems and interact with a local project.

How It Works

The agent follows a reasoning loop:
	1.	The user provides a prompt.
	2.	The AI decides which tool to use.
	3.	The tool runs and returns results.
	4.	The AI uses the new information to decide the next step.
	5.	The process repeats until the AI can provide a final answer.