import os
from gooey import Gooey, GooeyParser

@Gooey(program_name="Image File Renamer")
def main():
    parser = GooeyParser(description="Rename all images in a folder with a prefix")

    parser.add_argument(
        "FolderPath",
        help="Choose the folder containing images",
        widget="DirChooser"
    )
    parser.add_argument(
        "Prefix",
        help="Enter the prefix for renamed images"
    )

    args = parser.parse_args()
    folder = args.FolderPath
    prefix = args.Prefix

    # Allowed image extensions
    extensions = [".jpg", ".jpeg", ".png"]

    try:
        files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in extensions]
        if not files:
            print("❌ No image files found in the folder.")
            return

        for i, filename in enumerate(files, start=1):
            ext = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{i}{ext}"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")

        print(f"\n✅ Renaming complete! {len(files)} files renamed.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
