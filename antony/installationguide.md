# Pisi Linux installation guide

* This is a basic (quick-start) guide to installing Pisi Linux.
* This guide is based on an install of Pisi Linux 1.0 (RC v1 'Izmir').
* The installer itself is called YALI (Yet Another Linux Installer).

**Prerequisites:**
* **64bit** processor
* **12GB** recommended minimum space for install
* **Obtain ISO** http://packages.pisilinux.org/iso/
* **Burn ISO** to either optical or USB media (Optical media should be 'burnt' using a slow speed)
* CLI method for bootable USB media:
``sudo dd bs=4M if=Pisi-Linux-Rc1-izmir-v01.iso of=/dev/sdX``
(Replace 'X' to match your target USB drive, for example: sdb, sdc, etc ...)

## Language
* Press **F2**
* Select language
* Press **ENTER** to confirm

_Note: If no selection is made within 10 seconds the installer will proceed, using the default language (Turkish)._

## Launch Install
* Select **1st item** from tools menu (launch installer)
* Press **ENTER**

_Note: the Linux kernel will now load and some output will be displayed, before automatically moving on to the next step_

## Accept Terms
* Click in the check-box to accept the licensing terms
* Click _**Next**_

## Validate Media
* If you wish to check the integrity of the installation media, click **Validate**, then click **Next**

_Note: although this may take a little while, this step is worthwhile and recommended_

## Time-Zone
* Set date and time
* Set region and city
* Click **Next**

## Create Regular User/s
* Create a regular user account
* For more options or to create additional users, click on **Advanced** (note: additional users may optionally be created post-install)
* Click **Next**

## Create Administrator
* Create an Administrator
* You may also customise the host-name of your computer if you wish

_Note: as the Administrator (or Superuser) has absolute privileges, it is especially important that a strong password is allocated to this account_

## Partitioning Method
**Use All Disk**
- Installer will partition disk automatically. Any existing data will be lost

**Shrink Current System**
- Shrink an existing Windows (or other OS) partition to make room for Pisi Linux. Ensure existing data is backed up as a precaution

**Use Free Space**
- Installer will use available free space

**Manual Partitioning**
- As the other methods are either automatic or guided, a basic manual partitioning example is shown below: 

## File-System Type
* Click on free space
* Click **Create**
* Choose **Standard**
* Click **Partition**

## File-System Mount-points
* Click on the **USE** field and select / (this will be the 'root' file-system)
* Leave **file-system** as **ext4** if unsure
* Adjust partition size using either the slider, up-down arrows, or enter a value directly
* Click **force to be a primary partition**
* Click **OK**

## Swap-space
To create a 'swap' partition, repeat the same partitioning example, but ignore the **USE** step and select swap instead of ext4 file-system

_Note: 'Swap-space' is the term for swapping pages of memory from RAM to a predetermined area of a hard disk. This is performed, for instance, when RAM becomes full: data for lower priority tasks is 'demoted' from RAM, to hard disk 'swap space' As there are a few variables, you should tailor swap to your specific _
_system - and it's intended use. But just as a generic example: 2GB swap for a desktop with 2GB of RAM, plenty of HD space and general computing_

## Commit Partition Setup
* When you have finished partitioning click **Next**
* A warning will advise you that the partition setup will now be written to disk. Click **Format** to proceed
* Click **Next**

## Boot-loader
* If unsure, just accept the default setup and click **Next**

## Summary of proposed installation
* Review the summary, then click **Start Installation**
* Click **Write changes to disk** to commit the actual installation
* An introductory slide-show will then commence while the installation takes place

## All Done!
Upon re-boot, '**Kaptan**' the desktop-greeter will launch to help you configure some basic desktop settings