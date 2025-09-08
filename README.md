# SecureCode AI: LLM-Powered Vulnerability Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A submission for the AI Grand Challenge: PS-1 (Development of a software tool using LLMs for Detection of Vulnerabilities in Source Code).**

This project is a cutting-edge software security tool that harnesses the power of a fine-tuned Large Language Model (CodeBERT) to detect vulnerabilities in C/C++ source code. The tool analyzes code at the function level, identifying patterns indicative of common security flaws like buffer overflows, memory leaks, and more.

---

## 🚀 Key Features

-   **AI-Powered Detection:** Utilizes a `microsoft/codebert-base` model fine-tuned on the extensive NIST SARD (Software Assurance Reference Dataset) to understand the context and patterns of vulnerable code.
-   **Function-Level Granularity:** Scans source files and analyzes each function individually, pinpointing the exact location of potential threats.
-   **High Accuracy:** Achieved near-perfect accuracy on the validation set, demonstrating its effectiveness on structured, known vulnerability patterns.
-   **Command-Line Interface:** Provides a simple and scriptable command-line tool (`scan.py`) for easy integration into developer workflows.
-   **Open & Extensible:** Built with a modular architecture (`src/parser.py`, `scan.py`) that can be extended to support more languages and vulnerability types in the future.

---

## 🛠️ How It Works

The tool operates in a simple three-step process:

1.  **Parsing:** The input C/C++ source file is parsed using `tree-sitter` to accurately extract all function definitions, their names, and their starting line numbers.
2.  **Inference:** Each extracted function's code is passed to our fine-tuned CodeBERT model hosted on the [Hugging Face Hub](https://huggingface.co/jacpacd/vuln-detector-codebert-c-sard). The model classifies the function as either `Vulnerable` (LABEL_1) or `Safe` (LABEL_0).
3.  **Reporting:** A clear report is printed to the console, listing each potential vulnerability found, its location, and the model's confidence in the prediction.

---

## 📋 Prerequisites

-   Python 3.9+
-   An active internet connection (for downloading the model on first run)
-   Git and Git LFS installed

---

## ⚙️ Quick Start & Usage

**1. Clone the Repository:**
```bash
# Clone the repository
git clone https://github.com/CipherSaber/foss-vuln-scan.git

# Enter the project directory
cd foss-vuln-scan

# Install Git LFS hooks and pull the dataset pointer
git lfs install
git lfs pull
```

**2. Set Up the Python Environment:**
```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install the required libraries
pip install -r requirements.txt
```

**3. Run the Scanner:**
You can now use the `scan.py` script to analyze any C/C++ file.

```bash
# Scan a test file
python scan.py path/to/your/code.c
```

**Example:**
```bash
python scan.py ./path/to/test_buffer_overflow.c
```

**Example Output:**
```
[*] Loading model 'jacpacd/vuln-detector-codebert-c-sard' from Hugging Face Hub...
[+] Model loaded successfully.

[*] Scanning file: ./path/to/test_buffer_overflow.c
[+] Found 3 functions to analyze.
[*] Analyzing functions with the AI model...

-------------------------------------------
[!] VULNERABILITY DETECTED!
    - Function: vulnerable_function
    - Location: Line 8
    - Confidence: 99.98%
-------------------------------------------

[+] Scan Complete. Found 1 potential vulnerabilities.
```

---

## 🧠 The AI Model

The core of this project is a CodeBERT model fine-tuned for sequence classification.

-   **Base Model:** `microsoft/codebert-base`
-   **Training Data:** NIST SARD (Juliet Test Suite for C/C++)
-   **Task:** Binary Classification (Vulnerable vs. Safe)
-   **Model Hub Link:** You can view the model card and details here: **[jacpacd/vuln-detector-codebert](https://huggingface.co/jacpacd/vuln-detector-codebert)**

The model achieved a validation loss of 0.0000, indicating perfect classification on the highly structured SARD dataset.

---

## 🔮 Future Work (Roadmap)

This MVP is the foundation for a more comprehensive security tool. The next steps include:

-   **Phase 2: Web Interface:** Develop a user-friendly web application using Streamlit for easy, interactive code scanning.
-   **Phase 3: Mitigation Suggestions:** Train a second, sequence-to-sequence model (`CodeT5`) to automatically suggest code fixes for detected vulnerabilities.
-   **Language Expansion:** Fine-tune separate models for other languages like Python, Java, and PHP using relevant datasets.
-   **IDE Integration:** Create a VS Code extension for real-time vulnerability feedback as developers write code.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
