"""
auth0-customer-detections test suite

Author: Mathew Woodyard

Copyright (C) 2025 Okta, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pathlib import Path
import pytest
import yaml
import yamllint.config
import yamllint.linter


class TestYamlValidation:
    @pytest.fixture
    def yaml_files(self):
        path = Path(__file__).parent.parent / "detections"
        yaml_files = list(path.glob("*.yml")) + list(path.glob("*.yaml"))

        return yaml_files

    @pytest.fixture
    def yamllint_config(self):
        yamllint_config = yamllint.config.YamlLintConfig(file=".yamllint")

        return yamllint_config

    def test_yaml_files_should_have_content(self, yaml_files):
        empty_files = []
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        empty_files.append(yaml_file)
            except Exception as e:
                pytest.fail(f"Error reading {yaml_file}: {e}")

        if empty_files:
            pytest.fail(f"The following YAML files are empty: {', '.join(empty_files)}")

    def test_yaml_syntax_should_be_valid(self, yaml_files):
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"YAML syntax error in {yaml_file}: {e}")
            except Exception as e:
                pytest.fail(f"Error reading {yaml_file}: {e}")

    def test_yamllint_should_be_valid(self, yaml_files, yamllint_config):
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    content = f.read()

                problems = list(
                    yamllint.linter.run(content, yamllint_config, yaml_file)
                )

                if problems:
                    error_messages = []
                    for problem in problems:
                        error_messages.append(
                            f"Line {problem.line}, Column {problem.column}: "
                            f"{problem.level} - {problem.message} ({problem.rule})"
                        )

                    pytest.fail(
                        f"yamllint validation failed for {yaml_file}:\n"
                        + "\n".join(error_messages)
                    )

            except Exception as e:
                pytest.fail(f"Error during yamllint validation of {yaml_file}: {e}")
