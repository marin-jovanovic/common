import argparse
import pathlib
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s")
    parser.add_argument("--description", "-d")

    args = parser.parse_args()

    base_dir = pathlib.Path(args.source)

    result = get_changed_files(base_dir)

    print(result)
    print(80 * "-")

    to_c = set()

    for line in result.split("\n"):
        if line.startswith("	"):
            line = line.strip()

            if line.startswith("renamed:"):
                line = line.split("-> ")[1]
                to_c.add(line)
                continue

            try:
                line = line.split(":")[1].strip()
            except IndexError:
                pass

            to_c.add(line)

    sh_script_content = []

    print("enter messages")

    for file in set(to_c):
        if not args.description:
            desc = input(f"{file}\n")
        else:
            desc = args.description

        message = "git commit -m " + f'\"{" ".join(file.split("/"))} - {desc}\"'

        file_full_path = base_dir / file
        sh_script_content.append(f"git add {file_full_path}")
        sh_script_content.append(message)

    with open('git.sh', 'w+') as f:
        [f.write(f"{i}\n") for i in sh_script_content]


def get_changed_files(base_dir):
    result = subprocess.run(
        ["git", "-C", base_dir, "status"],
        capture_output=True, text=True
    )
    return result.stdout


if __name__ == '__main__':
    main()