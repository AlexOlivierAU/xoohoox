from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.batch_tracking import BatchTracking

class BatchNumberGenerator:
    """Service for generating standardized batch numbers."""
    
    @staticmethod
    def generate_batch_id(
        db: Session,
        fruit_type: str,
        process_type: str,
        grower_id: Optional[str] = None
    ) -> str:
        """
        Generate a unique batch ID with the format: YYMMDD-FT-PT-XXX
        where:
        - YYMMDD: Date in year/month/day format
        - FT: Fruit type code (AP: Apple, PE: Pear, etc.)
        - PT: Process type (FE: Fermentation, DI: Distillation, etc.)
        - XXX: Sequential number for the day
        
        Example: 240321-AP-FE-001
        """
        today = datetime.now()
        date_str = today.strftime("%y%m%d")
        
        # Convert fruit type to code
        fruit_code = fruit_type[:2].upper()
        
        # Convert process type to code
        process_code = process_type[:2].upper()
        
        # Get the latest batch number for today
        base_pattern = f"{date_str}-{fruit_code}-{process_code}"
        latest_batch = (
            db.query(BatchTracking)
            .filter(BatchTracking.batch_id.like(f"{base_pattern}%"))
            .order_by(BatchTracking.batch_id.desc())
            .first()
        )
        
        if latest_batch:
            # Extract the sequence number and increment
            seq_num = int(latest_batch.batch_id[-3:]) + 1
        else:
            seq_num = 1
            
        # Format the new batch ID
        batch_id = f"{base_pattern}-{seq_num:03d}"
        
        # If grower ID is provided, prepend it
        if grower_id:
            batch_id = f"{grower_id}-{batch_id}"
            
        return batch_id
    
    @staticmethod
    def validate_batch_id(batch_id: str) -> bool:
        """
        Validate that a batch ID follows the correct format.
        """
        try:
            # Basic format validation
            parts = batch_id.split("-")
            
            # Without grower ID: should have 4 parts
            # With grower ID: should have 5 parts
            if len(parts) not in [4, 5]:
                return False
                
            # If has grower ID, remove it for further validation
            if len(parts) == 5:
                parts = parts[1:]
                
            # Validate date part
            datetime.strptime(parts[0], "%y%m%d")
            
            # Validate fruit type code (2 letters)
            if not parts[1].isalpha() or len(parts[1]) != 2:
                return False
                
            # Validate process type code (2 letters)
            if not parts[2].isalpha() or len(parts[2]) != 2:
                return False
                
            # Validate sequence number (3 digits)
            if not parts[3].isdigit() or len(parts[3]) != 3:
                return False
                
            return True
            
        except (ValueError, IndexError):
            return False 