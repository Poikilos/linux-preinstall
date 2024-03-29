# Forensic Imaging Tools

Poikilos:
- Commands provided by installing [rotocanvas](https://github.com/poikilos/rotocanvas):
  - diffimage
  - diffimagesratio
  - findbyappearance
- diffimg (available on some Linux distro repos).

Arch:
- testdisk

AUR:
- rstudio
- whdd
- scrounge-ntfs
- safecopy: extract data from damaged disks
- magicrescue: "Find and recover deleted files on block devices"


## Other forensics tools
### Image Stacking (get more detail from series of frames)
#### AUR:
* immix "Aligns and merges a set of similar images in order to decrease their noise" (no increased res export)
* lxnstack
  * crashes--if run from terminal, says "ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()"

	Installs, but fails to run since uses `==None` or `== None` (should be `is None`) and uses `!=None` or `!= None` (should be `is not None`) several times in:
	* /usr/share/lxnstack/utils.py
	* /usr/share/lxnstack/main_app.py
	* /usr/share/lxnstack/cr2plugin.py

	Changing those instances fixes manually after install those errors.

	This is a problem since when the object contains more than one value (such as a list, gives an error that provides in incorrect fix given the way None is used by these files: "ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()"). This causes the program not to run due to where error occurs in utils.py.

	I contacted mauritiusdadd via the google site
	  https://sites.google.com/site/lxnstack/home/contact
	  and mentioned the following:
	  * github versions of these files (github user of same username as sourceforge) don't have the problem
	  * please make change AUR entry to use a git release, or fix sourceforge version
	  * please annotate both sourceforge and github pages (both are under their username) to indicate which repo should be used


* summovie "Calculates electron microscopy frame sums using alignment results from Unblur" (/usr/bin/summovie.exe)
  * terminal only
  * only takes mrc files

##### general data recovery (not image processing):
* ddrescue (arch)
* ddrescue-gui
* ddrescueview "Graphical viewer for ddrescue log files"
* ddrutility "Set of utilities for use with GNU ddrescue to aid with data recovery" downloads:
	* lazarus
	* lazarus-gtk2
* testdisk
	* comes with photorec which can recover photos from datastream even if partition table is not recoverable

#### Other
* ImageJ: mostly for annotating and measuring images, with an emphasis on microscopy https://imagej.nih.gov/ij/download.html (bundled with Java 1.8)
	* as of 2017-10, the site recommends getting Fiji instead (available in AUR; "a distribution of ImageJ which includes many useful plugins contributed by the community")
* qastrocam-g2 "unable to satisfy dependency avifile"hg
* SerialIM and IMOD: http://sphinx-emdocs.readthedocs.io/en/latest/align-movie-frames-imod.html
* starstax: "freeware," seems to just blend images (no res increase)
