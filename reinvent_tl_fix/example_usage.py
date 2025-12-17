"""
Example: How to Use REINVENT4 with the Pydantic Fix

This example shows how to properly configure REINVENT4 transfer learning
after applying the fix for the Pydantic validation error.
"""

# IMPORTANT: If you're using the monkey patch approach to fix REINVENT4,
# you MUST import it before importing any REINVENT4 modules:
#
#     import monkey_patch  # Do this FIRST
#     # Then import REINVENT4 modules
#
# Uncomment the line below if using the monkey patch:
# import monkey_patch

import json
from pathlib import Path


def create_fixed_config(output_path="config_fixed.json"):
    """
    Create a properly formatted transfer learning config file.
    
    This config will work with the patched REINVENT4.
    """
    config = {
        "run_type": "transfer_learning",
        "model_file": "/path/to/prior.model",
        "output_model_file": "/path/to/transfer_learning.model",
        "input_smiles_path": "/path/to/training_smiles.smi",
        "parameters": {
            # Core training parameters
            "batch_size": 128,
            "num_epochs": 100,
            "learning_rate": 0.0001,
            "save_every_n_epochs": 10,
            
            # Similarity search parameters (now properly supported)
            "type": "tanimoto",
            "lower_threshold": 0.99,
            "upper_threshold": 1.0,
            "min_cardinality": 1,
            "max_cardinality": 199
        },
        "logging": {
            "log_file": "transfer_learning.log",
            "verbosity": "info"
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Created config file: {output_path}")
    return config


def validate_config_with_fixed_model():
    """
    Validate the config using our fixed TLConfig model.
    
    This demonstrates that the fix works correctly.
    """
    from tl_config_fixed import TLConfigFixed
    
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
    
    try:
        config = TLConfigFixed(**config_data)
        print("✓ Configuration validated successfully!")
        print(f"  - Similarity type: {config.parameters.type}")
        print(f"  - Threshold range: {config.parameters.lower_threshold} - {config.parameters.upper_threshold}")
        print(f"  - Cardinality range: {config.parameters.min_cardinality} - {config.parameters.max_cardinality}")
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False


def main():
    """Main example execution."""
    print("=" * 70)
    print("REINVENT4 Transfer Learning - Configuration Example")
    print("=" * 70)
    print()
    
    print("Step 1: Creating properly formatted config file...")
    config = create_fixed_config("example_config.json")
    print()
    
    print("Step 2: Validating config with fixed model...")
    success = validate_config_with_fixed_model()
    print()
    
    if success:
        print("=" * 70)
        print("SUCCESS: Configuration is valid!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Apply the monkey patch or update REINVENT4 source code")
        print("2. Update your config file paths to point to real files")
        print("3. Run REINVENT4 transfer learning:")
        print()
        print("   reinvent config_fixed.json")
        print()
    else:
        print("=" * 70)
        print("ERROR: Configuration validation failed")
        print("=" * 70)
        print()
        print("Please check the error messages above and ensure:")
        print("1. All required dependencies are installed")
        print("2. The fix has been properly applied")


if __name__ == "__main__":
    main()
