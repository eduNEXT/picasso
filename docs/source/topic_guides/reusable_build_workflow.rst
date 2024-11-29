Reusable Build Workflow (Picasso)
##################################

The Picasso Workflow is a `reusable GitHub Actions workflow`_ designed to build Open edX Docker images for Tutor environments. It simplifies the process of building custom Open edX images with additional functionality, making it easier to maintain, extend, and deploy environments using modern CI/CD practices.

Purpose
=======

Picasso is a tool designed to help teams simplify the build process for the Open edX Docker images, tailored explicitly for use in Tutor environments. It enables the addition of custom behaviors and features through the internal plugin `tutor-contrib-picasso`_, allowing for additional flexibility during the build process.

This GitHub Actions workflow replaces the existing `Jenkins-based pipeline`_ and integrates directly with other workflows, allowing it to be called in custom jobs. Picasso leverages Tutor to build images from the **Olive** version of Open edX onwards. The resulting Docker images can be used for both production and development environments, simplifying the process of managing multiple environments while ensuring consistency.

With Picasso, teams can build custom Open edX images with additional functionality, making it easier to maintain, extend, and deploy environments using modern CI/CD practices.

.. _`Jenkins-based pipeline`: https://github.com/eduNEXT/dedalo-scripts/blob/main/jenkins/picasso_v2
.. _reusable GitHub Actions workflow: https://docs.github.com/en/actions/sharing-automations/reusing-workflows

Workflow Overview
=================

The Picasso Workflow is designed to build Open edX Docker images for Tutor environments.

Key features of the Picasso Workflow include:

- **Runs on GitHub-hosted runners**: By default, the workflow uses GitHub hosted runners to execute jobs. This can't be changed to self-hosted runners for the time being.
- **Builds and pushes Docker images**: The workflow pushes images to Dockerhub by default. This can be customized to push images to other registries.
- **Supports multiple services**: You can specify the service to build (e.g., ``openedx``, ``mfe``, ``codejail``, etc.) using the ``SERVICE`` input.
- **Customizable repository and strain**: The workflow allows for specifying the repository, branch, and path to the strain being built. This enables building images from different configurations.
- **Configurable BuildKit parallelism**: By default, the workflow limits parallelism during the build process to optimize resource usage, although this can be changed using the ``ENABLE_LIMIT_BUILDKIT_PARALLELISM`` input. This is useful for low-powered machines, like `Github Actions standard runners`_.
- **Private repository access**: SSH keys are used to clone private repositories securely. The SSH private key should be stored as a secret in the repository, and must have access to the repository specified in ``STRAIN_REPOSITORY``.
- **Configures docker registry**: The workflow sets up the Docker registry to push images to Dockerhub or AWS ECR.
- **Extra commands**: The workflow allows running additional custom commands with ``tutor picasso run-extra-commands``. For details, refer to the `tutor-contrib-picasso`_ documentation.
- **Environment setup**: The workflow sets up installs necessary plugins like ``tutor-contrib-picasso``, and prepares the environment to build and push Docker images using the `Tutor CLI`_.

.. _tutor-contrib-picasso: https://github.com/eduNEXT/tutor-contrib-picasso/
.. _Github Actions standard runners: https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
.. _Tutor CLI: https://docs.tutor.edly.io/
