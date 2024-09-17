Picasso Workflow Configurations
###################################

Picasso is a `Github Workflow`_ implemented to be flexible enough to be adopted by different organizations with their own requirements. This document will guide you through the different configurations available to you.

.. _`Github Workflow`: https://docs.github.com/en/actions/sharing-automations/reusing-workflows

Contents
********

- `Inputs <general_configuration.rst>`_
- `Secrets <secrets_configuration.rst>`_

Inputs
======

Inputs are the parameters that you can set to customize the behavior of the Picasso workflow. The following inputs are available:

* ``STRAIN_REPOSITORY (required)``: The URL of the repository that contains the strain configuration. This repository should contain a valid ``config.yml`` file that defines the strains that will be built.

.. code-block:: yaml
   :emphasize-lines: 6

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests

* ``STRAIN_REPOSITORY_BRANCH (required)``: The branch of the ``STRAIN_REPOSITORY`` that will be used to build the strains.

.. code-block:: yaml
   :emphasize-lines: 7

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/ironwood

* ``STRAIN_PATH (required)``: The path to the directory that contains the strain configuration file. This path should be relative to the root of the repository.

.. code-block:: yaml
   :emphasize-lines: 8

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: redwood/base

* ``SERVICE (required)``: The name of the service that will be built. This service should be supported by Tutor or by a tutor plugin previously installed.

.. code-block:: yaml
   :emphasize-lines: 9

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: mfe

* ``ENABLE_LIMIT_BUILDKIT_PARALLELISM``: If set to ``true``, the build process parallel steps will be limited by 3, which is the threshold found where both Open edX and MFE images are built without running out of resources in the Github Actions runner (please, see `PR #12`_ for more details) . If set to ``false``, the parallelism will the buildkit default. Default is ``true``. Set to ``false`` if you have a runner with more resources.

.. code-block:: yaml
   :emphasize-lines: 10

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false

.. _`PR #12`: https://github.com/eduNEXT/picasso/pull/12

Secrets
=======

Secrets are the sensitive data that you can set to customize the behavior of the Picasso workflow. The following secrets are available:

* ``DOCKERHUB_USERNAME (required)``: The username of the Docker Hub account where the images will be pushed. By default, the images are pushed to a ``docker.io`` registry using this username.

.. code-block:: yaml
   :emphasize-lines: 11

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false
            secrets:
                DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}

* ``DOCKERHUB_PASSWORD (required)``: The password of the Docker Hub account where the images will be pushed. This password is used to authenticate the Docker client when pushing the images.

.. code-block:: yaml
   :emphasize-lines: 12

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false
            secrets:
                DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
                DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}

* ``SSH_PRIVATE_KEY (required)``: The private SSH key that will be used to clone private repositories, including the ``STRAIN_REPOSITORY`` and all private requirements for the Open edX images. Therefore, this key should have read access to all the repositories that are required to build the images.

.. code-block:: yaml
   :emphasize-lines: 13

    jobs:
        build:
            name: Build with Picasso
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: edunext/build-manifests
                STRAIN_REPOSITORY_BRANCH: dev/test-latest-image
                STRAIN_PATH: mfe
                ENABLE_LIMIT_BUILDKIT_PARALLELISM: false
            secrets:
                DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
                DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
