InVEST Community Plugin Registry
================================

Welcome to the Community Plugin Registry! Here you can discover plugins for the Integrated
Valuation of Ecosystem Services and Tradeoffs (InVEST) software. For more information,
please see the `feature announcement <https://naturalcapitalalliance.stanford.edu/news/new-feature-opens-door-custom-models-mapping-and-valuing-natures-benefits>`_.

----

Browse available plugins
------------------------

A list of known community plugins can be found `here <plugins/index.html>`_. You can also
use the search bar in the left column to search on keywords.

If you find a plugin you'd like to use, you can install it from the InVEST Workbench. Take a
look at the :ref:`Plugin Installation Docs <installing>` for more details.

.. include:: docs/install_warning.rst

Contribute a plugin
-------------------

If you've created an InVEST plugin and would like to make it available to others in the
community, the best way to make it discoverable is to submit it for inclusion in this
registry. Take a look at the :ref:`Plugin Submission Docs <submission>` for a detailed
guide.

Have an idea for a plugin or an existing script that you'd like to turn into one? Take a
look at the `Plugin Developer Docs <https://invest.readthedocs.io/en/latest/plugins.html>`_
to learn more.

----

What is a plugin?
-----------------

Conceptually, an InVEST plugin is an ecosystem services model. Like the core InVEST
models, it takes in data of various formats (usually including some geospatial data),
processes that data, and produces output files that contain the results.
Unlike the core models, a plugin is not "official", i.e., not reviewed or maintained
by NatCap. Plugins may be developed, used, and distributed totally independently of
the ``natcap/invest`` repo and the Natural Capital Alliance.

In a technical sense, an InVEST plugin is a python package that conforms to the
``natcap.invest`` plugin API. This makes it possible to run the plugin from the
InVEST workbench and the ``invest`` command line tool. The plugin can execute any
arbitrary code when it runs. Commonly the ecosystem services model logic will be
implemented in the python package, but it could also invoke another software tool -
for example, if your model is already implemented in another language, you could
develop the plugin as a python wrapper for it.

Why make a plugin?
------------------

A plugin can be run in the InVEST workbench, which provides a graphical interface
where a user can enter the model inputs, run the model, watch its progress, and
access the results. All the necessary information to display the model in the
workbench is pulled from the plugin python package - no frontend development needed.
This is handy when resources are too limited to develop a separate GUI for a project.
It is a major benefit for developers to be able to focus on their model and not
worry about maintaining a desktop application or distributing it across multiple
operating systems.

The data validation component of InVEST is also very useful for projects that don't
have enough resources to develop this independently. The plugin API requires
that data inputs are rigorously specified. Before running a model, InVEST validates
that the provided data meets all of the requirements, and provides helpful feedback
if it does not. This prevents a lot of trouble with invalid data.

Even if resources were unlimited, we think there is value in having a shared interface
for ecosystem services models. Seeing different ecosystem service models, or different
versions of the same model, side-by-side in the workbench facilitates running them
together and comparing them.

The plugin API is a useful framework in which to think of developing a model.
This framework is helpful when tackling the task of turning a "model" (which may
exist in the form of mathematical equations, scripts, or other software)
into a well-documented, reusable, distributable software tool. Implementing the
plugin API requires attention to many details that are easily overlooked when
writing a basic script. Going through the process of developing a model into a
plugin will help to catch bugs and identify assumptions that may exist in your
math or your code.

Are you a Bot?
--------------

If so, you might be interested in our machine-readable package index files:

* JSON package index metadata: `metadata.json <./metadata.json>`__ and `SHA256 <./metadata.json.sha256>`__
* BZip2-compressed package index metadata: `metadata.json.bz2 <./metadata.json.bz2>`__ and `SHA256 <./metadata.json.bz2.sha256>`__


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Contents:

   plugins/index
   docs/index

.. toctree::
   :hidden:
   :caption: Links:

   GitHub <https://github.com/natcap/invest-plugin-registry/>
   Plugin Developer Docs <https://invest.readthedocs.io/en/latest/plugins.html>
   NatCap Community Forum <https://community.naturalcapitalalliance.org/latest>
