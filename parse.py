#!/usr/bin/env python
# Questions: damir.herman@gmail.com
# Wed Jul  8 18:17:55 PDT 2015

import os
import sys
import re

point_regex = re.compile('(.*)\s+point,?\s+X=\s*(\d+\.?\d*)\s+Y=\s*(\d+\.\d*)\s+Z=\s*(\d+\.?\d*)')

class LayerReader:

    def __init__(self, infile):
        self.infile = infile
        self.fh = open(self.infile)
        self._stack = []

    def __iter__(self):
        return self
    
    def next(self):
        if self.fh.closed:
            raise StopIteration

        for line in self.fh:
            line = line.strip()
            if len(line) == 0: continue
            self._stack.append(line)
            if 'Layer: ' in line:
                record = self._stack[:-1]
                self._stack = [self._stack[-1]]
                #return record
                if 'Layer:' in record[0]:
                    return Layer(record)
                else:
                    continue
        
        record = self._stack
        self.fh.close()
        return Layer(record)
        
class Layer:

    def __init__(self,record):
        self._record = record
        self.handle = self._getHandle()
        self.layer_type, self.layer_name = self._getLayer()
        self.pointLst = self._getPoints()

    def _getHandle(self):
        for r in self._record:
            if 'Handle =' in r:
                ret = r.replace('Handle = ','')
                return ret

    def _getLayer(self):
        l = self._record[0]
        (layer_type, layer_name) = l.split(' Layer: ')
        layer_name = layer_name.replace('"','')
        layer_type = layer_type.strip()
        return (layer_type, layer_name)

    def _getPoints(self):
        ret = []
        for l in self._record:
            if 'point' in l:
                z = Point(l)
                ret.append(z)
        return ret

class Point:

    def __init__(self, line):
        self.what, self.X, self.Y, self.Z = point_regex.search(line).groups()

def print_details(input_file):
    for layer in LayerReader(input_file):
        print '\nHandle: %s' % (layer.handle,)
        print 'Layer Name: %s' % (layer.layer_name,)
        print 'Layer Type: %s' % (layer.layer_type,)
        for i, point in enumerate(layer.pointLst):
            print '  %2d: %s: X = %s Y = %s Z = %s' % (i+1, point.what, point.X, point.Y, point.Z)

def print_table(input_file):

    for i, layer in enumerate(LayerReader(input_file)):
        if i == 0:
            header = ['Handle', 'Layer Name', 'Layer Type', 'No', 'Wtf', 'X', 'Y', 'Z']
            print '\t'.join(header)
        layer_out = [layer.handle, layer.layer_name, layer.layer_type]
        for i, point in enumerate(layer.pointLst):
            line_out = []
            line_out.extend(layer_out)
            line_out.extend([str(i+1),point.what,point.X,point.Y,point.Z])
            print '\t'.join(line_out)

if __name__ == '__main__':
    # Before you feed the input file on the command-line, run
    # textutil -convert txt test.rtf
    input_file = sys.argv[1]

    #print_details(input_file)
    print_table(input_file)