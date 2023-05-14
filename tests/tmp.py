import pathlib





def main():
    p = pathlib.Path("/home/kim/Documents/github/marin-jovanovic/ocr/a/b/c/d/d/d/d/")
    print(f"{p}")

    print(f"{create_nested_directory(p)=}")

if __name__ == '__main__':
    main()