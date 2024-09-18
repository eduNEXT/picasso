Trigger a build with the GitHub CLI
####################################

To trigger a build with the GitHub CLI, you can do the following:

1. Install the GitHub CLI by following the instructions in the `GitHub CLI documentation`_.
2. Authenticate with GitHub by running the following command:

   .. code-block:: bash

      gh auth login
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
      -f "inputs[STRAIN_REPOSITORY_BRANCH]=<STRAIN_REPOSITORY_BRANCH>"

   Replace ``<ORGANIZATION_NAME>`` with the name of the organization, ``<WORKFLOW_REPO>`` with the name of the repository where the workflow is located, ``<WORKFLOW_ID>`` with the workflow ID copied in step 4, ``<BRANCH_NAME>`` with the branch name where the workflow is located, and ``<STRAIN_REPOSITORY_BRANCH>`` with the branch name where the strain repository is located. You can also add more inputs as needed.

.. _GitHub CLI documentation: https://cli.github.com/manual/
