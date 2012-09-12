"""Contains a class and utilities to manipulate an axis-aligned bounding box.
Python Version: 2.7.3
Author: Matthew McMullan
"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------

# 3'rd Party Imports ------------------------------------------------

# Local Application/Library Specific Imports ------------------------

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

# Axis-Aligned Bounding Box
class AABB():
    def __init__(self,raw):
        split = raw.split(',')
        self.left = int(split[0])
        self.top = int(split[1])
        self.width = int(split[2])
        self.height = int(split[3])
    def __str__(self):
        return '{ left: ' + str(self.left) + ' top: ' + str(self.top) + \
                ' width: ' + str(self.width) + ' height: ' + str(self.height) \
                + '}'
    def __eq__(self, other):
        return self.left==other.left and self.top==other.top and \
                self.width==other.width and self.height==other.height
    def __ne__(self, other):
        return not self.__eq__(other)
