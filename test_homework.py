# Tests provided for the tool.

# Verbose, with stdout, filter by test name
# pytest -vv -s . -k 'test_some_name'
# Quiet, show summary in the end
# pytest -q -rapP
# Verbose, with stdout, show summary in the end
# pytest -s -vv -q -rapP
#
from contextlib import closing
from glob import glob
from hashlib import md5
from itertools import chain
from os import environ, getpgid, killpg, makedirs, mkdir, remove, setsid, walk
from os.path import exists, getsize, isfile, join, sep
from shutil import copytree, rmtree
from signal import SIGKILL, SIGTERM
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from subprocess import Popen, TimeoutExpired
from sys import argv, stderr, stdout
from time import sleep
from unittest import TestCase

ASSERT_TIMEOUT = 20
ASSERT_STEP = 1.0
SHUTDOWN_TIMEOUT = 0.2

SERVER_PATH = "/tmp/arlosync/server"
CLIENT_PATH = "/tmp/arlosync/client"

makedirs(SERVER_PATH, exist_ok=True)
makedirs(CLIENT_PATH, exist_ok=True)

SERVER_CMD = (
    "python3 -m arlosync.server {path} --port={port} "
    "--sync_wait_sec=0.5"  # Up the sync frequency for the tests.
)
CLIENT_CMD = "python3 -m arlosync.client {path} --port={port}"


