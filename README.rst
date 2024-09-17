Picasso Workflow
################

Simplifies the build of Open edX Docker images for Tutor environments, providing a solution that integrates directly with GitHub Actions.

Purpose
*******

Picasso is a tool designed to help teams simplify the build process for the Open edX Docker images, tailored explicitly for use in Tutor environments. It enables the addition of custom behaviors and features through the internal plugin `tutor-contrib-picasso`_, allowing for additional flexibility during the build process.

This GitHub Actions workflow replaces the existing Jenkins-based pipeline and integrates directly with other workflows, allowing it to be called in custom jobs. Picasso leverages Tutor to build images from the Palm version of Open edX onwards. The resulting Docker images can be used for both production and development environments, simplifying the process of managing multiple environments while ensuring consistency.

With Picasso, teams can build custom Open edX images with additional functionality, making it easier to maintain, extend, and deploy environments using modern CI/CD practices.

Workflow Overview
*****************

The Picasso Workflow is designed to build Open edX Docker images for Tutor environments.

Key features of the Picasso Workflow include:

- **Runs on GitHub-hosted runners**: By default, the workflow uses ``ubuntu-latest`` runners to execute jobs. This can't be changed to self-hosted runners for the time being.
- **Builds and pushes Docker images**: The workflow pushes images to Dockerhub by default. This can be customized to push images to other registries.
- **Supports multiple services**: You can specify the service to build (e.g., ``openedx``, ``mfe``, ``codejail``, etc.) using the ``SERVICE`` input.
- **Customizable repository and strain**: The workflow allows for specifying the repository, branch, and path to the strain being built. This enables building images from different configurations.
- **Configurable BuildKit parallelism**: By default, the workflow limits parallelism during the build process to optimize resource usage, although this can be changed using the ``ENABLE_LIMIT_BUILDKIT_PARALLELISM`` input. This is useful for low-powered machines, like `Github Actions standard runners`_.
- **Private repository access**: SSH keys are used to clone private repositories securely. The SSH private key should be stored as a secret in the repository, and must have access to the repository specified in ``STRAIN_REPOSITORY``.
- **Extra commands**: The workflow allows running additional custom commands with ``tutor picasso run-extra-commands``. For details, refer to the `tutor-contrib-picasso`_ documentation.
- **Environment setup**: The workflow sets up and configures Tutor Virtual Environments (TVM), installs necessary plugins like ``tutor-contrib-picasso``, and prepares the environment to build and push Docker images using the `Tutor CLI`_.

.. _tutor-contrib-picasso: https://github.com/eduNEXT/tutor-contrib-picasso/
.. _Github Actions standard runners: https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
.. _Tutor CLI: https://docs.tutor.edly.io/

Configuration
*************

Before using the workflow, ensure that you have set up the following configurations in your GitHub repository:

.. list-table:: Picasso Workflow Configuration
   :header-rows: 1

   * - Variable
     - Description
     - Type
     - Source
   * - DOCKERHUB_USERNAME (Required)
     - DockerHub username to push images. This username should be stored as a secret in the repository.
     - string
     - Secret
   * - DOCKERHUB_PASSWORD (Required)
     - DockerHub password for login. This password should be generated from DockerHub and stored as a secret in the repository.
     - string
     - Secret
   * - SSH_PRIVATE_KEY (Required)
     - SSH private key for repository checkout. This key should have access to the repository specified in ``STRAIN_REPOSITORY``.
     - string
     - Secret
   * - STRAIN_REPOSITORY (Required)
     - The repository to clone the strain from, e.g., ``edunext/repository-name``. This repository should contain the files necessary to build the image within the specified path.
     - string
     - Input
   * - STRAIN_REPOSITORY_BRANCH (Required)
     - The branch to clone the strain from, e.g., main. This branch should contain the version of configuration ``config.yml`` file used to build the image.
     - string
     - Input
   * - STRAIN_PATH (Required)
     - The path to the strain within the repository structure, e.g., ``path/to/strain``. This path should contain the tutor configuration ``config.yml`` file used to build the image.
     - string
     - Input
   * - SERVICE (Required)
     - The service name to build, e.g., ``openedx``. This can be any service recognized by the tutor ecosystem.
     - string
     - Input
   * - ENABLE_LIMIT_BUILDKIT_PARALLELISM (Optional)
     - Enable enables limiting parallelism with buildkit to a max of 3 parallel build steps that can run at the same time to decrease resource consumption for those setups with low-powered machines. Default is ``true``.
     - boolean
     - Input

Usage
*****

To use the Picasso Workflow, follow these steps:

1. Ensure that your repository includes a workflow YAML file similar to the one below. This example demonstrates how to build an Open edX image using the Picasso workflow:

   .. code-block:: yaml

      name: Build Open edX Image
      on:
        workflow_dispatch:
          inputs:
            STRAIN_REPOSITORY:
              description: 'Repository to clone the configuration from'
              default: 'eduNEXT/build-manifests'
              type: string
            STRAIN_REPOSITORY_BRANCH:
              description: 'Branch to clone the configuration from'
              default: 'master'
              type: string
            STRAIN_PATH:
              description: 'Path to the configuration within the repository'
              default: 'redwood/base'
              type: string
            SERVICE:
              description: 'Service to build'
              default: 'openedx'
              type: choice
              options:
                - openedx
                - mfe
                - codejail
                - aspects
                - aspects-superset
                - ecommerce
                - discovery

      jobs:
        build:
          name: Build Open edX Image
          uses: eduNEXT/picasso/.github/workflows/build.yml@main
          with:
            STRAIN_REPOSITORY: ${{ inputs.STRAIN_REPOSITORY }}
            STRAIN_REPOSITORY_BRANCH: ${{ inputs.STRAIN_REPOSITORY_BRANCH }}
            STRAIN_PATH: ${{ inputs.STRAIN_PATH }}
            SERVICE: ${{ inputs.SERVICE }}
          secrets:
            DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
            DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
            SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}

2. Modify the ``STRAIN_REPOSITORY``, ``STRAIN_REPOSITORY_BRANCH``, ``STRAIN_PATH``, and ``SERVICE`` inputs to match your project requirements.

3. Trigger the workflow manually via the GitHub Actions tab, using the `workflow_dispatch` feature to input the necessary values. You can also set up a custom trigger for the workflow based on your project requirements.

This example allows building Open edX images with various services such as ``openedx``, ``mfe``, ``codejail``, and more, using the Picasso workflow. You can configure the repository, branch, and strain path for the build, as well as choose the specific service to build.

Getting Help
************

If you encounter any issues with the workflow or need further assistance, please refer to the following resources:

- `GitHub Actions documentation`_ for troubleshooting steps.
- You can also open an issue in the `Picasso Workflow repository`_.

.. _GitHub Actions documentation: https://docs.github.com/en/actions
.. _Picasso Workflow repository: https://github.com/edunext/picasso/issues

License
*******

The code in this repository is licensed under the MIT License unless otherwise noted. Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are welcome and strongly encouraged! Please, open an issue or submit a pull request to suggest changes or improvements to the workflow.

Reporting Security Issues
*************************

Please do not report security vulnerabilities in public forums. Instead, email technical@edunext.co.

.. |license-badge| image:: https://img.shields.io/github/license/edunext/picasso.svg
    :target: https://github.com/edunext/picasso/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: http://badges.github.io/stability-badges/dist/Status-Maintained-brightgreen.svg
