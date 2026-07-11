import os
import subprocess
import sys


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    entry = os.path.join(project_root, "src", "main.py")
    src_path = os.path.join(project_root, "src")
    assets_src = os.path.join(project_root, "assets")
    icon_ico = os.path.join(assets_src, "icon.ico")

    sep = os.pathsep
    # Empaqueta toda la carpeta assets (estilos + ícono) junto al binario
    add_data = f"{assets_src}{sep}assets"

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
        "--paths",
        src_path,
        "--add-data",
        add_data,
    ]

    if os.path.isfile(icon_ico):
        cmd += ["--icon", icon_ico]

    cmd.append(entry)

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
