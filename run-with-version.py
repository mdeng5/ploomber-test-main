import argparse
import os
import subprocess
import platform


def main():
    parser = argparse.ArgumentParser(description="Run a .md file with specified Python version in Docker")
    parser.add_argument('file_path', type=str, help="Path to the .md file to run")
    parser.add_argument('--version', type=str, required=True, help="Python version to use (e.g., 3.10, 3.11)")

    args = parser.parse_args()

    file_path = args.file_path

    # Windows uses different slashes for directories
    if platform.system() == 'Windows':
        file_path = file_path.replace('\\', '/')

    # Validate file path
    if not os.path.isfile(file_path):
        print("File not found: {}".format(file_path))
        print("Please make sure the .md file is in the /examples/ folder")
        exit(1)

    python_version = args.version
    # Validate Python version
    if not python_version.startswith("3."):
        print(f"Error: Invalid Python version: {python_version}")
        exit(1)

    dockerfile = f"""
    FROM python:{python_version}-slim
    COPY {file_path} /app/
    WORKDIR /app
    RUN pip install markdown
    CMD python3 -m markdown {os.path.basename(file_path)}
    """

    dockerfile_path = 'Dockerfile'
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile)

    # Build the Docker container
    image_tag = f"md-runner:{python_version}"
    try:
        subprocess.run(['docker', 'build', '-t', image_tag, '.'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to build Docker image: {e}")
        exit(1)

    # Run Docker container
    try:
        subprocess.run(['docker', 'run', '--rm', image_tag], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to run Docker container: {e}")
        exit(1)

if __name__ == '__main__':
    main()
