#!/bin/bash
me=`basename $0`

# region common
postinstall="generated.md"
maindir=""
if [ -f api.rc ]; then
    maindir="."
elif [ -f ../api.rc ]; then
    maindir=".."
elif [ -f ../../api.rc ]; then
    maindir="../.."
elif [ -f ../../../api.rc ]; then
    maindir="../../.."
fi
if [ ! -z "$maindir" ]; then
    source $maindir/api.rc
    postinstall="$maindir/$_POSTINSTALL_NAME"
else
    echo "WARNING: api.rc cannot be found in `pwd` nor up to ../../.."
    echo "  tips will be placed in `pwd`/$postinstall instead."
fi
touch $postinstall
# endregion common

cat >> $postinstall <<EOF
# Post Install Instructions
(This file was generated by $me, so
DO NOT EDIT THIS FILE)
EOF
echo "You must do the following manual steps to enable newly-installed features:" >> $postinstall
echo " - [ ] Enable spell check plugin in Geany's \"Tools,\" \"Plugin manager\" window." >> $postinstall
#echo "(This file was generated by $me, so" > $postinstall
#echo "DO NOT EDIT THIS FILE)" >> $postinstall

#see also $HOME/git/integratoredu/data/units/0/tm/files/(system)/iedu-mps-hourly

# region home server

# * faster server if you have a home server:
# su -c 'echo "192.168.1.5 poikilos.dyndns.org" >> /etc/hosts'
# endregion home server


# region local git website without database
# (see <https://www.git-scm.com/docs/git-instaweb/1.5.5>)
dnf -y install git-instaweb
# (which also gets: lighthttpd lighttpd-filesystem)
cat >> $postinstall <<EOF

