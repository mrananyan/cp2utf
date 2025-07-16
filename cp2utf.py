#!/usr/bin/env python3

import os
import chardet

TARGET_EXTENSIONS = {'.php', '.inc', '.tpl', '.js', '.css'}

def is_cp1251(filepath):
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding and encoding.lower() in ('windows-1251', 'cp1251') and confidence > 0.8, raw_data

def convert_to_utf8_with_bom(filepath):
    is_cp, raw_data = is_cp1251(filepath)
    if is_cp:
        try:
            text = raw_data.decode('cp1251')
            with open(filepath, 'w', encoding='utf-8-sig') as f:
                f.write(text)
            print(f"[Converted] {filepath}")
        except Exception as e:
            print(f"[Error] Failed to convert {filepath}: {e}")
    else:
        print(f"[Skipped] {filepath} (not cp1251)")

def scan_and_convert(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in TARGET_EXTENSIONS:
                full_path = os.path.join(root, file)
                convert_to_utf8_with_bom(full_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python convert_cp1251_to_utf8.py <directory>")
        sys.exit(1)

    scan_and_convert(sys.argv[1])

