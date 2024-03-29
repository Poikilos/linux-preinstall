#!/usr/bin/env python
'''
This is deprecated.
You must use LBRY-Flatpak.sh, because:
- The page blocks this application.
- This application makes a new icon for every version.
- If you click "Yes" to upgrade LBRY using its own upgrade system, the
  icon created by this application will no longer work since it points
  to the old version and the updater removes the old version.
'''
from __future__ import print_function
import sys
import os
import platform
sys.stderr.write(__doc__)
sys.stderr.flush()
sys.exit(1)

if sys.version_info.major >= 3:
    import urllib.request
    request = urllib.request
else:
    # Python 2
    import urllib2 as urllib
    request = urllib

if sys.version_info.major >= 3:
    from html.parser import HTMLParser
else:
    # Python 2
    from HTMLParser import HTMLParser

profile_path = os.environ['HOME']
if platform.system() == "Windows":
    profile_path = os.environ['USERPROFILE']
repos_path = os.path.join(profile_path, "git")
lp_repo_path = os.path.join(repos_path, "linux-preinstall")
includes_path = os.path.join(lp_repo_path, "utilities")

if not os.path.isdir(includes_path):
    print("{} is missing.".format(includes_path))
    exit(1)
sys.path.insert(0, includes_path)

from install_any import install_program_in_place


