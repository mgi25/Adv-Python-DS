from gooey import Gooey, GooeyParser

@Gooey(program_name="Currency Converter")
def main():
    parser = GooeyParser(description="Convert currency (INR, USD, EUR) using fixed rates")

    parser.add_argument("Amount", help="Enter the amount to convert", type=float)
    parser.add_argument(
        "FromCurrency",
        help="Choose the currency you have",
        choices=["INR", "USD", "EUR"]
    )
    parser.add_argument(
        "ToCurrency",
        help="Choose the currency you want",
        choices=["INR", "USD", "EUR"]
    )

    args = parser.parse_args()

    amount = args.Amount
    from_currency = args.FromCurrency
    to_currency = args.ToCurrency

    # Fixed conversion rates (for demo purpose)
    rates = {
        "INR": {"USD": 0.012, "EUR": 0.011, "INR": 1},
        "USD": {"INR": 83.0, "EUR": 0.92, "USD": 1},
        "EUR": {"INR": 90.0, "USD": 1.09, "EUR": 1},
    }

    if from_currency == to_currency:
        result = amount
    else:
        result = amount * rates[from_currency][to_currency]

    print(f"{amount} {from_currency} = {result:.2f} {to_currency}")

if __name__ == "__main__":
    main()
