# Contributing to Air Canvas

Thank you for considering contributing to **Air Canvas**! 🎉

## How to contribute

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/Air_canvas.git
cd Air_canvas
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest          # for running tests
```

### 3. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make your changes

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style.
- Add docstrings to every new function and class.
- Update `config.py` if you introduce new tuneable parameters.
- Write tests in `tests/` for any new logic.

### 5. Run tests

```bash
pytest tests/
```

All tests must pass before opening a pull request.

### 6. Commit and push

```bash
git add .
git commit -m "feat: brief description of your change"
git push origin feature/your-feature-name
```

### 7. Open a pull request

Go to the original repository on GitHub and open a PR against the
`main` branch.  Describe **what** you changed and **why**.

---

## Code style

| Rule | Detail |
|------|--------|
| Formatter | PEP 8 (max line length 100) |
| Docstrings | NumPy style |
| Imports | `stdlib` → `third-party` → `local`, separated by blank lines |
| Naming | `snake_case` for variables/functions, `PascalCase` for classes |

---

## Reporting bugs

Open an issue using the **Bug report** template.  Include:

- Python version (`python --version`)
- OS and webcam model
- Steps to reproduce
- Expected vs actual behaviour

---

## Feature requests

Open an issue using the **Feature request** template and describe
the use case you want to address.

---

## Code of conduct

Be respectful and constructive.  Harassment of any kind will not be
tolerated.
