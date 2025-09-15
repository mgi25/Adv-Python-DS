from gooey import Gooey, GooeyParser

@Gooey(program_name="Simple Interest Calculator")
def main():
    parser = GooeyParser(description="Calculate Simple Interest and Total Amount")

    parser.add_argument("Principal", help="Enter the principal amount", type=float)
    parser.add_argument("Rate", help="Enter the annual interest rate (%)", type=float)
    parser.add_argument("Time", help="Enter the time in years", type=float)

    args = parser.parse_args()

    # Simple Interest formula: (P × R × T) / 100
    si = (args.Principal * args.Rate * args.Time) / 100
    total = args.Principal + si

    print(f"Principal Amount: {args.Principal}")
    print(f"Rate of Interest: {args.Rate}%")
    print(f"Time: {args.Time} years")
    print(f"Simple Interest = {si:.2f}")
    print(f"Total Amount (Principal + Interest) = {total:.2f}")

if __name__ == "__main__":
    main()
