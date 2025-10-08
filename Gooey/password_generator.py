# pip install Gooey
import random
import string
from gooey import Gooey, GooeyParser

# Symbol set for passwords
SYM = "!@#$%^&*_-+=?"

@Gooey(program_name="Password Generator")
def main():
    parser = GooeyParser(description="Generate a random password")

    # ✅ Slider as an optional flag (so no 'field required' error)
    parser.add_argument(
        "--length",
        type=int,
        default=12,
        help="Password length (6–20)",
        widget="Slider",
        gooey_options={"min": 6, "max": 20, "increment": 1},
    )

    # Checkboxes
    parser.add_argument("--include_digits", action="store_true", help="Include digits (0-9)")
    parser.add_argument("--include_symbols", action="store_true", help=f"Include symbols ({SYM})")

    args = parser.parse_args()

    # Build character pool
    pool = list(string.ascii_letters)  # always letters
    if args.include_digits:
        pool += list(string.digits)
    if args.include_symbols:
        pool += list(SYM)

    if not pool:
        print("❌ No characters available to generate password.")
        return

    # Always ensure at least one letter, digit, symbol if chosen
    password_chars = []
    password_chars.append(random.choice(string.ascii_letters))
    if args.include_digits:
        password_chars.append(random.choice(string.digits))
    if args.include_symbols:
        password_chars.append(random.choice(SYM))

    # Fill the rest
    while len(password_chars) < args.length:
        password_chars.append(random.choice(pool))

    random.shuffle(password_chars)
    password = "".join(password_chars[:args.length])

    print(f"✅ Generated Password: {password}")

if __name__ == "__main__":
    main()
