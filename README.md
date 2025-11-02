# Advanced Calculator (Midterm Project)

A feature-rich command-line calculator demonstrating **Factory**, **Memento**, and **Observer** design patterns, with undo/redo, history, logging, autosave to CSV, configuration via `.env`, a REPL interface, and CI coverage enforcement.

## Features
- Operations: add, subtract, multiply, divide, **power**, **root**, **modulus**, **int_divide**, **percent**, **abs_diff**
- **Factory Pattern** for operation creation
- **Memento Pattern** for undo/redo of calculation history
- **Observer Pattern** with:
  - `LoggingObserver` → logs each calculation
  - `AutoSaveObserver` → saves history to CSV on each new calculation
- Robust input validation and custom exceptions
- Config via `.env` (loaded with `python-dotenv`) with sane defaults
- History save/load using **pandas** CSV
- Colorized CLI using **colorama**
- Unit tests with **pytest**, **pytest-cov**, 90%+ coverage target
- GitHub Actions CI enforcing coverage

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app
```

## Configuration

Create and edit `.env` (defaults are present):

```
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1e12
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=history.csv
```

## REPL Commands
`add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff`  
`history, clear, undo, redo, save, load, help, exit`

Examples:
```
> add 2 3
> power 2 8
> percent 5 20  # 25.0 (% of 5 relative to 20 is 25%)
```

## Testing
```bash
pytest --cov=app --cov-fail-under=90
```

## CI
CI is configured in `.github/workflows/python-app.yml` to run tests and enforce coverage on pushes/PRs to `main`.

## Notes
- The REPL is excluded from coverage using `# pragma: no cover` on the entrypoint lines.
- CSV schema: `operation, operand1, operand2, result, timestamp`.
