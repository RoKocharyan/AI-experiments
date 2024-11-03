def calculate_volume(length, width, height):
    return length * width * height

def main():
    print("Welcome to Volume Calculator")
    while True:
        try:
            length = float(input("Enter Length: "))
            width = float(input("Enter Width: "))
            height = float(input("Enter Height: "))
            volume = calculate_volume(length, width, height)
            print(f"The volume of the cuboid is {volume} cubic units.")
            cont = input("Do you want to continue? (yes/no): ")
            if cont.lower() != 'yes':
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()