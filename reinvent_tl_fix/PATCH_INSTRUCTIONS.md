# Patch Instructions for REINVENT4 TLConfig

## Locating the File to Patch

The error originates from the REINVENT4 package. The file to patch is typically located at:

```
<your_env>/lib/python3.11/site-packages/reinvent/runmodes/TL/run_transfer_learning.py
```

Or more specifically, you need to find the TLConfig model definition, which might be in:

```
<your_env>/lib/python3.11/site-packages/reinvent/models/tl_config.py
```

## Finding Your REINVENT4 Installation

To find where REINVENT4 is installed:

```bash
python -c "import reinvent; print(reinvent.__file__)"
```

## Patch Option 1: Add Missing Fields to Parameters Model

Find the `Parameters` class or similar in the TLConfig model and add the missing fields:

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Parameters(BaseModel):
    # Existing fields...
    batch_size: Optional[int] = 128
    num_epochs: Optional[int] = 100
    # ... other existing fields ...
    
    # ADD THESE FIELDS:
    type: Optional[str] = None
    lower_threshold: Optional[float] = None
    upper_threshold: Optional[float] = None
    min_cardinality: Optional[int] = None
    max_cardinality: Optional[int] = None
```

## Patch Option 2: Allow Extra Fields

If you don't want to explicitly define all fields, modify the Parameters model to allow extra fields:

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    # Existing fields...
    batch_size: Optional[int] = 128
    num_epochs: Optional[int] = 100
    # ... other existing fields ...
```

## Creating a Monkey Patch (Temporary Solution)

If you can't or don't want to modify the REINVENT4 source code, you can monkey patch it in your script:

```python
# At the top of your script, before importing REINVENT4
from pydantic import ConfigDict

# Import the config class
from reinvent.models.tl_config import Parameters  # Adjust import path as needed

# Monkey patch to allow extra fields
Parameters.model_config = ConfigDict(extra="allow")

# Now continue with your normal REINVENT4 usage
```

## After Patching

1. Save the file
2. Restart your Python session
3. Re-run your transfer learning script

## Verifying the Fix

Create a small test script:

```python
from reinvent.models.tl_config import TLConfig  # Adjust import as needed

config_data = {
    "run_type": "transfer_learning",
    "model_file": "test.model",
    "output_model_file": "output.model",
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
    config = TLConfig(**config_data)
    print("✓ Configuration validated successfully!")
except Exception as e:
    print(f"✗ Still failing: {e}")
```

## Long-term Solution

Consider:
1. Opening an issue with the REINVENT4 maintainers
2. Contributing a pull request to fix this in the official repository
3. Checking if there's a newer version of REINVENT4 that already includes this fix
4. Reviewing the REINVENT4 documentation to see if the configuration format has changed
