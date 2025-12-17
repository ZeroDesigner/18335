# Quick Start Guide: Fixing REINVENT4 Transfer Learning Error

## The Problem You're Seeing

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

## Quick Fix (Choose One)

### Option A: Use the Monkey Patch (No Code Changes)

**Best for**: Users who don't want to modify REINVENT4 source code

1. Copy `monkey_patch.py` to your project directory
2. Import it before using REINVENT4:

```python
import monkey_patch  # MUST be first!
# Now use REINVENT4 normally
from reinvent import ...
```

3. Run your transfer learning script normally

### Option B: Update REINVENT4 Source Code

**Best for**: Permanent fix, or if you maintain REINVENT4

1. Find your REINVENT4 installation:
   ```bash
   python -c "import reinvent; print(reinvent.__file__)"
   ```

2. Locate the TLConfig Parameters model (usually in one of these locations):
   - `reinvent/runmodes/TL/config.py`
   - `reinvent/models/tl_config.py`
   - `reinvent/config.py`

3. Add these lines to the Parameters class:
   ```python
   from pydantic import ConfigDict
   
   class Parameters(BaseModel):
       model_config = ConfigDict(extra="allow")
       # ... rest of the class
   ```

4. Save and restart Python

### Option C: Update Your Config File

**Best for**: If these parameters are not needed

Simply remove the problematic parameters from your JSON config file:

```json
{
  "parameters": {
    "batch_size": 128,
    "num_epochs": 100
    // Remove: type, lower_threshold, upper_threshold, min_cardinality, max_cardinality
  }
}
```

## Testing Your Fix

Run this command to verify the fix:

```bash
python test_fix.py
```

You should see:
```
✓ All tests passed!
```

## Need More Details?

- **README.md** - Complete documentation
- **PATCH_INSTRUCTIONS.md** - Detailed patching guide
- **tl_config_fixed.py** - See the fixed code
- **examples/** - Example configuration files

## Still Having Issues?

1. Make sure you're using REINVENT4 (not REINVENT 3.x)
2. Check your Pydantic version: `pip show pydantic`
3. Ensure you imported the monkey patch BEFORE importing REINVENT4
4. Try restarting your Python session after applying fixes

## What Changed in REINVENT4?

REINVENT4 upgraded to Pydantic v2, which is stricter about extra fields. The old configuration format that worked in previous versions now triggers validation errors. This fix makes REINVENT4 accept those parameters again.
