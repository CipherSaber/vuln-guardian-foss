# ===================================================================
# SecureCode AI: Command-Line Scanner (MVP - Final Version)
# ===================================================================

import sys
import os
from transformers import pipeline, logging as hf_logging

# This is a trick to allow this script to import from the 'src' folder
# It adds the parent directory of the script's location to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from src.parser import parse_c_functions
except ImportError:
    print("[!] Error: Could not import 'parse_c_functions' from 'src/parser.py'.")
    print("[!] Please ensure 'src/parser.py' exists and is in the correct location.")
    sys.exit(1)

# --- Configuration ---
# Your actual model name from the Hugging Face Hub
MODEL_NAME = "jacpacd/vuln-detector-codebert"

# Suppress the informational "Using a pipeline without..." warning from transformers
hf_logging.set_verbosity_error()

# ===================================================================
# Main Application Logic
# ===================================================================

def load_model():
    """Loads the text-classification pipeline from the Hugging Face Hub."""
    print(f"[*] Loading model '{MODEL_NAME}' from Hugging Face Hub...")
    print("[*] (This may take a moment on the first run as the model is downloaded)...")
    try:
        # The 'pipeline' is the easiest way to use a model for inference.
        classifier = pipeline("text-classification", model=MODEL_NAME)
        print("[+] Model loaded successfully.")
        return classifier
    except Exception as e:
        print(f"\n[!] FATAL ERROR: Could not load model from Hugging Face Hub.")
        print(f"[!] Details: {e}")
        print("[!] Please check the following:")
        print("    1. The model name in the script is correct.")
        print("    2. You have a stable internet connection.")
        print("    3. The model exists at the specified Hugging Face repository.")
        sys.exit(1)

def scan_file(classifier, file_path):
    """
    Scans a single C file for vulnerabilities using the provided classifier.
    
    Args:
        classifier: The loaded Hugging Face pipeline.
        file_path (str): The path to the C file to scan.
    """
    print(f"\n[*] Scanning file: {file_path}")
    
    # --- 1. Read and Parse the File ---
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        functions = parse_c_functions(file_bytes)
        
        if not functions:
            print("[-] No functions were found to analyze in this file.")
            return

        print(f"[+] Found {len(functions)} functions to analyze.")
        vulnerabilities_found = 0

    except FileNotFoundError:
        print(f"[!] Error: The file at '{file_path}' was not found.")
        return
    except Exception as e:
        print(f"[!] Error reading or parsing file: {e}")
        return

    # --- 2. Classify Each Function ---
    function_codes = [func['code'] for func in functions]
    print("[*] Analyzing functions with the AI model...")
    
    # === THE CRITICAL FIX IS HERE ===
    # Add `truncation=True` to handle functions that are longer than the model's
    # maximum input size (512 tokens). This prevents the RuntimeError.
    results = classifier(function_codes, top_k=None, truncation=True) 

    for i, func in enumerate(functions):
        prediction = results[i]
        
        # Find the prediction score for the 'vulnerable' label (LABEL_1)
        vulnerable_prediction = next((item for item in prediction if item['label'] == 'LABEL_1'), None)
        
        # A confidence threshold of 50%
        if vulnerable_prediction and vulnerable_prediction['score'] > 0.5: 
            vulnerabilities_found += 1
            print("\n-------------------------------------------")
            print(f"[!] VULNERABILITY DETECTED!")
            print(f"    - Function: {func['name']}")
            print(f"    - Location: Line {func['line']}")
            print(f"    - Confidence: {vulnerable_prediction['score']:.2%}")
            print("-------------------------------------------")

    # --- 3. Final Report ---
    if vulnerabilities_found > 0:
        print(f"\n[+] Scan Complete. Found {vulnerabilities_found} potential vulnerabilities.")
    else:
        print("\n[+] Scan Complete. No potential vulnerabilities were detected.")

# ===================================================================
# Script Entry Point
# ===================================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nSecureCode AI Scanner")
        print("Usage: python scan.py <path_to_c_file_to_scan>")
        sys.exit(1)
    
    model_classifier = load_model()
    file_to_scan = sys.argv[1]
    scan_file(model_classifier, file_to_scan)