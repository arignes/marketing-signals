#!/usr/bin/env python3
"""
Validate signals JSON files against the schema.
"""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError


def validate_signals_file(signals_path: Path, schema_path: Path) -> bool:
    """Validate a signals file against the schema."""
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        with open(signals_path, 'r') as f:
            signals = json.load(f)
        
        validator = Draft202012Validator(schema)
        validator.validate(signals)
        
        print(f"✓ {signals_path} is valid")
        return True
        
    except ValidationError as e:
        print(f"✗ {signals_path} is invalid:")
        print(f"  {e.message}")
        if e.path:
            print(f"  Path: {'.'.join(str(p) for p in e.path)}")
        return False
        
    except json.JSONDecodeError as e:
        print(f"✗ {signals_path} contains invalid JSON:")
        print(f"  {e}")
        return False
        
    except Exception as e:
        print(f"✗ Error validating {signals_path}:")
        print(f"  {e}")
        return False


def main():
    """Main validation entry point."""
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / 'schema' / 'signals.schema.json'
    signals_dir = repo_root / 'signals'
    
    if not schema_path.exists():
        print(f"✗ Schema not found: {schema_path}")
        sys.exit(1)
    
    # Find all JSON files in signals/
    json_files = list(signals_dir.glob('**/*.json'))
    
    if not json_files:
        print("No JSON files found in signals/")
        sys.exit(0)
    
    print(f"Validating {len(json_files)} file(s) against schema...\n")
    
    all_valid = True
    for json_file in sorted(json_files):
        if not validate_signals_file(json_file, schema_path):
            all_valid = False
    
    print()
    if all_valid:
        print(f"All {len(json_files)} file(s) passed validation ✓")
        sys.exit(0)
    else:
        print("Some files failed validation ✗")
        sys.exit(1)


if __name__ == '__main__':
    main()
