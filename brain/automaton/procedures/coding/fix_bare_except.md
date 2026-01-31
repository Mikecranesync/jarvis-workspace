# Procedure: Fix Bare Except Clauses

## When to Use
- Found `except:` without exception type in Python code
- Part of autonomous code improvement

## Steps

1. **Find the bare except**
   ```bash
   grep -n "except:" path/to/file.py
   ```

2. **Read the context**
   - What operation is in the try block?
   - What exceptions could realistically occur?

3. **Determine appropriate exceptions**
   - Network operations: `ConnectionError, TimeoutError`
   - File I/O: `IOError, FileNotFoundError`
   - JSON parsing: `json.JSONDecodeError`
   - WebSocket: `WebSocketDisconnect, ConnectionError`
   - General: `Exception` (still better than bare)

4. **Add logging**
   - Log the exception for debugging
   - Include context about what failed

5. **Make the edit**
   ```python
   # Before
   except:
       handle_error()
   
   # After
   except (SpecificError, OtherError) as e:
       logger.debug(f"Error description: {e}")
       handle_error()
   ```

6. **Test if possible**
   - Run any existing tests
   - Verify import still works

7. **Log the improvement**
   - Update `brain/automaton/improvements-log.md`

## Success Criteria
- No bare except clauses remain
- Appropriate exceptions caught
- Logging added for debugging
- File still imports/runs

## Common Pitfalls
- Catching too broad (just `Exception`)
- Forgetting to log the error
- Missing import for exception types

## Examples
- 2026-01-31: Fixed WebSocket broadcast in API server
