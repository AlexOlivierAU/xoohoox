import pytest
from datetime import datetime
from app.models.quality_control import QualityControl
from app.models.enums import QualityTestType, TestResult

def test_quality_control_creation():
    """Test creating a quality control record with valid data."""
    test_date = datetime.utcnow()
    quality_control = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=7.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        test_result=TestResult.PASS,
        test_date=test_date,
        tester_id=1,
        notes="pH test within acceptable range"
    )
    
    assert quality_control.batch_id == 1
    assert quality_control.test_type == QualityTestType.PH
    assert quality_control.test_value == 7.0
    assert quality_control.expected_range_min == 6.5
    assert quality_control.expected_range_max == 7.5
    assert quality_control.test_result == TestResult.PASS
    assert quality_control.test_date == test_date
    assert quality_control.tester_id == 1
    assert quality_control.notes == "pH test within acceptable range"

def test_quality_control_defaults():
    """Test default values for quality control fields."""
    quality_control = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=7.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        tester_id=1
    )
    
    assert quality_control.test_result == TestResult.PENDING  # Should default to PENDING
    assert quality_control.notes is None
    assert isinstance(quality_control.test_date, datetime)  # Should default to current time

def test_quality_control_representation():
    """Test string representation of QualityControl model."""
    quality_control = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=7.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        tester_id=1
    )
    
    str_repr = str(quality_control)
    assert "QualityControl" in str_repr
    assert "PH" in str_repr
    assert "7.0" in str_repr

def test_quality_control_to_dict():
    """Test the to_dict method of QualityControl model."""
    test_date = datetime.utcnow()
    quality_control = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=7.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        test_result=TestResult.PASS,
        test_date=test_date,
        tester_id=1,
        notes="pH test within acceptable range"
    )
    
    qc_dict = quality_control.to_dict()
    
    assert qc_dict['batch_id'] == 1
    assert qc_dict['test_type'] == QualityTestType.PH.value
    assert qc_dict['test_value'] == 7.0
    assert qc_dict['expected_range_min'] == 6.5
    assert qc_dict['expected_range_max'] == 7.5
    assert qc_dict['test_result'] == TestResult.PASS.value
    assert 'test_date' in qc_dict
    assert qc_dict['tester_id'] == 1
    assert qc_dict['notes'] == "pH test within acceptable range"

def test_quality_control_validation():
    """Test quality control validation rules."""
    # Test invalid range (min > max)
    with pytest.raises(ValueError):
        QualityControl(
            batch_id=1,
            test_type=QualityTestType.PH,
            test_value=7.0,
            expected_range_min=7.5,  # Greater than max
            expected_range_max=6.5,
            tester_id=1
        )
    
    # Test invalid test value (negative for pH)
    with pytest.raises(ValueError):
        QualityControl(
            batch_id=1,
            test_type=QualityTestType.PH,
            test_value=-1.0,  # Negative pH
            expected_range_min=6.5,
            expected_range_max=7.5,
            tester_id=1
        )

def test_quality_control_result_calculation():
    """Test automatic test result calculation based on value and range."""
    # Test PASS result
    qc_pass = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=7.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        tester_id=1
    )
    assert qc_pass.test_result == TestResult.PASS
    
    # Test FAIL result (below range)
    qc_fail_low = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=6.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        tester_id=1
    )
    assert qc_fail_low.test_result == TestResult.FAIL
    
    # Test FAIL result (above range)
    qc_fail_high = QualityControl(
        batch_id=1,
        test_type=QualityTestType.PH,
        test_value=8.0,
        expected_range_min=6.5,
        expected_range_max=7.5,
        tester_id=1
    )
    assert qc_fail_high.test_result == TestResult.FAIL 