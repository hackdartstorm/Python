<!--
SPDX-License-Identifier: MIT
© 2026 Python Learning Repository
-->

<div align="center">

# 🐍 Python Learning Repository

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/hackdartstorm/Python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/hackdartstorm/Python)](https://github.com/hackdartstorm/Python/releases)
[![Stars](https://img.shields.io/github/stars/hackdartstorm/Python?style=flat-square)](https://github.com/hackdartstorm/Python/stargazers)
[![Forks](https://img.shields.io/github/forks/hackdartstorm/Python?style=flat-square)](https://github.com/hackdartstorm/Python/network)
[![Issues](https://img.shields.io/github/issues/hackdartstorm/Python?style=flat-square)](https://github.com/hackdartstorm/Python/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/hackdartstorm/Python?style=flat-square)](https://github.com/hackdartstorm/Python/pulls)
[![Contributors](https://img.shields.io/github/contributors/hackdartstorm/Python?style=flat-square)](https://github.com/hackdartstorm/Python/graphs/contributors)

### **800+ Python Programming Issues • From Beginner to Expert**

[Quick Start](#-quick-start) • [Issues](#-issues) • [Contributing](#-contributing) • [Code of Conduct](CODE_OF_CONDUCT.md)

</div>

---

## 📖 About

A comprehensive Python learning platform with **700+ curated programming issues** organized by difficulty. From your first "Hello World" to advanced algorithms and system design — everything you need to master Python is here.

**✨ All issues include:**
- ✅ Detailed problem descriptions
- ✅ Starter code templates
- ✅ Test case structures
- ✅ Progressive hints
- ✅ Complexity analysis
- ✅ Resource links

---

## 🚀 Quick Start

### Prerequisites

- ✅ Python 3.10 or higher
- ✅ Git installed
- ✅ Code editor (VS Code recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hackdartstorm/Python.git
cd Python

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies (optional)
pip install -r requirements.txt
```

### Your First Contribution

```bash
# 1. Browse issues
# Visit: https://github.com/hackdartstorm/Python/issues

# 2. Fork the repository
# Click "Fork" button on GitHub

# 3. Clone your fork
git clone https://github.com/YOUR_USERNAME/Python.git
cd Python

# 4. Create a branch
git checkout -b issue-<number>-your-name

# 5. Solve the issue
# Create your solution in the specified path

# 6. Commit and push
git add .
git commit -m "Solve issue #<number>"
git push origin issue-<number>-your-name

# 7. Create Pull Request
# Go to GitHub and click "New Pull Request"
```

---

## 📊 Issues

### Issue Distribution

| Difficulty | Count | Labels |
|------------|-------|--------|
| **Beginner** | 200+ | `beginner`, `good first issue` |
| **Medium** | 400+ | `medium` |
| **Advanced** | 100+ | `advanced` |

### Browse Issues

| Category | Link |
|----------|------|
| **All Issues** | [View 700+ Issues](https://github.com/hackdartstorm/Python/issues) |
| **Beginner Friendly** | [View Beginner Issues](https://github.com/hackdartstorm/Python/issues?q=label%3Abeginner) |
| **Good First Issues** | [View First Issues](https://github.com/hackdartstorm/Python/issues?q=label%3A%22good+first+issue%22) |
| **Medium Difficulty** | [View Medium Issues](https://github.com/hackdartstorm/Python/issues?q=label%3Amedium) |
| **Advanced** | [View Advanced Issues](https://github.com/hackdartstorm/Python/issues?q=label%3Aadvanced) |

### Issue Categories

| Category | Issues | Topics |
|----------|--------|--------|
| **Array Problems** | 150+ | Sorting, searching, manipulation |
| **String Problems** | 100+ | Manipulation, patterns, parsing |
| **Dynamic Programming** | 100+ | Optimization, recursion |
| **Graph Problems** | 80+ | BFS, DFS, shortest path |
| **Tree Problems** | 70+ | BST, traversal, balancing |
| **Stack/Queue** | 60+ | Data structures, algorithms |
| **Hash Table** | 50+ | Dictionaries, sets, mapping |
| **Math Problems** | 40+ | Number theory, calculations |

---

## 📁 Project Structure

```
python-learning/
├── basics/                     # Python fundamentals
│   ├── 01_introduction/        # Hello World, input/output
│   ├── 02_variables_types/     # Variables, operators
│   ├── 03_control_flow/        # If/else, loops
│   ├── 04_functions/           # Functions, recursion
│   ├── 05_data_structures/     # Lists, tuples, sets, dicts
│   ├── 06_strings/             # String operations
│   ├── 07_file_handling/       # File I/O
│   ├── 08_oop/                 # Object-Oriented Programming
│   ├── 09_error_handling/      # Exceptions, try/except
│   └── 10_advanced/            # Lambda, modules, advanced
├── fastapi/                    # FastAPI examples
├── rest_api/                   # Flask REST API
├── llm_fundamentals/           # LLM from scratch
├── exercises/                  # Exercise solutions
├── data/                       # Dataset files
├── .github/
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   └── workflows/              # GitHub Actions
├── README.md                   # This file
├── CONTRIBUTING.md             # Contribution guide
├── CODE_OF_CONDUCT.md          # Community guidelines
├── CHANGELOG.md                # Version history
├── SECURITY.md                 # Security policy
└── requirements.txt            # Dependencies
```

---

## 🤝 Contributing

We welcome contributions of all kinds! Here's how to help:

### Ways to Contribute

| Contribution Type | Description | Good For |
|-------------------|-------------|----------|
| **🐛 Fix Bugs** | Fix issues in existing code | All levels |
| **📝 Add Examples** | Contribute new Python examples | Beginner+ |
| **🧪 Write Tests** | Add unit tests for code | Intermediate+ |
| **📖 Improve Docs** | Enhance documentation | All levels |
| **💡 Suggest Features** | Propose new learning modules | All levels |
| **🔍 Review PRs** | Review and provide feedback | Advanced |

### Quick Start for Contributors

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Python.git
cd Python

# 3. Create a branch
git checkout -b issue-<number>-your-name

# 4. Make your changes
# - Follow PEP 8 style guidelines
# - Add comments explaining your code
# - Include test cases if applicable

# 5. Test your changes
python -m pytest  # or run individual scripts

# 6. Commit and push
git add .
git commit -m "feat: add your feature description"
git push origin issue-<number>-your-name

# 7. Create a Pull Request on GitHub
```

### Contribution Guidelines

#### Code Style
- **Variables/Functions:** `lowercase_with_underscores`
- **Classes:** `PascalCase`
- **Constants:** `UPPERCASE`
- Follow [PEP 8](https://pep8.org/) style guidelines

#### Commit Messages
Use conventional commits format:
```
type: short description

Optional details
```

**Types:**
| Type | Description |
|------|-------------|
| `feat:` | New feature or example |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | Formatting only |
| `refactor:` | Code restructuring |
| `test:` | Adding tests |

**Examples:**
```
feat: add list comprehension examples
fix: correct typo in calculator.py
docs: update README with quickstart guide
```

#### Code Quality
The project uses automated tools to ensure code quality:
- **Black** - Code formatting
- **Ruff** - Linting
- **Bandit** - Security scanning

Run locally before submitting:
```bash
# Format code
black .

# Lint code
ruff check .

# Security scan
bandit -r .
```

### Need Help?

- 📖 [Contributing Guide](CONTRIBUTING.md) - Detailed guidelines
- 💬 [GitHub Discussions](https://github.com/hackdartstorm/Python/discussions) - Ask questions
- 🐛 [Report an Issue](https://github.com/hackdartstorm/Python/issues) - Bug reports & features
- 📧 [Contact Maintainers](mailto:learn@pythonmastery.dev) - Direct contact

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive Behavior:**
- ✅ Demonstrating empathy and kindness
- ✅ Being respectful of differing opinions
- ✅ Giving and accepting constructive feedback
- ✅ Accepting responsibility and apologizing

**Unacceptable Behavior:**
- ❌ Sexualized language or imagery
- ❌ Trolling, insulting, or derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to **conduct@pythonmastery.dev**. All complaints will be reviewed and investigated promptly and fairly.

**Full Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Python Learning Repository

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Python Community** - For creating and maintaining Python
- **All Contributors** - Making this project possible
- **Open Source** - For the amazing tools and libraries
- **You** - For learning Python and joining our community!

---

## 📞 Support

### Get Help

- 📖 [Documentation](README.md)
- 💬 [Discussions](https://github.com/hackdartstorm/Python/discussions)
- 🐛 [Issues](https://github.com/hackdartstorm/Python/issues)
- 📧 [Email](mailto:learn@pythonmastery.dev)

### Stay Connected

- ⭐ **Star this repo** to show support
- 🔔 **Watch** for updates
- 🍴 **Fork** to contribute
- 📢 **Share** with friends

---

<div align="center">

## 🎉 Ready to Start Your Python Journey?

### [Browse 700+ Issues](https://github.com/hackdartstorm/Python/issues) • [Start Contributing](#-contributing) • [Join Community](https://github.com/hackdartstorm/Python/discussions)

---

## 🤝 Contributing

We welcome contributions of all kinds! Here's how you can help:

### Ways to Contribute

- 🐛 **Fix bugs** - Find and fix issues in the codebase
- 📝 **Add examples** - Contribute new Python examples
- 🧪 **Write tests** - Add unit tests for existing code
- 📖 **Improve docs** - Enhance documentation and explanations
- 💡 **Suggest features** - Propose new learning modules
- 🔍 **Review code** - Review pull requests from others

### Quick Contribution Guide

1. **Fork** the repository
2. **Create** a branch (`git checkout -b feature/your-feature`)
3. **Make** your changes
4. **Test** your code
5. **Commit** (`git commit -m 'Add feature'`)
6. **Push** (`git push origin feature/your-feature`)
7. **Open** a Pull Request

📖 **See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.**

---

## 👥 Meet Our Contributors

A huge thank you to everyone who has contributed to making this project better!

### 🌟 All Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/hackdartstorm">
        <img src="https://avatars.githubusercontent.com/u/246549462?v=4" width="100px;" alt="hackdartstorm"/>
        <br />
        <sub><b>hackdartstorm</b></sub>
      </a>
      <br />
      <sub>Project Creator & Maintainer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/guerrevg">
        <img src="https://avatars.githubusercontent.com/u/262503087?v=4" width="100px;" alt="guerrevg"/>
        <br />
        <sub><b>guerrevg</b></sub>
      </a>
      <br />
      <sub>Contributor</sub>
    </td>
    <td align="center">
      <a href="https://github.com/aldomelpignano">
        <img src="https://avatars.githubusercontent.com/u/245438599?v=4" width="100px;" alt="aldomelpignano"/>
        <br />
        <sub><b>aldomelpignano</b></sub>
      </a>
      <br />
      <sub>Contributor</sub>
    </td>
    <td align="center">
      <a href="https://github.com/Rey-han-24">
        <img src="https://avatars.githubusercontent.com/u/193631115?v=4" width="100px;" alt="Rey-han-24"/>
        <br />
        <sub><b>Rey-han-24</b></sub>
      </a>
      <br />
      <sub>Contributor</sub>
    </td>
    <td align="center">
      <a href="https://github.com/Samprithajgowda">
        <img src="https://avatars.githubusercontent.com/u/193631116?v=4" width="100px;" alt="Samprithajgowda"/>
        <br />
        <sub><b>Samprithajgowda</b></sub>
      </a>
      <br />
      <sub>Contributor</sub>
    </td>
  </tr>
</table>


**Want to be here?** [Make your first contribution!](https://github.com/hackdartstorm/Python/issues?q=is%3Aopen+label%3A%22good+first+issue%22)

---

### Made with ❤️ by the Python Learning Community

**Happy Coding! 🐍✨**

</div>