## git-instaweb
(view local git repos using your web browser; not cloned repos--see
make-localhost-git-Bucket_Game.sh)
* cd to your git directory then run git instaweb such as
  \`\`\`bash
  cd /home/owner/localrepos/Bucket_Game.git
  git instaweb
  \`\`\`
EOF
# endregion local git website without database



echo "You must install everyone.sh files first, or the repositories or programs may be missing."

#source /etc/os-release

dnf -y install \
    blender \
    inkscape \
    owncloud-client \
    git-cola \
    obs-studio \
    keepassxc \
    geany \
    geany-plugins-spellcheck \
    python \
    python2-pillow \
    python3-pillow \
    speedcrunch \
    filezilla \
    darktable \
    avidemux \
    codeblocks \
    qt-creator \
    mypaint \
    krita \
    kate \
    lmms \
    vinagre \
    scantailor \
    vlc \
    mpv \
    librecad \
    freecad \
    gedit \
    catfish \
    meld \
    hexchat \
    ghex \
    gxmms2 \
    python2-pygame \
    gucharmap \
    tiled \
    fontforge \
    qdirstat \
    frei0r-plugins \
    redshift \
    redshift-gtk \
    plasma-applet-redshift-control \
    projectM-pulseaudio \
    eclipse-jdt \
    icedtea-web \
    maven \
    shotcut \
    chromium-libs-media-freeworld \
    exfat-utils \
    fuse-exfat \
    unetbootin \
    gimp-elsamuko \
    gimp-resynthesizer \
    gimp-wavelet-denoise-plugin \
    gimp-paint-studio \
    gimp-lqr-plugin \
    gimp-normalmap \
    gimp-lensfun \
    gimp-data-extras \
    GREYCstoration-gimp \
    star \
    sloccount \
    icoutils \
    ladspa-cmt-plugins \
    ladspa-autotalent-plugins \
    ladspa-zam-plugins \
    ladspa-rev-plugins \
    PersonalCopy-Lite-soundfont \
    ardour5 \
    rhythmbox \
    scribus \
    libreoffice \
    remarkable \
    discord \
    icoutils \
    pandoc \
    git \
    git-credential-libsecret \  # remember password securely in terminal
    gstreamer-ffmpeg \
    sqlitebrowser \
    python3-pycodestyle \
    gmic-gimp \
    gnome-terminal \
    screen \
    ;


# gstreamer-ffmpeg: should allow dragon player to play the files it opens by default but can't play by default (mkv, mp4, mov)

cat >> $postinstall <<END
* The run-in-place version of Discord is necessary to get the latest
  updates automatically. The packaged version is too old to be allowed
  to login. If you want Discord, you'll have to get that version
  manually from https://discordapp.com/download (Select 'tar.gz' before
  clicking Download Now.)" >> $postinstall
END
# for scale2x (see install-as-user.sh):
dnf -y install zlib libpng

#Save git password without KDE keyring:
dnf -y install libsecret
# see also run as unpriveleged user (git config --global credential.helper libsecret automatically edits:
# echo > ~/.gitconfig <<END
# [credential]
# helper = libsecret
#END

#NOT lxmusic
#NOT bluez-hid2hci etc (see below for why using builtin KDE functionality instead)
#NOT retext (markdown editor for reStructuredText but not GitHub-style Markdown)
#NOT gnome-mplayer


# for testing php scripts such as via php -S localhost:8000 index.php:
dnf -y install php

# for butterflow (frame blending OR interpolation)--see install-as-user:
dnf -y install git python2-setuptools python2-virtualenv python2-numpy ocl-icd opencl-headers ffmpeg
# opencv-devel
# NOTE: as of Fedora 29, opencv-devel is opencv 3.4.1
# where ocl.hpp is totally DIFFERENT according to <https://stackoverflow.com/questions/34422276/opencv-3-0-error-include-ocl-hpp>
# not in readme, but if missing, prevents `pip install https://github.com/dthpham/butterflow/archive/master.zip`:
#    /tmp/pip-req-build-m6c87h1b/butterflow/avinfo.c:5:10: fatal error: libavcodec/avcodec.h: No such file or directory
#     #include <libavcodec/avcodec.h>
#              ^~~~~~~~~~~~~~~~~~~~~~
#    compilation terminated.
#    error: command 'gcc' failed with exit status 1
# could be solved by ffmpeg-compat-devel as per <https://ask.fedoraproject.org/en/question/31642/how-to-install-libav-devel-packages-properly/>
# but I installed ffmpeg-devel
# but error still occurs since ffmpeg has the h in ffmpeg/libavcodec/avcodec.h
# so edited butterflow/butterflow/avinfo.c to use that path
# still had error:
#    In file included from /tmp/pip-req-build-uquwiwd3/butterflow/avinfo.c:5:
#    /usr/include/ffmpeg/libavcodec/avcodec.h:31:10: fatal error: libavutil/samplefmt.h: No such file or directory
#     #include "libavutil/samplefmt.h"
#              ^~~~~~~~~~~~~~~~~~~~~~~
#    compilation terminated.
#    error: command 'gcc' failed with exit status 1
# so changed the two libavutil lines to use ffmpeg/libavutil as the path
# new error:
#    In file included from /tmp/pip-req-build-webiqhd6/butterflow/avinfo.c:5:
#    /usr/include/ffmpeg/libavcodec/avcodec.h:31:10: fatal error: libavutil/samplefmt.h: No such file or directory
#     #include "libavutil/samplefmt.h"
#              ^~~~~~~~~~~~~~~~~~~~~~~
#    compilation terminated.
#    error: command 'gcc' failed with exit status 1
#Command "/usr/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-req-build-webiqhd6/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-zettjosz/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-req-build-webiqhd6/
# * according to Eric Stdlib on <https://stackoverflow.com/questions/47562170/how-to-include-avcodec-h-in-c-in-fedora>
# the problem is solved by adding -I /usr/include/ffmpeg to the gcc command.
#   * I reverted back to the original butterflow/butterflow/avinfo.c (removed each ffmpeg/ added above)
#   * Path (-I) can be added via pip as per <https://stackoverflow.com/questions/18783390/python-pip-specify-a-library-directory-and-an-include-directory>
#     (see install-as-user)
# * another error remains:
#    /tmp/pip-req-build-gRg1yS/butterflow/ocl.cpp:10:10: fatal error: opencv2/ocl/ocl.hpp: No such file or directory
#     #include <opencv2/ocl/ocl.hpp>
#              ^~~~~~~~~~~~~~~~~~~~~
#    compilation terminated.
#    error: command 'gcc' failed with exit status 1
#
#    ----------------------------------------
#Command "/usr/bin/python2 -u -c "import setuptools, tokenize;__file__='/tmp/pip-req-build-gRg1yS/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-RA_EcH/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-req-build-gRg1yS/
#
#   * apparently since "opencv-ocl package or you did not compile your opencv with OCL activated." (see <https://github.com/slowmoVideo/slowmoVideo/issues/36>)
#     but there is no such package. locate says file is installed at: /usr/include/boost/compute/interop/opencv/ocl.hpp
#     so added interop to include path, but that doesn't work.
#   * Tried to install compat package from copr (see https://copr.fedorainfracloud.org/coprs/thofmann/opencv2/)
dnf -y install libav
# dnf -y copr enable thofmann/opencv2
# allowerasing will remove opencv (such as 3.0) if installed
# dnf -y --allowerasing install opencv2
# but install fails:
# Failed to synchronize cache for repo 'thofmann-opencv2', ignoring this repo.
# No match for argument: opencv2
# Error: Unable to find a match
#      * changing releasever to 26 doesn't work either (last build of thofmann-opencv2 <https://copr-be.cloud.fedoraproject.org/results/thofmann/opencv2/fedora-26-x86_64/repodata/>)
# No match for argument: opencv2
# Error: Unable to find a match
#   * tried installing python2-opencv, but as expected that did not help.
#   * so try including modules/ocl/include manually (see install-as-user)


