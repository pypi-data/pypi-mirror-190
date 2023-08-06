# Cerebrium

Cerebrium is the Python package built for use with the [Cerebrium](https://www.cerebrium.ai/) platform, which allows you to deploy your machine learning models as a REST API with a single line of code.

For usage consult the [documentation](https://docs.cerebrium.ai/). The repo for the documentation can be found [here](https://github.com/CerebriumAI/docs).

# Development environment
Cerebrium uses Poetry for dependency management and packaging. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Alternatively, consult our article on [how to manage your python environments](https://blog.cerebrium.ai/setting-up-your-data-science-and-ml-development-environment-949277339939?gi=54b980dd4e1d).

You can run the following steps to setup your Python development environment with the following commands:
```bash
poetry install
poetry shell
```
You should use this environment to run tests, notebooks and build the package.

Furthermore, you should set up a `.env` file in the project root with the following environment variables:
```bash
DEVELOPMENT_ENV=dev
```

## Running tests
To run the tests, run the following command:
```bash
poetry run pytest --cov-report html:cov_html\         (base) ─╯
          --cov-report annotate:cov_annotate\
          --cov=cerebrium tests/
```

## Publishing Development Builds
To publish a development build on CodeArtifact, run the following command to configure Poetry:
```bash
poetry config http-basic.cerebrium aws $(aws codeartifact get-authorization-token --domain-owner 288552132534 --domain cerebrium --query 'authorizationToken' --output text --region eu-west-1)
```

Then, run the following command to publish the package:
```bash
poetry publish --build -r cerebrium
```

## Install a development build
To install a development build, run the following command to configure pip:
```bash

aws codeartifact login --tool pip --repository cerebrium-pypi --domain cerebrium --domain-owner 288552132534 --region eu-west-1
```
Then, pip install:
```bash
pip install --pre cerebrium
```

### Resources for Poetry/CodeArtifact
- https://repost.aws/questions/QURD7aFNj_R9-8odJY5mfgrw/npm-publish-for-a-package-to-aws-code-artifact-repo-fails-with-error-the-provided-package-is-configured-to-block-new-version-publishes
- https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-pip.html