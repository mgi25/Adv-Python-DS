from gooey import Gooey, GooeyParser

@Gooey(program_name="Marks Calculator")
def main():
    parser = GooeyParser(description="Enter marks of 5 subjects")

    parser.add_argument("Subject1", help="Enter marks for Subject 1 (0-100)", type=float)
    parser.add_argument("Subject2", help="Enter marks for Subject 2 (0-100)", type=float)
    parser.add_argument("Subject3", help="Enter marks for Subject 3 (0-100)", type=float)
    parser.add_argument("Subject4", help="Enter marks for Subject 4 (0-100)", type=float)
    parser.add_argument("Subject5", help="Enter marks for Subject 5 (0-100)", type=float)

    args = parser.parse_args()

    marks = [args.Subject1, args.Subject2, args.Subject3, args.Subject4, args.Subject5]

    # Validation: All marks should be between 0 and 100
    for i, m in enumerate(marks, start=1):
        if m < 0 or m > 100:
            print(f"❌ Error: Marks in Subject {i} must be between 0 and 100.")
            return

    total = sum(marks)
    percentage = total / 5

    print(f"Marks Entered: {marks}")
    print(f"Total Marks = {total}")
    print(f"Percentage = {percentage:.2f}%")

if __name__ == "__main__":
    main()
