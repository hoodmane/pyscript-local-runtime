This heavily WIP script puts all of the Pyodide assets that a pyscript
`index.html` file needs into a `runtime` folder. If `index.html` is next to the
runtime folder, then you can put 
```toml
[[interpreters]]
src = "runtime/pyodide.js"
name = "pyodide-0.21.3"
lang = "python"
```
in your `<py-config>` and all of the Pyodide assets will be loaded from the runtime folder.

To run:
```shell
cd path/to/pyscript-project-folder
wget https://github.com/pyodide/pyodide/releases/download/0.22.1/pyodide-core-0.22.1.tar.bz2
tar -xf ./pyodide-core-0.22.1.tar.bz2
mv pyodide runtime
npx path/to/pyscript-local/
```
