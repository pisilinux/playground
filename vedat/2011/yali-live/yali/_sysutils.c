/*
* Copyright (c) 2005 - 2008 TUBITAK/UEKAE
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the
* Free Software Foundation; either version 2 of the License, or (at your
* option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <linux/cdrom.h>
#include <fcntl.h>
#include <unistd.h>
#include <ext2fs/ext2fs.h>
#include <sys/mount.h>
#include <sys/ioctl.h>
#include <sys/vfs.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/reboot.h>


PyDoc_STRVAR(umount__doc__,
"umount(target)\n"
"\n"
"method implements the umount(2) system call in Linux\n");

static PyObject*
_sysutils_umount(PyObject *self, PyObject *args)
{
  int ok;
  const char *tgt;

  if (!PyArg_ParseTuple(args, "s", &tgt))
  {
      Py_INCREF(Py_None);
      return Py_None;
  }

  ok = umount2(tgt, MNT_FORCE);

  return PyInt_FromLong( (long) ok );
}



PyDoc_STRVAR(eject__doc__,
"eject(mount_point)\n"
"ejects the cdrom mounted.\n"
"");

static PyObject*
_sysutils_eject(PyObject *self, PyObject *args)
{
    int fd=-1;
    const char *mount_point;

    if (!PyArg_ParseTuple(args, "s", &mount_point))
        goto failed;

    fd = open(mount_point, O_RDONLY|O_NONBLOCK, 0);
    if (fd == -1)
        goto failed;

    if (ioctl(fd, CDROMEJECT, 0))
        goto failed;

    close(fd);
    Py_INCREF(Py_True);
    return Py_True;

failed:
    if (fd != -1)
        close(fd);
    Py_INCREF(Py_False);
    return Py_False;
}



PyDoc_STRVAR(fastreboot__doc__,
"fastreboot()\n"
"\n"
"sync() and reboot() if root user ;)!\n");

void
_sysutils_fastreboot(PyObject *self)
{

  if (getuid() != 0)
    {
      return;
    }

  sync();
  sync();
  sync();
  reboot(RB_AUTOBOOT);
}


static int get_bits(unsigned long long v) {
    int  b = 0;

    if ( v & 0xffffffff00000000LLU ) { b += 32; v >>= 32; }
    if ( v & 0xffff0000LLU ) { b += 16; v >>= 16; }
    if ( v & 0xff00LLU ) { b += 8; v >>= 8; }
    if ( v & 0xf0LLU ) { b += 4; v >>= 4; }
    if ( v & 0xcLLU ) { b += 2; v >>= 2; }
    if ( v & 0x2LLU ) b++;

    return v ? b + 1 : b;
}

static PyObject * doDevSpaceFree(PyObject * s, PyObject * args) {
    char * path;
    struct statfs sb;
    unsigned long long size;

    if (!PyArg_ParseTuple(args, "s", &path)) return NULL;

    if (statfs(path, &sb)) {
        PyErr_SetFromErrno(PyExc_SystemError);
        return NULL;
    }

    /* Calculate a saturated addition to prevent oveflow. */
    if ( get_bits(sb.f_bfree) + get_bits(sb.f_bsize) <= 64 )
        size = (unsigned long long)sb.f_bfree * sb.f_bsize;
    else
        size = ~0LLU;

    return PyLong_FromUnsignedLongLong(size>>20);
}

static PyObject * doExt2Dirty(PyObject * s, PyObject * args) {
    char * device;
    ext2_filsys fsys;
    int rc;
    int clean;

    if (!PyArg_ParseTuple(args, "s", &device)) return NULL;

    rc = ext2fs_open(device, EXT2_FLAG_FORCE, 0, 0, unix_io_manager, &fsys);
    if (rc) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    clean = fsys->super->s_state & EXT2_VALID_FS;

    ext2fs_close(fsys);

    return Py_BuildValue("i", !clean); 
}
static PyObject * doExt2HasJournal(PyObject * s, PyObject * args) {
    char * device;
    ext2_filsys fsys;
    int rc;
    int hasjournal;

    if (!PyArg_ParseTuple(args, "s", &device)) return NULL;
    rc = ext2fs_open(device, EXT2_FLAG_FORCE, 0, 0, unix_io_manager,&fsys);
    if (rc) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    hasjournal = fsys->super->s_feature_compat & EXT3_FEATURE_COMPAT_HAS_JOURNAL;

    ext2fs_close(fsys);

    return Py_BuildValue("i", hasjournal); 
}
static PyMethodDef _sysutils_methods[] = {
    {"umount",  (PyCFunction)_sysutils_umount,  METH_VARARGS,  umount__doc__},
    {"eject",  (PyCFunction)_sysutils_eject,  METH_VARARGS,  eject__doc__},
    {"fast_reboot",  (PyCFunction)_sysutils_fastreboot,  METH_NOARGS,  fastreboot__doc__},
    {"device_space_free", (PyCFunction) doDevSpaceFree, METH_VARARGS, NULL },
    { "e2dirty", (PyCFunction) doExt2Dirty, METH_VARARGS, NULL },
    { "e2hasjournal", (PyCFunction) doExt2HasJournal, METH_VARARGS, NULL },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC
init_sysutils(void)
{
    PyObject *m;

    m = Py_InitModule("_sysutils", _sysutils_methods);

    return;
}
