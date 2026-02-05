#!/usr/bin/env python3
"""Log action finder operations to a YAML history file."""

import sys
import os
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

## ⬇️ Startup log - executed immediately when script is loaded
_STARTUP_TIMESTAMP = datetime.now().isoformat()
print(f"[STARTUP] log.py script loaded at {_STARTUP_TIMESTAMP}", file=sys.stderr)
print(f"[STARTUP] Python executable: {sys.executable}", file=sys.stderr)
print(f"[STARTUP] Script file: {__file__}", file=sys.stderr)
print(f"[STARTUP] Arguments received: {sys.argv}", file=sys.stderr)
sys.stderr.flush()
print(f"[STARTUP] log.py script loaded at {_STARTUP_TIMESTAMP}", file=sys.stdout)
print(f"[STARTUP] Arguments received: {sys.argv}", file=sys.stdout)
sys.stdout.flush()

## ⬇️ Write startup log to file immediately
try:
    script_dir = Path(__file__).parent.resolve() if '__file__' in globals() else Path.cwd() / 'scripts'
    startup_log_file = script_dir / 'startup.log'
    with open(startup_log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"SCRIPT STARTUP: {_STARTUP_TIMESTAMP}\n")
        f.write(f"Python executable: {sys.executable}\n")
        f.write(f"Script file: {__file__}\n")
        f.write(f"Arguments: {sys.argv}\n")
        f.write(f"Working directory: {Path.cwd()}\n")
        f.write(f"{'='*60}\n")
        f.flush()
        os.fsync(f.fileno())
except Exception as e:
    print(f"[STARTUP ERROR] Failed to write startup log: {e}", file=sys.stderr)
    sys.stderr.flush()


def log_error(error_msg: str, script_dir: Path, exception: Exception = None):
    """Log errors to error.log file."""
    error_file = script_dir / 'error.log'
    try:
        with open(error_file, 'a', encoding='utf-8') as ef:
            ef.write(f"\n=== ERROR {datetime.now().isoformat()} ===\n")
            ef.write(f"Error: {error_msg}\n")
            if exception:
                import traceback
                ef.write(f"Exception: {exception}\n")
                ef.write(f"Traceback:\n{traceback.format_exc()}\n")
            ef.write(f"Arguments received: {sys.argv}\n")
            ef.write(f"Script directory: {script_dir}\n")
            ef.write(f"Current working directory: {Path.cwd()}\n")
            ef.write("=" * 50 + "\n")
            ef.flush()
    except Exception as e:
        print(f"[DEBUG] Failed to write to error.log: {e}", file=sys.stderr)
        sys.stderr.flush()


def load_history(log_file: Path) -> list:
    """Load existing history from YAML file."""
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('operations', []) if data else []
        except Exception:
            return []
    return []


def save_history(log_file: Path, operations: list):
    """Save history to YAML file."""
    script_dir = Path(__file__).parent.resolve()
    try:
        print(f"[DEBUG] save_history: Creating parent directories for {log_file}", file=sys.stderr)
        sys.stderr.flush()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        print(f"[DEBUG] save_history: Parent directory exists: {log_file.parent.exists()}", file=sys.stderr)
        print(f"[DEBUG] save_history: Parent directory path: {log_file.parent}", file=sys.stderr)
        sys.stderr.flush()
        
        print(f"[DEBUG] save_history: Writing {len(operations)} operations to {log_file}", file=sys.stderr)
        print(f"[DEBUG] save_history: Absolute log file path: {log_file.resolve()}", file=sys.stderr)
        sys.stderr.flush()
        
        # Write the file
        with open(log_file, 'w', encoding='utf-8') as f:
            yaml.dump({'operations': operations}, f, default_flow_style=False, sort_keys=False)
            f.flush()
            os.fsync(f.fileno())  # Force write to disk
        
        # Verify file was written
        if log_file.exists():
            file_size = log_file.stat().st_size
            print(f"[DEBUG] save_history: File written successfully - size: {file_size} bytes", file=sys.stderr)
            sys.stderr.flush()
        else:
            error_msg = f"save_history ERROR: File was not created at {log_file}"
            print(f"[DEBUG] {error_msg}", file=sys.stderr)
            sys.stderr.flush()
            log_error(error_msg, script_dir)
            raise FileNotFoundError(error_msg)
            
    except Exception as e:
        error_msg = f"save_history ERROR: {e}"
        print(f"[DEBUG] {error_msg}", file=sys.stderr)
        import traceback
        print(f"[DEBUG] save_history Traceback: {traceback.format_exc()}", file=sys.stderr)
        sys.stderr.flush()
        # Log to error.log
        log_error(error_msg, script_dir, e)
        raise


