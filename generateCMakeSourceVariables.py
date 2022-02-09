#! /bin/python3
 
import os
import sys
import builtins

# gen cmake helper: format PROJECT_SUB_SOURCES_EXT

# ./generateCMakeSourceVariables.py "input directory" "output directory"

projectRoot = os.path.abspath(sys.argv[1] if sys.argv.__len__() > 1 else ".");
out_dir = os.path.abspath(sys.argv[2] if sys.argv.__len__() > 2 else "cmake/");


projectFolders : list = [
    "boot",
    "kernel/libk",
    "kernel/drivers"
];

enumerateFileTypes = [".asm", ".inc", ".c", ".h"];

def endsWithExt(file : str):
     
    for candidate in enumerateFileTypes: 
        if (file.endswith(candidate)): return True, candidate;

    return False, "";


def getDirectoryInfo():
    info = {};
  
    for dir, _, files in os.walk(projectRoot):
        info[dir] = []

        for file in files:
            info[dir].append(dir + '/' + file);
    
    return info;


def init():
    
    filepaths = {};

    for project in projectFolders: 
        filepaths[project] = {};
        for filetype in enumerateFileTypes: 
            filepaths[project][filetype] = [];

    return filepaths;


def parse():
    container = init();
    dirs = getDirectoryInfo();
    for project in projectFolders:

        for dir in dirs:

            for file in dirs.get(dir):

                if (not dir.startswith(projectRoot + '/' + project)): continue;

                valid, ext = endsWithExt(file);
                if (not valid): continue;

                container.get(project).get(ext).append(file);

    return container;


#set(varname ${varname}
#   path/to/file1
#   path/to/file2
#)
def writeCMakeSourceSection(project: str, extention: str, files: list) -> str:
    cmake_var = project.upper() + '_SOURCE_' + extention[1:].upper();
    content = 'set(' + cmake_var + ' ${' + cmake_var + '}';

    if (len(files) != 0): 
        content += '\n'

    for file in files:
        content += '\t' + file.replace(projectRoot, '${CMAKE_SOURCE_DIR}/' + sys.argv[1]).replace("\\", "/") + "\n";

    return content + ')';


def writeCMakeSourceDocument() -> str:
    cmake_document = "";

    info = parse();

    for project in info:
        for ext in info[project]:
            cmake_document += writeCMakeSourceSection(project.replace("/", "_"), ext, info[project][ext]) + '\n\n';

    return cmake_document;


def writeToFile():
    with open(out_dir + '/sources.cmake', 'wb') as test_file: 
        test_file.write(writeCMakeSourceDocument().encode('utf-8'));


writeToFile();
