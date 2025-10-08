from gooey import Gooey, GooeyParser

@Gooey(program_name="Email Generator")
def main():
    parser = GooeyParser(description="Generate an Email Address")

    parser.add_argument("Name", help="Enter your name (no spaces)")
    parser.add_argument(
        "Domain",
        help="Choose email domain",
        choices=["gmail.com", "yahoo.com", "outlook.com"]
    )

    args = parser.parse_args()

    # Clean name (remove spaces, lowercase)
    username = args.Name.replace(" ", "").lower()
    email = f"{username}@{args.Domain}"

    print(f"✅ Your generated email address is: {email}")

if __name__ == "__main__":
    main()
