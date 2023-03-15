#!/usr/bin/env node
import {loadPyodide} from "pyodide";
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));


async function main(){
    const indexURL = resolve(__dirname, "node_modules/pyodide");
    const pyodide = await loadPyodide({ indexURL });
    const mounts = [["/home/localdir", "."], ["/home/src_dir", __dirname], ["/home/index", indexURL]];
    for(let [mount, root] of mounts) {
        pyodide.FS.mkdirTree(mount);
        pyodide.FS.mount(pyodide.FS.filesystems.NODEFS, { root }, mount);
    }
    const sys = pyodide.pyimport("sys");
    sys.path.append(mounts[1][0]);
    pyodide.FS.chdir(mounts[0][0]);
    await pyodide.loadPackage(["tomli", "micropip", "beautifulsoup4", "soupsieve"]);
    await pyodide.pyimport("pyscript_local").process_html("./index.html", "./runtime");
}
main();