def log_operation(entity_name: str, template_selected: str, actions: list[str]):
    """
    Log an operation to the history file.
    
    Args:
        entity_name: Name of the entity
        template_selected: Template that was selected (CIDED, CIDRA, or CID)
        actions: List of action names that were found and returned
    """
    try:
        print(f"[DEBUG] Starting log_operation for entity: {entity_name}, template: {template_selected}", file=sys.stderr)
        sys.stderr.flush()
        
        # Get the log file path relative to the script directory
        # Use resolve() to get absolute path to avoid issues with working directory
        script_dir = Path(__file__).parent.resolve()
        log_file = script_dir / 'history.yaml'
        
        print(f"[DEBUG] Script directory: {script_dir}", file=sys.stderr)
        print(f"[DEBUG] Log file path: {log_file}", file=sys.stderr)
        print(f"[DEBUG] Log file absolute path: {log_file.resolve()}", file=sys.stderr)
        sys.stderr.flush()
        
        # Load existing history
        print(f"[DEBUG] Loading existing history from {log_file}", file=sys.stderr)
        sys.stderr.flush()
        operations = load_history(log_file)
        print(f"[DEBUG] Loaded {len(operations)} existing operations", file=sys.stderr)
        sys.stderr.flush()
        
        # Create new operation entry
        operation = {
            'datetime': datetime.now().isoformat(),
            'entity_name': entity_name,
            'template_selected': template_selected,
            'actions_found': actions,
            'actions_count': len(actions)
        }
        
        print(f"[DEBUG] Created operation entry: {operation}", file=sys.stderr)
        sys.stderr.flush()
        
        # Append to history
        operations.append(operation)
        print(f"[DEBUG] Total operations after append: {len(operations)}", file=sys.stderr)
        sys.stderr.flush()
        
        # Save updated history
        print(f"[DEBUG] Saving history to {log_file}", file=sys.stderr)
        sys.stderr.flush()
        save_history(log_file, operations)
        
        # Verify file was created - try multiple times with delays
        import time
        max_attempts = 5
        for attempt in range(max_attempts):
            if log_file.exists():
                file_size = log_file.stat().st_size
                print(f"[DEBUG] SUCCESS: Log file exists at {log_file} (size: {file_size} bytes)", file=sys.stderr)
                sys.stderr.flush()
                break
            elif attempt < max_attempts - 1:
                time.sleep(0.1)  # Wait 100ms and retry
            else:
                error_msg = f"ERROR: Log file was NOT created at {log_file} after {max_attempts} attempts"
                print(f"[DEBUG] {error_msg}", file=sys.stderr)
                sys.stderr.flush()
                log_error(error_msg, script_dir)
                raise FileNotFoundError(error_msg)
        
        # Also print to stdout for visibility
        print(f"SUCCESS: Logged operation: {entity_name} with template {template_selected} to {log_file}", file=sys.stdout)
        print(f"File location: {log_file.resolve()}", file=sys.stdout)
        sys.stdout.flush()
    except Exception as e:
        import traceback
        error_msg = f"ERROR in log_operation: {e}"
        print(f"[DEBUG] {error_msg}", file=sys.stderr)
        print(f"[DEBUG] Traceback: {traceback.format_exc()}", file=sys.stderr)
        sys.stderr.flush()
        # Log to error.log
        script_dir = Path(__file__).parent.resolve()
        log_error(error_msg, script_dir, e)
        raise