#if (( $VERSION_ID > 28 )) ; then
  # then use included gimp (29 has 2.10, 28 has 2.8 so use flatpak there)
#fi
#use git version of git-cola since packaged version for Fedora 28 is git-cola 2.10, and May 2018 git version fixes consistency of Ctrl S
# (but explicitly install git above, since needed, and since otherwise removing git-cola will remove git)
# [closed: keyboard shortcuts doesn't work](https://github.com/git-cola/git-cola/issues/852)
#other keyboard shortcut issues:
#* [Ambiguous hotkeys by default for Alt+U (formerly triggered Stage Untracked) #926](https://github.com/git-cola/git-cola/issues/926)
#dl_git="$HOME/Downloads/git"
#if [ ! -d "$dl_git" ]; then
#  mkdir -p "$dl_git"
#fi
#cd "$dl_git"
#git clone git://github.com/git-cola/git-cola.git
#cd git-cola
#see unpriveleged.sh instead

# wayback_machine_downloader (has option to filter by min or max date of snapshot, such as 20150424112013 for irc.minetest.ru--see ~/Downloads/websites/got.sh)
sudo dnf -y install ruby
gem install wayback_machine_downloader
# Usage: it will make a ./websites/* directories automatically when run on a specific web address.

#pandoc: convert from markdown to html (opposite by setting -f html -t markdown)
#remarkable: Markdown editor with GitHub markdown syntax support
#projectM-pulseaudio: The projectM visualization plugin for pulseaudio
#sloccount: Measures source lines of code (SLOC) in programs
#privacy-oriented browser:
dnf -y install dnf-plugins-core
dnf -y config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/
rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
dnf -y install brave-keyring brave-browser

#for kivy:
dnf -y install python-devel ffmpeg-libs SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel portmidi-devel libavdevice libavc1394-devel zlibrary-devel ccache mesa-libGL mesa-libGL-devel
dnf -y install python3-pip python2-pip xclip

