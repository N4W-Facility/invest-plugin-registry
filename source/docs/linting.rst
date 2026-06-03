
Linting Your Plugin's pyproject.toml
====================================

To lint your project's pyproject.toml before submitting a PR, just run our
handy linter below, built with Pyodide.


.. raw:: html

   <div id="custom-container">
		<table>
			<tr>
				<td><label for="githubusername">Github username</label></td>
				<td><input type="text" id="githubusername" name="githubusername"></td>
			</tr>
			<tr>
				<td><label for="githubrepo">Github repo</label></td>
				<td><input type="text" id="githubrepo" name="githubrepo"></td>
			</tr>
			<tr>
	   			<td><label for="githubref">Github ref (e.g. main)</label></td>
				<td><input type="text" id="githubref" name="githubref" value="main"></td>
			</tr>
		</table>
       	<button id="runBtn">Loading linting environment...</button>
       	<pre id="output">Initializing system...</pre>
   </div>

   <script src="https://cdn.jsdelivr.net/pyodide/v0.29.4/full/pyodide.js"></script>
   <script src="../_static/pyodide-linting.js" defer></script>
