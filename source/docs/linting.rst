
In-Browser Linting
==================

To lint your project's pyproject.toml before submitting a PR, just run our
handy linter below, built with Pyodide.  Validation messages related to you
``pyproject.toml`` file will appear just below the inputs.

.. note::
	 Only ``github.com``, ``gitlab.com`` and self-hosted Gitlab instances are
	 supported by the plugins registry at this time.


.. raw:: html

   <div id="custom-container">
		<table>
			<tr>
				<td><label for="githost">Git Host</label></td>
				<td><input type="text" id="githost" name="githost"></td>
				<td>e.g. github.com, gitlab.com, code.stanford.edu</td>
			</tr>
			<tr>
				<td><label for="githostusername">User/org</label></td>
				<td><input type="text" id="githostusername" name="githostusername"></td>
				<td>The user or org that owns the repository.</td>
			</tr>
			<tr>
				<td><label for="githostrepo">Repo name</label></td>
				<td><input type="text" id="githostrepo" name="githostrepo"></td>
				<td>The name of the repository (no spaces)</td>
			</tr>
			<tr>
	   			<td><label for="gitref">Branch name</label></td>
				<td><input type="text" id="gitref" name="gitref" value="main"></td>
			</tr>
		</table>
       	<button id="runBtn">Loading linting environment...</button>
       	<pre id="output">Loading linting dependencies ...</pre>
   </div>

   <script src="https://cdn.jsdelivr.net/pyodide/v0.29.4/full/pyodide.js"></script>
   <script src="../_static/pyodide-linting.js" defer></script>
