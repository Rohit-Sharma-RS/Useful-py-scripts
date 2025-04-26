import re
import chardet
from datetime import timedelta
import os

# DEFAULT_PATHS = [
#     r"D:\Suits S01-S09 (2011-)\Suits S01 (360p re-webrip)\Suits - 1x06 - Tricks of the Trade.HDTV.en.srt",
#     # Add more default paths here if you want
# ]

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def parse_timestamp(timestamp):
    parts = re.split('[:,]', timestamp)
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    milliseconds = int(parts[3])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def format_timestamp(td):
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def clean_path(path):
    path = path.strip().strip('"').strip("'")
    path = os.path.normpath(path)
    return path

def shift_srt_timestamps_in_place(file_path, offset_seconds):
    encoding = detect_encoding(file_path)

    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()

    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    def shift_match(match):
        start = parse_timestamp(match.group(1))
        end = parse_timestamp(match.group(2))
        offset = timedelta(seconds=offset_seconds)
        shifted_start = format_timestamp(start + offset)
        shifted_end = format_timestamp(end + offset)
        return f"{shifted_start} --> {shifted_end}"

    updated_content = timestamp_pattern.sub(shift_match, content)

    # Save to a temp file, then replace original
    temp_path = file_path + ".tmp"
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    os.remove(file_path)
    os.rename(temp_path, file_path)

    print(f"[✓] Shifted and replaced original: {file_path}")

if __name__ == "__main__":
    raw_input = input("Enter paths to .srt files separated by a semicolon (;) or press Enter to use defaults:\n").strip()

    if raw_input:
        paths = [clean_path(p) for p in raw_input.split(";") if p.strip()]
    else:
        paths = DEFAULT_PATHS

    try:
        offset = float(input("Enter offset in seconds (positive for delay, negative for advance): "))
    except ValueError:
        print("Invalid offset. Please enter a numeric value.")
        exit(1)

    for path in paths:
        if not os.path.isfile(path):
            print(f"[✗] File not found: {path}")
            continue
        try:
            shift_srt_timestamps_in_place(path, offset)
        except Exception as e:
            print(f"[✗] Error processing {path}: {e}")
