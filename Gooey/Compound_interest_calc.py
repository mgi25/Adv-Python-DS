from gooey import Gooey, GooeyParser

@Gooey(program_name="Compound Interest Calculator")
def main():
    parser = GooeyParser(description="Calculate Compound Interest")

    parser.add_argument("Principal", help="Enter the principal amount", type=float)
    parser.add_argument("Rate", help="Enter the annual interest rate (%)", type=float)
    parser.add_argument("Time", help="Enter the time in years", type=float)
    parser.add_argument("CompoundsPerYear", help="Enter compounds per year (e.g., 1=yearly, 4=quarterly, 12=monthly)", type=int)

    args = parser.parse_args()

    P = args.Principal
    R = args.Rate / 100  # convert % to decimal
    T = args.Time
    n = args.CompoundsPerYear

    # Compound Interest formula
    A = P * (1 + R/n) ** (n*T)

    print(f"Principal Amount: {P}")
    print(f"Rate of Interest: {args.Rate}%")
    print(f"Time: {T} years")
    print(f"Compounds per Year: {n}")
    print(f"Final Amount (A) = {A:.2f}")

if __name__ == "__main__":
    main()
