import obspython as obs
import inspect
import types
import numbers
print("hello")

lua = ""

members = inspect.getmembers(obs)

blackboxes = set()
classes = set()
known_types = set(("any", "boolean", "number", "string"))


def handle_arg(arg, ret):
    real_arg = arg

    if "inspect._empty" in arg:
        return "any"

    if "(" in arg:
        return "any"

    if "[" in arg:
        return "any"

    if arg == "void":
        return ""

    arg = arg.replace("const ", "")
    arg = arg.replace(" const ", "")
    arg = arg.replace(" const", "")

    if arg == "char **":
        return "List<|string|>"

    if arg == "char *":
        return "string"

    if arg == "uint8_t" or arg == "uint16_t" or arg == "uint32_t" or arg == "uint64_t":
        return "number"

    if arg == "int8_t" or arg == "int16_t" or arg == "int32_t" or arg == "int64_t":
        return "number"

    if arg == "bool":
        return "boolean"

    if arg == "void *":
        return "any"

    if arg == "void":
        return ""

    if arg == "int" or arg == "float" or arg == "double" or arg == "size_t" or arg == "long long" or arg == "long":
        return "number"

    if arg.startswith("enum "):
        return "number"

    if arg == "uint32_t *":
        return "List<|number|>"

    if arg == "long long *":
        return "List<|number|>"

    if arg == "double *":
        return "List<|number|>"

    if arg == "bool *":
        return "List<|boolean|>"

    if arg == "size_t *":
        return "List<|number|>"

    arg = arg.replace("struct ", "")
    arg = arg.replace("enum ", "")
    arg = arg.replace("*", "")
    arg = arg.replace(" ", "")

    blackboxes.add(arg)

    if ret and "*" in real_arg:
        arg = arg + " | nil"

    if arg != real_arg:
        arg = arg + "--[[ " + real_arg + " ]]"

    arg = "o." + arg

    return arg


for name, obj in members:
    if type(obj) == int:
        lua = lua + "type o." + name + " = " + str(obj) + "\n"

for name, obj in members:
    if type(obj) == str:
        lua = lua + "type o." + name + " = \"" + str(obj) + "\"\n"

for name, obj in members:
    if inspect.isclass(obj):
        classes.add(name)
        lua = lua + "type o." + name + " = {\n"
        for prop_name, obj in inspect.getmembers(obj):
            if isinstance(obj, property):
                lua = lua + "\t" + prop_name + " = any,\n"
        lua = lua + "}\n"

for name, obj in inspect.getmembers(obs):
    if isinstance(obj, types.FunctionType):
        signature = inspect.signature(obj)
        lua = lua + "type o." + name + " = function=("
        args = []
        for key, param in signature.parameters.items():
            args.append(handle_arg(str(param.annotation), False))
        lua = lua + ", ".join(args) + ")"

        lua = lua + \
            ">(" + handle_arg(str(signature.return_annotation), True) + ")\n"

header = "local type o = {}\n"
for name in blackboxes:
    print(name)
    if not name in classes:
        header = header + "type o." + name + \
            " = {__name = \"" + name + "\"}\n"

