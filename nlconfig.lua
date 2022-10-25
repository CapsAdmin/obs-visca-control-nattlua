local nl = require("nattlua")
local cmd = ...
local input_dir = "src/"
local input_file = "obs-visca-control.nlua"
local output_dir = "dist/"
local output_file = "obs-visca-control.lua"
local analyzer_config = {
	working_directory = input_dir,
	inline_require = true,
}

if cmd == "get-analyzer-config" then
	local analyzer_config = {
		inline_require = true,
		entry_point = input_file,
	}
	return analyzer_config
elseif cmd == "check" then
	require("nattlua.other.profiler").Start()
	local compiler = assert(
		nl.Compiler(
			[[return import("]] .. input_file .. [[")]],
			input_dir .. input_file,
			analyzer_config
		)
	)

	if cmd == "check-language-server" then return compiler end

	compiler:Analyze()
	require("nattlua.other.profiler").Stop()
elseif cmd == "build" then
	local nl = require("nattlua")
	local compiler = assert(
		nl.File(
			input_dir .. input_file,
			{
				working_directory = input_dir,
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
	local f = assert(io.open(output_dir .. output_file, "w"))
	f:write(code)
	f:close()
	-- analyze after file write so hotreload is faster
	compiler:Analyze()
end