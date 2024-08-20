import sys
import os
import jackAnalyzer

def main():
    src = sys.argv[1]

    # Check if the source path exists
    if not os.path.exists(src):
        print('Invalid folder/file path')
        return

    jackAnalyzer.JackAnalyzer(src)

if __name__ == '__main__':
    main()