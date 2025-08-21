from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.trial import create_random_trial
from app.models.upscale import UpscaleStage, UpscaleStatus

def test_create_upscale(
    client: TestClient,
    db: Session,
) -> None:
    trial = create_random_trial(db)
    data = {
        "trial_id": trial.id,
        "stage": UpscaleStage.TEST_4,
        "volume": 5.0,
    }
    response = client.post(
        f"{settings.API_V1_STR}/trials/{trial.id}/upscales",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["trial_id"] == trial.id
    assert content["stage"] == UpscaleStage.TEST_4
    assert content["volume"] == 5.0
    assert content["status"] == UpscaleStatus.PENDING
    assert "upscale_id" in content

def test_create_upscale_existing_active(
    client: TestClient,
    db: Session,
) -> None:
    trial = create_random_trial(db)
    # Create first upscale
    data = {
        "trial_id": trial.id,
        "stage": UpscaleStage.TEST_4,
        "volume": 5.0,
    }
    response = client.post(
        f"{settings.API_V1_STR}/trials/{trial.id}/upscales",
        json=data,
    )
    assert response.status_code == 200

    # Try to create another active upscale
    response = client.post(
        f"{settings.API_V1_STR}/trials/{trial.id}/upscales",
        json=data,
    )
    assert response.status_code == 400

def test_update_upscale(
    client: TestClient,
    db: Session,
) -> None:
    trial = create_random_trial(db)
    # Create upscale
    data = {
        "trial_id": trial.id,
        "stage": UpscaleStage.TEST_4,
        "volume": 5.0,
    }
    response = client.post(
        f"{settings.API_V1_STR}/trials/{trial.id}/upscales",
        json=data,
    )
    upscale_id = response.json()["id"]

    # Update upscale
    update_data = {
        "yield_amount": 0.48,
        "abv_result": 8.0,
        "compound_summary": "All compounds OK",
    }
    response = client.patch(
        f"{settings.API_V1_STR}/upscales/{upscale_id}",
        json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["yield_amount"] == 0.48
    assert content["abv_result"] == 8.0
    assert content["compound_summary"] == "All compounds OK"

def test_complete_upscale(
    client: TestClient,
    db: Session,
) -> None:
    trial = create_random_trial(db)
    # Create upscale
    data = {
        "trial_id": trial.id,
        "stage": UpscaleStage.TEST_4,
        "volume": 5.0,
    }
    response = client.post(
        f"{settings.API_V1_STR}/trials/{trial.id}/upscales",
        json=data,
    )
    upscale_id = response.json()["id"]

    # Try to complete without required fields
    response = client.post(
        f"{settings.API_V1_STR}/upscales/{upscale_id}/complete",
    )
    assert response.status_code == 400

    # Update with required fields
    update_data = {
        "yield_amount": 0.48,
        "abv_result": 8.0,
    }
    client.patch(
        f"{settings.API_V1_STR}/upscales/{upscale_id}",
        json=update_data,
    )

    # Complete upscale
    response = client.post(
        f"{settings.API_V1_STR}/upscales/{upscale_id}/complete",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == UpscaleStatus.COMPLETE 