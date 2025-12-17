"""
This file demonstrates the ORIGINAL problematic TLConfig structure
that causes Pydantic validation errors in REINVENT4.

The issue: Pydantic v2 forbids extra fields by default, and these
parameters are not defined in the model.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Any


class ParametersOriginal(BaseModel):
    """
    Original Parameters model that doesn't include the problematic fields.
    This will reject: type, lower_threshold, upper_threshold, 
    min_cardinality, max_cardinality
    """
    model_config = ConfigDict(extra="forbid")
    
    # Only basic parameters defined, causing validation errors
    # when additional fields are provided
    batch_size: Optional[int] = 128
    num_epochs: Optional[int] = 100


class TLConfigOriginal(BaseModel):
    """
    Original TLConfig that demonstrates the issue.
    By default, Pydantic v2 has extra="forbid" behavior.
    """
    run_type: str = "transfer_learning"
    model_file: str
    output_model_file: str
    input_smiles_path: str
    parameters: ParametersOriginal


# Demonstrate the error
if __name__ == "__main__":
    # This configuration will cause validation errors
    problematic_config = {
        "run_type": "transfer_learning",
        "model_file": "prior.model",
        "output_model_file": "transfer.model",
        "input_smiles_path": "smiles.smi",
        "parameters": {
            "batch_size": 128,
            "num_epochs": 100,
            # These fields will cause "Extra inputs are not permitted" errors
            "type": "tanimoto",
            "lower_threshold": 0.99,
            "upper_threshold": 1.0,
            "min_cardinality": 1,
            "max_cardinality": 199
        }
    }
    
    try:
        config = TLConfigOriginal(**problematic_config)
        print("✓ Configuration validated successfully")
    except Exception as e:
        print("✗ Validation Error:")
        print(f"  {type(e).__name__}: {e}")
