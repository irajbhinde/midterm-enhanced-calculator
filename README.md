# 🧮 Advanced Calculator (Midterm Project) — With Optional & Advanced Features

A **feature-rich, design-pattern-driven** command-line calculator built with Python.  
Implements **Factory**, **Memento**, **Observer**, **Decorator**, and **Command** patterns, 
with full CI/CD coverage enforcement, logging, persistence, and input validation.

---

## 🚀 Features

### ✳️ Operations Supported
- `add` — addition  
- `subtract` — subtraction  
- `multiply` — multiplication  
- `divide` — division  
- `power` — exponentiation  
- `root` — nth root of a number  
- `modulus` — remainder after division  
- `int_divide` — integer (floor) division  
- `percent` — percentage of one number to another  
- `abs_diff` — absolute difference

### 🧩 Design Patterns Implemented
| Pattern | Purpose | Example |
|----------|----------|----------|
| **Factory** | Create operation objects dynamically | `OperationFactory.create("add")` |
| **Memento** | Enable `undo` / `redo` history | `calc.undo()` → rolls back to previous state |
| **Observer** | Log or auto-save after each operation | `LoggingObserver`, `AutoSaveObserver` |
| **Decorator** | Dynamic help menu | New operations automatically appear in help |
| **Command** | Encapsulate REPL actions | `CommandRegistry` maps text to actions |

---

## ⚙️ Setup & Quickstart

### 1️⃣ Create and activate a virtual environment
```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Run the calculator
```bash
python -m app
```

---

## 🧾 Configuration

All key settings are loaded from `.env`:

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

Default values are automatically used if `.env` is missing.

---

## 💻 REPL Commands

| Command | Description |
|----------|--------------|
| `add a b` | Add two numbers |
| `subtract a b` | Subtract second number from first |
| `multiply a b` | Multiply two numbers |
| `divide a b` | Divide first by second |
| `power a b` | Raise `a` to the power of `b` |
| `root a b` | Take the `b`-th root of `a` |
| `modulus a b` | Compute remainder of `a / b` |
| `int_divide a b` | Perform integer division |
| `percent a b` | Compute (a / b) × 100 |
| `abs_diff a b` | Absolute difference |
| `undo`, `redo` | Undo or redo previous operation |
| `history` | View current history |
| `clear` | Clear history |
| `save`, `load` | Save/load history from CSV |
| `help` | Display dynamic help (auto-updates) |
| `exit` | Quit the program |

---

## 🧮 Example Sessions

### ✅ Basic Arithmetic
```
> add 10 5
add(10.0, 5.0) = 15.0
> subtract 10 3
subtract(10.0, 3.0) = 7.0
> divide 10 2
divide(10.0, 2.0) = 5.0
```

### 🧠 Undo / Redo with Memento Pattern
```
> add 2 2
add(2.0, 2.0) = 4.0
> multiply 3 3
multiply(3.0, 3.0) = 9.0
> undo
Undo completed.
> history
1. add(2.0, 2.0) = 4.0
> redo
Redo completed.
> history
1. add(2.0, 2.0) = 4.0
2. multiply(3.0, 3.0) = 9.0
```

### 💾 Save / Load History
```
> save
History saved.
> clear
History cleared.
> load
History loaded.
```

---

## 🔍 Input Validation Examples

| Input | Behavior |
|--------|-----------|
| `divide 10 0` | ❌ Displays “Division by zero is not allowed.” |
| `add 10` | ❌ Displays “Usage: <operation> a b” |
| `power 2 x` | ❌ Displays “Not a valid number: 'x'” |
| `add 9999999999999 2` | ❌ Exceeds max value (from `.env` → `CALCULATOR_MAX_INPUT_VALUE`) |
| `percent 5 20` | ✅ Outputs “percent(5.0, 20.0) = 25.0” |

All validation logic lives in **`input_validators.py`** and raises a custom `ValidationError`.

---

## 🎨 Colorized Output (via Colorama)

| Color | Meaning |
|--------|----------|
| 🟩 Green | Success |
| 🟥 Red | Error |
| 🟨 Yellow | Input prompt |
| 🟦 Cyan | Info/help messages |

Colorama is initialized with `autoreset=True` for consistent terminal output.

---

## 🧠 Testing

### Run Tests with Coverage
```bash
pytest --cov=app --cov-fail-under=90
```
### Coverage Target
✅ Minimum 90% enforced by GitHub Actions CI.

---

## ⚡ Continuous Integration (GitHub Actions)

`.github/workflows/python-app.yml` ensures:
- Install dependencies
- Run tests with coverage
- Enforce minimum coverage before merging

Example snippet:
```yaml
pytest --cov=app --cov-fail-under=90
```

---

## 🧩 Design Pattern Overview

| Pattern | Purpose | Key Files |
|----------|----------|-----------|
| **Factory** | Create operation objects dynamically | `operations.py` |
| **Memento** | Undo/Redo state history | `calculator_memento.py`, `history.py` |
| **Observer** | Notify on calculation events | `logger.py`, `calculator.py` |
| **Decorator** | Dynamic help menu | `help.py` |
| **Command** | Encapsulate REPL commands | `command.py` |

---

## 📚 Notes

- REPL excluded from coverage with `# pragma: no cover`.
- CSV schema: `operation, operand1, operand2, result, timestamp`.
- The project demonstrates modular OOP design, high testability, and adherence to SOLID principles.

---

## 🏁 Final Takeaway

This calculator isn't just functional — it's a **showcase of maintainable, scalable architecture** built using real-world software design techniques.  

