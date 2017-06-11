Contributing
------------

Guidelines
^^^^^^^^^^

* We are interested in various different kinds of improvement for ``api``; please feel free to raise an `Issue`_ if you would like to work on something major to ensure efficient collaboration and avoid duplicate effort.
* Use the provided templates to file an `Issue`_ or a `Pull Request`_.
* Create a topic branch from where you want to base your work.
* Make sure you have added tests for your changes.
* Run all the tests to ensure nothing else was accidentally broken.
* Reformat the code by following the formatting section below.
* Submit a pull request.

Formatting
----------

For formatting the files properly, please use `YAPF`_.

In the root directory of the project, run the following command:

.. code-block:: bash

  yapf -r -i api/

or

.. code-block:: bash

  make format

.. _`Issue`: https://github.com/Rémy Greinhofer/api/issues
.. _`Pull Request`: https://github.com/Rémy Greinhofer/api/pulls
.. _`YAPF`: https://github.com/google/yapf