# create a subclass and override the handler methods
class LBRYDownloadPageParser(HTMLParser):
    """
    This is based on DownloadPageParser from blendernightly
    """
    def __init__(self, meta):
        # avoid "...instance has no attribute rawdata":
        #   Old way:
        #     HTMLParser.__init__(self)
        #   On the next commented line, python2 would say:
        #       "argument 1 must be type, not classobj"
        #     super(LBRYDownloadPageParser, self).__init__()
        if sys.version_info.major >= 3:
            super().__init__()
            # print("Used python3 super syntax")
        else:
            # python2
            HTMLParser.__init__(self)
            # print("Used python2 super syntax")

        self.urls = []
        self.verbose = False
        self.must_contain = None
        self.release_version = "2.83"  # find href /download//blender-*
        self.meta = meta
        self.tag = None
        self.tag_stack = []
        self.archive_categories = {}  # based on install_any.py
        self.archive_categories["tar"] = [".tar.bz2", ".tar.gz",
                                          ".tar.xz"]
        self.archive_categories["zip"] = [".zip"]
        self.archive_categories["dmg"] = [".dmg"]
        self.extensions = []
        for category, endings in self.archive_categories.items():
            self.extensions.extend(endings)
        self.closers = ["-glibc"]
        self.openers = ["blender-"]
        self.remove_this_dot_any = ["-10."]
        # Linux, Darwin, or Windows:
        platform_system = platform.system()
        self.os_name = platform_system.lower()
        self.platform_flag = None
        self.release_arch = "linux64"
        self.os_flags = {"Win64": "windows", "Win32": "windows",
                         "linux": "linux", "OSX": "macos"}
        if self.os_name == "darwin":
            self.os_name = "macos"  # change to Blender build naming
            # parent css class of section (above ul): "platform-macOS"
            self.platform_flag = "OSX"
            self.release_arch = "macOS"  # macOS, formerly x86_64
        elif self.os_name == "windows":
            # parent css class of section (above ul): "platform-win"
            self.platform_flag = "windows64"
            self.release_arch = "windows64"
            # self.release_arch = "win32"
        elif self.os_name == "linux":
            # parent css class of section (above ul): "platform-linux"
            self.platform_flag = "linux"
            self.release_arch = "linux64"  # formerly x86_64
            # self.release_arch = "i686"
        else:
            print("WARNING: unknown system '" + platform_system + "'")

        self.os_release = platform.release()
        self.dl_os_name = None

    def handle_decl(self, decl):
        self.urls = []
        print("CLEARED dl list since found document decl: " + decl)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "html":
            self.urls = []
            print("CLEARED dl list since found <html...")
            # print("Links:  # with '" + str(self.must_contain) + "'")
        if self.verbose:
            print(" " * len(self.tag_stack) + "push: " + str(tag))
        self.tag_stack.append(tag)
        # attrs is an array of (name, value) tuples:
        attr_d = dict(attrs)
        href = attr_d.get("href")
        if href is not None:
            if (self.must_contain is None) or (self.must_contain in href):
                # print("  - " + href)
                self.urls.append(href)
            else:
                pass
                # print("#  - " + href)
        if self.verbose:
            # print(" " * len(self.tag_stack) + "attrs: " + str(attrs))
            print(" " * len(self.tag_stack) + "attr_d: " + str(attr_d))

        self.tag = tag

    def handle_endtag(self, tag):
        if tag.lower() != self.tag_stack[-1].lower():
            found = None
            for i in range(1, len(self.tag_stack)+1):
                if tag.lower() == self.tag_stack[-i].lower():
                    found = i
                    break
            if found is not None:
                for i in range(found, len(self.tag_stack)+1):
                    if self.verbose:
                        print(" " * len(self.tag_stack) +
                              "unwind: (" + self.tag_stack[-1] +
                              " at ) " + str(tag))
                    self.tag_stack.pop()
            else:
                if self.verbose:
                    print(" " * len(self.tag_stack) + "UNEXPECTED: " +
                          str(tag))
        else:
            self.tag_stack.pop()
            if self.verbose:
                print(" " * len(self.tag_stack) + ":" + str(tag))

    def handle_data(self, data):
        if self.verbose:
            print(" " * len(self.tag_stack) + "data:" + str(data))

    def id_from_name(self, filename, remove_arch=True,
                     remove_win_arch=False, remove_ext=False,
                     remove_openers=True, remove_closers=True):
        only_v = self.release_version
        only_p = self.platform_flag
        only_a = self.release_arch
        ret = filename
        if remove_openers:
            for opener in self.openers:
                # ret = ret.replace(opener, "")
                o_i = ret.find(opener)
                if o_i == 0:
                    ret = ret[len(opener):]
        # only remove platform and arch if not Windows since same
        # (only way to keep them & allow installing 64&32 concurrently)
        if only_p is not None:
            if remove_win_arch or ("win" not in only_p.lower()):
                ret = ret.replace("-"+only_p, "")
        if only_a is not None:
            if remove_win_arch or ("win" not in only_a.lower()):
                ret = ret.replace("-"+only_a, "")
        if remove_closers:
            for closer in self.closers:
                c_i = ret.find(closer)
                if c_i > -1:
                    next_i = -1
                    dot_i = ret.find(".", c_i+1)
                    hyphen_i = ret.find("-", c_i+1)
                    if dot_i > -1:
                        next_i = dot_i
                    if hyphen_i > -1:
                        if next_i > -1:
                            if hyphen_i < next_i:
                                next_i = hyphen_i
                        else:
                            next_i = hyphen_i
                    if next_i > -1:
                        # don't remove extension or other chunks
                        ret = ret[:c_i] + ret[next_i:]
                    else:
                        ret = ret[:c_i]
                    break
        for rt in self.remove_this_dot_any:
            for i in range(0, 99):
                osx = rt + str(i)
                ext_i = ret.find(osx)
                if ext_i > -1:
                    ret = ret[:ext_i]
                    break
        if remove_ext:
            for ext in self.extensions:
                ext_i = ret.find(ext)
                if ext_i > -1:
                    ret = ret[:ext_i]
        return ret

    def id_from_url(self, url, remove_arch=True,
                    remove_win_arch=False, remove_ext=False,
                    remove_openers=True, remove_closers=True):
        filename = name_from_url(url)
        return self.id_from_name(
            filename,
            remove_arch=remove_arch,
            remove_win_arch=remove_win_arch,
            remove_ext=remove_ext,
            remove_openers=remove_openers,
            remove_closers=remove_closers
        )

    def blender_tag_from_url(self, url):
        tag_and_commit = self.id_from_url(url, remove_ext=True)
        h_i = tag_and_commit.find("-")
        version_s = tag_and_commit
        if h_i > -1:
            version_s = tag_and_commit[:h_i]
        return version_s

    def blender_commit_from_url(self, url):
        tag_and_commit = self.id_from_url(url, remove_ext=True)
        h_i = tag_and_commit.find("-")
        commit_s = tag_and_commit
        if h_i > -1:
            commit_s = tag_and_commit[h_i+1:]
        return commit_s


