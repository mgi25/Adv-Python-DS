from gooey import Gooey, GooeyParser

@Gooey
def main():
    parser = GooeyParser(description='Demo App')
    parser.add_argument('name', help='Enter your name')
    parser.add_argument('age', type=int, help='Enter your age')
    args = parser.parse_args()
    print(f'Hello {args.name}, you are {args.age} years old!')

if __name__ == '__main__':
    main()