def find_free_port():
    with closing(socket(AF_INET, SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s.getsockname()[1]


def spit(filename, data):
    """Save data into the given filename."""
    with open(filename, "w") as file_:
        file_.write(data)


def reset_path(path):
    """Remove directory recursively and recreate again (empty)."""
    if exists(path):
        rmtree(path)
    mkdir(path)


def sync_paths(source_path, dest_path):
    """Sync paths so that they contain exactly the same set of files."""
    files = chain(glob(join(dest_path, "*")), glob(join(dest_path, ".*")))
    for filename in files:
        if isfile(filename):
            remove(filename)
        else:
            rmtree(filename)
    if exists(dest_path):
        rmtree(dest_path)
    copytree(source_path, dest_path)


def get_md5(filename):
    if not isfile(filename):
        return "0"
    hash_md5 = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def path_content_to_string(path):
    """Convert contents of a directory recursively into a string for easier comparison."""
    lines = []
    prefix_len = len(path + sep)
    for root, dirs, files in walk(path):
        for dir_ in dirs:
            full_path = join(root, dir_)
            relative_path = full_path[prefix_len:]
            size = 0
            type_ = "dir"
            hash_ = "0"
            line = "{},{},{},{}".format(relative_path, type_, size, hash_)
            lines.append(line)

        for filename in files:
            full_path = join(root, filename)
            relative_path = full_path[prefix_len:]
            size = getsize(full_path)
            type_ = "file" if isfile(full_path) else "dir"
            hash_ = get_md5(full_path)
            line = "{},{},{},{}".format(relative_path, type_, size, hash_)
            lines.append(line)

    lines = sorted(lines)
    return "\n".join(lines)


def assert_paths_in_sync(path1, path2, timeout=ASSERT_TIMEOUT, step=ASSERT_STEP):
    current_time = 0
    while current_time < timeout:
        contents1 = path_content_to_string(path1)
        contents2 = path_content_to_string(path2)
        if contents1 == contents2:
            return
        sleep(step)
        current_time += step
    assert current_time >= timeout, "we should always go around the loop at least once"
    assert contents1 == contents2


class Process:
    def __init__(self, cmd_line):
        self.cmd_line = cmd_line

    def __enter__(self):
        print("Starting ", self.cmd_line)
        self._process = Popen(
            self.cmd_line, shell=True, preexec_fn=setsid, stdout=stdout, stderr=stderr
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()

    def shutdown(self):
        killpg(getpgid(self._process.pid), SIGTERM)
        try:
            self._process.wait(SHUTDOWN_TIMEOUT)
        except TimeoutExpired:
            killpg(getpgid(self._process.pid), SIGKILL)
        sleep(2.0)


class TestBasic(TestCase):
    def run(self, result=None):
        port = find_free_port()
        self.spath = SERVER_PATH
        self.cpath = CLIENT_PATH
        reset_path(self.spath)
        reset_path(self.cpath)
        assert_paths_in_sync(self.cpath, self.spath)
        self.server_cmd = SERVER_CMD.format(port=port, path=self.spath)
        self.client_cmd = CLIENT_CMD.format(port=port, path=self.cpath)
        print(self.server_cmd)
        print(self.client_cmd)
        with Process(self.client_cmd), Process(self.server_cmd):
            sleep(0.5)
            super().run(result)

    def test_add_single_file(self):
        spit(join(self.cpath, "newfile.txt"), "contents")
        assert_paths_in_sync(self.cpath, self.spath)

    def test_single_file_completely_changes_3_times(self):
        spit(join(self.cpath, "newfile.txt"), "contents")
        assert_paths_in_sync(self.cpath, self.spath)

        spit(join(self.cpath, "newfile.txt"), "contents more")
        assert_paths_in_sync(self.cpath, self.spath)

        spit(join(self.cpath, "newfile.txt"), "beginning contents more")
        assert_paths_in_sync(self.cpath, self.spath)

        spit(join(self.cpath, "newfile.txt"), "new content")
        assert_paths_in_sync(self.cpath, self.spath)

    def test_single_file_change_and_remove(self):
        spit(join(self.cpath, "newfile.txt"), "contents")
        assert_paths_in_sync(self.cpath, self.spath)

        remove(join(self.cpath, "newfile.txt"))
        assert_paths_in_sync(self.cpath, self.spath)

    def test_add_empty_dir(self):
        mkdir(join(self.cpath, "newemptydir"))
        assert_paths_in_sync(self.cpath, self.spath)

    def test_add_and_remove_empty_dir(self):
        mkdir(join(self.cpath, "newemptydir"))
        assert_paths_in_sync(self.cpath, self.spath)

        rmtree(join(self.cpath, "newemptydir"))
        assert_paths_in_sync(self.cpath, self.spath)

    def test_3_new_files_1mb_each_add_instantly(self):
        spit(join(self.cpath, "file1.txt"), "*" * 10 ** 6)
        spit(join(self.cpath, "file2.txt"), "*" * 10 ** 6)
        spit(join(self.cpath, "file3.txt"), "*" * 10 ** 6)
        assert_paths_in_sync(self.cpath, self.spath)

    def test_3_new_files_1mb_each_add_with_delay(self):
        spit(join(self.cpath, "file1.txt"), "*" * 10 ** 6)
        sleep(1.0)
        spit(join(self.cpath, "file2.txt"), "*" * 10 ** 6)
        sleep(1.0)
        spit(join(self.cpath, "file3.txt"), "*" * 10 ** 6)
        assert_paths_in_sync(self.cpath, self.spath)

    def test_single_file_change_1_byte_beginning(self):
        spit(join(self.cpath, "file1.txt"), "0" + "*" * 10 ** 6)
        sleep(1.0)
        assert_paths_in_sync(self.cpath, self.spath)

        spit(join(self.cpath, "file1.txt"), "1" + "*" * 10 ** 6)
        sleep(1.0)
        assert_paths_in_sync(self.cpath, self.spath)

    def test_1_empty_file(self):
        spit(join(self.cpath, "file1.txt"), "")
        assert_paths_in_sync(self.cpath, self.spath)

    def test_3_empty_files_add_instantly(self):
        spit(join(self.cpath, "file1.txt"), "")
        spit(join(self.cpath, "file2.txt"), "")
        spit(join(self.cpath, "file3.txt"), "")
        assert_paths_in_sync(self.cpath, self.spath)

    def test_3_empty_files_add_with_delay(self):
        spit(join(self.cpath, "file1.txt"), "")
        sleep(1.0)
        spit(join(self.cpath, "file2.txt"), "")
        sleep(1.0)
        spit(join(self.cpath, "file3.txt"), "")
        assert_paths_in_sync(self.cpath, self.spath)

    def test_1_file_grows_twice_with_delay(self):
        sleep(1.0)
        spit(join(self.cpath, "file1.txt"), "*" * 10 ** 6)
        assert_paths_in_sync(self.cpath, self.spath)
        sleep(1.0)
        spit(join(self.cpath, "file1.txt"), "*" * 20 ** 6)
        sleep(1.0)
        assert_paths_in_sync(self.cpath, self.spath)

    def test_1_file_shrinks_twice_with_delay(self):
        spit(join(self.cpath, "file1.txt"), "*" * 20 ** 6)
        assert_paths_in_sync(self.cpath, self.spath)
        sleep(1.0)
        spit(join(self.cpath, "file1.txt"), "*" * 10 ** 6)
        assert_paths_in_sync(self.cpath, self.spath)


class TestInitialSync(TestCase):
    def setUp(self):
        self.spath = SERVER_PATH
        self.cpath = CLIENT_PATH
        reset_path(self.spath)
        reset_path(self.cpath)
        port = find_free_port()
        self.server_cmd = SERVER_CMD.format(port=port, path=self.spath)
        self.client_cmd = CLIENT_CMD.format(port=port, path=self.cpath)
        print(self.server_cmd)
        print(self.client_cmd)

    def test_one_file(self):
        spit(join(self.cpath, "newfile.txt"), "contents")

        with Process(self.client_cmd), Process(self.server_cmd):
            sleep(1.0)
            assert_paths_in_sync(self.cpath, self.spath)

    def test_file_and_empty_dir(self):
        spit(join(self.cpath, "newfile.txt"), "contents")
        mkdir(join(self.cpath, "newemptydir"))

        with Process(self.client_cmd), Process(self.server_cmd):
            sleep(1.0)
            assert_paths_in_sync(self.cpath, self.spath)
