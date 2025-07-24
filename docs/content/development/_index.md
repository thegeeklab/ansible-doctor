---
title: Development
---

## Template Generation and Testing

To generate documentation using an existing template:

```bash
# Test with example roles
ansible-doctor example/demo-role
ansible-doctor example/other-role

# Set a custom template
ANSIBLE_DOCTOR_TEMPLATE__NAME=readme ansible-doctor example/demo-role
```

## Testing

### Linting and Code Quality

```bash
# Run ruff linter
poetry run ruff check

# Fix auto-fixable linting issues
poetry run ruff check --fix

# Run ruff formatter
poetry run ruff format

# Check Jinja2 template syntax
poetry run j2lint ansibledoctor/templates/**/*.j2 -i jinja-statements-indentation jinja-statements-delimiter
```
