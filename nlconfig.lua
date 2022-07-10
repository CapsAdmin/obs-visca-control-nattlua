local cmd = ...
local analyzer_config = {
	working_directory = "src/",
	inline_require = true,
}

if cmd == "get-analyzer-config" then
	analyzer_config.entry_point = "obs-visca-control.nlua"
	return analyzer_config
elseif cmd == "check" then
	local compiler = assert(
		nl.Compiler(
			[[return import("./obs-visca-control.nlua")]],
			"src/obs-visca-control.nlua",
			analyzer_config
		)
	)

	if cmd == "check-language-server" then return compiler end

	assert(compiler:Analyze())
elseif cmd == "build" then
	local nl = require("nattlua")
	local compiler = assert(
		nl.File(
			"src/obs-visca-control.nlua",
			{
				working_directory = "src/",
				inline_require = true,
			}
		)
	)
	local code = compiler:Emit(
		{
			preserve_whitespace = false,
			string_quote = "\"",
			no_semicolon = true,
			omit_invalid_code = true,
			comment_type_annotations = true,
			type_annotations = true,
			force_parenthesis = true,
			extra_indent = {
				Start = {to = "Stop"},
				Toggle = "toggle",
			},
		}
	)
	local f = assert(io.open("dist/obs-visca-control.lua", "w"))
	f:write(code)
	f:close()
	-- analyze after file write so hotreload is faster
	compiler:Analyze()
end