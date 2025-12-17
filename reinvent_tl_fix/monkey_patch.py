"""
Monkey Patch for REINVENT4 Transfer Learning Config

This script patches the REINVENT4 TLConfig to accept the additional
parameters that cause validation errors in Pydantic v2.

Usage:
    Import this module BEFORE importing or using REINVENT4:
    
    import monkey_patch  # This applies the patch
    # Now use REINVENT4 normally
    from reinvent import ...

Alternative usage:
    Apply the patch explicitly:
    
    from monkey_patch import apply_patch
    apply_patch()
    # Now use REINVENT4 normally
"""

import sys
import warnings


def apply_patch():
    """
    Apply monkey patch to REINVENT4's TLConfig Parameters model.
    
    This function attempts to patch the Parameters model in the
    REINVENT4 package to accept additional fields.
    """
    try:
        # Try to import the REINVENT4 config module
        # Note: The actual import path may vary depending on REINVENT4 version
        import_paths = [
            ('reinvent.runmodes.TL.config', 'reinvent.runmodes.TL.config'),
            ('reinvent.models.tl_config', 'reinvent.models.tl_config'),
            ('reinvent.config', 'reinvent.config'),
        ]
        
        TLConfig = None
        Parameters = None
        config_module = None
        
        for module_path, module_name in import_paths:
            try:
                module = __import__(module_path, fromlist=['TLConfig', 'Parameters'])
                TLConfig = getattr(module, 'TLConfig', None)
                Parameters = getattr(module, 'Parameters', None)
                if TLConfig and Parameters:
                    config_module = module_name
                    break
            except ImportError:
                continue
        
        if not (TLConfig and Parameters):
            warnings.warn(
                "Could not find REINVENT4 TLConfig. "
                "Please ensure REINVENT4 is installed and update the import path in this patch."
            )
            return False
        
        # Import Pydantic's ConfigDict
        from pydantic import ConfigDict
        
        # Check if Parameters already allows extra fields
        if hasattr(Parameters, 'model_config'):
            current_config = Parameters.model_config
            if isinstance(current_config, dict) and current_config.get('extra') == 'allow':
                print("✓ Parameters model already allows extra fields. No patch needed.")
                return True
        
        # Apply the patch: Allow extra fields
        Parameters.model_config = ConfigDict(extra="allow")
        
        print(f"✓ Successfully patched {config_module}.Parameters to allow extra fields")
        return True
        
    except Exception as e:
        warnings.warn(f"Failed to apply monkey patch: {e}")
        return False


# Automatically apply patch when module is imported
if __name__ != "__main__":
    # Only auto-patch if imported as a module
    if 'reinvent' not in sys.modules:
        print("Applying REINVENT4 TLConfig patch...")
        apply_patch()
    else:
        warnings.warn(
            "REINVENT4 already imported. Monkey patch may not work correctly. "
            "Import this module BEFORE importing REINVENT4."
        )


if __name__ == "__main__":
    # When run as a script, show usage
    print("=" * 70)
    print("REINVENT4 TLConfig Monkey Patch")
    print("=" * 70)
    print()
    print("This script patches REINVENT4 to accept additional parameters")
    print("in the transfer learning configuration.")
    print()
    print("Usage:")
    print("  1. Import this module before using REINVENT4:")
    print("     >>> import monkey_patch")
    print("     >>> # Now use REINVENT4 normally")
    print()
    print("  2. Or apply the patch explicitly:")
    print("     >>> from monkey_patch import apply_patch")
    print("     >>> apply_patch()")
    print()
    print("Testing patch application...")
    success = apply_patch()
    if success:
        print("\n✓ Patch applied successfully (if REINVENT4 is installed)")
    else:
        print("\n✗ Patch application failed (REINVENT4 may not be installed)")
