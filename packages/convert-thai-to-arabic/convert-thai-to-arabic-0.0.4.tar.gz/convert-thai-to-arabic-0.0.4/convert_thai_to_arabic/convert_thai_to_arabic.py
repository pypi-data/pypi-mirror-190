import argparse
import os

def convert_thai_to_arabic(file_name):
    # Thai numbers to Arabic numbers mapping
    thai_to_arabic = {'๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9'}

    # Create a new file name with Arabic numbers
    new_file_name = ''
    for char in file_name:
        if char in thai_to_arabic:
            new_file_name += thai_to_arabic[char]
        else:
            new_file_name += char

    return new_file_name

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Convert Thai numbers in file names to Arabic numbers')

    # Add the directory argument
    parser.add_argument('-d', '--directory', help='The path to the directory containing the files', default=os.getcwd(), required=False)

    # Parse the arguments
    args = parser.parse_args()

    renamed_files = 0

    try:
        # Loop through all the files in the directory
        for filename in os.listdir(args.directory):
            file_path = os.path.join(args.directory, filename)

            # Skip non-files
            if not os.path.isfile(file_path):
                continue

            new_file_name = convert_thai_to_arabic(filename)
            new_file_path = os.path.join(args.directory, new_file_name)

            # Rename the file
            os.rename(file_path, new_file_path)

            renamed_files += 1

        print(f'Successfully renamed {renamed_files} files.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
