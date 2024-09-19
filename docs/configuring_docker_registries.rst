Configuring Docker Registries
###################################

In Tutor, you can configure docker registries by setting the variable ``DOCKER_REGISTRY`` in the ``config.yml`` file. This variable is used to specify the registry where the images will be pushed. By default, the images are pushed to the Docker Hub registry ``docker.io/``.

To allow further customization in the build process, Picasso Workflow also supports configuring multiple registries to push images. This can be done by:

1. Setting the ``DOCKER_REGISTRY`` variable in the ``config.yml`` file. If you're using Docker Hub, then you shouldn't have to set this variable, as the default value is already set to ``docker.io/``. However, if you're using a different registry, you should set the variable to the registry URL. For example, if you're using AWS ECR, you should set the variable to the ECR registry URL.
2. Setting the corresponding secrets in the Github Actions repository's secrets settings. If you're using Docker Hub, you should set the ``DOCKERHUB_USERNAME`` and ``DOCKERHUB_PASSWORD`` secrets. If you're using AWS ECR, you should set the ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, and ``AWS_REGION`` secrets.
3. Using the Picasso Workflow with the inputs and secrets set.

Here is an example of how to configure the Docker registries in the ``config.yml`` file:

.. code-block:: yaml

    DOCKER_REGISTRY: AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com

Here is an example of how to use the Picasso Workflow with the inputs and secrets set:

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
                AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
                AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                AWS_REGION: ${{ secrets.AWS_REGION }}
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}

.. warning::
    Since these files will contain sensitive data it is recommended to store the build configuration in a private repository.
