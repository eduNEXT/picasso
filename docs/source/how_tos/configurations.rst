Picasso Workflow Configurations
###################################

Picasso is a `Github Workflow`_ implemented to be flexible enough to be adopted by different organizations with their own requirements. This document will guide you through the different configurations available to you.

.. _`Github Workflow`: https://docs.github.com/en/actions/sharing-automations/reusing-workflows

Inputs
======

Inputs are the parameters that you can set to customize the behavior of the Picasso workflow. The following inputs are available:

* ``STRAIN_REPOSITORY (required)``: The URL of the repository that contains the strain configuration. This repository should contain a valid ``config.yml`` file that defines the strains that will be built.
* ``STRAIN_REPOSITORY_BRANCH (required)``: The branch of the ``STRAIN_REPOSITORY`` to clone the strain configuration from. This branch should contain the version of the configuration file used to build the image.
* ``STRAIN_PATH (required)``: The path to the directory that contains the strain configuration file. This path should be relative to the root of the repository.
* ``SERVICE (required)``: The name of the service that will be built. This service should be supported by Tutor or by a tutor plugin previously installed.
* ``ENABLE_LIMIT_BUILDKIT_PARALLELISM (optional)``: If set to ``true``, the build process parallel steps will be limited by 3, which is the threshold found where both Open edX and MFE images are built without running out of resources in the Github Actions runner (please, see `PR #12`_ for more details) . If set to ``false``, the buildkit configuration default will be used. Default is ``true``. Set to ``false`` if you have a runner with more resources.

These inputs can be set in the workflow file that calls the Picasso workflow using the ``with`` keyword, by manually setting them in the workflow file, or by using the ``workflow_dispatch`` event. For more details on how to set input values in Github Actions, please refer to the `Workflow syntax for GitHub Actions`_ documentation.

.. _`Workflow syntax for GitHub Actions`: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions

Here is an example of how to use the Picasso workflow with the inputs set:

.. code-block:: yaml

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: redwood/base
                SERVICE: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false

.. _`PR #12`: https://github.com/eduNEXT/picasso/pull/12

Secrets
=======

Secrets are the sensitive data that you can set to customize the behavior of the Picasso workflow. The following secrets are available:

* ``SSH_PRIVATE_KEY (required)``: The private SSH key that will be used to clone private repositories, including the ``STRAIN_REPOSITORY`` and all private requirements for the Open edX images. Therefore, this key should have read access to all the repositories that are required to build the images.
* ``DOCKERHUB_USERNAME (optional)``: The username of the Docker Hub account where the images will be pushed. By default, the images are pushed to a ``docker.io`` registry using this username.
* ``DOCKERHUB_PASSWORD (optional)``: The password of the Docker Hub account where the images will be pushed. This password is used to authenticate the Docker client when pushing the images.
* ``AWS_ACCESS_KEY_ID (optional)``: The access key ID of the AWS account where the images will be pushed. This key is used to authenticate the AWS client when pushing the images to the ECR registry.
* ``AWS_SECRET_ACCESS_KEY (optional)``: The secret access key of the AWS account where the images will be pushed. This key is used to authenticate the AWS client when pushing the images to the ECR registry.
* ``AWS_REGION (optional)``: The region of the AWS account where the images will be pushed. This region is used to determine the ECR registry URL where the images will be pushed.

These variables are mainly used to authenticate with some services like Docker Hub, AWS or GitHub. They should be set in the Github Actions repository's secrets settings. For more information on how to set secrets in Github, please refer to the `Using secrets in GitHub Actions`_ documentation.

To correctly use Docker Hub or AWS registries to push images, you should set the corresponding configuration in your ``config.yml`` file. For more information on how to configure the Docker Hub or AWS registries in the ``config.yml`` file, please refer to the `Configuring Docker Registries <configuring_docker_registries>`_ documentation.

.. _`Using secrets in GitHub Actions`: https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions

Here is an example of how to use the Picasso workflow with the inputs and secrets set:

.. code-block:: yaml

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: redwood/base
                SERVICE: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false
            secrets:
                DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
                DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}

Or using an AWS registry:

.. code-block:: yaml

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: redwood/base
                SERVICE: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false
            secrets:
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
                AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
                AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                AWS_REGION: ${{ secrets.AWS_REGION }}
