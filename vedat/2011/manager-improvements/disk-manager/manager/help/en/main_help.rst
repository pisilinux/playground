Disk Manager
------------

You do configure how your disk partitions will be initialized at system startup with **Disk Manager**. Disks are integrated into system's file system with this configuration. So that you do not have to mount your disks manually again and again. Disk Manager also allows you to mount or unmount your disk partitions.


Adding An Entry For Mounting Disk Automaticaly
----------------------------------------------

If you want a partition to be mounted to a specific point in system for every startup, you must add an entry with **Disk Manager**. In order to add an entry, first of all, select the disk partition you want to add from the list of **Disk Manager**. Check the 'Mount Automatically' checkbox below the list and set related values. Here are what these values can be and their descriptions:

* Mount Point: System mounts your disk partition to mount point in its file system. '/media' and '/mnt' are widely used points for mounting devices. For example, /media/MyDisk can be a mount point.
* File System Type: File system type of your disk partition. Select the type you chose while you were creating your partition. If you don't know what is your partition's file system type, you can learn it via 'blkid' command. 
* Additional Options: System uses these options at startup while disk is being mounted to system. **Disk Manager** adds some default options for your disk's file system type. If you want to add some additional options, you can. Man pages for mount gives you more information about these options. And there is a 'Reset' button for setting options to default value.

After these steps by clicking the 'Save' button you can add the entry. If any error occurs system will inform you otherwise system will try to mount your partition to system and it will be mounted if it is not alredy.

Deleting An Entry
-----------------

In order to delete an entry select related disk partition from the list and uncheck the 'Mount Automatically' checkbox below the list. Then click the 'Save' button.


Mounting A Partition
--------------------

In order to mount a disk partition to your system, select it from the list and click the 'Mount' button.


Unmounting A Partition
----------------------

In order to unmount a disk partition from your system, select it from the list and click the 'Unmount' button.