# see *-nonroot.sh for:
# * gimp export selection plugin,:
# runuser -l owner -c 'sh developer-nonroot.sh'


dnf -y config-manager --add-repo https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
dnf -y install sublime-text


#fix No valid kits found error in qtcreator
#(see <https://stackoverflow.com/questions/40978510/qt-creator-on-fedora-25-no-valid-kits-found>):
dnf -y install make gcc-c++ gdb qt5*-devel
#qt5-devel

#ignore xgalaga-sdl -- says works with SDL2 but configure fails on finding SDL (should compile with SDL1.2-devel packages though)
#SDL_gfxPrimitves (with alpha), SDL_rotozoom, SDL_framerate, SDL_imageFilter (with MMX), SDL_gfxBlitFunc (Custom Blit functions)
#such as for xgalaga-sdl `mkdir -p ~/Downloads/git && cd ~/Downloads/git && https://github.com/frank-zago/xgalaga-sdl.git`
#(successor to SDL_gfxPrimitives):
#dnf -y install SDL2_gfx-devel

#such as for XGalaga++ (C++ rewrite of XGalaga, but still pure X11):
dnf -y install libXpm-devel

#autoconf (including autoreconf etc):
dnf -y groupinstall "C Development Tools and Libraries"

#configure redshift (location for yourself can be found via Google Maps):
#where 5600 is day temp and 3400 is night temp
#redshift -l 40.3832256:-75.2748652 -t 5600:3400
#Has to remain running, so use GUI instead (drag widget to KDE panel, then right-click to configure:
# * turn on smooth transitions
# * set temps to 5600 and 3400
# * click Locate [if fails, use coords for your location such as above]
# * Apply

#projectM-pulseaudio: a GUI program for viewing audio input using MilkDrop scripts!
# * controlled using hotkeys (see F1 for help, and https://wiki.archlinux.org/index.php/ProjectM)
#

# BLUETOOTH:
# bluez-tools bluez-hid2hci blueman
# blueman pulls in: bluez-obexd (others didn't install anything additional)
# rfkill is not removeable. It was never manually installed (dnf history list rfkill says: "No transaction which manipulates package 'rfkill' was found.") and it can't be removed without removing systemd.
# Doing the above causes KDE to prompt for privs after login for both blueman and RfKill (separate prompt for each)
# Doing the above also results in two bluetooth symbol icons on the task tray (one blurry blue blueman one, plus one themed one)

sudo dnf -y groupinstall "Development Tools"
echo "The correct package is `sudo dnf grouplist | grep Development | grep -v "D Development"`" >> $postinstall

cat >> $postinstall <<END
## Manually Install
* bluegriffon: graphical HTML editor [may mangle php]
* zerobrane-studio: Lua editor with the possibility of code completion
* gespeaker
* tsMuxeR
* COLMAP  # (2D to 3D) structure from motion
* GeekBench
* hardinfo  # System Profiler and Benchmark
* renpy [arch community]: Ren'Py is a visual novel engine that helps you use words, images, and sounds to tell interactive stories that run on computers and mobile devices


from source or flatpak for latest version:
  kdenlive
  openshot
  gimp  # if packaged version is not 2.10.8 yet
  #   (~2.10 has wavelet resize and denoise)
from source:
  minetest (see EnlivenMinetest)
  kivy (see above for dependencies)
  lxqt (see $me for packages already installed)

END

cat >> $postinstall <<END
### Change Settings via GUI:
* For QT 5.* if you face error at Kits, like No Valid Kits Found, go to
  Options->Build&Run-> then you see a Manual Option which included
  Desktop as a default.
* Set hotkeys for Geany (Edit, Preferences, Keybindings, Format; Ctrl 3
  is already 'Send to custom command 3'):
  * Ctrl Shift 3: comment
  * Alt Shift 3: uncomment
END

