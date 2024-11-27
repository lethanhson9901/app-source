import os
from pathlib import Path


def remove_comments(code):
    lines = code.split("\n")
    cleaned_lines = [line for line in lines if not line.strip().startswith("#")]
    return "\n".join(cleaned_lines)


def combine_python_files(source_dir: str, output_file: str) -> None:
    source_path = Path(source_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(source_path):
            python_files = [f for f in files if f.endswith(".py")]

            for file_name in sorted(python_files):
                file_path = Path(root) / file_name
                abs_path = str(file_path.absolute())

                outfile.write(f"## {abs_path}\n\n")
                outfile.write("```python\n")

                try:
                    with open(file_path, encoding="utf-8") as pyfile:
                        content = pyfile.read()
                        cleaned_content = remove_comments(content)
                        if (
                            cleaned_content.strip()
                        ):  # Only write if there's content after removing comments
                            outfile.write(cleaned_content)
                            if not cleaned_content.endswith("\n"):
                                outfile.write("\n")
                except Exception as e:
                    outfile.write(f"Error reading file: {str(e)}\n")

                outfile.write("```\n\n")


if __name__ == "__main__":
    source_directory = "/home/son/Documents/note/project/ci-cd-setup/app-source/src"
    output_markdown = "python_code_collection.md"

    try:
        combine_python_files(source_directory, output_markdown)
        print(f"Successfully combined Python files into {output_markdown}")
    except Exception as e:
        print(f"Error: {str(e)}")
