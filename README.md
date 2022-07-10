This is a typed version of https://github.com/vwout/obs-visca-control as an excercise 

First clone [nattlua](https://github.com/CapsAdmin/NattLua) somewhere and run
```
luajit build.lua
luajit install.lua
luajit build.lua vscode # optional if you want the language extension for vscode
```

Then you can run the following commands:

* `nattlua build` build dist/obs-visca-control.lua from dist/obs-visca-control.nlua

running `nattlua build` will build `dist/obs-visca-control.lua` which is a single lua file based on the imports of `src/obs-visca-control.nlua` and type information stripped.

For now, to update `src/obslua.nlua` you have to load `build_obslua_types.py` in obs studio and modify its output at the bottom to point to `src/obslua.nlua`

It's written in python as the obslua types are available as metadata for all the functions. It's not a very good solution. I think ideally it should be built using swig somehow.