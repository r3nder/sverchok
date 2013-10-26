import bpy
from node_s import *
from mathutils import *
from util import *

class MatrixDeformNode(Node, SverchCustomTreeNode):
    ''' MatrixDeform '''
    bl_idname = 'MatrixDeformNode'
    bl_label = 'Matrix Deform'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    def init(self, context):
        self.inputs.new('MatrixSocket', "Original", "Original")
        self.inputs.new('VerticesSocket', "Location", "Location")
        self.inputs.new('VerticesSocket', "Scale", "Scale")
        self.inputs.new('VerticesSocket', "Rotation", "Rotation")
        self.inputs.new('StringsSocket', "Angle", "Angle")
        self.outputs.new('MatrixSocket', "Matrix", "Matrix")
        

    def update(self):
        # inputs
        if 'Matrix' in self.outputs and len(self.outputs['Matrix'].links)>0:
            if self.inputs['Original'].links and \
                type(self.inputs['Original'].links[0].from_socket) == MatrixSocket:
                if not self.inputs['Original'].node.socket_value_update:
                    self.inputs['Original'].node.update()
                orig_ = eval(self.inputs['Original'].links[0].from_socket.MatrixProperty)
                orig = Matrix_generate(orig_)
            else:
                return
                
            if self.inputs['Location'].links and \
                type(self.inputs['Location'].links[0].from_socket) == VerticesSocket:
                if not self.inputs['Location'].node.socket_value_update:
                    self.inputs['Location'].node.update()
                loc_ = eval(self.inputs['Location'].links[0].from_socket.VerticesProperty)
                loc = Vector_generate(loc_)
            else:
                loc = [[]]
            
            if self.inputs['Scale'].links and \
                type(self.inputs['Scale'].links[0].from_socket) == VerticesSocket:
                if not self.inputs['Scale'].node.socket_value_update:
                    self.inputs['Scale'].node.update()
                scale_ = eval(self.inputs['Scale'].links[0].from_socket.VerticesProperty)
                scale = Vector_generate(scale_)
            else:
                scale = [[]]
                
            if self.inputs['Rotation'].links and \
                type(self.inputs['Rotation'].links[0].from_socket) == VerticesSocket:
                if not self.inputs['Rotation'].node.socket_value_update:
                    self.inputs['Rotation'].node.update()
                rot_ = eval(self.inputs['Rotation'].links[0].from_socket.VerticesProperty)
                rot = Vector_generate(rot_)
                #print ('matrix_def', str(rot_))
            else:
                rot = [[]]
            
            if self.inputs['Angle'].links and \
                type(self.inputs['Angle'].links[0].from_socket) == StringsSocket:
                if not self.inputs['Angle'].node.socket_value_update:
                    self.inputs['Angle'].node.update()
                angle = eval(self.inputs['Angle'].links[0].from_socket.StringsProperty)
            else:
                angle = [[0.0]]
            
            # outputs
        
            if not self.outputs['Matrix'].node.socket_value_update:
                self.outputs['Matrix'].node.update()
            
            matrixes_ = matrixdef(orig, loc, scale, rot, angle)
            matrixes = Matrix_listing(matrixes_)
            self.outputs['Matrix'].MatrixProperty = str(matrixes)
            #print ('matrix_def', str(matrixes))
    
                
    def update_socket(self, context):
        self.update()


    

def register():
    bpy.utils.register_class(MatrixDeformNode)
    
def unregister():
    bpy.utils.unregister_class(MatrixDeformNode)

if __name__ == "__main__":
    register()