def main():
    """Main entry point for the script."""
    ## ⬇️ Enhanced startup logging
    startup_time = datetime.now().isoformat()
    print("="*60, file=sys.stderr)
    print(f"[MAIN] log.py main() function called at {startup_time}", file=sys.stderr)
    print(f"[MAIN] Script file: {__file__}", file=sys.stderr)
    print(f"[MAIN] Python executable: {sys.executable}", file=sys.stderr)
    print(f"[MAIN] Arguments count: {len(sys.argv)}", file=sys.stderr)
    print(f"[MAIN] Arguments: {sys.argv}", file=sys.stderr)
    print(f"[MAIN] Working directory: {Path.cwd()}", file=sys.stderr)
    print("="*60, file=sys.stderr)
    sys.stderr.flush()
    
    print("="*60, file=sys.stdout)
    print(f"[MAIN] log.py main() function called at {startup_time}", file=sys.stdout)
    print(f"[MAIN] Arguments: {sys.argv}", file=sys.stdout)
    print("="*60, file=sys.stdout)
    sys.stdout.flush()
    
    # Write debug info to a debug file as well - use absolute path to ensure it works
    try:
        script_dir = Path(__file__).parent.resolve()
    except Exception as e:
        # Fallback if __file__ doesn't work
        script_dir = Path.cwd() / 'scripts'
        print(f"Warning: Could not resolve script directory, using: {script_dir}", file=sys.stderr)
        sys.stderr.flush()
    
    debug_file = script_dir / 'debug.log'
    error_file = script_dir / 'error.log'
    
    # Create a test file immediately to verify we can write
    test_file = script_dir / 'test_script_running.txt'
    try:
        test_file.write_text(f"Script ran at {datetime.now().isoformat()}\nArguments: {sys.argv}\n")
        print(f"Test file created: {test_file}", file=sys.stderr)
        sys.stderr.flush()
    except Exception as e:
        print(f"Failed to create test file: {e}", file=sys.stderr)
        import traceback
        print(traceback.format_exc(), file=sys.stderr)
        sys.stderr.flush()
        log_error(f"Failed to create test file: {e}", script_dir, e)
    
    try:
        with open(debug_file, 'a', encoding='utf-8') as df:
            df.write(f"\n=== {datetime.now().isoformat()} ===\n")
            df.write(f"main() called with {len(sys.argv)} arguments: {sys.argv}\n")
            df.write(f"Script directory: {script_dir}\n")
            df.write(f"Current working directory: {Path.cwd()}\n")
            df.flush()
            os.fsync(df.fileno())
        print(f"Debug file written: {debug_file}", file=sys.stderr)
        sys.stderr.flush()
    except Exception as e:
        # Even if debug file fails, try to write to stderr
        print(f"[DEBUG] Failed to write to debug.log: {e}", file=sys.stderr)
        sys.stderr.flush()
    
    print(f"[DEBUG] main() called with {len(sys.argv)} arguments: {sys.argv}", file=sys.stderr)
    print(f"[DEBUG] Script directory: {script_dir}", file=sys.stderr)
    print(f"[DEBUG] Current working directory: {Path.cwd()}", file=sys.stderr)
    sys.stderr.flush()
    
    if len(sys.argv) < 4:
        error_msg = f"Invalid arguments: Expected at least 4 arguments (entity_name, template, and at least one action), but got {len(sys.argv)} arguments.\nUsage: log.py <entity_name> <template> <action1> [action2] ...\nExample: log.py User CIDED createUser listUsers getUser editUser deleteUser"
        print(error_msg, file=sys.stderr)
        sys.stderr.flush()
        log_error(error_msg, script_dir)
        sys.exit(1)
    
    entity_name = sys.argv[1]
    template_selected = sys.argv[2]
    actions = sys.argv[3:]
    
    print(f"[DEBUG] Parsed arguments - entity: {entity_name}, template: {template_selected}, actions: {actions}", file=sys.stderr)
    sys.stderr.flush()
    
    try:
        with open(debug_file, 'a', encoding='utf-8') as df:
            df.write(f"Parsed: entity={entity_name}, template={template_selected}, actions={actions}\n")
            df.flush()
    except Exception as e:
        print(f"[DEBUG] Failed to write parsed args to debug.log: {e}", file=sys.stderr)
        sys.stderr.flush()
    
    # Validate template
    valid_templates = ['CIDED', 'CIDRA', 'CID']
    if template_selected not in valid_templates:
        error_msg = f"Invalid template: '{template_selected}'. Valid templates are: {', '.join(valid_templates)}"
        print(f"[ERROR] {error_msg}", file=sys.stderr)
        sys.stderr.flush()
        log_error(error_msg, script_dir)
        sys.exit(1)
    
    # Validate actions (check if they look like template names instead of camelCase)
    template_action_names = ['Create', 'Index', 'Details', 'Edit', 'Delete', 'Reject', 'Approve']
    suspicious_actions = [action for action in actions if action in template_action_names]
    if suspicious_actions:
        error_msg = f"Invalid action names detected: {suspicious_actions}. These look like template action names, not generated camelCase names. Expected format: createUser, listUsers, etc. (camelCase)."
        print(f"[ERROR] {error_msg}", file=sys.stderr)
        sys.stderr.flush()
        log_error(error_msg, script_dir)
        # Don't exit - log the error but continue, as the script might still work
    
    try:
        log_operation(entity_name, template_selected, actions)
        print(f"[DEBUG] main() completed successfully", file=sys.stderr)
        sys.stderr.flush()
        
        try:
            with open(debug_file, 'a', encoding='utf-8') as df:
                df.write("main() completed successfully\n")
                df.flush()
        except:
            pass
    except Exception as e:
        error_msg = f"ERROR in main() during log_operation: {e}"
        print(error_msg, file=sys.stderr)
        import traceback
        print(traceback.format_exc(), file=sys.stderr)
        sys.stderr.flush()
        log_error(error_msg, script_dir, e)
        try:
            with open(debug_file, 'a', encoding='utf-8') as df:
                df.write(f"{error_msg}\n{traceback.format_exc()}\n")
                df.flush()
        except:
            pass
        raise


if __name__ == "__main__":
    main()
