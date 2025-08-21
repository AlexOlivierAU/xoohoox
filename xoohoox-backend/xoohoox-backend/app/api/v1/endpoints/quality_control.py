from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas import (
    QualityControlCreate,
    QualityControlUpdate,
    QualityControlResponse,
    QualityControlList,
    TestResult
)
from app.crud import quality_control
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=QualityControlResponse, status_code=status.HTTP_201_CREATED)
def create_test(
    *,
    db: Session = Depends(get_db),
    test_in: QualityControlCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new quality control test.
    """
    return quality_control.create(db=db, obj_in=test_in)

@router.get("/", response_model=QualityControlList)
def read_tests(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    batch_id: Optional[str] = None,
    result: Optional[TestResult] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve quality control tests with optional filtering.
    """
    tests = quality_control.get_multi(
        db=db, skip=skip, limit=limit, batch_id=batch_id, result=result
    )
    total = quality_control.count(db=db, batch_id=batch_id, result=result)
    pages = (total + limit - 1) // limit
    
    return {
        "items": tests,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": pages
    }

@router.get("/{test_id}", response_model=QualityControlResponse)
def read_test(
    *,
    db: Session = Depends(get_db),
    test_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific quality control test by ID.
    """
    db_test = quality_control.get_by_test_id(db=db, test_id=test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test with ID {test_id} not found"
        )
    return db_test

@router.put("/{test_id}", response_model=QualityControlResponse)
def update_test(
    *,
    db: Session = Depends(get_db),
    test_id: str,
    test_in: QualityControlUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a quality control test.
    """
    db_test = quality_control.get_by_test_id(db=db, test_id=test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test with ID {test_id} not found"
        )
    return quality_control.update(db=db, db_obj=db_test, obj_in=test_in)

@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(
    *,
    db: Session = Depends(get_db),
    test_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a quality control test.
    """
    db_test = quality_control.get_by_test_id(db=db, test_id=test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test with ID {test_id} not found"
        )
    quality_control.remove(db=db, id=db_test.id)
    return None

@router.get("/batch/{batch_id}", response_model=QualityControlList)
def read_batch_tests(
    *,
    db: Session = Depends(get_db),
    batch_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get all quality control tests for a specific batch.
    """
    tests = quality_control.get_multi(
        db=db, skip=skip, limit=limit, batch_id=batch_id
    )
    total = quality_control.count(db=db, batch_id=batch_id)
    pages = (total + limit - 1) // limit
    
    return {
        "items": tests,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": pages
    }

@router.post("/{test_id}/verify", response_model=QualityControlResponse)
def verify_test(
    *,
    db: Session = Depends(get_db),
    test_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Verify a quality control test.
    """
    db_test = quality_control.get_by_test_id(db=db, test_id=test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test with ID {test_id} not found"
        )
    
    if db_test.result != TestResult.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Test must be in pending status to verify. Current status: {db_test.result}"
        )
    
    return quality_control.verify_test(db=db, db_obj=db_test)

@router.post("/{test_id}/request-retest", response_model=QualityControlResponse)
def request_retest(
    *,
    db: Session = Depends(get_db),
    test_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Request a retest for a failed quality control test.
    """
    db_test = quality_control.get_by_test_id(db=db, test_id=test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test with ID {test_id} not found"
        )
    
    if db_test.result != TestResult.FAIL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can only request retest for failed tests. Current result: {db_test.result}"
        )
    
    return quality_control.request_retest(db=db, db_obj=db_test)

@router.get("/")
def get_quality_checks():
    return {"message": "List of quality checks"}

@router.get("/parameters", response_model=List[str])
def get_quality_parameters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get available quality control parameters.
    """
    # This could be moved to a configuration file or database table
    parameters = [
        "ph",
        "brix",
        "temperature",
        "acidity",
        "turbidity",
        "color",
        "viscosity",
        "sugar_content",
        "alcohol_content",
        "microbial_count"
    ]
    return parameters 