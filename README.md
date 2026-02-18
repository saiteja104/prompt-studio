🧠 Prompt Studio
A powerful, developer-friendly platform to write, test, compare, and track LLM prompts across multiple AI models — all from a clean UI.

📌 Table of Contents

Overview
Features
Tech Stack
Project Structure
Getting Started

Prerequisites
Backend Setup
Frontend Setup
Environment Variables


Database Schema
API Reference
Git Workflow
Roadmap
Contributing


Overview
Prompt Studio is a full-stack web application that lets users:

Log in and manage projects
Write prompts with dynamic variable support (e.g. {{name}}, {{context}})
Select model parameters (temperature, max tokens, etc.)
Run prompts across multiple LLMs simultaneously and compare outputs side by side
Save, version, and track prompts over time

Think of it as a Postman for LLMs — built for developers and AI teams who iterate fast on prompts.

Features
✅ Phase 1 (MVP)

User authentication (register, login, JWT-based sessions)
Project management (create, rename, delete projects)
Prompt editor with syntax highlighting
Dynamic variable detection — auto-generates input fields for {{variables}}
Model selector — choose one or multiple LLMs to run against
Model parameter controls — temperature, max tokens, top-p per run
Multi-model parallel execution — see all responses at once
Prompt saving and versioning (v1, v2, v3...)
Run history — every execution logged with inputs, outputs, latency, token usage

🔜 Phase 2

Response diff view — compare outputs across models visually
Collections/folders — organize prompts within projects
Export runs — download as JSON or Markdown
Team collaboration — invite members to a project
Prompt templates — reusable prompt patterns


Tech Stack
LayerTechnologyFrontendReact.js, HTML, CSS, JavaScriptBackendPython, FastAPIDatabasePostgreSQLAuthJWT (JSON Web Tokens)ORMSQLAlchemy + Alembic (migrations)LLM APIsOpenAI, Anthropic, Google GeminiDev ToolsDocker, Docker Compose