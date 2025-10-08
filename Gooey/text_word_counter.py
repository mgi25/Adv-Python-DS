# pip install gooey docx2txt
from gooey import Gooey, GooeyParser
import docx2txt
import re

WORD_TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[’'\-][A-Za-z0-9]+)*")

@Gooey(program_name="Word (.docx) Word Counter")
def main():
    parser = GooeyParser(description="Count words in a Word (.docx) file")
    parser.add_argument("FilePath", help="Choose a .docx file", widget="FileChooser")
    args = parser.parse_args()

    try:
        # Extract text from paragraphs, tables, headers/footers, and text boxes
        text = docx2txt.process(args.FilePath)
        text = re.sub(r"\s+", " ", text).strip()

        # Tokenize similar to Word: include numbers, keep contractions/hyphenated words as one
        words = WORD_TOKEN.findall(text)
        print(f"File: {args.FilePath}")
        print(f"Total Words: {len(words)}")
    except Exception as e:
        print(f"Error: {e}\nTip: Ensure the file is .docx and docx2txt is installed.")

if __name__ == "__main__":
    main()
