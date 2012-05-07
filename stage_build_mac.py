#!/usr/bin/env python
'''
Created on Apr 15, 2012

@author: Magnus Knutas
'''

import shutil
import sys
import getopt
import os
import glob

verbose = False

help_message = '''
Usage: build_mac.py [options]

Options:
    --run                    Start app with "open ./dist/Unknown Horizons.app" when done (all is cleaned before this)
    --fife-dir=<Location>    Location of FIFE-trunk
    --python-bin=<Location>  For people with a lot of python
    --verbose                Just as it sounds :) will output more info
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def setup(fife_dir):
    """
    Setup files and directories
    """
    if verbose: print "Setting up environment"
    # If these two exists we remove them for a clean build
    if os.path.exists('./build'):
        if verbose: print "Cleaning build path"
        shutil.rmtree('./build')
    if os.path.exists('./dist'):
        if verbose: print "Cleaning dist path"
        shutil.rmtree('./dist')
    
    if verbose: print "Create src directory"
    # The source files, for building app correctly
    os.mkdir('./src/')
    os.mkdir('./src/Contents/')
    os.mkdir('./src/Contents/Resources/')
    
    #Copy fife and content
    if verbose: print "Copying Icon.icns"
    shutil.copy('./content/gui/icons/Icon.icns','./src/Contents/Resources/')
    
    if verbose: print "Copying fife source from "+fife_dir+"engine/python/fife"
    while shutil.copytree(fife_dir+'engine/python/fife', './fife'):
        if verbose: print "..."
    
    if verbose: print "Copying content into src"
    while shutil.copytree('./content', './src/Contents/Resources/content'):
        if verbose: print "..."
    
def tearDown(run):
    shutil.rmtree('./src/')
    shutil.rmtree('./fife')
    
    #Remove some other styff
    files = glob.glob('*.egg')
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
        else:
            shutil.rmtree(f)
    
    #If the -r or --run arg is passed we start the app after build
    if run:
        os.popen("open ./dist/Unknown\ Horizons.app")

def build(pyver):
    os.system(pyver+" setup.py build_i18n")
    os.system(pyver+" setup_mac.py py2app")

def main(argv=None):
    fife_dir = False
    pyver = "/usr/bin/python"
    run = False
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hfp:rv", ["help", "fife-dir=", "python-bin=", "run", "--verbose"])
        except getopt.error, msg:
            raise Usage(msg)
        
        
        # option processing
        for option, value in opts:
            if option in ("-p","--python-bin",):
                pyver = value
            if option in ("-f","--fife-dir",):
                fife_dir = value
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-r","--run",):
                run = True
            if option in ("-v","--verbose",):
                verbose = True
        
        #We got to have the fife source!!!!!
        if not fife_dir:
            raise Usage(help_message)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2
    
    setup(fife_dir)
    build(pyver)
    tearDown(run)
    
if __name__ == "__main__":
    sys.exit(main())