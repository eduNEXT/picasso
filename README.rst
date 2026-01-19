Picasso Workflow
################

Simplifies the build of Open edX Docker images for Tutor environments, providing a solution that integrates directly with GitHub Actions.

Purpose
*******

Picasso is a tool designed to help teams simplify the build process for the Open edX Docker images, tailored explicitly for use in Tutor environments. It enables the addition of custom behaviors and features through the internal plugin `tutor-contrib-picasso`_, allowing for additional flexibility during the build process.

This workflow integrates seamlessly with existing internal workflows, enabling it to be invoked in custom jobs. It leverages Tutor to build images starting from the **Olive** version, which can be deployed across both production and development environments. This ensures consistency in managing multiple environments while simplifying the overall process.

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
- **Environment setup**: The workflow sets up installs necessary plugins like ``tutor-contrib-picasso``, and prepares the environment to build and push Docker images using the `Tutor CLI`_.
- **Dynamic tag generation**: If this workflow configuration is enabled, a dynamic tag will be generated to build the image for the specified service. Additionally, it is possible to create a commit in the repository where the config.yml used to build the service is located, updating it with the new image tag.

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
   * - DOCKERHUB_USERNAME (Optional)
     - Docker Hub username to push images.
     - string
     - Secret
   * - DOCKERHUB_PASSWORD (Optional)
     - Docker Hub password for login.
     - string
     - Secret
   * - AWS_ACCESS_KEY_ID (Optional)
     - AWS access key ID for pushing images to ECR.
     - string
     - Secret
   * - AWS_SECRET_ACCESS_KEY (Optional)
     - AWS secret access key for pushing images to ECR.
     - string
     - Secret
   * - AWS_REGION (Optional)
     - AWS region for pushing images to ECR.
     - string
     - Secret
   * - SSH_PRIVATE_KEY (Required)
     - SSH private key for repository checkout. This key should have access to the repository specified in ``STRAIN_REPOSITORY``.
     - string
     - Secret
   * - STRAIN_REPOSITORY (Required)
     - The repository to clone the strain from, e.g., ``edunext/repository-name``.
     - string
     - Input
   * - STRAIN_REPOSITORY_BRANCH (Required)
     - The branch to clone the strain from, e.g., main. This branch should contain the version of configuration ``config.yml`` file used to build the image.
     - string
     - Input
   * - STRAIN_PATH (Required)
     - The path to the strain within the repository structure, e.g., ``path/to/strain``.
     - string
     - Input
   * - SERVICE (Required)
     - The service name to build, e.g., ``openedx``. This can be any service recognized by the tutor ecosystem.
     - string
     - Input
   * - BUILDKIT_MAX_PARALLELISM (Optional)
     - Configure the maximum parallelism for your builds. Default is ``0`` (no limit).
     - number
     - Input
   * - RUNNER_WORKFLOW_LABEL (Optional)
     - The label of the runner workflow to use. Default is ``ubuntu-24.04``.
     - string
     - Input
   * - PYTHON_VERSION (Optional)
     - The Python version to use in the workflow. Default is ``3.12``.
     - string
     - Input
   * - PICASSO_VERSION (Optional)
     - Picasso version to use for the workflow scripts and utility functions. This should be a valid branch, tag or commit and it should match the version of the workflow used. Default is the latest release major version, e.g., ``v1``.
     - string
     - Input
   * - USE_DYNAMIC_IMAGE_TAG (Optional)
     - If set to ``true``, the image tag defined in config.yml will be ignored, and a dynamically generated tag will be used instead. Default is ``false``
     - boolean
     - Input
   * - UPDATE_IMAGE_TAG_IN_REPO (Optional)
     - If this field is set to ``true``, a commit will be created with the updated image tag name in the config.yml file. Only used if ``USE_DYNAMIC_IMAGE_TAG`` is enabled. Default is ``false``
     - boolean
     - Input
   * - CLEAN_UP_DISK_SPACE (Optional)
     - If this field is set to ``true``, some non-essential pre-installed resources on the runner will be removed to free up disk space and avoid running out of resources during image builds. Default is ``true``. Recommended when using GitHub’s default hosted runners or any runner with limited resources.
     - boolean
     - Input
   * - ADD_RANDOM_SUFFIX_TO_IMAGE_TAG (Optional)
     - Appends a random four-character alphanumeric suffix to the image tag. Only used if ``USE_DYNAMIC_IMAGE_TAG`` is enabled. Default is ``false``
     - boolean
     - Input
   * - RANDOM_SUFFIX_LENGTH (Optional)
     - Specifies the number of random characters to append as a random suffix. Default is ``4``
     - string
     - Input
   * - IMAGE_TAG_PREFIX (Optional)
     - Prefix added to the dynamically generated image tag. Only used if ``USE_DYNAMIC_IMAGE_TAG`` is enabled. Default is ``empty``
     - string
     - Input
   * - TIMESTAMP_FORMAT (Optional)
     - Timestamp format used in the generated image tag. Follows Python’s ``strftime`` syntax. Only used if ``USE_DYNAMIC_IMAGE_TAG`` is enabled. Default is ``%Y%m%d-%H%M``
     - string
     - Input

