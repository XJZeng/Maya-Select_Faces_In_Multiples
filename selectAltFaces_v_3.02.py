import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import os, string, math, re
from os import path, listdir, rename
from string import Template, zfill
from functools import partial

class Get_Sorted_List:
    def __init__(self, start_face):
        self.start_face = start_face
        cmds.select(self.start_face)
        self.start_face_sel = cmds.ls(sl=True)
        self.slice_point = self.start_face_sel[0].find('.')
        self.geom_name = self.start_face_sel[0][:int(self.slice_point)]
        self.ordered_list = [self.start_face]
    
    def get_edges(self, face):
        cmds.select(cmds.polyListComponentConversion( face, ff=True, te=True ))
        return cmds.ls(sl=True, fl=True)
        
            
    
    def sort(self):
        cmds.select(self.geom_name+'.f[*]')
        selection_list = cmds.ls(sl=True, fl=True)
        work_range = len(selection_list)
        selection_list.remove(self.start_face)
        
        for dummy_count in range(len(selection_list)):
            if len(self.ordered_list) <= len(selection_list):
                for dummy_face in selection_list:
                    ordered_edge_list = self.get_edges(self.ordered_list[-1])
                    dummy_face_edge_list = self.get_edges(dummy_face)
                    for dummy_edge in dummy_face_edge_list:
                         if dummy_edge in ordered_edge_list:
                             if dummy_face not in self.ordered_list:
                                  self.ordered_list.append(dummy_face)
                             else:
                                 pass
                         else:
                             pass                             
        return self.ordered_list
                    

class Select_By_Multiple:
    def __init__(self, number, face):
        self.number = number
        try:
            int(self.number)
        except:
            print 'Needs to be a number and not letters!'
            pass

        self.face = face
        sort_list = Get_Sorted_List(self.face)
        sorted_list = sort_list.sort()
        face_selection = list()
        for dummy_key, dummy_val in enumerate(sorted_list):
            if dummy_key%int(self.number) == 0:
                face_selection.append(dummy_val)
            else:
                pass            
        cmds.select(clear = True)
        cmds.select(face_selection)

        
class SelectAlternateFaces():
    def __init__(self, *args):
        window = cmds.window( title="Select Alternate Faces", iconName='SelAF', widthHeight=(200, 80) )
        cmds.columnLayout( adjustableColumn=True )
        cmds.text( label='Enter Multiples', align='left' )
        self.text_box=cmds.textField()
        cmds.button( label='Select By Multiples', command=partial(self.run_cmd, 1) )    
        cmds.setParent( '..' )
        cmds.showWindow( window )
        
                
    def run_cmd(self, *args):
        divider = cmds.textField(self.text_box, text=True, q=True)
        selection = cmds.ls(sl = True)
        Select_By_Multiple(divider, selection[0])

SelectAlternateFaces()
