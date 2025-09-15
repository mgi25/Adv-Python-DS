# Create a BMI Calculator using Gooey where
# the user enters weight and height.

from gooey import Gooey, GooeyParser

@Gooey(program_name="BMI Calculator")  #decorater to create GUI
def main():
    parser = GooeyParser(description="Calculate your Body Mass Index (BMI)")

    parser.add_argument("Weight", help="Enter your weight in kilograms", type=float)
    parser.add_argument("Height", help="Enter your height in centimeters", type=float)

    args = parser.parse_args()

    # Convert height from cm to meters
    height_m = args.Height / 100  

    if height_m <= 0:
        print("Height must be greater than 0.")
        return

    bmi = args.Weight / (height_m ** 2)

    print(f"Your BMI is: {bmi:.2f}")

    if bmi < 18.5:
        print("You are Underweight.")
    elif 18.5 <= bmi < 24.9:
        print("You have a Normal weight.")
    elif 25 <= bmi < 29.9:
        print("You are Overweight.")
    else:
        print("You are Obese.")

if __name__ == "__main__":
    main()