## see also (installed as dep)
# python3-mutagen (python module to handle audio meta-data)
if [ ! -d "$HOME/palettes" ]; then
    mkdir "$HOME/palettes"
fi
cat >> $postinstall <<END

see also Downloads/1.InstallManually
see also $HOME/ownCloud/Downloads
and try:
  cd ~/ownCloud/Downloads/Graphics,2D/gimp-stuff/
  chmod +x install-plugins
  ./install-plugins

To to via GUI"
* Install color profile from
  $HOME/ownCloud/Downloads/Drivers/Monitor/W2361VV-Windows7/
  or <https://www.lg.com/us/support-product/lg-W2361V-PF>
* Open your linux Desktop's System Settings,
  Color Corrections, Add Profile,
  then choose the downloaded icm profile.
* Enable plugins in Blender:
  - MeasureIT
  - Paint Palettes
    - You must manually set a full path to a palette directory such as:
      - Got to texture paint mode, tools side tab, Color Palette section
      - Paste $HOME/palettes/ (created by $me)
        or other (directory must exist and be writeable) into
        Palettes Folder box.
  - 3D Print Toolbox
  - Extra Objects
  - B3D Exporter (install from file--download github.com/minetest/ fork)
  -
END
#dnf -y install psutils
#echo "psutils allows printing multiple pages per sheet:"
#echo "  psnup -4 file.ps print.ps"
#echo "  lpr print.ps"
#echo "according to https://www.cade.utah.edu/faqs/how-can-i-print-multiple-pages-per-sheet-in-linux/"
#echo "but tests were unsuccessful with `psnup -2 file.ps print.ps`."
dnf -y install pdfjam
#Debian-based: apt install pdfjam
#Arch-based: yaourt -S pdfnup
echo "pdfnup allows printing multiple pages per sheet (default is 2):"
echo "  pdfnup -o output.pdf input.pdf"


#unique folder so it doesn't erase other stuff you may be working on;
THIS_MAINTAINER=poikilos
if [ ! -d "$HOME/git" ]; then mkdir -p "$HOME/git"; fi
cd "$HOME/git"
#if [ -d "Gedit-External-Tools-SaveSession" ]; then rm -Rf "Gedit-External-Tools-SaveSession"; fi
git_url=https://github.com/$THIS_MAINTAINER/Gedit-External-Tools-SaveSession.git
if [ ! -d "Gedit-External-Tools-SaveSession" ]; then
  git clone $git_url
else
  cd Gedit-External-Tools-SaveSession
  git pull
  cd ..
fi
if [ ! -d "Gedit-External-Tools-SaveSession" ]; then
  echo "FAILED to get Gedit-External-Tools-SaveSession from $git_url" >> $postinstall
else
  cd "Gedit-External-Tools-SaveSession"
  bash install || echo "cd Gedit-External-Tools-SaveSession && bash install # FAILED" >> $postinstall
fi

adduser nonet
sudo iptables -A OUTPUT -m owner --uid-owner nonet -j REJECT
cat >> $postinstall <<END
* nonet user has been denied internet on purpose.
  If you want to allow the nonet user to have internet, undo as follows:
    sudo iptables -D OUTPUT -m owner --uid-owner nonet -j REJECT
  Add the command without -D to /etc/rc.local if setting doesn't persist.

## Tips
* Experiment and get good at G'MIC plugins section of gimp filters,
  because they can also be used in terminal and in other programs:
  * Flowblade
  * Krita
* Disable hardware acceleration in Brave to prevent horrible glitches
  (invisible interface that only updates when you move the Window):
  - Click Settings (hamburger button), "Advanced," "System,"
    then turn off "Hardware Acceleration."

## See Also
* python3-mutagen (python module to handle audio meta-data)
  installed as dependency.

END
echo "Showing $postinstall..."
cat $postinstall
echo "(to see this generated post-install information again, see `pwd`/$postinstall)"