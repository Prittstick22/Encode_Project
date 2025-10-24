# Contributing to Portfolio Management Application

Thank you for your interest in contributing to this project!

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Encode_Project.git
   cd Encode_Project
   ```
3. **Set up the development environment**
   ```bash
   cp .env.example .env
   docker-compose up -d
   ```

## Development Workflow

### Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run backend tests
   docker-compose exec backend python -m pytest

   # Check code style
   docker-compose exec backend python -m flake8 .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Documentation
- Update README.md for user-facing changes
- Update API_DOCUMENTATION.md for API changes
- Add inline comments for complex logic

### Git Commits
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep commits focused on single changes

## Areas for Contribution

### Features
- [ ] Add more portfolio analytics metrics
- [ ] Implement user authentication
- [ ] Add email notifications for portfolio updates
- [ ] Create mobile-responsive frontend
- [ ] Add more data sources beyond yfinance
- [ ] Implement portfolio comparison features
- [ ] Add risk analysis tools

### Improvements
- [ ] Optimize database queries
- [ ] Add caching layer (Redis)
- [ ] Improve error handling
- [ ] Add more comprehensive tests
- [ ] Enhance Grafana dashboards
- [ ] Add data export functionality

### Documentation
- [ ] Add video tutorials
- [ ] Create architecture diagrams
- [ ] Write blog posts about features
- [ ] Translate documentation to other languages

### Bug Fixes
- Check open issues for bugs to fix
- Report new bugs with detailed information

## Testing Guidelines

### Writing Tests
- Place tests in appropriate test files
- Test both success and failure cases
- Mock external API calls (yfinance, OpenAI)
- Aim for good test coverage

### Running Tests
```bash
# All tests
docker-compose exec backend python -m pytest

# Specific test file
docker-compose exec backend python -m pytest test_app.py

# With coverage
docker-compose exec backend python -m pytest --cov=.
```

## Code Review Process

1. All PRs require review before merging
2. Address reviewer feedback
3. Keep PRs focused and reasonably sized
4. Update your PR if main branch changes

## Questions?

- Open an issue for discussion
- Join project discussions
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
