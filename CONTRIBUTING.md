# Contributing to UltraRF Protocol

First off, thank you for considering contributing to UltraRF! It's people like you that will make amateur radio digital communications faster and more reliable for emergency communications and experimentation.

## 🤝 Code of Conduct

This project adheres to the amateur radio spirit of experimentation, learning, and helping others. Please:
- Be respectful and considerate in all interactions
- Help newcomers learn and contribute
- Share knowledge freely
- Give credit where credit is due
- Follow amateur radio ethics and regulations

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, please include:

- **Description**: Clear and concise description of the bug
- **Steps to Reproduce**: List of steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **System Information**: 
  - OS and version
  - SDR hardware model
  - GNU Radio version
  - Python version
- **Logs**: Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use Case**: Explain why this enhancement would be useful
- **Proposed Solution**: Describe your proposed solution
- **Alternatives**: List any alternative solutions you've considered
- **Additional Context**: Add any other context or screenshots

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/GeorgeCottrell/UltraRF/ultrarf.git
   cd ultrarf-protocol
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Style

- **Python**: Follow PEP 8 (enforced by `black` and `flake8`)
- **C++**: Follow Google C++ Style Guide
- **GNU Radio**: Follow GNU Radio coding conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for all functions and classes

#### Testing

- Write unit tests for new functionality
- Ensure all tests pass: `pytest tests/`
- Add integration tests for protocol features
- Test with actual SDR hardware when possible
- Document test results in pull request

#### Pull Request Process

1. Update documentation for any API changes
2. Add tests for new functionality
3. Ensure CI/CD checks pass
4. Update CHANGELOG.md with your changes
5. Submit PR with clear description of changes
6. Be responsive to code review feedback

### Documentation Contributions

Good documentation is crucial for adoption. You can help by:

- Improving installation guides
- Writing tutorials and how-tos
- Creating diagrams and flowcharts
- Updating API documentation
- Translating documentation
- Fixing typos and clarifying confusing sections

### Hardware Contributions

- Test with different SDR platforms
- Design and test frequency converters
- Optimize antenna configurations
- Document hardware setups that work well
- Share PCB designs for custom hardware

### Testing and QA

- Field test the protocol in real conditions
- Report performance metrics
- Test edge cases and error conditions
- Participate in coordinated test events
- Document interference observations

## 📋 Development Priorities

Current high-priority areas needing contributions:

1. **LDPC Implementation**: Optimize error correction coding
2. **Channel Bonding**: Implement multi-channel aggregation
3. **Mesh Routing**: Port BATMAN to RF-aware metrics
4. **GNU Radio Blocks**: Create reusable signal processing blocks
5. **FPGA Acceleration**: Implement critical paths in FPGA
6. **Web Dashboard**: Create monitoring/configuration interface

## 🔧 Technical Guidelines

### Protocol Layers

When working on specific protocol layers:

#### Physical Layer
- Maintain spectral efficiency targets
- Ensure FCC bandwidth compliance
- Document modulation parameters
- Consider hardware limitations

#### MAC Layer
- Minimize overhead and latency
- Implement fair channel access
- Support QoS for emergency traffic
- Handle hidden node problem

#### Network Layer
- Optimize for dynamic RF links
- Implement self-healing capabilities
- Scale to 50+ nodes
- Minimize routing overhead

### Performance Considerations

- Target <10ms latency for time-critical operations
- Minimize CPU usage for embedded deployments
- Use SIMD instructions where available
- Profile code to identify bottlenecks

## 📝 Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Follow conventional commits format:
  ```
  type(scope): subject
  
  body
  
  footer
  ```
- Types: feat, fix, docs, style, refactor, test, chore
- Keep commits focused and atomic

## 🏆 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Project presentations at ham conventions
- Academic papers about the protocol
- Monthly community calls

## 🤔 Questions?

- Open a GitHub Discussion for general questions
- Join our Discord for real-time chat
- Email the core team for sensitive matters
- Check the FAQ in our wiki

## 🎯 First-Time Contributors

Looking for a good first issue? Check out issues labeled:
- `good first issue` - Simple tasks to get started
- `help wanted` - More complex tasks needing assistance
- `documentation` - Help improve our docs
- `testing` - Help test the protocol

## 📚 Resources for Contributors

- [GNU Radio Development](https://wiki.gnuradio.org/index.php/Development)
- [SDR with Python](https://pysdr.org/)
- [Digital Signal Processing](https://www.dspguide.com/)
- [Mesh Networking Basics](https://www.open-mesh.org/)
- [FCC Part 97 Rules](https://www.law.cornell.edu/cfr/text/47/part-97)

Thank you for helping make ultra high-speed amateur radio a reality!

The UltraRF Team