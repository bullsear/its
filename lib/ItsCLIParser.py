"""ItsCLIParser.py - Parse CLI Output
NAME:
    ItsCLIParser.py - Parse CLI Output
"""

import os, sys, re
import ItsException

class ItsCLIParser ():
    
    def __init__( self ):
        pass
    
    def parseTable ( self, string, rowLength=None, matchIndex=None, matchString=None ):
        table = []        
        lines = re.split( "\n", string )
        for line in lines:
            line = re.sub( '\s+', ' ', line )        # Replace redundant space characters with one space
            fields =  re.split( "\s", line )         # Split on space
            if len( fields[0] ) == 0:                # Remove leading empty string
                fields.pop(0)
            # Accumulate rows of the correct length with the correct value in the correct field
            #if len( fields ) == rowLength and fields[matchIndex] == matchString: 
            if len( fields ) == rowLength and re.search( matchString, fields[matchIndex] ):
               table.append( fields )
        return table

    def parseTableFieldList ( self, string, rowLength=None, matchIndex=None, matchString=None ):
        table = []        
        lines = re.split( "\n", string )
        for line in lines:
            line = re.sub( '\s+', ' ', line )        # Replace redundant space characters with one space
            fields =  re.split( "\s", line )         # Split on space
            if len( fields[0] ) == 0:                # Remove leading empty string
                fields.pop(0)
            if len( fields ) == rowLength and re.search( matchString, fields[matchIndex] ):
               table.append( fields[matchIndex] )
        return table
    
    def grepTable ( self, string, matchString=None ):
        table = []        
        lines = re.split( "\n", string )        
        for line in lines:
            if re.search( matchString, line ):
                table.append( line )
        return table

    
