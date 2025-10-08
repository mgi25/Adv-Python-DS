# pip install Gooey
from gooey import Gooey, GooeyParser
import os

@Gooey(program_name="Basic Resume Form")
def main():
    parser = GooeyParser(description="Enter basic resume details")
    parser.add_argument("Name", help="Your full name")
    parser.add_argument("Age", help="Your age (number)", type=int)
    parser.add_argument("Skills", help="List your skills (one per line)", widget="Textarea")
    parser.add_argument("Photo", help="Choose a profile photo (optional)", widget="FileChooser")

    args = parser.parse_args()

    # Simple validation
    if args.Age < 0:
        print("❌ Age must be non-negative.")
        return

    # Format skills (split lines, drop empties)
    skill_lines = [s.strip() for s in args.Skills.splitlines() if s.strip()]

    print("="*40)
    print("            BASIC RESUME")
    print("="*40)
    print(f"Name : {args.Name}")
    print(f"Age  : {args.Age}")
    print("-"*40)
    print("Skills:")
    if skill_lines:
        for i, sk in enumerate(skill_lines, 1):
            print(f"  {i}. {sk}")
    else:
        print("  (No skills provided)")
    print("-"*40)
    if args.Photo and os.path.isfile(args.Photo):
        print(f"Photo Path: {args.Photo}")
    else:
        print("Photo Path: (none)")
    print("="*40)

if __name__ == "__main__":
    main()
