# 🔐 Python Sandbox Code Execution Demo

This is a minimal Python project that demonstrates how to run Python code inside a **secure, sandboxed Docker container**.

---

## 📦 What It Does

- Creates a simple CSV file
- Simulates LLM-generated Python code (using pandas)
- Saves the code to a file
- Builds a Docker image (sandbox)
- Executes the code inside the Docker container
- Returns the output safely

---

## 🛠️ Requirements

- Python 3.8+
- Docker installed and running

Install dependencies:

```bash
pip install python-dotenv
````

---

## 🚀 How to Run

```bash
python sandbox_demo.py
```

This will:

1. Create a folder `sandbox/`
2. Write a `data.csv` and `code.py` file
3. Create a `Dockerfile` for a pandas-based environment
4. Build the Docker image (`sandbox-demo`)
5. Run the container with limits (`--cpus=1.0`, `--memory=512m`)
6. Print the result to your terminal

---

## 🧱 Folder Structure

After running once, you'll see:

```
sandbox/
├── data.csv        # Sample dataset
├── code.py         # Simulated code from LLM
└── Dockerfile      # Safe Python environment
```

---

## 🔐 Security Notes

* Code runs inside an isolated Docker container
* RAM and CPU are capped using Docker flags:

  * `--memory=512m`
  * `--cpus=1.0`
* The container is auto-removed after each run using `--rm`

---

## ✅ Example Output

```
🛠️ Building sandbox image...
🚀 Running code in Docker (sandbox)...

📤 Output:
Average age: 27.5
```

---

## 🙌 Use Cases

* Safe LLM code execution
* Building a "chat with your CSV" tool
* Prototype for Jupyter sandboxing
* Teaching isolated Python environments

---

## 📄 License

MIT License — free to use, learn from, and modify.

