#  Live camera preview on main DPI display as well as HDMI0 monitor.
#
#  Works only after running "rpi-update" until this commit will be available:
#
#    https://github.com/raspberrypi/userland/commit/2549c149d8aa7f18ff201a1c0429cb26f9e2535a
# 
#    Values are Dispmanx display enums, therefore predominantly
#    0 = DSI/DPI LCD
#    2 = HDMI0
#    3 = SDTV
#    7 = HDMI1
#    Behaviour should the chosen display not be present should be to
#    revert to the primary display that is present.
#
#  Based on this script:
#
#    https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=232991&p=1582640#p1580053
#
from picamera import mmalobj as mo, mmal
from signal import pause

camera = mo.MMALCamera()
splitter = mo.MMALSplitter()
render_l = mo.MMALRenderer()
render_r = mo.MMALRenderer()

camera.outputs[0].framesize = (500, 500)
camera.outputs[0].framerate = 30
camera.outputs[0].commit()

camera.control.params[mmal.MMAL_PARAMETER_DRAW_BOX_FACES_AND_FOCUS] = 1


p = render_l.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]
p.set = mmal.MMAL_DISPLAY_SET_FULLSCREEN | mmal.MMAL_DISPLAY_SET_DEST_RECT | mmal.MMAL_DISPLAY_SET_NUM


p.display_num = 2    # HDMI0
p.fullscreen = False
p.dest_rect = mmal.MMAL_RECT_T(0, 18, 500, 500)

render_l.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION] = p


p.display_num = 7    # HDMI1
p.dest_rect = mmal.MMAL_RECT_T(512, 18, 500, 500)

render_r.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION] = p


splitter.connect(camera.outputs[0])
render_l.connect(splitter.outputs[0])
render_r.connect(splitter.outputs[1])

splitter.enable()
render_l.enable()
render_r.enable()

pause()
