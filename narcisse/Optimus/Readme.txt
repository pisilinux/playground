PISILINUX OPTIMUS TESTING INSTRUCTIONS

*** Building a package ***

In order to build a package from this repo, you will need to do those steps:

1- You need a raw link of pspec.xml file for that package. Open pspec.xml file of that package on browser, click "Raw" button on the page and copy the address from the adress bar.

2- Build the package via this command. Substitute the address you've just copied here with <address here>

   sudo pisi build <address here> --ignore-sandbox -y
   
3- In order to install packages:

   sudo pisi install *.pisi --ignore-file-conflicts


*** UPDATE: Build libdrm from here. It's updated version for mesa. ***
*** UPDATE: Build libbsd from here. It's updated version. ***
*** UPDATE: Build libjpeg-turbo from here. It's updated version for VirtualGL. ***


PACKAGE BUILDING AND INSTALLATION ORDER

0- Build && install libomxil-bellagio from here.

1- Build && install libclc. This is just a dependency for Mesa OpenCL. It may be unnecessary.



2- Build mesa. After successful build, you will see a lot of packages. Just install regular mesa packages and mesa-dri-intel, optional mesa-opencl.
   The others are irrelevant. Actually, we just avoid swrast and vmware drivers' installation. 
   
   *** Delete those packages after build and install remaining ***
   
   * mesa-dri-swrast
   * mesa-dri-nouveau
   * mesa-dri-radeon
   * mesa-dri-vmware
   

   
3- Build && install module-nvidia-current


4- Install module-bbswitch.


5- Build && install libbsd from here.


6- Build && install fltk from here. This one has been added 32-bit support for virtualgl.


7- Build && install virtualgl. This one has been added 32 bit support for 32-bit applications.


8- Build && install bumblebee from here.

9- Build && install nv-scripts from here.


Now we've got everything we need. Before reboot, do these too;


* sudo groupadd bumblebee

* sudo gpasswd -a $USER bumblebee

* Add these line to the end of /etc/modprobe.d/blacklist.conf file
  
  blacklist nouveau


Reboot. After reboot, start bumblebee daemon by this:

* sudo bumblebeed --daemon


And we're ready. Test with this:

* optirun glxinfo | grep "NVIDIA"


If you get nothing, try to switch libGL and try again previous step:

* sudo run-nv


To activate Nvidia card:

* sudo run-nv

To deactivate:

* sudo kill-nv


And done. Enjoy...


Idris Kalp

  
