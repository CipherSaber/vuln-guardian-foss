import os
import sys
import json
from tqdm import tqdm

# This is a trick to allow this script to import from the 'src' folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.parser import parse_c_functions

# --- CONFIGURATION ---
DATASET_ROOT_FOLDER = "2022-08-11-juliet-c-cplusplus-v1-3-1-with-extra-support"
OUTPUT_FILE = "dataset.jsonl"
# Increase the minimum length to ensure we get real code
MIN_FUNCTION_LENGTH = 75 

def process_sard_by_parsing():
    """
    Processes the SARD Juliet Test Suite by parsing and STRICTLY FILTERING functions.
    """
    print(f"Starting SARD processing with strict filtering from: {DATASET_ROOT_FOLDER}...")

    if not os.path.exists(DATASET_ROOT_FOLDER):
        print(f"ERROR: Directory not found at '{DATASET_ROOT_FOLDER}'")
        return

    file_paths = []
    for root, _, files in os.walk(DATASET_ROOT_FOLDER):
        for file in files:
            if file.endswith('.c'):
                file_paths.append(os.path.join(root, file))

    print(f"Found {len(file_paths)} total C files to parse.")
    
    functions_saved = 0
    with open(OUTPUT_FILE, 'w') as f:
        for file_path in tqdm(file_paths, desc="Parsing C files"):
            try:
                with open(file_path, 'rb') as code_file:
                    file_bytes = code_file.read()
                
                extracted_functions = parse_c_functions(file_bytes)

                for func in extracted_functions:
                    func_name = func['name'].lower()
                    func_code = func['code']
                    label = -1
                    
                    # --- NEW, STRICTER FILTERING LOGIC ---
                    
                    # Filter 1: Function name MUST contain these specific patterns.
                    # This eliminates simple "good1", "bad1", etc.
                    is_main_bad_func = "_bad" in func_name
                    is_good_fix_func = "goodg2b" in func_name or "goodb2g" in func_name
                    
                    if not is_main_bad_func and not is_good_fix_func:
                        continue # Skip this function immediately

                    # Filter 2: The function's code MUST be of a minimum length.
                    # This eliminates all empty or trivial functions like "void good1() {}"
                    if len(func_code) < MIN_FUNCTION_LENGTH:
                        continue # Skip this function

                    # If the function passes BOTH filters, we assign a label and save it.
                    if is_main_bad_func:
                        label = 1
                    elif is_good_fix_func:
                        label = 0
                    
                    if label != -1:
                        data_entry = {"code": func_code, "label": label}
                        f.write(json.dumps(data_entry) + '\n')
                        functions_saved += 1

            except Exception as e:
                continue

    print(f"\nSARD processing complete.")
    print(f"Filtered and saved {functions_saved} high-quality functions to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    process_sard_by_parsing()