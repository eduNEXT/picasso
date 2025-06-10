How to Configure Dynamic Tag Generation in Picasso
===================================================

Sometimes, due to the nature of Docker image generation, it's necessary to configure image tags dynamically. This avoids the need to update the strain every time a new image is built. These tags follow a pattern previously defined by the Picasso development team. Additionally, the feature includes the ability to generate a commit and update the `config.yml` file of the repository where the Docker image was built.

Configurable Pattern for Dynamic Tag Generation
-----------------------------------------------

It is important to note that this implementation **only** generates the **tag** of the Docker image dynamically. The rest of the image name is retrieved from the previously established configuration. Further below, we explain how to properly configure it to use this feature.

The pattern used for generating dynamic tags is illustrated below:

::

    {tutor_version}-{image_tag_prefix}{timestamp}-{random_suffix}

- ``tutor_version``: The version of Tutor used to build the image.
- ``image_tag_prefix (optional)``: A static prefix that can be added to the image tag (string type).
- ``timestamp``: The date and time when the image was built.
- ``random_suffix (optional)``: A 4-character alphanumeric string generated randomly.

Configuring Dynamic Tag Generation
----------------------------------

To configure this implementation, you need to set up Picasso in your desired repository. You can follow the steps described in the article :ref:`reuse-workflow`.

To enable dynamic tag generation, pass the setting ``USE_DYNAMIC_IMAGE_TAG: true`` to the Picasso job. This automatically enables tag overwriting and builds the image using the newly generated tag.

By default, when this setting is enabled, the generated tag will look like:

::

    v19.0.3-20250606-1012

This tag is composed using the following parameters:

::

    {tutor_version}-{timestamp}

The timestamp follows the format ``"%Y%m%d-%H%M"``.

Additional Parameters
---------------------

You can further customize the tag by using additional input parameters:

- ``IMAGE_TAG_PREFIX``: Allows you to define a custom string to appear before the timestamp.
- ``TIMESTAMP_FORMAT``: Allows you to define the timestamp format. This must be a valid format supported by Python's ``strftime`` function.
- ``ADD_RANDOM_SUFFIX_TO_IMAGE_TAG``: When set to ``true``, a random 4-character alphanumeric string will be appended to the tag.
- ``RANDOM_SUFFIX_LENGTH``: Specifies the number of random characters to append as a random suffix

Committing Updated Tags to the Repository
-----------------------------------------

An additional feature allows the newly generated tag to be committed and pushed back to the repository where the strain resides. This was designed specifically for Cirrus Hosting, to maintain clear control of the tags associated with each image.

To enable this behavior:

- The job executing the Picasso workflow **must have** `contents: write` permissions.
- The input ``UPDATE_IMAGE_TAG_IN_REPO`` **must be set to** `true`.
- This will only work **if** ``USE_DYNAMIC_IMAGE_TAG`` is also enabled.

Considerations
--------------

- It is important that the image for the service to be built has been previously defined, as this implementation relies on the existing information—such as the Docker registry, repository, and organization—from the image already configured in the strain. Including a tag is not required, but if one is present, it will not cause any errors.
- Ensure the ``PICASSO_VERSION`` parameter is set to a version of Picasso that includes these changes for the feature to function properly.

Example Configuration
---------------------

.. code-block:: yaml

    jobs:
      build:
        permissions:
          contents: write
        name: Build with Picasso
        uses: eduNEXT/picasso/.github/workflows/build.yml@dmh/create-image-tag
        with:
          BUILDKIT_MAX_PARALLELISM: ${{ fromJSON(inputs.BUILDKIT_MAX_PARALLELISM) }}
          STRAIN_REPOSITORY: ${{ github.repository }}
          STRAIN_REPOSITORY_BRANCH: ${{ inputs.STRAIN_REPOSITORY_BRANCH }}
          STRAIN_PATH: 'build'
          SERVICE: ${{ inputs.SERVICE }}
          USE_DYNAMIC_IMAGE_TAG: true
          UPDATE_IMAGE_TAG_IN_REPO: true
          ADD_RANDOM_SUFFIX_TO_IMAGE_TAG: true
          RANDOM_SUFFIX_LENGTH: "8"
          TIMESTAMP_FORMAT: "%Y%m%d"
          IMAGE_TAG_PREFIX: "picasso-"
          PICASSO_VERSION: dmh/create-image-tag
        secrets:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.AWS_REGION }}
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
