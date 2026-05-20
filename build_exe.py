import os
import subprocess
import sys


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    entry = os.path.join(project_root, "src", "main.py")
    styles_src = os.path.join(project_root, "assets", "styles")
    add_data = f"{styles_src}{os.pathsep}assets/styles"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        "Margoth",
        "--windowed",
        "--onedir",
        "--noconfirm",
        "--clean",
        "--add-data",
        add_data,
        entry,
    ]

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
