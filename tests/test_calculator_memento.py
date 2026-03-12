from datetime import datetime
from decimal import Decimal
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_to_dict():
    """Test converting memento to dictionary"""
    calc = Calculation(operation="Addition", operand1=Decimal("5"), operand2=Decimal("3"))
    memento = CalculatorMemento(history=[calc])
    result = memento.to_dict()
    
    assert result['history'][0]['operation'] == "Addition"
    assert result['history'][0]['operand1'] == "5"
    assert result['history'][0]['operand2'] == "3"
    assert result['history'][0]['result'] == "8"


def test_from_dict():
    """Test creating memento from dictionary"""
    timestamp = datetime.now()
    data = {
        'history': [{
            'operation': "Addition",
            'operand1': "5",
            'operand2': "3",
            'result': "8",
            'timestamp': timestamp.isoformat()
        }],
        'timestamp': timestamp.isoformat()
    }
    memento = CalculatorMemento.from_dict(data)
    
    assert memento.history[0].operation == "Addition"
    assert memento.history[0].operand1 == Decimal("5")
    assert memento.history[0].operand2 == Decimal("3")
