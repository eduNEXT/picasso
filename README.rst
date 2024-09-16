Picasso Workflow
################

Streamlines the build of Open edX Docker images for Tutor environments, providing a flexible and scalable solution that integrates directly with GitHub Actions.

Purpose
*******

Picasso is a tool designed to help teams streamline the build process for both Open edX platform and Micro-Frontends (MFEs) Docker images, specifically tailored for use in Tutor environments. It enables the addition of custom behaviors and features through the internal plugin `tutor-contrib-picasso`, allowing for enhanced flexibility during the build process.

This GitHub Actions workflow replaces the existing Jenkins-based pipeline and integrates directly with other workflows, allowing it to be invoked in custom jobs. Picasso leverages Tutor technology to build images from the Palm version of Open edX onwards, enabling configuration-driven builds using a configuration file. The resulting Docker images can be used for both production and development environments, simplifying the process of managing multiple environments while ensuring consistency.

With Picasso, teams can create custom Open edX and MFE images with additional functionality, making it easier to maintain, extend, and deploy environments using modern CI/CD practices.

Configuration
*************

Before using the workflow, ensure that you have set up the following configurations in your GitHub repository:

.. list-table:: Picasso Workflow Configuration
   :header-rows: 1

   * - Name
     - Description
     - Type
     - Default
     - Source
   * - DOCKERHUB_USERNAME
     - DockerHub username to push images. This username should be stored as a secret in the repository.
     - string
     - None
     - Secret
   * - DOCKERHUB_PASSWORD
     - DockerHub password for login. This password should be generated from DockerHub and stored as a secret in the repository.
     - string
     - None
     - Secret
   * - SSH_PRIVATE_KEY
     - SSH private key for repository checkout. This key should have access to the repository specified in `STRAIN_REPOSITORY`.
     - string
     - None
     - Secret
   * - STRAIN_REPOSITORY
     - The repository to clone the strain from, e.g., edunext/repository-name. This repository should contain the files necessary to build the image within the specified path.
     - string
     - None
     - Environment Variable
   * - STRAIN_REPOSITORY_BRANCH
     - The branch to clone the strain from, e.g., main. This branch should contain the version of configuration `config.yml` file used to build the image.
     - string
     - main
     - Environment Variable
   * - STRAIN_PATH
     - The path to the strain within the repository structure, e.g., path/to/strain. This path should contain the tutor configuration `config.yml` file used to build the image.
     - string
     - None
     - Environment Variable
   * - SERVICE
     - The service name to build, e.g., openedx.
     - string
     - None
     - Environment Variable

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
          name: Build with Picasso
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

2. Modify the `STRAIN_REPOSITORY`, `STRAIN_REPOSITORY_BRANCH`, `STRAIN_PATH`, and `SERVICE` inputs to match your project requirements.

3. Trigger the workflow manually via the GitHub Actions tab, using the `workflow_dispatch` feature to input the necessary values. You can also set up a custom trigger for the workflow based on your project requirements.

This example allows building Open edX images with various services such as `openedx`, `mfe`, `codejail`, and more, using the Picasso workflow. You can configure the repository, branch, and strain path for the build, as well as choose the specific service to build.


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

Contributions are welcome. Please review the `How to Contribute`_ guide for more information.

.. _How to Contribute: https://openedx.org/r/how-to-contribute

All contributors are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

Reporting Security Issues
*************************

Please do not report security vulnerabilities in public forums. Instead, email technical@edunext.co.

.. |license-badge| image:: https://img.shields.io/github/license/edunext/picasso.svg
    :target: https://github.com/edunext/picasso/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: http://badges.github.io/stability-badges/dist/experimental.svg
