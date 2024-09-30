Reusing the Picasso Workflow
###################################

This document will guide you through different ways of reusing the Picasso workflow in your own repository.

To use a reusable workflow from your own repository, you can use the ``uses`` keyword in your workflow file. The ``uses`` keyword specifies the location of the reusable workflow file, which can be a specific tag, branch, or commit, either in the same repository or a different repository.

The (caller) workflow can access the reusable workflow file (callee) without restriction if the callee is public. If the callee is in a private repository, then the caller must belong to the same organization as the callee.

For more information, see `Reusing workflows`_.

.. _`Reusing workflows`: https://docs.github.com/en/actions/sharing-automations/reusing-workflows

Workflow Dispatch Event
=======================

Here is an example of how to use the Picasso workflow using the `workflow_dispatch`_ event:

.. code-block:: yaml

    name: Build Open edX Image
    run-name: Build image for service '${{ inputs.SERVICE }}' from repository '${{ inputs.STRAIN_REPOSITORY }}' on branch '${{ inputs.STRAIN_REPOSITORY_BRANCH }}'
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

In this example, you can trigger the workflow manually via the GitHub Actions tab, using the ``workflow_dispatch`` feature to input the necessary values. Based on the provided inputs, the workflow will then build the Open edX image.

Push Event
==========

Here's an example of how to use the Picasso workflow using the `push`_ event:

.. code-block:: yaml

    name: Build Open edX Image
    run-name: Build image for service '${{ inputs.SERVICE }}' from repository '${{ inputs.STRAIN_REPOSITORY }}' on branch '${{ inputs.STRAIN_REPOSITORY_BRANCH }}'
    on:
        push:
            branches:
                - master
                - main
            paths:
                - 'redwood/base/**'

    jobs:
        build:
            name: Build Open edX Image
            uses: eduNEXT/picasso/.github/workflows/build.yml@main
            with:
                STRAIN_REPOSITORY: eduNEXT/build-manifests
                STRAIN_REPOSITORY_BRANCH: master
                STRAIN_PATH: redwood/base
                SERVICE: openedx
            secrets:
                DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
                DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}


In this example, the workflow will be triggered automatically when a push event occurs on the ``master`` or ``main`` branch, affecting the path ``redwood/base/**``. Based on the provided inputs, the workflow will then build the Open edX image.

For more details on the available events, see `Events that trigger workflows`_.

.. note:: To better identify the workflow run, you can set the ``run-name`` attribute in the workflow file. This attribute will be displayed in the GitHub Actions tab.

.. _`Events that trigger workflows`: https://docs.github.com/en/actions/reference/events-that-trigger-workflows
.. _`workflow_dispatch`: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#workflow_dispatch
.. _`push`: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#push
