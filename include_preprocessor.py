import os
import re

def include_file(match):
    filename = match.group(1)
    file_path = os.path.join(filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        # Rekursive Ersetzung im gelesenen Inhalt
        return include_files(content)
    else:
        return f"{{{{{filename}}}}}"  # Beibehaltung des Musters, falls Datei fehlt

def include_files(markdown_content: str):
    pattern = r"\{\{(.+?)\}\}"
    return re.sub(pattern, include_file, markdown_content)

def preprocess(markdown_content: str) -> str:
    result = include_files(markdown_content)
    return result
