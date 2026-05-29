.. _submission:

=========================
Plugin Submission Process
=========================

If you'd like to share your plugin with the InVEST community, the best way to do so
is to submit it to the official list of plugins. Once your plugin is reviewed by a
member of the reviewer pool, other users will be able to find it on the registry and
install it from the InVEST Workbench.

.. note::
   If you have already submitted a version of your plugin for inclusion in the
   registry and want to update the version the registry tracks, jump to
   :ref:`updating_version`.

.. _contributing:

Contribution Policy
-------------------

The maintainers of the ``invest-plugin-registry``
`repository <https://github.com/natcap/invest-plugin-registry/>`_ will generally accept
all contributed plugins. Community-contributed plugins are **not** reviewed for quality
or accuracy. The purpose of this list is simply to facilitate plugin sharing and
discovery. The inclusion of a plugin in this list does not guarantee anything about
its quality, suitability, or security. You are fully responsible for assessing the
plugins you wish to use. Be aware that running third-party code can introduce risks.
The maintainer team reserves the right to decline contributions that seem inappropriate
or malicious.

----

.. _security_policy:

Security Policy
---------------

The inclusion of a plugin in the InVEST plugins registry does not imply or guarantee
anything about the plugin's quality, suitability, or security, and the Natural Capital
Alliance reserves the right to remove any plugin from the registry that is believed to be
a security risk. If you believe a plugin poses a security risk, please see
<LINK TO THIS FILE> for instructions.

----

Prerequisites
-------------

In order to complete the submission process, you will need a
`GitHub <https://github.com/>`_ account.

----

.. _submission_requirements:

Before you begin: Submission requirements
-----------------------------------------

Before you submit your plugin, make sure you have the following files in the root
folder of your repository:

* A ``pyproject.toml`` that describes your plugin and contains all of the required
  metadata (see :ref:`Required pyproject.toml metadata <pyproj_reqs>` below). For
  more information on writing a pyproject.toml that meets the InVEST plugin
  requirements, please refer to the
  `Plugin Developer Docs <https://invest.readthedocs.io/en/latest/plugins.html>`_.
* A ``LICENSE.txt`` that determines how others are allowed to use the plugin and its
  source code. More information about `adding a license <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository>`_
  to your plugin repo or `choosing a license <https://choosealicense.com/>`_ can be
  found at the respective links. **Note:** All plugins must have a permissive open
  source license compatible with Apache-2.0 in order to be included in the plugin
  registry.
* A ``README.md`` / ``README.rst`` that describes your plugin.

.. _pyproj_reqs:

Required ``pyproject.toml`` metadata:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following keys are required for inclusion in the community plugin registry:

* In the ``[project]`` section:

  * ``name``: The name of your project.
  * ``authors`` and/or ``maintainers``: You only need to include one of these, but if
    the authors and maintainer of the plugin differ, you may include both.
  * ``description``: A brief description of your plugin.
  * ``readme``: This is a longer description of your plugin. Typically, a project will
    have a ``README.md`` or ``README.rst`` file and you should put that file name here.
  * ``license``: This is an `SPDX license <https://packaging.python.org/en/latest/glossary/#term-License-Expression>`_ expression consisting of one or more `license identifiers <https://packaging.python.org/en/latest/glossary/#term-License-Identifier>`_.
  * ``license-files``: A list of license files and files containing other legal information
    you want to distribute with your plugin. If there are any limitations on the use of
    your plugin, these should be made clear in the license(s).

* In the ``[project.urls]`` section:

  * ``Repository``: The link to your plugin's repository.
  * ``Issues``: The link to your preferred issue tracker. This could be the repo's Issues
    page, or it could be something else. Many users of InVEST often look to the
    `NatCap Forum <https://community.naturalcapitalalliance.org/latest>`_ for help, so if
    you'd like to engage with users of your plugin on the Forum, that's also an option! 
  * ``Documentation``: The link to your plugin documentation. It's fine if this URL points
    to your README.

