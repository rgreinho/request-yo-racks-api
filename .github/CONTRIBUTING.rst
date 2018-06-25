Contributing
============

We are interested in various different kinds of improvement for "Request yo racks". Please feel free to raise an
`Issue`_ if you would like to work on something major to ensure
efficient collaboration and avoid duplicate effort, or submit a
`Pull Request`_.

Guidelines
----------

Fork the project and set this repository as the upstream remote.

.. code-block::bash

  git remote add upstream git@github.com:request-yo-racks/infra.git


Use the provided templates to file an `Issue`_ or a
`Pull Request`_. Be as clear as possible when providing information.

Create a topic branch following the these naming conventions:
* if it fixes an existing issue, name you branch `issue/xxx/branch-topic`, where `xxx` is the issue number, and the branch topic is a set of keywords describing your branch.
* if it does not have a related issue, simply name it `branch-topic`

For instance, for the issue `request-yo-racks/api#41`_:

.. code-block::bash

  git pull upstream master
  git checkout master
  git checkout -b issues/41/update-dependencies

Make sure you added tests to validate your changes.

Run all the tests to ensure nothing else was accidentally broken.

Commit messages must start with a capitalized and short summary (max. 50 chars) written in the imperative, followed by
an optional, more detailed explanatory text which is separated from the summary by an empty line.

Commit messages should follow best practices, including explaining the context of the problem and how it was solved,
including in caveats or follow up changes required. They should tell the story of the change and provide readers
understanding of what led to it. Please refer to `How to Write a Git Commit Message`_ for more details.

.. _`Issue`: https://github.com/request-yo-racks/api/issues
.. _`Pull Request`: https://github.com/request-yo-racks/api/pulls
.. _`request-yo-racks/api#41`: https://github.com/request-yo-racks/api/issues/41
.. _`How to Write a Git Commit Message`: http://chris.beams.io/posts/git-commit
