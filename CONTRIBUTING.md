# Contributing to URL Phishing Detector

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!

### Coding Standards

#### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function parameters and return types
- Write docstrings for all functions and classes
- Maximum line length: 100 characters

Example:
```python
def analyze_url(url: str) -> dict:
    """
    Analyze a URL for phishing characteristics.
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dictionary with analysis results
    """
    # Implementation
    pass
```

#### HTML/CSS/JavaScript
- Use meaningful variable and function names
- Add comments for complex logic
- Follow consistent indentation (2 spaces for web, 4 for Python)
- Validate HTML and CSS

### Commit Messages

Write clear, descriptive commit messages:

```
Good: "Add HTTPS validation to URL analyzer"
Bad: "Fixed stuff" or "WIP"

Good: "Implement batch URL processing API"
Bad: "Update server.py"
```

Format:
```
Subject (50 chars max)
<blank line>
Body (wrap at 72 chars)
<blank line>
Fixes #123
```

### Testing

- Write tests for all new features
- Run `pytest tests/` before submitting PR
- Aim for >80% code coverage
- Test both happy paths and edge cases

Example test:
```python
def test_https_validation():
    """Test that HTTPS URLs pass protocol check."""
    result = analyze_url("https://example.com")
    assert result['checks'][0]['status'] == 'pass'

def test_http_validation():
    """Test that HTTP URLs fail protocol check."""
    result = analyze_url("http://example.com")
    assert result['checks'][0]['status'] == 'fail'
```

### Documentation

- Update README.md with any new features
- Add docstrings to new functions
- Include examples for new API endpoints
- Update docs/ folder if appropriate

### Areas to Contribute

#### Backend
- [ ] Improve URL analysis heuristics
- [ ] Add more security checks
- [ ] Optimize performance
- [ ] Add caching layer
- [ ] Improve error handling

#### Frontend
- [ ] Enhance UI design
- [ ] Add dark mode
- [ ] Improve responsiveness
- [ ] Add new visualizations
- [ ] Improve accessibility

#### Features
- [ ] BERT AI integration
- [ ] Email security checks
- [ ] Batch URL analysis
- [ ] API rate limiting
- [ ] Advanced analytics

#### Documentation
- [ ] Write tutorials
- [ ] Add more examples
- [ ] Create video guides
- [ ] Improve existing docs

## Reporting Bugs

### Before Submitting a Bug Report

- **Check the documentation** to see if the problem is documented
- **Check GitHub issues** to see if someone already reported it
- **Try the latest code** to see if the problem is already fixed

### How to Submit a Bug Report

When filing a bug report, include:

1. **Title**: Short description of the problem
2. **Description**: What you expected vs what happened
3. **Steps to Reproduce**: Exact steps to reproduce the issue
4. **Screenshots**: If applicable
5. **Environment**: OS, Python version, browser version
6. **Code sample**: If applicable

Example:
```
Title: URL with special characters causes error

Description:
When analyzing URLs with special characters, the app crashes.

Steps to Reproduce:
1. Enter URL: https://example.com/?param=value&other=test
2. Click Analyze
3. App crashes

Expected: Should analyze the URL
Actual: Shows "Internal Server Error"

Environment:
- Python 3.10
- Chrome 120
- Windows 11
```

## Proposing Features

1. **Use a clear, descriptive title**
2. **Provide a step-by-step description**
3. **Provide examples to demonstrate the feature**
4. **Describe why this enhancement would be useful**

Example:
```
Title: Add ability to analyze email headers for phishing

Description:
Currently we only analyze URLs. Many phishing attacks use 
email headers to appear legitimate.

Proposed Solution:
Add new endpoint POST /api/analyze-email-header that:
- Parses email headers
- Checks sender SPF/DKIM/DMARC
- Identifies spoofing

Use Cases:
- Email client integration
- Corporate email filtering
- User education

This would make the tool more comprehensive.
```

## Code Review Process

1. **Automated checks**: Tests and linting must pass
2. **Code review**: Team members review your code
3. **Feedback**: We'll request changes if needed
4. **Approval**: Once approved, you can merge

We appreciate your patience during review!

## Additional Notes

### Project Governance

- **Maintainers**: Have admin access and manage releases
- **Contributors**: Help with code, docs, issues
- **Community**: Users who report bugs and suggest features

### License

By contributing, you agree your code will be licensed under its existing license (MIT).

### Questions?

- Open an issue with the question tag
- Start a discussion
- Email the team

---

## Team Member Guidelines

If you're on the development team:

### Daily Workflow

1. Pull latest: `git pull origin main`
2. Create feature branch: `git checkout -b feature/task`
3. Make changes
4. Commit: `git commit -m "Clear message"`
5. Push: `git push origin feature/task`
6. Create Pull Request
7. Request review from teammate
8. Address feedback
9. Merge when approved

### Code Review for Team

When reviewing teammate's code:

- Be respectful and constructive
- Suggest improvements, don't criticize
- Ask questions if code is unclear
- Approve when quality meets standards
- Merge when changes are complete

### Weekly Sync

- 15-30 minute standup
- What we accomplished
- What we're working on
- Any blockers
- Plan for next week

---

## Attribution

This Contributing guide is adapted from best practices in open source.

Thank you for contributing! 🙏