* Optional, in the ``[tool.natcap.invest]`` section:

  * ``registry_description``: If you'd like to provide a longer description of your plugin
    specifically for use on its Community Plugin Registry page, please include the key
    ``registry_description`` in the ``[tool.natcap.invest]`` section and provide the path
    to a file in your repo. If you don't include a description file, the registry will
    use the value of the description key in the ``[project]`` section instead.

    * Supported file types: ``.md``, ``.rst``, and ``.txt``
    * Note: This should be a file path relative to the root of your repo, **not** an HTTPS
      URL!

.. _readme_reqs:

Recommended to include in your ``README``:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your ``README`` is likely the first place a potential user of your plugin will look when
deciding whether or not your plugin will suit their needs. As such, your plugin should have
documentation that explains how to use it correctly (and any limitations of its use) to a
potential user. You can include this in your ``README`` if you don't wish to host
documentation elsewhere. If you do want to put your documentation somewhere else, you
should link to it from your ``README``.

The ``README`` is also a good place to include any peer-reviewed paper(s) associated
with your plugin, as well as any funding source(s) that contributed to its creation.

----

.. _host_plugin:

Step 1: Make your plugin available on GitHub or GitLab
------------------------------------------------------

In order for your plugin to be included in the registry, the source code needs to be
hosted publicly on GitHub or GitLab. If you're unfamiliar with GitHub, refer to the
GitHub docs for how to `create a new repository <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository>`_.

----

.. _create_release:

Step 2: Create a release
------------------------

Depending upon where your plugin repository is hosted, the process for creating a
release may differ slightly. Please refer to the guide for your repo host:

* `GitHub documentation <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release>`_
* `GitLab documentation <https://docs.gitlab.com/user/project/releases/#create-a-release-in-the-releases-page>`_

For the Tag, we require that you follow the `semantic versioning <https://semver.org/>`_
specification, e.g. 1.0.0 for an initial release. Only versions with the format ``x.y.z``
are supported; do not prefix your version with ``v``.

----

.. _fork_and_edit:

Step 3: Fork the ``invest-plugin-registry`` repo and edit ``plugins.json``
--------------------------------------------------------------------------
In this step, you will make the edits to the community plugin list that are needed for
the inclusion of your plugin.

To get set up, first `fork <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`_ the ``invest-plugin-registry``
`repo on GitHub <https://github.com/natcap/invest-plugin-registry/>`_.

On your fork, add a new entry at the bottom of the ``plugins.json`` file: ::

    {
         "repo_url": "https://github.com/natcap/invest-routedem-tfa-range.git",
         "version": "1.0.0",
         "plugin_type": "invest_model_variant",
         "keywords": ["RouteDEM", "hydrology", "streams", "routing"]
    }

* Remember to add a comma after the closing curly bracket, ``}``, of the previous entry!
* ``repo_url`` should be the ``https`` URL of your repository.
* For ``version``, use the tag associated with your release from
  :ref:`Step 2 <create_release>`. Remember that semantic versioning is required; this
  version should match the format ``x.y.z``.
* For ``plugin_type``, please enter one of the following, which best describes the
  category of functionality of your plugin:

  * ``preprocessing``: This plugin performs pre-processing steps to prepare data for
    use in ecosystem services modeling.
  * ``postprocessing``: This plugin performs post-processing steps on the outputs from
    an ecosystem services model or models.
  * ``workflow``: This plugin composes multiple models to solve a domain-specific problem.
  * ``invest_model_variant``: This plugin is a variant on an existing model in core InVEST.
  * ``new_model``: This plugin implements a new model that does not exist in core InVEST.
  * ``other``: It's recommended not to use this label in most cases. The purpose of
    tracking plugin_type is to assist users in searching for plugins that may meet their
    needs. However, if your plugin really does not fit into any of the above categories,
    you may use the ``other`` label. **You are encouraged to describe why none of the
    other labels apply in your pull request submission** – this will help the maintainer
    team know if they need to introduce any additional categories in the future!

