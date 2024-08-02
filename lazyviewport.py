"""Lazy Viewport 1.3.1

1.3.1
--Jul 29 2024--
**this is a fork by phordan allowing a toggle to enable/disable the addon and hotkeys with Shift-F1**

1.3 Updates
- Fixed error on previous versions of blender

1.2 Updates:
- Compatibility with Blender 4.0

1.1 Updates:
Now supporting the modes: 
- Pose Edit Mode
- Armature Edit Mode
- Lattice Edit Mode
- UV Edit Mode
- Metaball Mode
- Pose Mode


"""
import bpy
from bpy.props import BoolProperty

bl_info = {
    "name": "Lazy Viewport 1.3.1",
    "blender": (2, 80, 0),
    "category": "Object",
}

addon_keymaps = []
is_enabled = True

class LazyViewportPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    enabled: BoolProperty(
        name="Enable Add-on",
        default=True,
        update=lambda self, context: toggle_addon(self, context)
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enabled")

def toggle_addon(self, context):
    global is_enabled
    is_enabled = self.enabled
    show_notification(f"Lazy Viewport {'Enabled' if is_enabled else 'Disabled'}")
    if not is_enabled:
        set_active_tool('builtin.select_box')
    update_keymaps()

def show_notification(message):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title="Lazy Viewport", icon='INFO')

class LazyViewPortMove(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_move"
    bl_label = "Lazy Viewport Move"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if is_enabled:
            set_active_tool('builtin.move')
        return {'FINISHED'}

class LazyViewPortRotate(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_rotate"
    bl_label = "Lazy Viewport Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if is_enabled:
            set_active_tool('builtin.rotate')
        return {'FINISHED'}

class LazyViewPortScale(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_scale"
    bl_label = "Lazy Viewport Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if is_enabled:
            set_active_tool('builtin.scale')
        return {'FINISHED'}

class LazyViewPortSelect(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_select"
    bl_label = "Lazy Viewport Select"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if is_enabled:
            set_active_tool('builtin.select_box')
        return {'FINISHED'}

class LazyViewPortToggle(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_toggle"
    bl_label = "Toggle Lazy Viewport"

    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        preferences.enabled = not preferences.enabled
        return {'FINISHED'}

def set_active_tool(tool_name):
    for area in bpy.context.screen.areas:
        types = ['VIEW_3D', 'IMAGE_EDITOR']
        for t in types:
            if area.type == t:
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area
                override["region"] = area.regions[0]
                
                with bpy.context.temp_override(**override):
                    bpy.ops.wm.tool_set_by_id(name=tool_name)

def update_keymaps():
    global addon_keymaps
    wm = bpy.context.window_manager

    # Clear existing keymaps
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)

    # Always keep the toggle hotkey
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    km.keymap_items.new(LazyViewPortToggle.bl_idname, 'F1', 'PRESS', shift=True)

    if is_enabled:
        # Add other hotkeys only when enabled
        types = ['Object Mode', 'Mesh', 'Curve', 'Lattice', 'Armature', "Metaball", "UV Editor", "Pose"]
        for t in types:
            km = wm.keyconfigs.addon.keymaps.new(name=t, space_type='EMPTY')
            km.keymap_items.new(LazyViewPortMove.bl_idname, 'G', 'PRESS', ctrl=False, shift=False)
            km.keymap_items.new(LazyViewPortRotate.bl_idname, 'R', 'PRESS', ctrl=False, shift=False)
            km.keymap_items.new(LazyViewPortScale.bl_idname, 'S', 'PRESS', ctrl=False, shift=False)
            km.keymap_items.new(LazyViewPortSelect.bl_idname, 'W', 'PRESS', ctrl=False, shift=False)
            addon_keymaps.append(km)

def register():
    bpy.utils.register_class(LazyViewportPreferences)
    bpy.utils.register_class(LazyViewPortMove)
    bpy.utils.register_class(LazyViewPortRotate)
    bpy.utils.register_class(LazyViewPortScale)
    bpy.utils.register_class(LazyViewPortSelect)
    bpy.utils.register_class(LazyViewPortToggle)
    update_keymaps()

def unregister():
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(LazyViewportPreferences)
    bpy.utils.unregister_class(LazyViewPortMove)
    bpy.utils.unregister_class(LazyViewPortRotate)
    bpy.utils.unregister_class(LazyViewPortScale)
    bpy.utils.unregister_class(LazyViewPortSelect)
    bpy.utils.unregister_class(LazyViewPortToggle)

if __name__ == "__main__":
    register()
