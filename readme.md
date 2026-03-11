# Advanced Calculator Application

## Project Description

An educational advanced calculator application that showcases object-oriented programming principles, design patterns, and Python best practices. The calculator provides a comprehensive command-line interface (REPL) with support for multiple arithmetic operations, calculation history management with undo/redo functionality, automatic logging, and data persistence.

### Key Features

- **10 Arithmetic Operations**: Addition, subtraction, multiplication, division, power, root, modulus, integer division, percentage, and absolute difference
- **Design Patterns Implementation**:
  - **Factory Pattern**: Dynamic operation creation and management
  - **Memento Pattern**: Undo/redo functionality with state management
  - **Observer Pattern**: Event-driven logging and auto-save features
  - **Singleton & Strategy Patterns**: Configuration and operation management
- **Robust Error Handling**: Custom exception hierarchy for operational and validation errors
- **Input Validation**: Comprehensive validation of numerical inputs and operation constraints
- **Logging System**: Detailed application logging with file persistence
- **History Management**: CSV-based calculation history with pandas serialization
- **Configuration Management**: Environment-based configuration with python-dotenv
- **Comprehensive Testing**: 99% test coverage with pytest
- **CI/CD Pipeline**: GitHub Actions automation with coverage enforcement

---

## Installation Instructions

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment manager (venv)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd module5_is601
```

### Step 2: Create and Activate Virtual Environment

**Windows (PowerShell/CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python main.py
```

You should see the calculator prompt: `Enter command:`

---

## Configuration Setup

The application uses environment variables for configuration. A `.env` file is provided in the project root with the following settings:

### .env Configuration Parameters

```env
CALCULATOR_LOG_DIR=logs                 # Directory for application logs
CALCULATOR_HISTORY_DIR=history          # Directory for calculation history CSV files
CALCULATOR_MAX_HISTORY_SIZE=100         # Maximum number of calculations to retain in memory
CALCULATOR_AUTO_SAVE=true               # Enable automatic history saving after each calculation
CALCULATOR_PRECISION=10                 # Number of decimal places for calculations
CALCULATOR_MAX_INPUT_VALUE=1e999        # Maximum allowed input value (preventing overflow)
CALCULATOR_DEFAULT_ENCODING=utf-8       # Character encoding for file operations
```

### Customizing Configuration

To modify configuration settings:

1. Edit the `.env` file in the project root
2. Change the values according to your needs
3. The application will automatically reload configuration on next start

**Example: Disable auto-save**
```env
CALCULATOR_AUTO_SAVE=false
```

---

## Usage Guide

### Starting the Calculator

```bash
python main.py
```

### Available Commands

#### Arithmetic Operations

Perform calculations using the following commands:

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Addition of two numbers | `add` then enter operands |
| `subtract` | Subtraction of two numbers | `subtract` then enter operands |
| `multiply` | Multiplication of two numbers | `multiply` then enter operands |
| `divide` | Division of two numbers | `divide` then enter operands |
| `power` | Raise one number to the power of another | `power` then enter base, exponent |
| `root` | Calculate the nth root of a number | `root` then enter number, degree |
| `modulus` | Compute remainder of division | `modulus` then enter dividend, divisor |
| `int_divide` | Integer division (discards fractional part) | `int_divide` then enter dividend, divisor |
| `percent` | Calculate percentage (a/b)*100 | `percent` then enter numerator, denominator |
| `abs_diff` | Absolute difference between two numbers | `abs_diff` then enter two numbers |

#### History Commands

| Command | Description |
|---------|-------------|
| `history` | Display all calculations performed in current session |
| `clear` | Clear all calculation history |
| `save` | Manually save history to CSV file |
| `load` | Load history from CSV file |

#### Undo/Redo Commands

| Command | Description |
|---------|-------------|
| `undo` | Revert the last calculation and remove from history |
| `redo` | Restore the last undone calculation |

#### System Commands

| Command | Description |
|---------|-------------|
| `help` | Display all available commands |
| `exit` | Save history and exit gracefully |

### Interactive Session Example

