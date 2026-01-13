# Contributing to Bradesco PDF to Excel Converter

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Submitting Changes](#submitting-changes)
6. [Reporting Bugs](#reporting-bugs)
7. [Suggesting Enhancements](#suggesting-enhancements)

---

## Code of Conduct

This project aims to be welcoming and inclusive. Please be respectful and considerate when interacting with others.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

---

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Describe the issue briefly
2. **Description**: Detailed explanation of the bug
3. **Steps to reproduce**: How to reproduce the issue
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**: OS, Python version, etc.
7. **Screenshots**: If applicable

**Example**:
```
Title: PDF with special characters fails to convert

Description:
When uploading a PDF that contains special characters (ç, ã, õ),
the conversion fails with an encoding error.

Steps to Reproduce:
1. Start the server
2. Upload PDF with special characters
3. Click convert

Expected: PDF converts successfully
Actual: Error 500 with encoding exception

Environment:
- OS: Ubuntu 22.04
- Python: 3.10.5
- Browser: Chrome 120
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. **Use case**: Why is this enhancement needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: Any alternative approaches?
4. **Additional context**: Screenshots, mockups, etc.

### Pull Requests

Pull requests are always welcome! See [Submitting Changes](#submitting-changes) below.

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Mywebsocket.git
cd Mywebsocket
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# Install development dependencies (if added)
pip install pytest black flake8 mypy
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 5. Make Your Changes

Edit the code, add tests, update documentation.

### 6. Test Your Changes

```bash
# Run the server
uvicorn main:app --reload

# Test manually or with scripts
python -m pytest  # If tests exist
```

---

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names

### Code Formatting

Use Black for formatting:

```bash
pip install black
black .
```

### Linting

Use flake8 for linting:

```bash
pip install flake8
flake8 . --max-line-length=88 --extend-ignore=E203
```

### Type Hints

Add type hints where possible:

```python
def convert_pdf(filename: str) -> bytes:
    """Convert PDF to Excel"""
    pass
```

### Documentation

- Add docstrings to functions and classes
- Update README.md if adding features
- Add examples to EXAMPLES.md if applicable
- Update TECHNICAL.md for architecture changes

**Example Docstring**:
```python
def process_page(df: pd.DataFrame, page_num: int) -> pd.DataFrame:
    """
    Process a single page of the bank statement.
    
    Args:
        df: DataFrame containing extracted table data
        page_num: Page number (1-indexed)
    
    Returns:
        Cleaned and formatted DataFrame
    
    Raises:
        ValueError: If DataFrame is empty or invalid
    """
    pass
```

### Comments

- Write comments for complex logic
- Avoid obvious comments
- Use Portuguese for domain-specific terms when appropriate
- Use English for technical terms

---

## Submitting Changes

### Before Submitting

1. **Test your changes**: Ensure everything works
2. **Update documentation**: If you changed functionality
3. **Add examples**: If you added new features
4. **Format code**: Run Black and flake8
5. **Commit message**: Write clear commit messages

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Longer description if needed

Fixes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(converter): add support for multi-column statements

fix(helpers): handle empty rows correctly

docs(readme): update installation instructions

refactor(convert): simplify page detection logic
```

### Pull Request Process

1. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request on GitHub**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the template

3. **PR Description** should include:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Related issues (if any)

**Example PR Description**:
```markdown
## Description
Added support for bank statements with multiple accounts on the same PDF.

## Changes
- Modified `convert.py` to detect account changes
- Updated `helpers.py` to handle multi-account data
- Added new function `split_by_account()`

## Testing
1. Upload the test file `multi_account_statement.pdf`
2. Verify output has separate sheets for each account
3. Check data integrity for each account

## Related Issues
Fixes #42
```

4. **Wait for Review**:
   - Address any feedback
   - Make requested changes
   - Update the PR

5. **Merge**:
   - Once approved, maintainer will merge
   - Delete your branch after merge

---

## Reporting Bugs

### Security Issues

**Do not** open public issues for security vulnerabilities. Instead:
- Email the maintainer directly
- Provide detailed information
- Wait for response before disclosing

### Bug Reports

Use the issue template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Browser: [e.g. Chrome 120]

**Additional context**
Any other context about the problem.
```

---

## Suggesting Enhancements

### Feature Requests

Use this template:

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Screenshots, mockups, examples, etc.
```

### Enhancement Ideas

Some areas where contributions would be valuable:

1. **Multi-Bank Support**: Add support for other Brazilian banks
2. **Improved Error Handling**: Better error messages and recovery
3. **Progress Bar**: Implement client-side progress tracking
4. **Authentication**: Add user authentication
5. **Database**: Store conversion history
6. **Tests**: Add comprehensive test suite
7. **Docker**: Create Docker image
8. **API Documentation**: Add Swagger/OpenAPI docs
9. **Internationalization**: Add English translations
10. **Performance**: Optimize for large PDFs

---

## Development Guidelines

### Adding New Features

1. **Discuss first**: Create an issue to discuss the feature
2. **Keep it focused**: One feature per PR
3. **Maintain compatibility**: Don't break existing functionality
4. **Add tests**: If adding test infrastructure
5. **Document**: Update all relevant documentation

### Fixing Bugs

1. **Reproduce first**: Ensure you can reproduce the bug
2. **Minimal fix**: Make the smallest change that fixes it
3. **Add test**: Prevent regression
4. **Document**: Update docs if behavior changed

### Improving Documentation

1. **Clarity**: Make it easy to understand
2. **Examples**: Add practical examples
3. **Completeness**: Cover all aspects
4. **Accuracy**: Ensure information is correct
5. **Formatting**: Follow markdown best practices

---

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with the "question" label
4. Be specific and provide context

---

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes (for significant contributions)
- Special mentions for major features

Thank you for contributing! 🎉
