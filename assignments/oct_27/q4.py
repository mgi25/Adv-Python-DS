# Q4. Create a Gooey-based command-line GUI that accepts two numerical inputs and performs basic arithmetic operations (addition, subtraction, multiplication, division).


from gooey import Gooey, GooeyParser

@Gooey(program_name="Simple Arithmetic Calculator",
       program_description="A Gooey-based calculator for basic arithmetic operations.")
def main():
    # 1️⃣ Create GUI parser
    parser = GooeyParser(description="Enter two numbers and choose an operation.")
    
    # 2️⃣ Number inputs
    parser.add_argument("Number_1", type=float, help="Enter the first number")
    parser.add_argument("Number_2", type=float, help="Enter the second number")
    
    # 3️⃣ Operation selection (Dropdown menu)
    parser.add_argument(
        "Operation",
        choices=["Addition", "Subtraction", "Multiplication", "Division"],
        help="Select the arithmetic operation to perform"
    )

    # 4️⃣ Parse user inputs
    args = parser.parse_args()
    a = args.Number_1
    b = args.Number_2
    op = args.Operation

    # 5️⃣ Perform selected operation
    print("=== Result ===")
    if op == "Addition":
        print(f"{a} + {b} = {a + b}")
    elif op == "Subtraction":
        print(f"{a} - {b} = {a - b}")
    elif op == "Multiplication":
        print(f"{a} × {b} = {a * b}")
    elif op == "Division":
        if b != 0:
            print(f"{a} ÷ {b} = {a / b}")
        else:
            print("Error: Division by zero ❌")
    print("==============================")

# Run GUI
if __name__ == "__main__":
    main()
