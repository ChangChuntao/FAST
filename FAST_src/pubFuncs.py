#############################File_Folder##############################
from FAST_Print import PrintGDD


def mkdir(path, isdel=False):
    # Creating a folder
    # If the folder exists and isdel is true, the folder is emptied
    import os
    import shutil
    path = path.strip()
    path = path.rstrip('\\')
    if path == '':
        path = '..'
    isExists = os.path.exists(path)
    if not isExists:
        PrintGDD(path + ' created successfully', 'normal')
        os.makedirs(path)
        return True
    else:
        if isdel:
            shutil.rmtree(path)
        os.makedirs(path)
        PrintGDD(path + ' created successfully', 'normal')
        return False


def EmptyFolder(folder):
    # Empty one folder but do not delete the folder
    import os
    import shutil
    # check whether the input folder exists
    if not os.path.isdir(folder):
        return
    for path in os.listdir(folder):
        path = os.path.join(folder, path)
        if os.path.isfile(path):  # regular file
            os.remove(path)
        elif os.path.isdir(path):  # existing directory
            shutil.rmtree(path)
    return None


def getFileInPath(path):
    import os
    all_file = []
    for f in os.listdir(path):
        f_name = os.path.join(path, f)
        all_file.append(f_name)
    return all_file


def copyFolder(oldFolder, nowFolder):
    import os
    import shutil
    if os.path.isdir(nowFolder):
        shutil.rmtree(nowFolder)
    shutil.copytree(oldFolder, nowFolder)


def modifyFile(file, lineStr, lineNum=None, lineStrFlag=None):
    fileOpen = open(file, 'r+')
    fileLines = fileOpen.readlines()
    fileOpen.close()
    if lineNum is None and lineStrFlag is None:
        raise IOError('LineNum or lineStrFlag is not passed to the function!')
    elif lineNum is not None:
        fileLines[lineNum - 1] = lineStr + '\n'
    elif lineStrFlag is not None:
        for lineNumInFile in range(len(fileLines)):
            if lineStrFlag in fileLines[lineNumInFile]:
                fileLines[lineNumInFile] = lineStr
    fileWrite = open(file, 'w+')
    fileWrite.writelines(fileLines)


def copyFile(ori_file, target):
    import os
    import shutil
    if not os.path.isfile(ori_file):
        raise IOError(ori_file + ' is not file!')
    if os.path.isdir(target):
        shutil.copy(ori_file, target)
    if os.path.isfile(target):
        os.remove(target)
        shutil.copy(ori_file, target)
    else:
        shutil.copy(ori_file, target)


def moveFile(ori_file, target):
    import os
    import shutil
    if not os.path.isfile(ori_file):
        raise IOError(ori_file + ' is not file!')
    if os.path.isdir(target):
        shutil.move(ori_file, target)
    if os.path.isfile(target):
        os.remove(target)
        shutil.move(ori_file, target)
    else:
        shutil.move(ori_file, target)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