lua = header + lua
lua = lua + """
type o.source_list = {__name = "source_list"} 

type o.obs_enum_sources = function=()>(o.source_list)
type o.obs_scene_enum_items = function=(o.obs_scene_t)>(any)
type o.obs_add_main_render_callback = function=(function=()>())>()
type o.obs_remove_main_render_callback = function=(function=()>())>()
type o.signal_handler_connect = function=(o.signal_handler_t, string, function=(o.calldata_t)>())>()
type o.signal_handler_disconnect = function=(o.signal_handler_t, string, function=(o.calldata_t)>())>()
type o.signal_handler_connect_global = function=(o.signal_handler_t, function=(o.calldata_t)>())>()
type o.signal_handler_disconnect_global = function=(o.signal_handler_t, function=(o.calldata_t)>())>()
type o.obs_hotkey_register_frontend = function=(string, string, function=(boolean)>())>(o.obs_hotkey_id)
type o.obs_hotkey_unregister = function=(o.obs_hotkey_id)>()
type o.obs_properties_add_button = function=(o.obs_properties_t, string, string, function=(o.obs_properties_t, o.obs_property_t)>())>()
type o.remove_current_callback = function=()>()
type o.source_list_release = function=(o.source_list)>()
type o.sceneitem_list_release = function=(any)>()

type script_load = function=(o.obs_data_t)>()
type script_unload = function=()>()
type script_save = function=(o.obs_data_t)>()
type script_defaults = function=(o.obs_data_t)>()
type script_update = function=(o.obs_data_t)>()
type script_properties = function=()>(o.obs_properties_t)
type script_tick = function=(number)>()

type o.obs_register_source = function=(Partial<|{

    --[[
    const char *obs_source_info.id
    enum obs_source_type obs_source_info.type
    uint32_t obs_source_info.output_flags
    const char *(*obs_source_info.get_name)(void *type_data)
    void *(*obs_source_info.create)(obs_data_t *settings, obs_source_t *source)
    void (*obs_source_info.destroy)(void *data)
    uint32_t (*obs_source_info.get_width)(void *data)
    uint32_t (*obs_source_info.get_height)(void *data)
    void (*obs_source_info.get_defaults)(obs_data_t *settings)
    void (*obs_source_info.get_defaults2)(void *type_data, obs_data_t *settings)
    obs_properties_t *(*obs_source_info.get_properties)(void *data)
    obs_properties_t *(*obs_source_info.get_properties2)(void *data, void *type_data)
    void (*obs_source_info.update)(void *data, obs_data_t *settings)
    void (*obs_source_info.activate)(void *data)
    void (*obs_source_info.deactivate)(void *data)
    void (*obs_source_info.show)(void *data)
    void (*obs_source_info.hide)(void *data)
    void (*obs_source_info.video_tick)(void *data, float seconds)
    void (*obs_source_info.video_render)(void *data, gs_effect_t *effect)
    struct obs_source_frame *(*obs_source_info.filter_video)(void *data, struct obs_source_frame *frame)
    struct obs_audio_data *(*obs_source_info.filter_audio)(void *data, struct obs_audio_data *audio)
    void (*obs_source_info.enum_active_sources)(void *data, obs_source_enum_proc_t enum_callback, void *param)
    void (*obs_source_info.save)(void *data, obs_data_t *settings)
    void (*obs_source_info.load)(void *data, obs_data_t *settings)
    void (*obs_source_info.mouse_click)(void *data, const struct obs_mouse_event *event, int32_t type, bool mouse_up, uint32_t click_count)
    void (*obs_source_info.mouse_move)(void *data, const struct obs_mouse_event *event, bool mouse_leave)
    void (*obs_source_info.mouse_wheel)(void *data, const struct obs_mouse_event *event, int x_delta, int y_delta)
    void (*obs_source_info.focus)(void *data, bool focus)
    void (*obs_source_info.key_click)(void *data, const struct obs_key_event *event, bool key_up)
    void (*obs_source_info.filter_remove)(void *data, obs_source_t *source)
    void *obs_source_info.type_data
    void (*obs_source_info.free_type_data)(void *type_data)
    bool (*obs_source_info.audio_render)(void *data, uint64_t *ts_out, struct obs_source_audio_mix *audio_output, uint32_t mixers, size_t channels, size_t sample_rate)
    void (*obs_source_info.enum_all_sources)(void *data, obs_source_enum_proc_t enum_callback, void *param)
    void (*obs_source_info.transition_start)(void *data)
    void (*obs_source_info.transition_stop)(void *data)
    enum obs_icon_type obs_source_info.icon_type
    void (*obs_source_info.media_play_pause)(void *data, bool pause)
    void (*obs_source_info.media_restart)(void *data)
    void (*obs_source_info.media_stop)(void *data)
    void (*obs_source_info.media_next)(void *data)
    void (*obs_source_info.media_previous)(void *data)
    int64_t (*obs_source_info.media_get_duration)(void *data)
    int64_t (*obs_source_info.media_get_time)(void *data)
    void (*obs_source_info.media_set_time)(void *data, int64_t miliseconds)
    enum obs_media_state (*obs_source_info.media_get_state)(void *data)
    enum gs_color_space (*obs_source_info.video_get_color_space)(void *data, size_t count, const enum gs_color_space *preferred_spaces)¶
    ]]


    id = string,
    type = number,
    output_flags = number,
    get_name = function=(any)>(string),
    create = function=(o.obs_data_t, o.obs_source_t)>(any),
    destroy = function=(any)>(),
    get_width = function=(number)>(),
    get_height = function=(number)>(),
    get_defaults = function=(o.obs_data_t)>(),
    get_defaults2 = function=(any, o.obs_data_t)>(),
    get_properties = function=(any)>(o.obs_properties_t),
    get_properties2 = function=(any, any)>(o.obs_properties_t),
    update = function=(any, o.obs_data_t)>(),
    activate = function=(any)>(),
    deactivate = function=(any)>(),
    show = function=(any)>(),
    hide = function=(any)>(),
    video_tick = function=(any, number)>(),
    video_render = function=(any, o.gs_effect_t)>(),
    filter_video = function=(any, o.obs_source_frame)>(o.obs_source_frame),
    filter_audio = function=(any, o.obs_audio_data)>(o.obs_audio_data),
    enum_active_sources = function=(any, o.obs_source_enum_proc_t, any)>(),
    save = function=(any, o.obs_data_t)>(),
    load = function=(any, o.obs_data_t)>(),
    mouse_click = function=(any, o.obs_mouse_event, number, boolean, number)>(),
    mouse_move = function=(any, o.obs_mouse_event, boolean)>(),
    mouse_wheel = function=(any, o.obs_mouse_event, number, number)>(),
    focus = function=(any, boolean)>(),
    key_click = function=(any, o.obs_key_event, boolean)>(),
    filter_remove = function=(any, o.obs_source_t)>(),
    type_data = any,
    free_type_data = function=(any)>(),
    audio_render = function=(any, number, o.obs_source_audio_mix, number, number, number)>(boolean),
    enum_all_sources = function=(any, o.obs_source_enum_proc_t, any)>(),
    transition_start = function=(any)>(),
    transition_stop = function=(any)>(),
    icon_type = number,
    media_play_pause = function=(any, boolean)>(),
    media_restart = function=(any)>(),
    media_stop = function=(any)>(),
    media_next = function=(any)>(),
    media_previous = function=(any)>(),
    media_get_duration = function=(any)>(number),
    media_get_time = function=(any)>(number),
    media_set_time = function=(any, number)>(),
    media_get_state = function=(any)>(number),
    video_get_color_space = function=(any, number, any)>(number),
}|>)>()

o.obs_frontend_get_current_scene = o.obs_frontend_get_current_preview_scene

"""

lua = lua + "type obslua = o\n"

f = open("/home/caps/github/nattlua/examples/projects/obs-visca-control/src/obslua.nlua", "w")
f.write(lua)
f.close()
