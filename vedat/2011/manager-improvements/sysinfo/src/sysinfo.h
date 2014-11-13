//////////////////////////////////////////////////////////////////////////
// sysinfo.h                                                            //
//                                                                      //
// Copyright (C)  2009  Gökmen GÖKSEL <gokmen@pardus.org.tr             //
//                      TUBITAK/UEKAE                                   //
// Copyright (C)  2005  Lukas Tinkl <lukas.tinkl@suse.cz>               //
//                                                                      //
// This program is free software; you can redistribute it and/or        //
// modify it under the terms of the GNU General Public License          //
// as published by the Free Software Foundation; either version 2       //
// of the License, or (at your option) any later version.               //
//                                                                      //
// This program is distributed in the hope that it will be useful,      //
// but WITHOUT ANY WARRANTY; without even the implied warranty of       //
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        //
// GNU General Public License for more details.                         //
//                                                                      //
// You should have received a copy of the GNU General Public License    //
// along with this program; if not, write to the Free Software          //
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA        //
// 02110-1301, USA.                                                     //
//////////////////////////////////////////////////////////////////////////

#ifndef _sysinfo_H_
#define _sysinfo_H_

#include <qstring.h>
#include <qmap.h>
#include <QtCore/QtGlobal>
#include <qstringlist.h>

#include <kurl.h>
#include <kicontheme.h>
#include <kio/global.h>
#include <kio/slavebase.h>

#include <solid/predicate.h>

struct DiskInfo
{
    // taken from media:/
    QString id;
    QString name;
    QString label;
    bool mountable;
    QString deviceNode;
    QString mountPoint;
    QString fsType;
    bool mounted;
    QString iconName;
    QString model;

    // own stuff
    quint64 total, avail; // space on device
};


/**
 * System information IO slave.
 *
 * Produces an HTML page with system information overview
 */
class kio_sysinfoProtocol : public KIO::SlaveBase
{

public:
    kio_sysinfoProtocol( const QByteArray &pool_socket, const QByteArray &app_socket );
    virtual ~kio_sysinfoProtocol();
    virtual void mimetype( const KUrl& url );
    virtual void get( const KUrl& url);

    /**
     * Info field
     */
    enum
    {
        MEM_TOTALRAM = 0,       // in sysinfo.mem_unit
        MEM_FREERAM,
        MEM_TOTALSWAP,
        MEM_FREESWAP,
        MEM_USAGE,
        SYSTEM_UPTIME,          // in seconds
        CPU_MODEL,
        CPU_SPEED,              // in MHz
        CPU_CORES,
        CPU_TEMP,
        OS_SYSNAME,             // man 2 uname
        OS_RELEASE,
        OS_VERSION,
        OS_MACHINE,
        OS_USER,                // username
        OS_SYSTEM,              // OS version
        OS_HOSTNAME,
        GFX_VENDOR,              // Display stuff
        GFX_MODEL,
        GFX_DRIVER,
        GFX_3D,
        SYSINFO_LAST,
        ARCH
    };

private:
    /**
     * Gather basic memory info
     */
    void memoryInfo();

    /**
     * Gather CPU info
     */
    void cpuInfo();

    /**
     * @return a formatted table with disk partitions
     */
    QString diskInfo();

    /**
     * Get info about kernel and OS version (uname)
     */
    void osInfo();

    /**
     * Gather basic OpenGL info
     */
    bool glInfo();

    /**
     * Gather Hardware platform
     */
    void getArch();

    /**
     * Helper function to locate a KDE icon
     * @return img tag with full path to the icon
     */
    QString icon( const QString & name, int size = KIconLoader::SizeSmall, bool justPath = false) const;

    /**
     * Fill the list of devices (m_devices) with data from the media KIO protocol
     * @return true on success
     */
    bool fillMediaDevices();

    /**
     * Map holding the individual info attributes
     */
    QMap<int, QVariant> m_info;

    QString startStock( const QString title, const QString liveID = "");
    QString addToStock( const QString _icon, const QString text, const QString details = "", const QString link = "" );
    QString addProgress( const QString _icon, const unsigned long long size );
    QString finishStock( bool isLive = false);

    void updateContent( const QString liveID );
    QList<DiskInfo> m_devices;
    Solid::Predicate m_predicate;
};

#endif