```
Calculator started. Type 'help' for commands.

Enter command: add
Enter numbers (or 'cancel' to abort):
First number: 10
Second number: 5

Result: 15

Enter command: multiply
Enter numbers (or 'cancel' to abort):
First number: 15
Second number: 3

Result: 45

Enter command: history
Calculation History:
1. Addition: 10 + 5 = 15
2. Multiplication: 15 * 3 = 45

Enter command: undo
Operation undone

Enter command: redo
Operation redone

Enter command: save
History saved successfully

Enter command: exit
History saved successfully.
Goodbye!
```

### Operation-Specific Notes

**Division Operations:**
- Division by zero will raise an error
- Results are returned as decimal values for precision

**Power Operation:**
- Negative exponents are not supported
- Use root operation for fractional powers

**Root Operation:**
- Cannot calculate roots of negative numbers
- Zero root is undefined

**Percentage Operation:**
- Denominator cannot be zero
- Result is expressed as a percentage (0-100 scale)

**Integer Division:**
- Discards the fractional part of the result
- Divisor cannot be zero

---

## Testing Instructions

### Running Unit Tests

Execute all tests with pytest:

```bash
pytest
```

Run pytest with verbose output:

```bash
pytest -v
```

### Coverage Requirements

The project maintains **99% code coverage** (exceeding the 90% minimum requirement). All intentionally non-covered lines are marked with `# pragma: no cover` comments.


---

## CI/CD Information

This project uses **GitHub Actions** for continuous integration and deployment automation.

### Workflow Overview

The CI/CD pipeline is defined in `.github/workflows/tests.yml` and automatically:

1. **Triggers** on every push to `main` branch and any pull request targeting `main`
2. **Sets Up Environment**: Configures Python 3.x runtime
3. **Installs Dependencies**: Runs `pip install -r requirements.txt`
4. **Runs Tests**: Execute `pytest`
5. **Enforces Coverage**: Fails the build if coverage drops below 90%

### Workflow File (path to file: .github/workflows/tests.yml)

```yaml
name: Run Tests on Push or Pull Request to Main

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies from requirements.txt
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with pytest and enforce 90% coverage
        run: |
          pytest --cov=app --cov-fail-under=90
```

### Checking CI/CD Status

1. Navigate to the **Actions** tab in this GitHub repository
2. View the status of recent workflow runs
3. Click on a run to see detailed logs and coverage reports

---

## Project Structure

```
module5_is601/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── calculator.py             # Core calculator class with operations management
│   ├── calculation.py            # Calculation model and result representation
│   ├── calculator_config.py      # Configuration management with environment variables
│   ├── calculator_memento.py     # Memento pattern for undo/redo functionality
│   ├── calculator_repl.py        # Read-Eval-Print Loop (REPL) interface
│   ├── exceptions.py             # Custom exception classes
│   ├── history.py                # Observer pattern implementation for logging/saving
│   ├── input_validators.py       # Input validation utilities
│   └── operations.py             # Arithmetic operation implementations and factory
├── tests/                        # Unit test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration and fixtures
│   ├── test_calculator.py        # Calculator class tests
│   ├── test_calculation.py       # Calculation model tests
│   ├── test_operations.py        # Operation implementation tests
│   ├── test_config.py            # Configuration tests
│   ├── test_exceptions.py        # Exception handling tests
│   ├── test_history.py           # Observer and history tests
│   ├── test_validators.py        # Validator tests
│   ├── test_calculator_memento.py # Undo/redo tests
│   └── test_calculator_repl.py   # REPL interface tests
├── .github/
│   └── workflows/
│       └── tests.yml             # GitHub Actions CI/CD workflow
├── history/                      # Calculation history storage
│   └── calculator_history.csv
├── logs/                         # Application logs
├── htmlcov/                      # Code coverage reports
├── .env                          # Environment configuration
├── .gitignore
├── requirements.txt              # Python package dependencies
├── main.py                       # Entry point
├── pytest.ini                    # Pytest configuration
├── LICENSE
└── readme.md                     # This file
```

---

## Code Documentation
---

## Best Practices Implemented

- **DRY Principle**: Code reuse and modular design
- **Design Patterns**: Factory, Memento, Observer, Singleton, Strategy
- **Error Handling**: Custom exceptions with meaningful messages
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: 99% code coverage with pytest
- **Logging**: Structured logging with file persistence
- **Configuration**: Environment-based configuration management

---


## License

This project is provided as educational material for IS601 coursework.
MIT LIcense
