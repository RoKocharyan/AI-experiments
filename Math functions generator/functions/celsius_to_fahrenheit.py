def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def main():
    while True:
        try:
            celsius = float(input("Enter temperature in Celsius: "))
            fahrenheit = round(celsius_to_fahrenheit(celsius), 2)
            print(f"{celsius}C is equal to {fahrenheit}F")
        except ValueError:
            print("Invalid input. Please enter a number.")
        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != 'y':
            break


if __name__ == "__main__":
    main()