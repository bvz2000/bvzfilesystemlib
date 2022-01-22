import os
import re


# ----------------------------------------------------------------------------------------------------------------------
def count_files_recursively(dir_d):
    """
    Given a directory, returns the number of files in that directory AND all subdirectories. Does not include the
    actual subdirectories in the count. Just the files they contain.

    :param dir_d:
            The directory to count.

    :return:
            In integer of the number of files found.
    """

    assert type(dir_d) is str

    if not os.path.exists(dir_d):
        raise ValueError(f"{dir_d} does not exist.")
    if not os.path.isdir(dir_d):
        raise ValueError(f"{dir_d} is not a directory.")

    return sum(len(files) for x, y, files in os.walk(dir_d))


# ----------------------------------------------------------------------------------------------------------------------
def invert_dir_list(parent_d,
                    subdirs_n,
                    pattern=None):
    """
    Given a parent directory and a list of directory names, returns any other directories in this parent dir that are
    NOT in this list (effectively inverting the list of subdirectories).

    :param parent_d:
            The directory containing the sub-dirs we are trying to invert.
    :param subdirs_n:
            A list of subdirectories that are the inverse of the ones we want to return.
    :param pattern:
            An optional regex pattern to limit our inverse to. If None, then all subdirectories will be included.
            Defaults to None.

    :return:
            A list of all subdirectories in parent_d that are not in the list subdirs_n.
    """

    assert type(subdirs_n) is list
    assert pattern is None or type(pattern) is str

    if not os.path.exists(parent_d):
        raise ValueError(f"{parent_d} does not exist.")
    if not os.path.isdir(parent_d):
        raise ValueError(f"{parent_d} is not a directory.")

    items_n = os.listdir(parent_d)
    output = list()

    for item_n in items_n:
        if os.path.isdir(os.path.join(parent_d, item_n)):
            if item_n not in subdirs_n:
                result = True
                if pattern:
                    result = re.match(pattern, item_n)
                if result:
                    output.append(item_n)

    return output


# ----------------------------------------------------------------------------------------------------------------------
def convert_unix_path_to_os_path(path):
    """
    Given a path string (in a unix-like path format), converts it into an OS appropriate path format. Note, it does not
    check to see whether this path exists. It merely re-formats the string into the OS specific format.

    :param path:
            The path string to be reformatted.

    :return:
            An OS appropriate path string.
    """

    assert type(path) is str

    return os.path.join(*path.lstrip("/").split("/"))


# ----------------------------------------------------------------------------------------------------------------------
# TODO: Make windows friendly
def symlinks_to_real_paths(symlinks_p):
    """
    Given a list of symbolic link files, return a list of their real paths. Only
    works on Unix-like systems for the moment.

    :param symlinks_p:
            A symlink or list of symlinks. If a file in this list is not a symlink, its path will be included unchanged.
            If a file in this list does not exist, it will be treated as though it is not a symlink. Accepts either a
            path to a symlink or a list of paths.

    :return:
            A list of the real paths being pointed to by the symlinks.
    """

    assert type(symlinks_p) is list or type(symlinks_p) is str

    if type(symlinks_p) != list:
        symlinks_p = list(symlinks_p)

    output = list()

    for symlink_p in symlinks_p:
        output.append(os.path.realpath(symlink_p))
    return output


# ----------------------------------------------------------------------------------------------------------------------
def recursively_list_files_in_dirs(source_dirs_d):
    """
    Recursively list all the files in the directory or directories

    :param source_dirs_d:
            The directory or list of directories we want to recursively list. Accepts either a string or a list.

    :return:
            A list of files with full paths that are in any of the directories (or any of their subdirectories)
    """

    assert type(source_dirs_d) is list or type(source_dirs_d) is str

    if type(source_dirs_d) is str:
        source_dirs_d = [source_dirs_d]

    for source_dir_d in source_dirs_d:
        if not os.path.exists(source_dir_d):
            raise ValueError(f"{source_dir_d} does not exist.")
        if not os.path.isdir(source_dir_d):
            raise ValueError(f"{source_dir_d} is not a directory.")

    output = list()

    for source_dir_d in source_dirs_d:
        for dir_d, sub_dirs_n, files_n in os.walk(source_dir_d):
            for file_n in files_n:
                output.append(os.path.join(dir_d, dir_d, file_n))
    return output


