# TV Tuners

## Analog

### WinTV-HVR 850
WinTV-HVR 850 is a hybrid DTV stick with analog and digital TV.

The instructions below only work for developers or CLI (Command-Line
Interface) users. Another reliable and lossless method wasn't found yet.
The card has hardware MPEG encoding, so getting anything other than the
raw data will recompress it (causing a 2nd-generation of loss), MPEG or
not.

```
#lsusb shows:
#Bus 002 Device 006: ID 2040:b140 Hauppauge

#v4l-dvb-git: V4L-DVB drivers [collection of drivers for capture cards]
#ivtv-tune: userspace tools for hauppauge cards
ivtv-tune --channel=3
#output is: /dev/video0: 61.250 MHz
 #HOWEVER, on Windows, AMCap succeeds (via scan) only with Video 61.3MHz, Audio 65.8MHz
 #so first do:
ivtv-tune --freqtable=us-bcast --channel=3
#didn't work, doesn't show output /dev/video0 message anymore. Don't know why. There was a crash with screen corruption before it stopped working (but the device still works on Windows)

#mtvcgui: mencoder TV capture gui [pyqt4]
#Can schedule a recording
#Sets the following environment variables (according to Advanced tab):
#LD_PRELOAD=/usr/lib/libv4l/v4l2convert.so
#Can generate command previews such as:
#* lossless capture:
#mencoder tv:// -tv channel=3:driver=v4l2:device=/dev/video0:input=0:chanlist=us-bcast:brightness=0:contrast=0:hue=0:saturation=0 -oac copy -ovc copy -quiet -o /home/owner/Video/capture_3_20170829_221733.avi
#* faac+x264 as mp4:
#mencoder tv:// -tv channel=3:driver=v4l2:device=/dev/video0:input=0:chanlist=us-bcast:brightness=0:contrast=0:hue=0:saturation=0 -oac faac -ovc x264 -quiet -x264encopts crf=23.0 -o /home/owner/Video/capture_3_20170829_222020.mp4
#*
#
#xawtv: acts glitchy (can't open many things from the right-click menu)--dont work: Channel Window, Channel Hopping, Launcher Window
#most reliable method:
#TUNE first (see above) to channel 3 for VCR, then:
cat /dev/video0 > ~/capture.mpg
```
