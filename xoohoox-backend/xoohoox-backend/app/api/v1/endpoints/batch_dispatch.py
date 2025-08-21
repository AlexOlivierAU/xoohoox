from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_batch_dispatch import batch_dispatch
from app.schemas.batch_dispatch import BatchDispatch, BatchDispatchCreate, BatchDispatchUpdate

router = APIRouter()

@router.post("/dispatch", response_model=BatchDispatch, status_code=status.HTTP_201_CREATED)
def create_batch_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    batch_dispatch_in: BatchDispatchCreate,
) -> BatchDispatch:
    """
    Create a new batch dispatch.
    """
    # Check if batch_id already exists
    existing_batch = batch_dispatch.get_by_batch_id(db, batch_id=batch_dispatch_in.batch_id)
    if existing_batch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch with ID {batch_dispatch_in.batch_id} already exists",
        )
    
    # Create the batch dispatch
    batch = batch_dispatch.create(db, obj_in=batch_dispatch_in)
    return batch

@router.get("/{batch_id}", response_model=BatchDispatch)
def get_batch_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
) -> BatchDispatch:
    """
    Get a batch dispatch by ID.
    """
    batch = batch_dispatch.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch with ID {batch_id} not found",
        )
    return batch

@router.get("/grower/{grower_id}", response_model=List[BatchDispatch])
def get_batches_by_grower(
    *,
    db: Session = Depends(deps.get_db),
    grower_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[BatchDispatch]:
    """
    Get all batches for a specific grower.
    """
    batches = batch_dispatch.get_by_grower_id(db, grower_id=grower_id, skip=skip, limit=limit)
    return batches

@router.put("/{batch_id}", response_model=BatchDispatch)
def update_batch_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
    batch_dispatch_in: BatchDispatchUpdate,
) -> BatchDispatch:
    """
    Update a batch dispatch.
    """
    batch = batch_dispatch.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch with ID {batch_id} not found",
        )
    batch = batch_dispatch.update(db, db_obj=batch, obj_in=batch_dispatch_in)
    return batch

@router.delete("/{batch_id}", response_model=BatchDispatch)
def delete_batch_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    batch_id: str,
) -> BatchDispatch:
    """
    Delete a batch dispatch.
    """
    batch = batch_dispatch.get_by_batch_id(db, batch_id=batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch with ID {batch_id} not found",
        )
    batch = batch_dispatch.remove(db, id=batch.id)
    return batch 