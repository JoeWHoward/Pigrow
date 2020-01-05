#!/usr/bin/python
import time
import os, sys
try:
    from picamera import PiCamera
except:
    print("Picamera is not installed, is this even a raspberry pi?!")
    exit()

homedir = os.getenv("HOME")

for argu in sys.argv[1:]:
    if argu == '-h' or argu == '--help':
        print(" Picam capture script")
        print(" ")
        print(" this will be rewritten soon - you might need to manually edit the python code to make it do what you want")
        print("")
        print(" -- this script is due an update, don't expect perfection --")
        sys.exit(0)
    elif argu == "-flags":
        sys.exit(0)

def load_picam_set(setloc= homedir + "/Pigrow/config/picam_settings.txt"):
    picam_dic = {}
    with open(setloc, "r") as f:
        for line in f:
            s_item = line.split("=")
            picam_dic[s_item[0]]=s_item[1].rstrip('\n')
    return picam_dic

def take_picam_py(picam_dic, caps_path):
    #
    # take and save photo
    #
    #get current time and set filename
    timenow = str(time.time())[0:10]
    filename= "cap_"+str(timenow)+".jpg"
    try:
        camera = PiCamera()
        #camera.resolution = (2592,1944)
        camera.resolution = (int(picam_dic['resolution_x']),int(picam_dic['resolution_y']))
        camera.brightness = int(picam_dic['brightness'])
        camera.contrast = int(picam_dic['contract'])
        camera.saturation = int(picam_dic['saturation'])
        camera.iso =  int(picam_dic['iso'])
        camera.sharpness = int(picam_dic['sharpness'])
        camera.shutter_speed = int(picam_dic['shutter_speed'])
        camera.zoom = (picam_dic['zoom_x'], picam_dic['zoom_y'], picam_dic['zoom_w'], picam_dic['zoom_h'])
        camera.image_denoise = (picam_dic['image_denoise'] == 'True')
        camera.awb_mode = picam_dic['awb_mode']
        time.sleep(2)
        print ("resolution = " + str(camera.resolution))
        print ("analog_gain = " + str(camera.analog_gain))
        print ("digital_gain = " + str(camera.digital_gain))
        print ("iso =" + str(camera.iso))
        print ("brightness = " + str(camera.brightness))
        print ("contrast =  " + str(camera.contrast))
        print ("saturation = " + str(camera.saturation))
        print ("sharpness = " + str(camera.sharpness))
        print ("zoom = " + str(camera.zoom))
        print ("drc_strength = " + str(camera.drc_strength))
        print ("exposure_compensation = " + str(camera.exposure_compensation))
        print ("exposure_mode = " + str(camera.exposure_mode))
        print ("exposure_speed = " + str(camera.exposure_speed))
        print ("hflip = " + str(camera.hflip))
        print ("vflip = " + str(camera.vflip))
        print ("rotation = " + str(camera.rotation))
        print ("meter_mode = " + str(camera.meter_mode))
        print ("image_denoise = " + str(camera.image_denoise))
        print ("image_effect = " + str(camera.image_effect))
        print ("image_effect_params = " + str(camera.image_effect_params))
        print ("awb_mode = " + str(camera.awb_mode))
        camera.capture(caps_path+filename)
        camera.close()
        return filename
    except:
        print("Sorry, picture not taken :(")
        raise

def take_picam_raspistill(picam_dic, caps_path):
    # take and save photo
    timenow = str(time.time())[0:10]
    filename= "cap_"+str(timenow)+".jpg"
    try:
        extra_commands = picam_dic['extra_commands']
    except:
        extra_commands = ''
    os.system("raspistill -o "+caps_path+filename+" "+extra_commands)
    return filename


if __name__ == '__main__':
    sys.path.append(homedir + '/Pigrow/scripts/')
    script = 'picamcap.py'
    import pigrow_defs
    loc_locs = homedir + '/Pigrow/config/dirlocs.txt'
    loc_dic = pigrow_defs.load_locs(loc_locs)
    caps_path = loc_dic["caps_path"]
    picam_dic = load_picam_set(setloc=homedir + "/Pigrow/config/picam_settings.txt")
    filename = take_picam_py(picam_dic, caps_path)
    #filename = take_picam_raspistill(picam_dic, caps_path)
    print("Image taken and saved to "+caps_path+filename)
