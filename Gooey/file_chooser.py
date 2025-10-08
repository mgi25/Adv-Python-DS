from gooey import Gooey, GooeyParser

@Gooey(program_name="Text File Word & Character Counter")
def main():
    parser = GooeyParser(description="Count words and characters in a text file")

    parser.add_argument(
        "FilePath",
        help="Choose a text (.txt) file",
        widget="FileChooser"
    )

    args = parser.parse_args()

    try:
        with open(args.FilePath, "r", encoding="utf-8") as f:
            text = f.read()

        # Count words and characters
        words = text.split()
        word_count = len(words)
        char_count = len(text)

        print(f"📄 File: {args.FilePath}")
        print(f"Total Words: {word_count}")
        print(f"Total Characters: {char_count}")

    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    main()