* For ``keywords``, you may include a comma-separated list of terms that relate to your
  plugin. You're encouraged to look through the ``keywords`` used to describe other plugins
  in this list and use the same terms wherever possible.

  * If your plugin is a model variant, please include the name of the InVEST model of
    which it is a variant. For instance, if your plugin is a variant of the Sediment
    Delivery Ratio model, include "Sediment Delivery Ratio" in the ``keywords`` list.
  * **Note:** The maintainer team may periodically make changes to the ``keywords`` lists
    associated with plugins tracked in the repository, to normalize and unify the
    terminology used in an effort to better enable search functionality.

----

.. _submit_pr:

Step 4: Submit a pull request for review
----------------------------------------

When you open a pull request, a template is provided to help ensure you're providing all of
the information about your plugin that is needed for review and inclusion in the registry.
Most of the required information will be automatically pulled from your ``pyproject.toml``;
please double-check the :ref:`submission_requirements` to make sure you've included all
required fields.

1. In the name of the pull request, enter "Add plugin: [...]", where [...] is the name of
   your plugin.
2. Fill in the details in the description for the pull request, as prompted by the template.
   For the checkboxes, you can check them by inserting an x between the brackets: ``[x]``.
3. Click "Create pull request"

Once you submit the pull request, some automated checks will run, including:

* A check confirming that your new entry in ``plugins.json`` is properly formatted. This
  includes checking that the ``plugin_type`` value you've entered is one of the expected
  values.
* A basic security scan to help guard against malicious code.
* A test confirming that your plugin can be installed and loaded by InVEST.
* A test confirming that all of the required pieces of your ``pyproject.toml`` are included.

If tests fail:
^^^^^^^^^^^^^^

If any of these tests fail, the bot will add a comment to the PR tagging you and providing
a message explaining what went wrong. At this stage, if you have questions about how to fix
the problem(s), you can request help from someone on the maintainer team; please leave a
comment on the PR tagging ``@natcap/software-team`` and they will do their best to assist.

Once tests pass:
^^^^^^^^^^^^^^^^

After your PR has passed automated validation, the bot will add a comment to the PR that
includes several pieces of metadata extracted from your ``pyproject.toml``, to facilitate
easy review. At this stage, the team of reviewers will also receive a ping. The aim is to
review plugins promptly (usually within 5 working days of submission), but please keep in
mind the maintainer team is small. **Please note that the reviewers will not be completing
a code review**; rather, they will be checking submissions for context / subject relevance.
Specifically, they will evaluate based on the following questions:

* Did you include all of the information required by the template in the body of your pull
  request?
* Does the plugin have to do with nature and/or nature's benefits to people? Or does the
  plugin appear to be something quite unrelated, e.g. tax software?
* Does the plugin have documentation? Does the documentation look relevant to the plugin's
  description?
* Is the plugin's name unique and appropriate? Does it adhere to the
  `Code of Conduct <code_of_conduct.html>`_? (It's generally recommended to give your
  plugin a name that's related to what it does. Don't call your plugin "banana" unless
  it's modeling something about bananas!)

If you would like to view the exact rubric the reviewers use, you may do so
:ref:`here <review_rubric>`.

----

.. _address_comments:

Step 5: Address any review comments
-----------------------------------

If your plugin fails review for any reason, the reviewer will add a comment to the PR
tagging you and explaining why the plugin failed to meet the criteria. Please address
any required changes and update the GitHub release with those changes. Leave a comment
on the PR to let the reviewer know you've addressed the feedback. Don't open a new PR.

Once your plugin passes review, the reviewer will merge the PR and your plugin will be
available for other users to discover and install from the registry!

----

.. _updating_version:

Updating your plugin version
----------------------------

If you want to update the version of your plugin that is tracked in the community
list, please do the following:

* Create a new release following the instructions in :ref:`create_release`.
* On your fork of the ``invest-plugin-registry`` repository, find your entry in
  ``plugins.json`` and update the version to match your new release.
* Submit a PR using the provided template
* The same automated checks described in :ref:`Step 4: Submit a PR <submit_pr>` will run.

  * If any of the tests fail, you will be notified of the failure and prompted to address
    the error(s).
  * Once these tests pass, the PR will be automatically merged; no further action is
    required!
