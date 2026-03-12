import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

# Fixture to initialize Calculator with a temporary directory for file paths
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch properties to use the temporary directory paths
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # Set return values to use paths within the temporary directory
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            # Return an instance of Calculator with the mocked config
            yield Calculator(config=config)

# Test Calculator Initialization

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Test Logging Setup

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        
        # Instantiate calculator to trigger logging
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

# Test Adding and Removing Observers

def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test Setting Operations

def test_set_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

# Test Performing Operations

def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(2, 3)
    assert result == Decimal('5')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 3)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

# Test Undo/Redo Functionality

def test_undo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

# Test History Management

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    # Mock CSV data to match the expected format in from_dict
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Addition'],
        'operand1': ['2'],
        'operand2': ['3'],
        'result': ['5'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    
    # Test the load_history functionality
    try:
        calculator.load_history()
        # Verify history length after loading
        assert len(calculator.history) == 1
        # Verify the loaded values
        assert calculator.history[0].operation == "Addition"
        assert calculator.history[0].operand1 == Decimal("2")
        assert calculator.history[0].operand2 == Decimal("3")
        assert calculator.history[0].result == Decimal("5")
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")
        
            
# Test Clearing History

def test_clear_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

# Test REPL Commands (using patches for input/output handling)

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")

"""
Test to execute the except statement to Log a warning if history could not be loaded
"""
@patch('app.calculator.logging.warning')
def test_calculator_initialization_load_history_warning(mock_logging_warning):
    # Simulate an exception when loading history
    with patch.object(Calculator, 'load_history', side_effect=Exception("File not found")):
        calculator = Calculator()
        mock_logging_warning.assert_called_once_with("Could not load existing history: File not found")
        assert calculator.history == []

"""
The goal is to execute the except statement in the _setup_logging method ensuring the log directory DOES NOT EXIST 

"""
@patch("app.calculator.logging.basicConfig", side_effect=OSError("Disk full"))
def test_setup_logging_exception(mock_basicconfig, capsys):
    with pytest.raises(OSError):
        Calculator(CalculatorConfig())

    captured = capsys.readouterr()
    assert "Error setting up logging" in captured.out

"""
The goal is to test for exceeding the maximum history size
"""
def test_history_exceeds_max_size(calculator):
    calculator.config.max_history_size = 1

    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)

    calculator.perform_operation(2, 3)
    calculator.perform_operation(4, 5)

    assert len(calculator.history) == 1
    assert calculator.history[0].operand1 == Decimal("4")


"""
The goal here is to log and raise operation errors for any other exceptions
"""
@patch('app.calculator.logging.error')
def test_perform_operation_generic_exception(mock_logging_error, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)

    # Force execute() to fail with a generic exception
    with patch.object(operation, 'execute', side_effect=Exception("Unexpected failure")):
        with pytest.raises(OperationError, match="Operation failed: Unexpected failure"):
            calculator.perform_operation(2, 3)

    mock_logging_error.assert_called_once_with("Operation failed: Unexpected failure")

"""
The goal is to have an empty history and create an empty csv with headers
"""
def test_save_empty_history(calculator):
    calculator.save_history()

    # Read the file that was created
    df = pd.read_csv(calculator.config.history_file)

    # Ensure the dataframe exists but is empty
    assert df.empty

    # Ensure the headers are correct
    assert list(df.columns) == [
        'operation',
        'operand1',
        'operand2',
        'result',
        'timestamp'
    ]

"""
The goal is to log and raise an OperationError if saving fails
"""
@patch("app.calculator.logging.error")
@patch("app.calculator.pd.DataFrame.to_csv", side_effect=Exception("Disk full"))
def test_save_history_failure(mock_to_csv, mock_logging_error, calculator):
    with pytest.raises(OperationError, match="Failed to save history: Disk full"):
        calculator.save_history()

    mock_logging_error.assert_called_once_with("Failed to save history: Disk full")

"""
The goal here is to load an empty history file
"""
@patch("app.calculator.logging.info")
@patch("app.calculator.pd.read_csv")
@patch("app.calculator.Path.exists", return_value=True)
def test_load_empty_history(mock_exists, mock_read_csv, mock_logging_info, calculator):
    # Simulate an empty CSV file
    mock_read_csv.return_value = pd.DataFrame()

    calculator.load_history()

    assert calculator.history == []
    mock_logging_info.assert_called_with("Loaded empty history file")

"""
The goal is to log and raise an OperatioError if loading fails
"""
@patch("app.calculator.logging.error")
@patch("app.calculator.pd.read_csv", side_effect=Exception("Corrupted file"))
@patch("app.calculator.Path.exists", return_value=True)
def test_load_history_failure(mock_exists, mock_read_csv, mock_logging_error, calculator):
    with pytest.raises(OperationError, match="Failed to load history: Corrupted file"):
        calculator.load_history()

    mock_logging_error.assert_called_once_with("Failed to load history: Corrupted file")

"""
The goal is to test the get_history_dataframe method to ensure it returns a DataFrame with the correct structure and data
"""
def test_get_history_dataframe(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)

    calculator.perform_operation(2, 3)

    df = calculator.get_history_dataframe()

    assert not df.empty
    assert list(df.columns) == [
        'operation',
        'operand1',
        'operand2',
        'result',
        'timestamp'
    ]

    assert df.iloc[0]['operation'] == 'Addition'
    assert df.iloc[0]['operand1'] == '2'
    assert df.iloc[0]['operand2'] == '3'
    assert df.iloc[0]['result'] == '5'
    
"""
The goal is to test the show_history method to ensure it returns a list of formatted strings representing the history of operations
"""
def test_show_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)

    calculator.perform_operation(2, 3)
    history = calculator.show_history()

    assert len(history) == 1
    assert history[0] == "Addition(2, 3) = 5"

"""
The goal is to test the undo method when the undo stack is empty to ensure it returns False and does not raise an exception
"""
def test_undo_empty_stack(calculator):
    result = calculator.undo()

    assert result is False

def test_redo_empty_stack(calculator):
    assert calculator.redo_stack == []
    result = calculator.redo()

    assert result is False
    assert calculator.history == []