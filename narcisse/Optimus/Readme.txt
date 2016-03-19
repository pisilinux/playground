Bumblebee Yükleme Talimatları / Bumblebee Install Instructions

1- system.devel paketlerini yükleyin 
   install system.devel packages

   sudo pisi install -c system.devel
   

2- libbsd derleme ve kurulumu 
   libbsd build and install

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/libbsd/pspec.xml && sudo pisi install libbsd*.pisi
   
   
3- fltk derleme ve kurulumu 
   fltk build and install

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/fltk/pspec.xml && sudo pisi install fltk*.pisi
   
   
4- virtualgl derleme ve kurulumu 
   virtualgl build and install

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/virtualgl/pspec.xml && sudo pisi install virtualgl*.pisi
   
   
5- Eğer Pisi 1.2 sürümünü kullanıyorsanız, bu modülü derleyin. 
   If you are using Pisi version 1.2, build and install this module

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/module-nvidia-current-p12/pspec.xml && sudo pisi install *nvidia*.pisi
   

6- Eğer Pisi 2.0 sürümünü kullanıyorsanız, bu modülü derleyin 
   If you are using Pisi version 2.0, build and install this module

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/module-nvidia-current-p20/pspec.xml && sudo pisi install *nvidia*.pisi
   
7- primus paketini derleyin ve kurun
   Build and install primus package
   
   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/primus/pspec.xml && sudo pisi install primus*.pisi
   
8- nvidia-settings paketini derleyin ve kurun
   build and install nvidia-settings
   
   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/nvidia-settings/pspec.xml && sudo pisi install nvidia-settings*.pisi
   

9- Çeşitli paketler kurun 
   Various packages

   sudo pisi install mesa-demos mesa-demos-32bit mesa-utils module-bbswitch   

   
   
10- Son olarak bumblebee paketini derleyin ve kurun 
   Finally build and install bumblebee packages

   sudo pisi build https://raw.githubusercontent.com/pisilinux/playground/master/narcisse/Optimus/bumblebee/pspec.xml && sudo pisi install bumblebee*.pisi
   
   
11- Yeniden başlatın ve şu komutlarla çalıştığını test edin.
   Reboot and test if it works by those commands
   
   optirun glxinfo
   optirun glxgears
   optirun glxspheres
   
   primusrun glxinfo
   primusrun glxgears
   primusrun glxspheres
   
12- Çalıştırmak istediğiniz komutun önüne primusrun veya optirun getirerek, programı Nvidia üzerinden çalıştırabilirsiniz.
    By typing primusrun or optirun before the command, you can run the program on Nvidia card.
    
    
    
