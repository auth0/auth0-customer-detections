# Contributing to Auth0 Security Detection Catalog

Thank you for your interest in contributing to the Auth0 Security Detection Catalog! 🛡️

We're proud to have you in our community. Your expertise in identifying and crafting detection rules helps protect Auth0 environments for everyone. Whether you're responding to emerging threats, improving existing detections, or sharing knowledge from real-world incidents, your contributions make a meaningful impact.

## Getting Started

### 1. Clone the Repository and Prepare for Development

First, fork the repository on GitHub, then clone your fork locally:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/auth0-customer-detections.git
cd auth0-customer-detections
```

### 2. Set Up Your Local Development Environment

We use Python for testing and validation. Here's how to set up your environment:

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

This installs:
- **PyYAML**: For parsing detection rule files
- **yamllint**: For YAML syntax validation
- **ruff**: For code formatting and linting
- **pytest**: For running tests
- **sigma-cli**: For testing detection rules

### 3. Keep Your Fork Updated

Before starting work, sync with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Creating a New Detection Rule

### Detection Rule Structure

Detection rules live in the `detections/` directory as YAML files. Each rule follows this structure:

```yaml
title: Clear, descriptive title of what the detection identifies
id: UUID
status: stable|test|experimental
description: >
    Detailed explanation of the security concern this detection addresses.
    Include context about when this might occur and why it's significant.
author: Your Name or Organization
date: YYYY-MM-DD
modified: YYYY-MM-DD
logsource:
    product: auth0
    service: relevant_auth0_service
detection:
    # Sigma detection rules go here
tenant_logs: |
    # Lucene syntax query for Auth0 event search API
    type: "event_type" AND field: "value"
explanation: |
    Human-readable explanation of what the query detects and why.
    Include guidance for analysts investigating alerts.
false_positives:
    - List potential legitimate scenarios that might trigger this detection
    - Help analysts understand when alerts might be benign
references:
    - https://relevant-documentation-or-advisory.com
level: low|medium|high|critical
tags:
    # ATT&CK classifications go here
    - attack.example
```

### Step-by-Step: Creating Your Detection

1. **Create a new YAML file** in the `detections/` directory:
   ```bash
   touch detections/your_detection_name.yml
   ```

2. **Choose a descriptive filename** using underscores (e.g., `suspicious_admin_role_changes.yml`)

3. **Write your detection rule** following the structure above. Look at existing files for examples:
   ```bash
   # Browse existing detections for reference
   ls detections/
   cat detections/attack_protection_features_turned_off.yml
   ```

4. **Focus on the detection logic**:
   - The `tenant_logs` field should contain a Lucene syntax query
   - Test your query in the Auth0 Dashboard first
   - Make it specific enough to avoid false positives
   - Include relevant event types and field conditions

## Testing Your Detection Rule

### Using Sigma CLI

The Sigma CLI helps validate your detection rules:

```bash
# Test a specific detection file
sigma check detections/your_detection_name.yml

# Validate all detection files
sigma check detections/*.yml

# Convert to different SIEM formats (optional)
sigma convert --target datadog detections/your_detection_name.yml
```

### Running the Test Suite

We have automated tests to ensure all detection rules are valid:

```bash
# Run all tests
pytest


# Run tests for a specific file
pytest test/test_yaml_should_be_valid.py -v
```

### What the Tests Check

Our test suite validates:

1. **YAML Syntax**: Ensures all detection files are valid YAML
2. **Required Fields**: Verifies that mandatory fields are present
3. **Field Format**: Checks that dates, threat mappings, and other fields follow the expected format
4. **File Naming**: Ensures detection files follow naming conventions

If tests fail, they'll provide specific error messages to help you fix issues.

### Manual Testing

Before submitting, manually verify your detection:

1. **Test the query** in your Auth0 Dashboard logs section
2. **Review for false positives** by considering legitimate use cases
3. **Validate MITRE ATT&CK mappings** using the [MITRE ATT&CK website](https://attack.mitre.org/)
4. **Check references** to ensure links are accessible and relevant

## Quality Guidelines

### Writing Effective Detections

- **Be specific**: Target actual malicious behavior, not just configuration changes
- **Consider context**: Include relevant fields that help with investigation
- **Think like an analyst**: Your detection will generate alerts that someone needs to investigate
- **Document thoroughly**: Clear descriptions help analysts understand the threat

### Common Pitfalls to Avoid

- **Overly broad queries** that generate excessive false positives
- **Missing edge cases** in legitimate administrative activities
- **Incomplete threat attribution** or incorrect MITRE mappings
- **Unclear descriptions** that don't help analysts understand the alert

## Submitting Your Contribution

### Creating a Pull Request

1. **Create a feature branch**:
   ```bash
   git checkout -b add-detection-suspicious-behavior
   ```

2. **Add and commit your changes**:
   ```bash
   git add detections/your_detection_name.yml
   git commit -m "Add detection for suspicious admin behavior
   
   - Detects unusual patterns in administrative actions
   - Covers MITRE T1078.004 - Valid Accounts: Cloud Accounts
   - Includes guidance for analyst investigation"
   ```

3. **Push to your fork**:
   ```bash
   git push origin add-detection-suspicious-behavior
   ```

4. **Create a Pull Request** on GitHub:
   - Navigate to your fork on GitHub
   - Click "New Pull Request"
   - Provide a clear title and description
   - Reference any related issues or security advisories

### Review Process

Our team will review your contribution for:
- Technical accuracy of the detection logic
- Completeness of documentation
- Alignment with the catalog's quality standards
- Potential impact on security monitoring

We may suggest improvements or ask questions to better understand your detection. This collaborative process helps ensure high-quality additions to the catalog.

## Getting Help

- **Questions about detection logic**: Open an issue with the `question` label
- **Technical issues**: Check existing issues or create a new one
- **Security concerns**: Follow [Auth0's Responsible Disclosure Program](https://auth0.com/docs/troubleshoot/customer-support/responsible-disclosure-program-security-support-tickets)

## Recognition

Contributors are recognized in our release notes and may be mentioned in related security blog posts. Your expertise helps the entire Auth0 security community!
