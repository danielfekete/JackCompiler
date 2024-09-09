# Jack Compiler

This project is a full implementation of the **Jack Compiler**, part of the **Nand2Tetris** course (Projects 10 & 11). The compiler translates high-level Jack programs into VM (Virtual Machine) code, which can be executed on the Hack computer platform.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Directory Structure](#directory-structure)
- [Limitations](#limitations)
- [Acknowledgements](#acknowledgements)

## Project Overview

The Jack Compiler takes a `.jack` source file and translates it into VM code, which can be executed by the **Nand2Tetris VM Emulator**. This compiler implements:

- **Lexical Analysis (Tokenization)**: Breaking the Jack code into meaningful tokens.
- **Syntax Analysis (Parsing)**: Parsing tokens to validate syntax and generate a parse tree.
- **Code Generation**: Generating corresponding VM commands from the parse tree.

## Features

- **Full Jack language support**, including:
  - Variables (local, static, field, argument)
  - Functions, methods, and constructors
  - Conditional statements (if-else)
  - Loops (while)
  - Expressions and arithmetic operations
  - Class-based object creation
- **OS Library Support**: The compiler recognizes and handles calls to built-in OS classes like `Output`, `String`, `Array`, and more.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/jack-compiler.git
   cd jack-compiler

   ```

2. **This project uses Python, so ensure you have Python 3.x installed. Optionally, create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

## Usage

1. **Compiling a Jack File**:To compile a Jack file or directory of Jack files, use the following command:

   ```bash
   python main.py path/to/your/jackfile.jack
   ```

   Example:

   ```bash
   python JackCompiler.py ./tests/Seven.jack
   ```

2. **Compiling a directory:** To compile all .jack files in a directory:

   ```bash
   python JackCompiler.py ./tests/Seven.jack
   ```

3. **Output**: The compiler will generate a .vm file for each compiled .jack file in the same directory.

## Testing

The Jack Compiler has been tested against all provided test programs from the Nand2Tetris suite, including:

- Seven: A simple program for testing arithmetic.
- ConvertToBin: Converts a decimal number to binary.
- Square: Draws a square on the screen and allows it to be moved.
- Pong: A classic Pong game implemented in Jack.

To run the tests, you can:

1. Compile the .jack files using the JackCompiler.
2. Run the generated .vm files in the VM Emulator.

## Directory Structure

```bash
jack-compiler/
│
├── jackCompiler.py # Main driver for the compiler
├── compilationEngine.py # Handles compilation logic for each construct
├── jackTokenizer.py # Breaks Jack code into tokens
├── symbolTable.py # Manages symbol tables (variables, subroutine symbols)
├── vmWriter.py # Translates parsed code into VM code
├── osUtils.py # Contains os utilites such as os subroutine data
├── tests/ # Contains Jack test files for the compiler
│ ├── Seven.jack
│ ├── Pong.jack
│ └── ...
├── README.md # Project documentation
└── ...
```

## Limitations

- Error Handling: This compiler assumes that the input .jack code is valid. No extensive error handling is implemented for malformed code.
- Performance: The focus of this project was on correctness, so performance optimizations were not a priority.

## Acknowledgements

This project is based on the **Nand2Tetris** course by **Shimon Schocken** and **Noam Nisan**. Special thanks to the creators for the amazing course and resources.
