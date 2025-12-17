"""
This file demonstrates the FIXED TLConfig structure that properly
accepts the previously problematic parameters.

Solution: Explicitly define all required fields in the Parameters model,
or use ConfigDict with extra="allow" to permit additional fields.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ParametersFixed(BaseModel):
    """
    Fixed Parameters model that explicitly includes all required fields.
    """
    # Basic training parameters
    batch_size: Optional[int] = 128
    num_epochs: Optional[int] = 100
    
    # Similarity search parameters - now properly defined
    type: Optional[str] = None
    lower_threshold: Optional[float] = None
    upper_threshold: Optional[float] = None
    min_cardinality: Optional[int] = None
    max_cardinality: Optional[int] = None


class TLConfigFixed(BaseModel):
    """
    Fixed TLConfig that accepts all necessary parameters.
    """
    run_type: str = "transfer_learning"
    model_file: str
    output_model_file: str
    input_smiles_path: str
    parameters: ParametersFixed


class ParametersFlexible(BaseModel):
    """
    Alternative solution: Use ConfigDict to allow extra fields.
    This is more flexible but less strict about validation.
    """
    model_config = ConfigDict(extra="allow")
    
    # Only define essential parameters
    batch_size: Optional[int] = 128
    num_epochs: Optional[int] = 100


class TLConfigFlexible(BaseModel):
    """
    Alternative TLConfig using flexible parameters that allow extra fields.
    """
    run_type: str = "transfer_learning"
    model_file: str
    output_model_file: str
    input_smiles_path: str
    parameters: ParametersFlexible


# Demonstrate the fix
if __name__ == "__main__":
    # This configuration now works with the fixed model
    config_data = {
        "run_type": "transfer_learning",
        "model_file": "prior.model",
        "output_model_file": "transfer.model",
        "input_smiles_path": "smiles.smi",
        "parameters": {
            "batch_size": 128,
            "num_epochs": 100,
            "type": "tanimoto",
            "lower_threshold": 0.99,
            "upper_threshold": 1.0,
            "min_cardinality": 1,
            "max_cardinality": 199
        }
    }
    
    print("Testing Fixed Configuration (Explicit Fields):")
    try:
        config_fixed = TLConfigFixed(**config_data)
        print("✓ Configuration validated successfully")
        print(f"  Type: {config_fixed.parameters.type}")
        print(f"  Thresholds: {config_fixed.parameters.lower_threshold} - {config_fixed.parameters.upper_threshold}")
        print(f"  Cardinality: {config_fixed.parameters.min_cardinality} - {config_fixed.parameters.max_cardinality}")
    except Exception as e:
        print(f"✗ Validation Error: {e}")
    
    print("\nTesting Flexible Configuration (Extra='allow'):")
    try:
        config_flexible = TLConfigFlexible(**config_data)
        print("✓ Configuration validated successfully")
        print(f"  Parameters: {config_flexible.parameters}")
    except Exception as e:
        print(f"✗ Validation Error: {e}")
