from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
import pytest
from app.calculator_repl import calculator_repl
from app.exceptions import ValidationError, OperationError



"""
Each of the following functions will test a specific part of the calculator_repl function, ensuring that all branches and error handling are covered. The use of mocks allows us to simulate user input and control the behavior of the Calculator class without relying on actual file I/O or user interaction.
"""

def test_save_history_on_exit():
    """Test saving history before exiting (lines 54-55)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        calc_mock.save_history.assert_called_once()


def test_show_history_command(capsys):
    """Test displaying calculation history (lines 61-68)"""
    calc_mock = Mock()
    calc_mock.show_history.return_value = ["2 + 3 = 5", "10 - 2 = 8"]
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['history', 'exit']):
        calculator_repl()
        calc_mock.show_history.assert_called()


def test_clear_history_command():
    """Test clearing calculation history (lines 72-74)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['clear', 'exit']):
        calculator_repl()
        calc_mock.clear_history.assert_called_once()


def test_undo_command():
    """Test undo operation (lines 78-82)"""
    calc_mock = Mock()
    calc_mock.undo.return_value = True
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['undo', 'exit']):
        calculator_repl()
        calc_mock.undo.assert_called_once()


def test_redo_command():
    """Test redo operation (lines 86-90)"""
    calc_mock = Mock()
    calc_mock.redo.return_value = True
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['redo', 'exit']):
        calculator_repl()
        calc_mock.redo.assert_called_once()


def test_save_command():
    """Test save history command with error handling (lines 94-99)"""
    calc_mock = Mock()
    calc_mock.save_history.return_value = None
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['save', 'exit']):
        calculator_repl()
        calc_mock.save_history.assert_called()


def test_load_command():
    """Test load history command with error handling (lines 103-108)"""
    calc_mock = Mock()
    calc_mock.load_history.return_value = None
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['load', 'exit']):
        calculator_repl()
        calc_mock.load_history.assert_called()


def test_cancel_first_operand(capsys):
    """Test cancelling operation by entering 'cancel' for first number (lines 116-117)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['add', 'cancel', 'exit']):
        calculator_repl()
        # Should not call perform_operation if cancelled
        calc_mock.perform_operation.assert_not_called()


def test_cancel_second_operand(capsys):
    """Test cancelling operation by entering 'cancel' for second number (lines 120-121)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['add', '5', 'cancel', 'exit']):
        calculator_repl()
        # Should not call perform_operation if cancelled
        calc_mock.perform_operation.assert_not_called()


def test_normalize_decimal_result():
    """Test normalizing Decimal result (lines 135-140)"""
    calc_mock = Mock()
    calc_mock.perform_operation.return_value = Decimal('5.0000')
    calc_mock.set_operation.return_value = None
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
        calculator_repl()
        calc_mock.perform_operation.assert_called()


def test_validation_error_handling():
    """Test handling ValidationError during operation (lines 144-163)"""
    calc_mock = Mock()
    calc_mock.perform_operation.side_effect = ValidationError("Invalid input")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['add', '2', 'abc', 'exit']):
        calculator_repl()
        # Should handle error gracefully


def test_operation_error_handling():
    """Test handling OperationError during operation (lines 144-163)"""
    calc_mock = Mock()
    calc_mock.perform_operation.side_effect = OperationError("Division by zero")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['divide', '5', '0', 'exit']):
        calculator_repl()
        # Should handle error gracefully


def test_unknown_command():
    """Test handling unknown command (lines 164-165)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['invalid', 'exit']):
        calculator_repl()
        # Should continue to accept commands


def test_show_empty_history():
    """Test displaying empty calculation history (line 63)"""
    calc_mock = Mock()
    calc_mock.show_history.return_value = []
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['history', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print "No calculations in history"
        print_mock.assert_any_call("No calculations in history")


def test_undo_nothing_to_undo():
    """Test undo when nothing to undo (line 81)"""
    calc_mock = Mock()
    calc_mock.undo.return_value = False
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['undo', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print "Nothing to undo"
        print_mock.assert_any_call("Nothing to undo")


def test_redo_nothing_to_redo():
    """Test redo when nothing to redo (line 89)"""
    calc_mock = Mock()
    calc_mock.redo.return_value = False
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['redo', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print "Nothing to redo"
        print_mock.assert_any_call("Nothing to redo")


def test_save_history_error_on_exit():
    """Test error saving history on exit (lines 54-55)"""
    calc_mock = Mock()
    calc_mock.save_history.side_effect = Exception("Save failed")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print warning about save failure
        print_mock.assert_any_call("Warning: Could not save history: Save failed")


def test_save_command_error():
    """Test save command error handling (lines 97-98)"""
    calc_mock = Mock()
    calc_mock.save_history.side_effect = Exception("Write error")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['save', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print error message
        print_mock.assert_any_call("Error saving history: Write error")


def test_load_command_error():
    """Test load command error handling (lines 106-107)"""
    calc_mock = Mock()
    calc_mock.load_history.side_effect = Exception("Read error")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=['load', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print error message
        print_mock.assert_any_call("Error loading history: Read error")


def test_normalize_integer_result():
    """Test integer result is not normalized (line 138)"""
    calc_mock = Mock()
    calc_mock.perform_operation.return_value = 5
    calc_mock.set_operation.return_value = None
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['add', '2', '3', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print result as is
        print_mock.assert_any_call("\nResult: 5")


def test_normalize_decimal_zero():
    """Test normalizing Decimal zero (line 140)"""
    calc_mock = Mock()
    calc_mock.perform_operation.return_value = Decimal('0.00000')
    calc_mock.set_operation.return_value = None
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['add', '5', '-5', 'exit']):
        calculator_repl()
        calc_mock.perform_operation.assert_called()


def test_unexpected_exception_during_operation():
    """Test handling unexpected exception during operation (line 149)"""
    calc_mock = Mock()
    calc_mock.perform_operation.side_effect = RuntimeError("Unexpected error")
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('app.calculator_repl.OperationFactory'), \
         patch('builtins.input', side_effect=['add', '2', '3', 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print unexpected error message
        print_mock.assert_any_call("Unexpected error: Unexpected error")


def test_keyboard_interrupt():
    """Test handling Ctrl+C interruption (line 153)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit']), \
         patch('builtins.print') as print_mock:
        calculator_repl()
        # Should print operation cancelled
        print_mock.assert_any_call("\nOperation cancelled")


def test_eof_error():
    """Test handling EOF error (Ctrl+D) (line 158)"""
    calc_mock = Mock()
    
    with patch('app.calculator_repl.Calculator', return_value=calc_mock), \
         patch('builtins.input', side_effect=EOFError()):
        calculator_repl()
        # Should exit gracefully


def test_fatal_error_during_initialization():
    """Test handling fatal error during Calculator initialization (lines 154-163)"""
    with patch('app.calculator_repl.Calculator', side_effect=Exception("Fatal initialization error")), \
         patch('builtins.print') as print_mock, \
         patch('app.calculator_repl.logging.error') as logging_mock:
        with pytest.raises(Exception):
            calculator_repl()
        # Should print fatal error and log it
        print_mock.assert_any_call("Fatal error: Fatal initialization error")
        logging_mock.assert_called_once()
