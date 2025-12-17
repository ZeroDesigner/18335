"""
Test script to demonstrate the problem and verify the fix.
"""

import sys
from tl_config_original import TLConfigOriginal
from tl_config_fixed import TLConfigFixed, TLConfigFlexible


def test_original():
    """Test the original configuration that causes errors."""
    print("=" * 70)
    print("TEST 1: Original Configuration (Should Fail)")
    print("=" * 70)
    
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
        config = TLConfigOriginal(**config_data)
        print("✗ UNEXPECTED: Configuration validated (should have failed)")
        return False
    except Exception as e:
        print("✓ EXPECTED: Validation failed as expected")
        print(f"\nError details:")
        error_lines = str(e).split('\n')
        for line in error_lines[:10]:  # Show first 10 lines
            print(f"  {line}")
        if len(error_lines) > 10:
            print(f"  ... ({len(error_lines) - 10} more lines)")
        return True


def test_fixed_explicit():
    """Test the fixed configuration with explicit fields."""
    print("\n" + "=" * 70)
    print("TEST 2: Fixed Configuration (Explicit Fields)")
    print("=" * 70)
    
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
        print("✓ SUCCESS: Configuration validated")
        print(f"\nValidated parameters:")
        print(f"  - Batch size: {config.parameters.batch_size}")
        print(f"  - Epochs: {config.parameters.num_epochs}")
        print(f"  - Similarity type: {config.parameters.type}")
        print(f"  - Lower threshold: {config.parameters.lower_threshold}")
        print(f"  - Upper threshold: {config.parameters.upper_threshold}")
        print(f"  - Min cardinality: {config.parameters.min_cardinality}")
        print(f"  - Max cardinality: {config.parameters.max_cardinality}")
        return True
    except Exception as e:
        print(f"✗ UNEXPECTED ERROR: {e}")
        return False


def test_flexible():
    """Test the flexible configuration with extra='allow'."""
    print("\n" + "=" * 70)
    print("TEST 3: Flexible Configuration (extra='allow')")
    print("=" * 70)
    
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
            "max_cardinality": 199,
            # Can even add extra fields not defined anywhere
            "some_new_parameter": "value"
        }
    }
    
    try:
        config = TLConfigFlexible(**config_data)
        print("✓ SUCCESS: Configuration validated")
        print(f"\nValidated parameters (including extra fields):")
        print(f"  - Batch size: {config.parameters.batch_size}")
        print(f"  - Epochs: {config.parameters.num_epochs}")
        # Access extra fields by getting model fields from the class
        model_fields = set(config.parameters.__class__.model_fields.keys()) if hasattr(config.parameters.__class__, 'model_fields') else set()
        extra_fields = {k: v for k, v in config.parameters.__dict__.items() 
                       if k not in model_fields and not k.startswith('_')}
        print(f"  - Extra fields: {extra_fields}")
        return True
    except Exception as e:
        print(f"✗ UNEXPECTED ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("REINVENT4 Transfer Learning Config - Pydantic Fix Test")
    print("=" * 70)
    
    results = []
    results.append(("Original (should fail)", test_original()))
    results.append(("Fixed (explicit fields)", test_fixed_explicit()))
    results.append(("Flexible (extra allow)", test_flexible()))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
