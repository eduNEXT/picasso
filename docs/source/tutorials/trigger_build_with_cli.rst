Trigger a build with the GitHub CLI
####################################

Consider you're using the Picasso Workflow like in the following snippet to build Open edX images:

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

.. note::
    For more information on how to use the Picasso Workflow, please refer to the `Reusing the Picasso Workflow <reuse_workflow.rst>`_.

With this workflow you can trigger a build manually via the GitHub Actions tab, using the ``workflow_dispatch`` feature to input the necessary values. However, you can also trigger the workflow using the GitHub CLI.

To trigger a build with the GitHub CLI with this workflow setup, you can do the following:

1. Install the GitHub CLI by following the instructions in the `GitHub CLI documentation`_.
2. Authenticate with GitHub by running the following command:

   .. code-block:: bash

      gh auth login

   To trigger a build the user logged in with the GitHub CLI must have the necessary permissions to trigger the workflow.

3. Get the workflow ID by running the following command:

   .. code-block:: bash

      gh api \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      /repos/<ORGANIZATION_NAME>/<WORKFLOW_REPO>/actions/workflows


   Replace ``<ORGANIZATION_NAME>`` with the name of the organization and ``<WORKFLOW_REPO>`` with the name of the repository where the workflow is located.
4. Copy the workflow ID from the output.
5. Trigger the workflow by running the following command:

   .. code-block:: bash

      gh api \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -X POST \
      /repos/<ORGANIZATION_NAME>/<WORKFLOW_REPO>/actions/workflows/<WORKFLOW_ID>/dispatches \
      -f ref=<BRANCH_NAME> \
      -f "inputs[STRAIN_REPOSITORY]=<STRAIN_REPOSITORY>"
      -f "inputs[STRAIN_REPOSITORY_BRANCH]=<STRAIN_REPOSITORY_BRANCH>"
      -f "inputs[STRAIN_PATH]=<STRAIN_PATH>"
      -f "inputs[SERVICE]=<SERVICE>"

   Replace each configuration value with the corresponding value for your project. For more information on the configuration values available for the workflow, please refer to the `Picasso Workflow Configuration <configurations.rst>`_. Since the workflow specifies defaults for the inputs, you can omit them if you want to use them instead.

This example demonstrate how to trigger a build using the gh cli and the GitHub API, but you can also exclusively use the GitHub CLI to trigger the workflow using the ``gh workflow run`` command. For more information on how to trigger workflows with the GitHub CLI, please refer to the `GitHub CLI documentation`_.

.. _GitHub CLI documentation: https://cli.github.com/manual/
.. _GitHub Actions permissions: https://docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions
