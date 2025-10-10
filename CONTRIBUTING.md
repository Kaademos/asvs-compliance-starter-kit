# Contributing to the ASVS 5.0 Starter Kit

First off, thank you for considering contributing! This project thrives on community involvement, and every contribution helps make our applications more secure. Whether you're correcting a typo, improving a template, or adding a new secure coding pattern, your input is valuable.

This document provides guidelines for contributing to this repository.

## How Can I Contribute?


- **Reporting bugs:** Find something wrong with a script, a template, or a document? Open an issue via the issue chooser and select the **Bug report** template.

- **Suggesting enhancements:** Have an idea for a new template, a better secure coding pattern, or an improvement to the repository structure? Open an issue via the issue chooser and select the **Feature request** template.

-   **Pull Requests:** If you're ready to contribute code or documentation, we welcome your pull requests.

## Your First Contribution

Unsure where to begin? A great place to start is by looking for issues tagged with `good first issue` or `help wanted`. These are typically well-defined tasks that are a great introduction to the project.

You can also contribute by:

-   Improving the documentation in any of the `.md` files.

-   Adding a secure coding example for a language you're familiar with.

-   Adding a new verification test for a specific ASVS requirement.

## Pull Request Process

1.  **Fork the repository:** Create your own copy of the project to work on.

2.  **Create a new branch:** Make a branch from `main` for your changes. Please use a descriptive name (e.g., `feat/add-python-csrf-pattern` or `fix/typo-in-readme`).

3.  **Make your changes:** Make your changes locally, adhering to the style guides below.

4.  **Commit your changes:** Use clear and descriptive commit messages. We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/ "null") specification. For example:

    -   `feat: Add new decision template for V5 File Handling`

    -   `docs: Clarify instructions in the main README.md`

    -   `fix: Corrected field name in V8 Authorization template`

    -   `ci: Add markdown linting GitHub Action`

5.  **Push to your branch:** Push your changes to your forked repository.

6.  **Open a Pull Request:** Submit a pull request to the main repository. Please fill out the pull request template with a clear description of your changes. The project maintainers will review your PR, provide feedback, and merge it when it's ready.

## Issue and PR templates

This repository provides issue and pull request templates to help structure reports and contributions. When opening an issue or PR, please use the appropriate template (Bug report, Feature request, or Pull request).

## Style Guides

-   **Markdown:** Use clear, concise language. Use Prettier-compatible formatting for consistency. Our CI pipeline will check this automatically.

-   **JSON:** Ensure any JSON files are well-formatted and valid. Our CI pipeline will also check this.

-   **Code (Scripts, Tests):** Follow standard conventions for the language you are writing in. Add comments to explain complex logic.

Thank you again for your interest in making this framework better!