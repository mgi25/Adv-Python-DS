import os
from gooey import Gooey, GooeyParser

@Gooey(program_name="File Renamer")
def main():
    parser = GooeyParser(description="Rename a selected file")

    parser.add_argument(
        "FilePath",
        help="Choose the file you want to rename",
        widget="FileChooser"
    )
    parser.add_argument(
        "NewName",
        help="Enter the new name for the file (with extension, e.g., newfile.txt)"
    )

    args = parser.parse_args()

    file_path = args.FilePath
    new_name = args.NewName
    folder = os.path.dirname(file_path)
    new_path = os.path.join(folder, new_name)

    try:
        os.rename(file_path, new_path)
        print(f"✅ File renamed successfully!")
        print(f"Old Name: {os.path.basename(file_path)}")
        print(f"New Name: {new_name}")
    except Exception as e:
        print(f"❌ Error renaming file: {e}")

if __name__ == "__main__":
    main()
