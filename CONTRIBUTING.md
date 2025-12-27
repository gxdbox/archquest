# Contributing to ArchQuest

Thank you for your interest in contributing to ArchQuest! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue describing:
- The feature you'd like to see
- Why it would be useful
- How it might work

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/archquest.git
cd archquest

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write clear, descriptive commit messages
- Add comments for complex logic

### Adding New Quests

To add a new quest level:

1. Create a YAML file in `data/quests/` (e.g., `level5_quest.yaml`)
2. Update `backend/engine/game_engine.py` to include the new level
3. Add corresponding skills in `data/skill_tree.json`
4. Test the new quest thoroughly

### Questions?

Feel free to open an issue for any questions about contributing!

---

**Thank you for helping make ArchQuest better!** 🚀