# ----------------------------------------------------------------------------------------------------------------------
def recursively_list_symlink_targets_in_dirs(source_dirs_d):
    """
    Recursively list all of the symlink targets of all the files in the directory or directories.

    :param source_dirs_d:
                The directory or list of directories we want to recursively list. Accepts either a string or a list.

    :return:
            A list of files with full paths that are in any of the directories (or any of their subdirectories)
    """

    assert type(source_dirs_d) is list or type(source_dirs_d) is str

    if type(source_dirs_d) is str:
        source_dirs_d = [source_dirs_d]

    for source_dir_d in source_dirs_d:
        if not os.path.exists(source_dir_d):
            raise ValueError(f"{source_dir_d} does not exist.")
        if not os.path.isdir(source_dir_d):
            raise ValueError(f"{source_dir_d} is not a directory.")

    output = list()

    files_p = recursively_list_files_in_dirs(source_dirs_d)
    for file_p in files_p:
        if os.path.islink(file_p) and os.path.exists(file_p):
            output.append(os.readlink(file_p))

    return output


# ----------------------------------------------------------------------------------------------------------------------
def add_file_to_dict_by_size(file_p,
                             dict_files_by_size):
    """
    Given a file path, adds it to the dictionary keyed by file size.

    :param file_p:
            The path of the file to add to the dictionary.
    :param dict_files_by_size:
            The dictionary that contains the files keyed by file sizes.

    :return:
            Nothing.
    """

    assert type(file_p) is str
    assert type(dict_files_by_size) is dict

    if not os.path.exists(file_p):
        raise ValueError(f"{file_p} does not exist.")
    if os.path.isdir(file_p):
        raise ValueError(f"{file_p} is a directory. Should be a file.")

    file_size = os.path.getsize(file_p)
    if file_size not in dict_files_by_size.keys():
        dict_files_by_size[file_size] = [file_p]
    else:
        existing_files = dict_files_by_size[file_size]
        existing_files.append(file_p)
        dict_files_by_size[file_size] = existing_files


# ----------------------------------------------------------------------------------------------------------------------
def dir_files_keyed_by_size(path_d):
    """
    Builds a dictionary of file sizes in a directory. The key is the file size, the value is a list of file names.

    :param path_d:
            The dir that contains the files we are evaluating. Does not traverse into subdirectories.

    :return:
            A dict where the key is the file size, the value is a list of paths to the files of this size.
    """

    assert type(path_d) is str

    if not os.path.exists(path_d):
        raise ValueError(f"{path_d} does not exist.")
    if not os.path.isdir(path_d):
        raise ValueError(f"{path_d} is not a directory.")

    output = dict()

    files_n = os.listdir(path_d)
    for file_n in files_n:
        file_p = os.path.join(path_d, file_n)
        add_file_to_dict_by_size(file_p, output)
    return output


# ----------------------------------------------------------------------------------------------------------------------
def is_root(path_p):
    """
    Returns True if the path given is the root of the filesystem.

    :param path_p:
            The path we are testing to see if it is the root path.

    :return:
            True if path_p is the root of the filesystem.
    """

    root = os.path.abspath(os.sep)
    return path_p == root


