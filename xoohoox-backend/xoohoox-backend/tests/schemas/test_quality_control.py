from datetime import datetime, timedelta
import pytest
from pydantic import ValidationError

from app.schemas.quality_control import (
    QualityTestCreate,
    TestType,
    TestResult,
    TestStatus,
    QualityCheckCreate,
    QualityGrade,
)

def test_valid_quality_test():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-001",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "brix": 12.5,
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "test_user",
        "reviewed_by": "supervisor"
    }
    
    quality_test = QualityTestCreate(**test_data)
    assert quality_test.test_id == "TEST-001"
    assert quality_test.batch_id == "BATCH-001"
    assert quality_test.test_type == TestType.PHYSICAL
    assert quality_test.status == TestStatus.COMPLETED
    assert quality_test.result == TestResult.PASS

def test_invalid_test_id():
    now = datetime.now()
    
    test_data = {
        "test_id": "",  # Invalid: empty test ID
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "brix": 12.5,
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "test_user",
        "reviewed_by": "supervisor"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityTestCreate(**test_data)
    assert "Test ID cannot be empty" in str(exc_info.value)

def test_invalid_batch_id():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-002",
        "batch_id": "",  # Invalid: empty batch ID
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "brix": 12.5,
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "test_user",
        "reviewed_by": "supervisor"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityTestCreate(**test_data)
    assert "Batch ID cannot be empty" in str(exc_info.value)

def test_invalid_parameters():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-003",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "brix": -12.5,  # Invalid: negative brix value
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "test_user",
        "reviewed_by": "supervisor"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityTestCreate(**test_data)
    assert "Brix value must be positive" in str(exc_info.value)

def test_invalid_result_status_combination():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-004",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.PENDING,  # Invalid: pending status with result
        "result": TestResult.PASS,
        "parameters": {
            "brix": 12.5,
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "test_user",
        "reviewed_by": "supervisor"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityTestCreate(**test_data)
    assert "Cannot have result when status is not completed" in str(exc_info.value)

def test_invalid_performer():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-005",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "brix": 12.5,
            "acidity": 0.8,
            "ph": 3.5
        },
        "notes": "Standard quality test",
        "performed_by": "",  # Invalid: empty performer
        "reviewed_by": "supervisor"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityTestCreate(**test_data)
    assert "Performer cannot be empty" in str(exc_info.value)

def test_microbiological_test():
    now = datetime.now()
    
    test_data = {
        "test_id": "TEST-006",
        "batch_id": "BATCH-001",
        "test_type": TestType.MICROBIOLOGICAL,
        "test_date": now,
        "status": TestStatus.COMPLETED,
        "result": TestResult.PASS,
        "parameters": {
            "total_plate_count": 100,
            "yeast_count": 10,
            "mold_count": 0
        },
        "notes": "Microbiological quality test",
        "performed_by": "microbiologist",
        "reviewed_by": "supervisor"
    }
    
    quality_test = QualityTestCreate(**test_data)
    assert quality_test.test_type == TestType.MICROBIOLOGICAL
    assert "total_plate_count" in quality_test.parameters
    assert "yeast_count" in quality_test.parameters
    assert "mold_count" in quality_test.parameters

def test_valid_quality_check():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-001",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "quality_operator",
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": 3.5,
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    check = QualityCheckCreate(**test_data)
    assert check.check_id == "QC-001"
    assert check.batch_id == "BATCH-001"
    assert check.test_type == TestType.PHYSICAL
    assert check.result == TestResult.PASS
    assert check.grade == QualityGrade.A

def test_invalid_check_id():
    now = datetime.now()
    
    test_data = {
        "check_id": "",  # Invalid: empty check ID
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "quality_operator",
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": 3.5,
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityCheckCreate(**test_data)
    assert "Check ID cannot be empty" in str(exc_info.value)

def test_invalid_batch_id():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-002",
        "batch_id": "",  # Invalid: empty batch ID
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "quality_operator",
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": 3.5,
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityCheckCreate(**test_data)
    assert "Batch ID cannot be empty" in str(exc_info.value)

def test_invalid_test_date():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-003",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now + timedelta(days=1),  # Invalid: future date
        "operator": "quality_operator",
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": 3.5,
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityCheckCreate(**test_data)
    assert "Test date cannot be in the future" in str(exc_info.value)

def test_invalid_operator():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-004",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "",  # Invalid: empty operator
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": 3.5,
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityCheckCreate(**test_data)
    assert "Operator cannot be empty" in str(exc_info.value)

def test_invalid_parameters():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-005",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "quality_operator",
        "result": TestResult.PASS,
        "grade": QualityGrade.A,
        "notes": "All parameters within specification",
        "parameters": {
            "ph": -1.0,  # Invalid: negative pH
            "brix": 12.0,
            "acidity": 0.8
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        QualityCheckCreate(**test_data)
    assert "pH must be positive" in str(exc_info.value)

def test_failed_check():
    now = datetime.now()
    
    test_data = {
        "check_id": "QC-006",
        "batch_id": "BATCH-001",
        "test_type": TestType.PHYSICAL,
        "test_date": now,
        "operator": "quality_operator",
        "result": TestResult.FAIL,
        "grade": QualityGrade.C,
        "notes": "pH out of specification",
        "parameters": {
            "ph": 4.5,
            "brix": 12.0,
            "acidity": 0.8
        },
        "corrective_actions": "Adjust pH to target range",
        "follow_up_required": True
    }
    
    check = QualityCheckCreate(**test_data)
    assert check.result == TestResult.FAIL
    assert check.grade == QualityGrade.C
    assert check.corrective_actions is not None
    assert check.follow_up_required is True 