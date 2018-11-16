# This file is part of project Sverchok. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/nortikin/sverchok/commit/master
#  
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

import sys
import bpy
# import mathutils
from mathutils import Matrix, Vector
from bpy.props import FloatProperty, IntProperty, StringProperty, BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, node_id
from sverchok.utils.sv_operator_mixins import SvGenericCallbackWithParams
from sverchok.utils.sv_bmesh_utils import bmesh_from_pydata, pydata_from_bmesh

sn_callback = "node.svfunctor_callback"

def make_name(type_, index_):
    return type_ + '_0{0}'.format(index_)


class SvSNCallbackFunctor(bpy.types.Operator, SvGenericCallbackWithParams):
    bl_idname = sn_callback
    bl_label = "Callback for functor node"


def make_annotations():
    annotations = {}
    for i in range(5):
        iname = make_name('int', i)
        annotations[iname] = IntProperty(name=iname, update=updateNode)
        fname = make_name('float', i)
        annotations[fname] = FloatProperty(name=fname, update=updateNode)
        bname = make_name('bool', i)
        annotations[bname] = BoolProperty(name=bname, update=updateNode)
    return annotations

class SvSNPropsFunctor:
    __annotations__ = make_annotations()

    def clear_sockets(self):
        self.inputs.clear()
        self.outputs.clear()

class SvSNFunctor(bpy.types.Node, SverchCustomTreeNode, SvSNPropsFunctor):
    """
    Triggers:  functor
    Tooltip:  use a simpler nodescript style
    
    A short description for reader of node code
    """

    bl_idname = 'SvSNFunctor'
    bl_label = 'SN Functor'
    bl_icon = 'SYSTEM'

    script_name: StringProperty()
    script_str: StringProperty()
    loaded: BoolProperty()
    node_dict = {}

    def handle_execution_nid(self, func_name, msg, *args):
        ND = self.node_dict.get(hash(self))
        if not ND:
            print(self.name,': node dict not found for', hash(self))
            return

        try:
            ND[func_name](*args)
        except Exception as err:
            print(msg, ": error in funcname :", func_name)
            sys.stderr.write('ERROR: %s\n' % str(err))
            exec_info = sys.exc_info()[-1]
            print('on line # {}'.format(exec_info.tb_lineno))
            print('code:', exec_info.tb_frame.f_code)

    def init_socket(self, context):
        """ This will call the hoisted function:  functor_init(self, context) """
        msg = 'failed to initialize sockets'
        self.handle_execution_nid("functor_init", msg, (self, context))

    def draw_buttons(self, context, layout):

        if not self.loaded:
            row = layout.row()
            row.prop_search(self, 'script_name', bpy.data, 'texts', text='', icon='TEXT')
            row.operator(sn_callback, text='', icon='PLUGIN').fn_name = 'load'

        row = layout.row()
        row.operator(sn_callback, text='Load').fn_name='load'
        row.operator(sn_callback, text='Reset').fn_name='reset'

        if self.loaded:
            self.draw_buttons_script(context, layout)

    def draw_buttons_script(self, context, layout):
        """ This will call the hoisted function:  draw_buttons(self, context, layout) """
        msg = 'failed to load custom draw_buttons function'
        self.handle_execution_nid("draw_buttons", msg, (self, context, layout))

    def process(self):
        if not all([self.script_name, self.script_str]):
            return        
        self.process_script(context)

    def process_script(self, context):
        """ This will call the hoisted function:  process(self, context) """
        msg = 'failed to process custom function'
        self.handle_execution_nid("process", msg, (self, context))

    def load(self, context):
        print('time to load', self.script_name)
        return

        self.init_socket(context)
        self.loaded = True

    def reset(self, context):
        print('reset')
        self.loaded = ""
        self.script_name = ""
        self.script_str = ''
        self.node_dict[hash(self)] = {}
        self.clear_sockets()

    def copy(self, node):
        self.node_dict[hash(self)] = {}
        self.load()


classes = [SvSNCallbackFunctor, SvSNFunctor]
register, unregister = bpy.utils.register_classes_factory(classes)