# ----------------------------------------------------------------------------------------------------------------------
def ancestor_contains_file(path_p,
                           files_n,
                           depth=None):
    """
    Returns the path of any parent directory (evaluated recursively up the hierarchy) that contains any of the files in
    the list: files_n. This is typically used to see if any parent directory contains a semaphore file.

    For example: If your current path (where "current" just means some path you want to start inspecting its ancestors)
                 is /this/is/my/path, and you want to see if any of the parent paths contain a specific file named:
                 '.asset', then this method will allow you to do that.

    :param path_p:
            The path we are testing.
    :param files_n:
            A file name or a list of file names we are looking for. Accepts both a string and a list.
    :param depth:
            Limit the number of levels up to look. If None, then the search will continue all the way up to the root
            level. Defaults to None.

            For example: a depth of 1 will only check the immediate parent of the given path. 2 will check the immediate
            parent and its parent. Searches will never progress "past" the root, regardless of depth.

    :return:
            The path of the first parent that contains any one of these files. If no ancestors contain any of these
            files, returns None.
    """

    assert type(path_p) is str
    assert type(files_n) is str or type(files_n) is list
    assert depth is None or type(depth) is int

    if not os.path.exists(path_p):
        raise ValueError(f"{path_p} does not exist.")
    if not os.path.isdir(path_p):
        raise ValueError(f"{path_p} is not a directory.")

    if type(files_n) != list:
        files_n = [files_n]

    path_p = path_p.rstrip(os.path.sep)

    if not os.path.isdir(path_p):
        path_p = os.path.dirname(path_p)

    already_at_root = False
    count = 0

    test_p = os.path.dirname(path_p)
    while True:

        # Check each of the test files.
        for file_n in files_n:
            if os.path.exists(os.path.join(test_p, file_n)):
                return test_p

        # If nothing is found, move up to the next parent dir.
        test_p = os.path.dirname(test_p)

        # Increment the count and bail if we have hit our max depth.
        count += 1
        if depth and count >= depth:
            return None

        # Check to see if we are at the root level (bail if we are)
        if is_root(os.path.dirname(test_p)):
            if already_at_root:
                return None
            already_at_root = True


# ----------------------------------------------------------------------------------------------------------------------
# TODO: Actually make this work. Does nothing at the moment
def lock_dir(path_d):
    """
    Changes the permissions on a directory so that it is readable and executable, but may not be otherwise altered.

    :param path_d:
            The path to the directory we want to lock.

    :return:
            Nothing.
    """

    assert type(path_d) is str

    if not os.path.exists(path_d):
        raise ValueError(f"{path_d} does not exist.")
    if not os.path.isdir(path_d):
        raise ValueError(f"{path_d} is not a directory.")


# ----------------------------------------------------------------------------------------------------------------------
# TODO: Actually make this work. Does nothing at the moment
def lock_file(path_p):
    """
    Changes the permissions on a file so that it is readable and executable, but may not be otherwise altered.

    :param path_p:
            The path to the file we want to lock.

    :return:
            Nothing.
    """

    assert type(path_p) is str

    if not os.path.exists(path_p):
        raise ValueError(f"{path_p} does not exist.")
    if not os.path.isfile(path_p):
        raise ValueError(f"{path_p} is not a file.")


# ----------------------------------------------------------------------------------------------------------------------
# TODO: make this windows friendly
def symlink_source_is_in_dir(link_p,
                             path_d,
                             include_subdirs=True) -> bool:
    """
    Returns True if the source file of the given link is in a directory or any of its subdirectories (depending on
    options). Does not care if the source path does not actually exist or not.

    :param link_p:
            The full path to the symlink to be evaluated.
    :param path_d:
            The directory we are checking to see if the symlink source is inside of.
    :param include_subdirs:
            Whether we should also consider being in a subdirectory of the above directory as "being in" this
            directory. Defaults to True

    :return:
            True if the source file of the symlink is in the passed directory (or any subdirectory if include_subdirs is
            True). False otherwise.
    """

    assert type(link_p) is str
    assert type(path_d) is str
    assert type(include_subdirs) is bool

    if not os.path.islink(link_p):
        raise ValueError(f"{link_p} is not a symlink.")

    source_d, source_n = os.path.split(symlinks_to_real_paths(link_p)[0])

    if include_subdirs:
        return source_d.startswith(path_d)
    return source_d == path_d
