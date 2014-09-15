PISILINUX OPTIMUS TESTING INSTRUCTIONS


1- Build && install libclc. This is just a dependency for Mesa OpenCL. It may be unnecessary.



2- Build mesa. After successful build, you will see a lot of packages. Just install regular mesa packages and mesa-dri-intel, optional mesa-opencl.
   The others are irrelevant. Actually, we just avoid swrast and vmware drivers' installation. 
   

   
3- Build && install module-nvidia-current


4- Build && install module-bbswitch from extra repo.


5- Install libbsd from repo.


6- Build && install fltk from here. This one has been added 32-bit support for virtualgl.


7- Build && install virtualgl. This one has been added 32 bit support for 32-bit applications.


8- Build && install bumblebee from marcin's playground.



Now we've got everything we need. Before reboot, do these too;


* sudo groupadd bumblebee

* sudo gpasswd -a $USER bumblebee


Reboot. After reboot, start bumblebee daemon by this:

* sudo bumblebeed --daemon


And we're ready. Test with this:

* optirun glxinfo | grep "NVIDIA"


If you get nothing, try to switch libGL and try again previous step:

* sudo alternatives --config libGL    // Set up the second libGL, nvidia's libGL


And done. Enjoy...


narcisse

  