Usage
*****

To use the Picasso Workflow, follow these steps:

1. Ensure your repository calls the Picasso workflow like the one below. This example demonstrates how to build an Open edX image using the Picasso workflow:

   .. code-block:: yaml

      jobs:
        build:
          name: Build Open edX Image
          uses: eduNEXT/picasso/.github/workflows/build.yml@main
          with:
            STRAIN_REPOSITORY: edunext/builds
            STRAIN_REPOSITORY_BRANCH: main
            STRAIN_PATH: redwood/base
            SERVICE: openedx
          secrets:
            DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
            DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
            SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}

2. Modify the ``STRAIN_REPOSITORY``, ``STRAIN_REPOSITORY_BRANCH``, ``STRAIN_PATH``, and ``SERVICE`` inputs to match your project requirements.

3. You can also set up a custom trigger for the workflow based on your project requirements.

..

    **Note**

    When attempting to build an MFE image it might be possible to exhaust the resources
    on the GitHub runner. You can specify a lower value of ``BUILDKIT_MAX_PARALLELISM``
    to reduce the amount of resources used, if that isn't enough you can use a
    different runner (e.g. a hosted `large runner`_) via the
    ``RUNNER_WORKFLOW_LABEL`` input.

.. _large runner: https://docs.github.com/en/actions/using-github-hosted-runners/using-larger-runners

Getting Help
************

If you encounter any issues with the workflow or need further assistance, please refer to the following resources:

- `GitHub Actions documentation`_ for troubleshooting steps.
- You can also open an issue in the `Picasso Workflow repository`_.
- For more information on the workflow, refer to the `documentation on Read the Docs`_.

.. _GitHub Actions documentation: https://docs.github.com/en/actions
.. _Picasso Workflow repository: https://github.com/edunext/picasso/issues
.. _documentation on Read the Docs: https://picasso.docs.edunext.co/en/latest/

Contributing
************

Contributions are welcome and strongly encouraged! Please, open an issue or submit a pull request to suggest changes or improvements to the workflow.

License
********

This project is licensed under the `AGPL-3.0 License`_. . Please note that no support or maintenance is guaranteed for public users. Any updates, bug fixes, or improvements will be made based on internal priorities, and contributions from the community may not receive immediate attention.

.. _AGPL-3.0 License: https://github.com/edunext/picasso/blob/main/LICENSE

Reporting Security Issues
*************************

Please do not report security vulnerabilities in public forums. Instead, email technical@edunext.co.

.. |license-badge| image:: https://img.shields.io/github/license/edunext/picasso.svg
    :target: https://github.com/edunext/picasso/blob/main/LICENSE
    :alt: License

.. |status-badge| image:: http://badges.github.io/stability-badges/dist/Status-Maintained-brightgreen.svg
