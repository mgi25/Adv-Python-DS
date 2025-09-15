from gooey import Gooey, GooeyParser

@Gooey(program_name="Temperature Converter")
def main():
    parser = GooeyParser(description="Convert between Celsius, Fahrenheit, and Kelvin")

    parser.add_argument("Temperature", help="Enter the temperature value", type=float)
    parser.add_argument(
        "Conversion",
        help="Choose conversion type",
        choices=["Celsius to Fahrenheit", "Fahrenheit to Celsius", "Celsius to Kelvin", "Kelvin to Celsius"]
    )

    args = parser.parse_args()

    temp = args.Temperature
    conv = args.Conversion

    if conv == "Celsius to Fahrenheit":
        result = (temp * 9/5) + 32
        print(f"{temp} °C = {result:.2f} °F")
    elif conv == "Fahrenheit to Celsius":
        result = (temp - 32) * 5/9
        print(f"{temp} °F = {result:.2f} °C")
    elif conv == "Celsius to Kelvin":
        result = temp + 273.15
        print(f"{temp} °C = {result:.2f} K")
    elif conv == "Kelvin to Celsius":
        result = temp - 273.15
        print(f"{temp} K = {result:.2f} °C")

if __name__ == "__main__":
    main()
