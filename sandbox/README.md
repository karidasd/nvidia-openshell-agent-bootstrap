# Local AI Agent Sandbox (Docker + Ollama)

This sandbox environment allows you to run open-source LLMs locally on your NVIDIA GPU using **Ollama** and execute autonomous agent operations inside an isolated container space.

---

## 🛠️ Prerequisites

1.  **Docker Desktop** installed on your system.
2.  **NVIDIA Container Toolkit** installed to expose GPU hardware to Docker.
    *   [NVIDIA Installation Guide Reference](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

---

## 🚀 How to Run the Local Sandbox

### 1. Launch the containers
Navigate to this folder and start the services in the background:
```bash
docker compose up -d
```

### 2. Pull a local model into Ollama
Expose model weights to your local hardware. For example, to download Llama 3:
```bash
docker exec -it openshell-ollama ollama run llama3
```

### 3. Verify Agent execution
The agent runner container binds to the parent project directory and executes `src/main.py` inside the containerized sandbox environment:
```bash
docker logs openshell-agent-runner
```
