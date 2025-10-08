from gooey import Gooey, GooeyParser

@Gooey(program_name="File Merger Tool")
def main():
    parser = GooeyParser(description="Merge two text files into one")

    parser.add_argument(
        "File1",
        help="Choose the first text file",
        widget="FileChooser"
    )
    parser.add_argument(
        "File2",
        help="Choose the second text file",
        widget="FileChooser"
    )
    parser.add_argument(
        "OutputFile",
        help="Enter the output file name (e.g., merged.txt)"
    )

    args = parser.parse_args()

    try:
        with open(args.File1, "r", encoding="utf-8") as f1:
            content1 = f1.read()
        with open(args.File2, "r", encoding="utf-8") as f2:
            content2 = f2.read()

        with open(args.OutputFile, "w", encoding="utf-8") as out:
            out.write(content1 + "\n" + content2)

        print(f"✅ Files merged successfully into: {args.OutputFile}")

    except Exception as e:
        print(f"❌ Error merging files: {e}")

if __name__ == "__main__":
    main()
