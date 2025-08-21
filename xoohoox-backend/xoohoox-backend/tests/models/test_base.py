import pytest
from datetime import datetime
from sqlalchemy import Column, Integer, String
from app.models.base import Base

class TestModel(Base):
    """Test model for base class testing."""
    __tablename__ = "test_model"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

def test_base_model_timestamps():
    """Test that base model includes created_at and updated_at timestamps."""
    model = TestModel()
    
    # Check that timestamps are initialized
    assert hasattr(model, 'created_at')
    assert hasattr(model, 'updated_at')
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)
    
    # Check that created_at and updated_at are initially the same
    assert model.created_at == model.updated_at

def test_base_model_to_dict():
    """Test the to_dict method of the base model."""
    model = TestModel(name="test")
    model_dict = model.to_dict()
    
    # Check that all fields are included
    assert 'id' in model_dict
    assert 'name' in model_dict
    assert 'created_at' in model_dict
    assert 'updated_at' in model_dict
    
    # Check field values
    assert model_dict['name'] == "test"
    assert isinstance(model_dict['created_at'], str)
    assert isinstance(model_dict['updated_at'], str)

def test_base_model_str_representation():
    """Test the string representation of the base model."""
    model = TestModel(name="test")
    str_repr = str(model)
    
    # Check that string representation includes model name and id
    assert "TestModel" in str_repr
    assert "id=" in str_repr

def test_base_model_equality():
    """Test equality comparison of base models."""
    model1 = TestModel(name="test")
    model2 = TestModel(name="test")
    model3 = TestModel(name="different")
    
    # Models with same ID should be equal
    model1.id = 1
    model2.id = 1
    assert model1 == model2
    
    # Models with different IDs should not be equal
    model3.id = 2
    assert model1 != model3

def test_base_model_hash():
    """Test that base models can be used in sets and as dict keys."""
    model1 = TestModel(name="test")
    model2 = TestModel(name="test")
    model1.id = 1
    model2.id = 1
    
    # Models with same ID should have same hash
    assert hash(model1) == hash(model2)
    
    # Models can be added to sets
    model_set = {model1, model2}
    assert len(model_set) == 1  # Only one unique model 