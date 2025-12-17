# REINVENT4 Transfer Learning Pydantic Validation Fix

## Problem

When running REINVENT4 transfer learning with certain configuration parameters, you may encounter a Pydantic validation error:

```
pydantic_core._pydantic_core.ValidationError: 5 validation errors for TLConfig
parameters.type
  Extra inputs are not permitted [type=extra_forbidden, input_value='tanimoto', input_type=str]
parameters.lower_threshold
  Extra inputs are not permitted [type=extra_forbidden, input_value=0.99, input_type=float]
parameters.upper_threshold
  Extra inputs are not permitted [type=extra_forbidden, input_value=1.0, input_type=float]
parameters.min_cardinality
  Extra inputs are not permitted [type=extra_forbidden, input_value=1, input_type=int]
parameters.max_cardinality
  Extra inputs are not permitted [type=extra_forbidden, input_value=199, input_type=int]
```

## Root Cause

This issue occurs because:
1. REINVENT4 upgraded to Pydantic v2, which has stricter validation by default
2. Pydantic v2 uses `extra="forbid"` as the default behavior, rejecting any fields not explicitly defined in the model
3. The `TLConfig` model's `parameters` field does not include these specific parameters as allowed fields

## Solution

There are two approaches to fix this issue:

### Option 1: Update the Configuration File (Recommended)

Remove the unsupported parameters from your configuration file. These parameters may have been deprecated or moved to a different section in the newer version of REINVENT4.

**Before:**
```json
{
  "parameters": {
    "type": "tanimoto",
    "lower_threshold": 0.99,
    "upper_threshold": 1.0,
    "min_cardinality": 1,
    "max_cardinality": 199
  }
}
```

**After:**
```json
{
  "parameters": {
    // Remove deprecated fields or consult REINVENT4 documentation
    // for the correct parameter names and structure
  }
}
```

### Option 2: Patch TLConfig Model (If Parameters Are Required)

If these parameters are necessary for your workflow, you need to patch the REINVENT4 source code to accept them. This can be done by modifying the TLConfig model definition.

See `tl_config_fixed.py` for an example of how to properly define a TLConfig that accepts these parameters.

## Files in This Directory

- `README.md` - This file, explaining the issue and solution
- `tl_config_original.py` - Demonstrates the problematic configuration
- `tl_config_fixed.py` - Shows the corrected TLConfig model
- `examples/config_original.json` - Example of problematic configuration
- `examples/config_fixed.json` - Example of corrected configuration

## Testing the Fix

Run the test script to verify the fix:

```bash
python test_fix.py
```

## Additional Resources

- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [REINVENT4 Documentation](https://github.com/MolecularAI/REINVENT4)
