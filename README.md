# Welcome to Treebeard 🌲

[![PyPI version](https://badge.fury.io/py/treebeard.svg)](https://badge.fury.io/py/treebeard)
[![Docs](https://readthedocs.org/projects/treebeard/badge/?version=latest)](https://treebeard.readthedocs.io/)
![Test Examples](https://github.com/treebeardtech/treebeard/workflows/Test%20Examples/badge.svg)
![End to End Test](https://github.com/treebeardtech/treebeard/workflows/End%20to%20End%20Test/badge.svg)

Treebeard is a library which reproduces Python data science work in the cloud, natively supporting Jupyter Notebooks.

Treebeard allows you to do the following without bash scripts:

- Schedule notebooks in the cloud, working with all types of dependencies
- Setup continuous integration for your Github repo, to test notebooks on each push
- Fetch outputs from each cloud run using versioned URLs

The goal is to allow data scientists to set up continuous integration with minimal changes to their project.

Read the [docs](https://treebeard.readthedocs.io/en/latest/) to get started.

![admin view](https://storage.googleapis.com/treebeard_image_dump_public/admin_view.png "Admin view")

## Integration with Managed Services

We want this library to be useful with existing services so it hooks into our minimal backend which runs the notebooks and talks to Slack and Github free of charge.

Our runtime provides 24 hours of free usage per month for open source projects.

Our docs describe how to check your repository for errors and produce notebook outputs when you push.

![Github Check](https://storage.googleapis.com/treebeard_image_dump_public/github_check.png "Github Check")

Slack users can choose to be notified upon completion.

![Slack Notification](https://storage.googleapis.com/treebeard_image_dump_public/slack_notif.png "Slack Notification")

## More Information

- Our [docs](https://treebeard.readthedocs.io/en/latest/)
- Our [website](https://treebeard.io)

## License

Treebeard is free and open source and licensed under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license.

Note that by default Treebeard has some integrations with backend services and a webpage which we are working on open sourcing.
