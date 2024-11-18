# Contributing to BioStat Academy

Thank you for your interest in contributing to BioStat Academy! This website aims to help biologists learn basic statistics, and we welcome your contributions to improve the content, user experience, and overall usefulness of the site.

Whether you're fixing a typo, improving an explanation, adding a new example, or suggesting new content, your help is valuable. Please follow these guidelines to make the process smooth and efficient for everyone.

## Table of Contents
- [Contributing to Biostat Academy] (#contributing-to-biostat-academy)
    - [Table of Contents] (#table-of-contents)
    - [Setting Up Your Development Environment] (#setting-up-your-development-environment)
        - [Required Python Packages] (#required-python-packages)
    - [Testing] (#testing)
    - [Pull Request Guidelines] (#pull-request-guidelines)
    - [Creating Pages] (#creating-pages)
    - [Thank You for Contributing!] (#thank-you-for-contributing!)

## How to Contribute
1. Report Issues

If you find an error or issue on the website, please open an issue in our GitHub Issues section. When reporting issues, please provide:

- A clear description of the problem
- The specific page or content where the issue occurs
- Any suggestions or ideas for improvement

 2. Suggest Content

If you have ideas for new topics, explanations, or examples, please let us know! We are particularly interested in:

- Additional statistics concepts that are important for biologists (e.g., hypothesis testing, regression models, p-values)
- Real-world biological examples to help illustrate statistical concepts (e.g., how to interpret ecological data, analyze genetic variation)
- Further interactive features (like quizzes or exercises) to reinforce learning

To suggest content, simply open an issue, or if you're comfortable, create a pull request with the proposed addition!

3. Improve Existing Content

If you notice areas where content could be clarified, expanded, or simplified, feel free to contribute. We're always looking to:

- Improve the clarity of explanations
- Add more examples or diagrams
- Correct any inaccuracies

You can either:

- Edit the Markdown files directly if you’re familiar with Git.
- Submit feedback or suggestions by opening an issue.

4. Fix Bugs or Errors

If you spot technical or content errors (broken links, typos, formatting issues), please feel free to fix them. Common things you can help with:

- Fixing broken links or incorrect references
- Correcting typos or grammatical errors
- Improving accessibility (e.g., adding alt text to images)

5. Contribute Code

If you’re familiar with web development and would like to improve the website’s functionality (e.g., adding interactive tools, improving layout), you’re welcome to contribute code. Here's how:

- Fork the repository and clone it to your local machine.
- Create a new branch for your changes.
- Make sure your changes are well-documented and tested.
- Submit a pull request with a detailed description of what you've done.

## Setting Up Your Development Environment

If you're contributing code, follow these steps to set up your local environment:

1. Fork the repository and clone your fork:
```
git clone https://github.com/hbrackney/StatsApp.git
```

2. Install environment and dependencies (see Required Python Packages below for a list off all required dependencies):
```
conda env create -f environment.yaml
```

### Required Python Packages
- Pylint
- Pytest
- Pycodestyle
- Flask
- Waitress
- Dash
- Pandas
- Scipy
- Statsmodels

## Testing

If you're contributing code or making changes to interactive content, please make sure everything works before submitting a pull request:

- Test locally to make sure your changes render correctly on the site.
- Check that the website is responsive and accessible (works well on different devices and browsers).
- Add or update any relevant tests for new features.

## Pull Request Guidelines

When submitting a pull request (PR), please follow these guidelines to help us review and merge your contribution more quickly:

- Provide a descriptive title for your pull request.
- Write a clear description of the changes you’ve made, including why you made them and what problem they solve.
- Link to any related issues using keywords like “Fixes #123” or “Closes #456” in the PR description.
- If you’ve added new content or features, be sure to:
    - Add examples, explanations, or screenshots as needed.

## Creating pages
Please follow the layout in example_page.html.

## Thank You for Contributing!

We appreciate all contributions, whether big or small. If you're unsure about something, feel free to reach out with questions! Let's make this resource as useful as possible for biologists learning statistics!