class LBRYLinkManager:
    """
    Based on DownloadManager from https://github.com/Hierosoft/hierosoft
    (formerly LinkManager from blendernightly) and relicensed by
    author.
    """

    def __init__(self):
        self.meta = {}
        self.html_url = "https://lbry.com/linux"
        self.parser = LBRYDownloadPageParser(self.meta)
        self.profile_path = profile_path

    def get_urls(self, verbose=False, must_contain=None):
        # self.parser.urls = []  # done automatically on BODY tag
        if sys.version_info.major >= 3:
            try:
                response = request.urlopen(self.html_url)
            except urllib.error.HTTPError as e:
                print("Opening {}".format(e))
                return None
        else:
            try:
                response = urllib.urlopen(self.html_url)
            except urllib.error.HTTPError as e:
                print("Opening {}".format(e))
                return None
        dat = response.read()
        self.parser.must_contain = must_contain
        self.parser.verbose = verbose
        # print("GOT:" + dat)
        # Decode dat to avoid error on Python 3:
        #   htmlparser self.rawdata  = self.rawdata + data
        #   TypeError: must be str not bytes
        self.parser.feed(dat.decode("UTF-8"))
        return self.parser.urls

    def download(self, file_path, url, cb_progress=None, cb_done=None,
                 chunk_size=16*1024, evt=None):
        response = request.urlopen(url)
        if evt is None:
            evt = {}
        evt['loaded'] = 0
        # evt['total'] is not implemented (would be from contentlength
        # aka content-length)
        with open(file_path, 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                evt['loaded'] += chunk_size
                if cb_progress is not None:
                    cb_progress(evt)
                f.write(chunk)
        if cb_done is not None:
            cb_done(evt)

    def get_downloads_path(self):
        return os.path.join(self.profile_path, "Downloads")


shown_progress = 0


def d_progress(evt):
    global shown_progress
    # global pbar
    if evt['loaded'] - shown_progress > 1000000:
        shown_progress = evt['loaded']
        # pbar['value'] = evt['loaded']
        amt_s = str(int(evt['loaded']/1024/1024)) + "MB         "
        sys.stderr.write("\rDownloading..." + amt_s)
        # evt['total'] is not implemented
        # count_label.config(text="downloading..." +amt_s)
    # master.update()


def d_done(evt):
    print("...Download finished!")
    # pbar['value'] = 0
    # master.update()


def main():
    mgr = LBRYLinkManager()
    urls = mgr.get_urls()
    # print("URLs: {}".format(urls))
    AppImage_URLs = []
    for url in urls:
        if url.endswith(".AppImage"):
            if url not in AppImage_URLs:
                AppImage_URLs.append(url)
    print("AppImage_URLs: {}".format(AppImage_URLs))
    if len(AppImage_URLs) > 1:
        print("WARNING: There is more than one AppImage: {}"
              "".format(AppImage_URLs))
    dls_path = mgr.get_downloads_path()
    if not os.path.isdir(dls_path):
        os.makedir(dls_path)
    for url in AppImage_URLs:
        fname = url.split("/")[-1]
        src_path = os.path.join(dls_path, fname)
        if os.path.isfile(src_path):
            print("* removing download not installed: {}"
                  "".format(src_path))
            os.remove(src_path)
        print("* downloading {}".format(url))
        mgr.download(src_path, url, cb_progress=d_progress, cb_done=d_done)
        print("* installing {}".format(src_path))

        install_program_in_place(
            src_path,
            caption="LBRY",
            move_what='file',
            do_uninstall=False,
            enable_reinstall=False
        )
        return 0


if __name__ == "__main__":
    sys.exit(main())
