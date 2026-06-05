//let pyodideEnv;

// 2. Initialize Pyodide on page load
async function initPyodide() {
		try {
				// Initialize the main WebAssembly Python runtime
				pyodideEnv = await loadPyodide();

				// Load micropip to manage package installations from PyPI
				await pyodideEnv.loadPackage("micropip");
				const micropip = pyodideEnv.pyimport("micropip");

				// Install requests and the essential pyodide-http patch library
				document.getElementById("output").innerText = "Installing packages from PyPI...";
				await micropip.install(["packaging>=24.2", "requests", "pyodide-http", "validate_pyproject"]);

				// Enable the action button once the environment is completely ready
				document.getElementById("output").innerText = "Environment ready!";
				const btn = document.getElementById("runBtn");
				btn.innerText = "Run validation";
				btn.disabled = false;

		} catch (err) {
				document.getElementById("output").innerText = `Initialization failed: ${err.message}`;
		}
}

// 3. Define and execute the script inside a Python function scope
async function executePythonScript() {
		document.getElementById("output").innerText = "Executing Python script...";

		// We write a multi-line string containing a Python function definition
		const pythonCode = String.raw`
{{__METADATA_LINTING_SCRIPT__}}
`;

		try {
				// runPythonAsync returns the evaluated result of the last line/expression
				await pyodideEnv.runPython(pythonCode);
				const validateFunc = pyodideEnv.globals.get('_validate_pyproject_file');
			  const gitHost = document.getElementById("githost").value;
				const githostUser = document.getElementById("githostusername").value;
				const githostRepo = document.getElementById("githostrepo").value;
				const gitRef = document.getElementById("gitref").value;

			  const githubPattern = /github\.com/;
			  let tomlpath;
				if (githubPattern.test(gitHost)) {
					tomlpath = `https://raw.githubusercontent.com/${githostUser}/${githostRepo}/refs/heads/${gitRef}/pyproject.toml`;
				} else {
					// Assume gitlab.  Other git hosts could come later.
					// Public gitlab-hosted repos don't have CORS headers on the `raw` urls, so we need to use the API instead.
					// We can only access data from public with the required CORS headers
					tomlpath = `https://${gitHost}/api/v4/projects/${githostUser}%2F${githostRepo}/repository/files/pyproject.toml/raw?ref=${gitRef}`;
				}
				console.log(`Validating tomlpath ${tomlpath}`);
				const result = validateFunc(tomlpath);
				document.getElementById("output").innerText = result;
		} catch (err) {
				document.getElementById("output").innerText = `Python Runtime Error:\n${err.message}`;
		}
}

// Wire event listeners and run setup
document.getElementById("runBtn").addEventListener("click", executePythonScript);
initPyodide();

