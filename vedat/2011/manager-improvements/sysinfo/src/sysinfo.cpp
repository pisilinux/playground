//////////////////////////////////////////////////////////////////////////
// sysinfo.cpp                                                          //
//                                                                      //
// Copyright (C)  2009  Gökmen GÖKSEL <gokmen@pardus.org.tr             //
//                      TUBITAK/UEKAE                                   //
// Copyright (C)  2005, 2008  Lukas Tinkl <lukas.tinkl@suse.cz>         //
//                                        <ltinkl@redhat.com>           //
//           (C)  2008  Dirk Mueller <dmueller@suse.de>                 //
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

#include "sysinfo.h"

#ifdef HAVE_HD_H
#include <hd.h>
#endif

#include <QFile>
#include <QDir>
#include <QTextStream>
#include <QtGui/QX11Info>
#include <QDesktopWidget>

#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <mntent.h>
#include <sys/vfs.h>
#include <string.h>
#include <sys/utsname.h>
#include <hal/libhal.h>

#include <kapplication.h>
#include <kdebug.h>
#include <kglobal.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kmimetype.h>
#include <kiconloader.h>
#include <kdeversion.h>
#include <kuser.h>
#include <kglobalsettings.h>
#include <kmountpoint.h>

#include <solid/networking.h>
#include <solid/device.h>
#include <solid/storageaccess.h>
#include <solid/storagevolume.h>
#include <solid/block.h>
#include <solid/devicenotifier.h>
#include <solid/deviceinterface.h>
#include <solid/processor.h>

#define SOLID_MEDIALIST_PREDICATE \
    "[[ StorageVolume.usage == 'FileSystem' OR StorageVolume.usage == 'Encrypted' ]" \
    " OR " \
    "[ IS StorageAccess AND StorageDrive.driveType == 'Floppy' ]]"

#define BR "<br>"

static QString formattedUnit( quint64 value, int post=1 )
{
    if (value >= (1024 * 1024))
        if (value >= (1024 * 1024 * 1024))
            return i18n("%1 GB", KGlobal::locale()->formatNumber(value / (1024 * 1024 * 1024.0),
                        post));
        else
            return i18n("%1 MB", KGlobal::locale()->formatNumber(value / (1024 * 1024.0), post));
    else
        return i18n("%1 KB", KGlobal::locale()->formatNumber(value / 1024.0, post));
}

static QString formatStr( QString st ) 
{
    if ( st == "" )
        return i18n("Not Available");
    return st;
}


static QString htmlQuote(const QVariant& _s)
{
    QString s(_s.toString());
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
}

static QString readFromFile( const QString & filename, const QString & info = QString(),
                             const char * sep = 0, bool returnlast = false )
{
    //kDebug(1242) << "Reading " << info << " from " << filename;

    QFile file( filename );

    if ( !file.exists() || !file.open( QIODevice::ReadOnly ) )
        return QString::null;

    QTextStream stream( &file );
    QString line, result;

    do
    {
        line = stream.readLine();
        if ( !line.isEmpty() )
        {
            if ( !sep )
                result = line;
            else if ( line.startsWith( info ) )
                result = line.section( sep, 1, 1 );

            if (!result.isEmpty() && !returnlast)
                return result;
        }
    } while (!line.isNull());

    return result;
}

static QString netStatus()
{
    switch (Solid::Networking::status())
    {
    case Solid::Networking::Disconnecting:
        return i18n( "Network is <strong>shutting down</strong>" );
    case Solid::Networking::Connecting:
        return i18n( "<strong>Establishing</strong> connection to the network" );
    case Solid::Networking::Connected:
        return i18n( "You are <strong>online</strong>" );
    case Solid::Networking::Unconnected:
        return i18n( "You are <strong>offline</strong>" );
    case Solid::Networking::Unknown:
    default:
        return i18n( "Unknown network status" );
    }
}

kio_sysinfoProtocol::kio_sysinfoProtocol( const QByteArray & pool_socket, const QByteArray & app_socket )
    : SlaveBase( "kio_sysinfo", pool_socket, app_socket )
{
    m_predicate = Solid::Predicate::fromString(SOLID_MEDIALIST_PREDICATE);
}

kio_sysinfoProtocol::~kio_sysinfoProtocol()
{
}

QString kio_sysinfoProtocol::startStock( const QString title, const QString liveID)
{
    QString templator = QString ("<table class=\"stock\">"
                                 "<tr>"
                                 "     <th colspan=3><h2>%1</h2></th>"
                                 "</tr>").arg(title);
    if ( liveID != "")
        templator += QString("<span id=\"%1\">").arg(liveID);

    return templator;
}

QString kio_sysinfoProtocol::addToStock( const QString _icon, const QString text, const QString details, const QString link )
{
    QString iconpath = icon(_icon, 22, true);
    QString templator;
    QString temp = "";

    if ( link != "" )
        temp = QString(" onClick=\"location.href='%1'\" ").arg(link);

    templator += QString ("<tr class=\"info\" %1>").arg(temp);
    templator += QString ("<td><img src=\"%1\"></td><td>%2").arg(iconpath).arg(text);

    if ( details != "" )
        templator += QString("<span class=\"detail\">[ %1 ]</span>").arg(details);

    templator += "</td><td></td></tr>";
    return templator;
}

QString kio_sysinfoProtocol::addProgress( const QString _icon, const unsigned long long size )
{
    QString iconpath = icon(_icon, 22, true);
    QString progress = "file:" + KStandardDirs::locate( "data", "sysinfo/about/images/progress.png" );
    QString templator;

    templator += QString ("<tr class=\"progress\">");
    templator += QString ("<td><img src=\"%1\"></td>").arg(iconpath);
    templator += QString ("<td><img src=\"%1\" width=\"%2%\"></td><td></td></tr>").
                         arg(progress).arg(size);
    return templator;
}

QString kio_sysinfoProtocol::finishStock( bool isLive )
{
    if ( isLive )
        return QString("</span></table>");
    return QString ("</table>");
}

QString kio_sysinfoProtocol::icon( const QString & name, int size, bool justPath) const
{
    QString path = KIconLoader::global()->iconPath( name, -size );
    if ( justPath == true )
        return QString( "file:%1" ).arg( path );
    return QString( "<img src=\"file:%1\" width=\"%2\" height=\"%3\" valign=\"center\"/>" )
        .arg( htmlQuote(path) ).arg( size ).arg( size );
}

void kio_sysinfoProtocol::get( const KUrl &)
{
    mimeType( "application/x-sysinfo" );
    // header
    QString location = KStandardDirs::locate( "data", "sysinfo/about/index.html" );
    QFile f( location );
    f.open( QIODevice::ReadOnly );
    QTextStream t( &f );

    QString content = t.readAll();

    infoMessage( i18n( "Looking for hardware information..." ) );

    content = content.arg( i18n( "System" ) ); // <title>
    content = content.arg( "file:" + KStandardDirs::locate( "data", "sysinfo/about/stil.css" ) );

    QString dynamicInfo, staticInfo;

    // Dynamic Info

    // common folders
    dynamicInfo += startStock( i18n( "Common Folders" ) );
    dynamicInfo += addToStock( "folder-home", i18n( "My Home Folder" ), QDir::homePath(), "file:" + QDir::homePath() );
    dynamicInfo += addToStock( "folder-red", i18n( "Root Folder" ), QDir::rootPath(), "file:" + QDir::rootPath() );
    dynamicInfo += addToStock( "folder-remote", i18n( "Network Folders" ), "remote:/" , "remote:/" );
    dynamicInfo += finishStock();

    // net info
    QString state = netStatus();
    dynamicInfo += startStock( i18n( "Network" ), "idNetwork" );
    dynamicInfo += addToStock( "applications-internet", state);
    dynamicInfo += finishStock( true );

    // memory info
    memoryInfo();

    dynamicInfo += startStock( i18n( "Memory" ) );
    dynamicInfo += addToStock( "media-flash",
                                i18n( "Ram : %1 free of %2", m_info[MEM_FREERAM].toString(), m_info[MEM_TOTALRAM].toString()));
    dynamicInfo += addToStock("media-flash",(m_info[MEM_TOTALSWAP]!="0" ?
                                  i18n("Swap: %1 free of %2", m_info[MEM_FREESWAP].toString(), m_info[MEM_TOTALSWAP].toString()):
                                  i18n("Swap: Not in use")));

    dynamicInfo += finishStock();

    content = content.arg( dynamicInfo ); // put the dynamicInfo text into the dynamic left box

    // Disk Info

    content = content.arg( i18n( "Disks" ) );
    content = content.arg(diskInfo()); // put the discInfo text into the disk right box

    // Static Info
    getArch();
    // Os info
    osInfo();
    staticInfo += startStock( i18n( "Operating System" ) );
    staticInfo += addToStock( "computer", m_info[OS_SYSNAME].toString() +
                              " <b>" + m_info[OS_RELEASE].toString() + "</b>",
                              m_info[OS_USER].toString() + "@" + m_info[OS_HOSTNAME].toString() );
    staticInfo += addToStock( "computer", i18n( "Kde <b>%1</b> on <b>%2</b>", KDE::versionString(), m_info[OS_SYSTEM].toString()), m_info[ARCH].toString());
    staticInfo += finishStock();

    // update content..
    content = content.arg( staticInfo );
    staticInfo = "";

    // CPU info
    cpuInfo();
    if ( !m_info[CPU_MODEL].isNull() )
    {
        staticInfo += startStock( i18n( "Processor" ) );
        staticInfo += addToStock( "cpu", m_info[CPU_MODEL].toString(), m_info[CPU_TEMP].toString());
        staticInfo += addToStock( "cpu", i18n( "%1 MHz", KGlobal::locale()->formatNumber( m_info[CPU_SPEED].toDouble(), 2 )),
                                         m_info[CPU_CORES].toString() + i18n( " core" ));
        staticInfo += finishStock();
    }

    // update content..
    content = content.arg( staticInfo );
    staticInfo = "";

    // OpenGL info
    if ( glInfo() )
    {
        staticInfo += startStock( i18n( "Display" ) );
        staticInfo += addToStock( "video-display", formatStr(m_info[GFX_MODEL].toString()), formatStr(m_info[GFX_VENDOR].toString()) );
        if (!m_info[GFX_DRIVER].isNull())
            staticInfo += addToStock( "xorg", m_info[GFX_DRIVER].toString(), m_info[GFX_3D].toString());
        staticInfo += finishStock();
    }

    // update content
    content = content.arg( staticInfo );
    staticInfo = "";

    // Send the data
    data( content.toUtf8() );
    data( QByteArray() );
    finished();

}

void kio_sysinfoProtocol::updateContent( const QString liveID )
{
    QString cont = liveID;
    data( cont.toUtf8() );
    data( QByteArray() );
    finished();
}

void kio_sysinfoProtocol::mimetype( const KUrl & /*url*/ )
{
    mimeType( "application/x-sysinfo" );
    finished();
}

static QString formatMemory(unsigned long long value)
{
    // value is in kB
    double temp;

    if (value <= 0)
        return "0";

    temp = value / 1024.0; // MB
    if (temp >= 1024) {
        temp /= 1024.0; // GB
        return i18n("%1 GB").arg(KGlobal::locale()->formatNumber(temp));
    }
    return i18n("%1 MB").arg(KGlobal::locale()->formatNumber(temp));
}

void kio_sysinfoProtocol::memoryInfo(void)
{
    QFile file("/proc/meminfo");
    unsigned long long memtotal = 0,
                       memfree = 0,
                       buffers = 0,
                       cached = 0,
                       swaptotal = 0,
                       swapfree = 0;

    // Parse /proc/meminfo for memory usage statistics
    if (file.exists() && file.open(QIODevice::ReadOnly))
    {
        QTextStream stream(&file);
        QString line;

        // Avoid using stream.atEnd() for /proc files as it always returns 1 in Qt4.
        do
        {
            line = stream.readLine();
            if (!line.isEmpty())
            {
                if (line.startsWith("MemTotal"))
                    memtotal = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
                else if (line.startsWith("MemFree"))
                    memfree = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
                else if (line.startsWith("Buffers"))
                    buffers = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
                else if (line.startsWith("Cached"))
                    cached = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
                else if (line.startsWith("SwapTotal"))
                    swaptotal = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
                else if (line.startsWith("SwapFree"))
                    swapfree = line.section(":", 1, 1).replace(" kB", "").trimmed().toULongLong();
            }
        }
        while (!line.isNull());
    }

    // Disk cache and buffers are ignored as they will always be available
    // upon request before swapping.
    m_info[MEM_TOTALSWAP] = formatMemory(swaptotal);
    m_info[MEM_FREESWAP] = formatMemory(swapfree);
    m_info[MEM_TOTALRAM] = formatMemory(memtotal);
    m_info[MEM_FREERAM] = formatMemory(memfree+buffers+cached);
}

void kio_sysinfoProtocol::osInfo()
{
    struct utsname uts;
    uname( &uts );
    m_info[ OS_SYSNAME ] = uts.sysname;
    m_info[ OS_RELEASE ] = uts.release;
    m_info[ OS_VERSION ] = uts.version;
    m_info[ OS_MACHINE ] = uts.machine;
    m_info[ OS_HOSTNAME ] = uts.nodename;

    m_info[ OS_USER ] = KUser().loginName();

    m_info[ OS_SYSTEM ] = readFromFile( "/etc/pardus-release" );
    m_info[ OS_SYSTEM ].toString().replace("X86-64", "x86_64");
}

void kio_sysinfoProtocol::cpuInfo()
{
    QString speed = readFromFile( "/proc/cpuinfo", "cpu MHz", ":" );

    if ( speed.isNull() )    // PPC?
        speed = readFromFile( "/proc/cpuinfo", "clock", ":" );

    if ( speed.endsWith( "MHz", Qt::CaseInsensitive ) )
        speed = speed.left( speed.length() - 3 );

    m_info[CPU_SPEED] = speed.toFloat();

    const char* const names[] = { "THM0", "THRM", "THM" };
    for ( unsigned i = 0; i < sizeof(names)/sizeof(*names); ++i )
    {
        m_info[CPU_TEMP] = readFromFile(QString("/proc/acpi/thermal_zone/%1/temperature").arg(names[i]), "temperature", ":");
        m_info[CPU_TEMP] = m_info[CPU_TEMP].toString().trimmed();
        m_info[CPU_TEMP] = m_info[CPU_TEMP].toString().replace(" C",QString::fromUtf8("°C"));
        if (!m_info[CPU_TEMP].isNull())
            break;
    }

    // Use Solid to get Processor Information
    // Ignore Solid for 2011
    //
    // QList<Solid::Device> list = Solid::Device::listFromType(Solid::DeviceInterface::Processor, QString());
    // if ( list.size() == 0 ) {
    m_info[CPU_CORES] = int(readFromFile( "/proc/cpuinfo", "processor", ":", true ).toInt()) + 1;
    m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "model name", ":" );
    // } else {
    //     Solid::Device device = list[0];
    //     m_info[CPU_CORES] = list.size();
    //     m_info[CPU_MODEL] = device.product();
    // }
}

#include <GL/glx.h>

bool isOpenGlSupported() {

    int scr = 0;               // print for screen 0
    Display *dpy;              // Active X display
    GLXContext ctx;            // GLX context
    XVisualInfo *visinfo;      // Visual info
    char *displayname = NULL;  // Server to connect
    Bool allowDirect = true;   // Direct rendering only
    Bool isEnabled = false;

    // GLX attributes
    int attribSingle[] = {
        GLX_RGBA,
        GLX_RED_SIZE,   1,
        GLX_GREEN_SIZE, 1,
        GLX_BLUE_SIZE,  1,
        None
    };
    int attribDouble[] = {
        GLX_RGBA,
        GLX_RED_SIZE, 1,
        GLX_GREEN_SIZE, 1,
        GLX_BLUE_SIZE, 1,
        GLX_DOUBLEBUFFER,
        None
    };

    // Open the display with screen#:scr to fiddle with
    dpy = XOpenDisplay (displayname);

    if (!dpy)
        return false;

    visinfo = glXChooseVisual(dpy, scr, attribSingle);
    if (!visinfo) 
    {
        visinfo = glXChooseVisual(dpy, scr, attribDouble);
        if (!visinfo) 
        {
            XCloseDisplay (dpy);
            return false;
        }
    }

    ctx = glXCreateContext( dpy, visinfo, NULL, allowDirect );
    if (!ctx) 
    {
       fprintf(stderr, "Error: glXCreateContext failed\n");
       XFree(visinfo);
       XCloseDisplay (dpy);
       return false;
    }

    if(glXIsDirect(dpy, ctx))
        isEnabled = true;

    glXDestroyContext (dpy,ctx);
    XFree(visinfo);
    XCloseDisplay (dpy);

    return isEnabled;
}

bool kio_sysinfoProtocol::glInfo()
{
    FILE *fd = popen( "glxinfo", "r" );
    if ( !fd )
        return false;

    bool openGlSupported = isOpenGlSupported();
    QTextStream is( fd, QIODevice::ReadOnly );

    while ( !is.atEnd() )
    {
        QString line = is.readLine();
        if ( line.startsWith( "OpenGL vendor string:" ) )
            m_info[GFX_VENDOR] = line.section(':', 1, 1);
        else if ( line.startsWith( "OpenGL renderer string:" ) )
            m_info[GFX_MODEL] = line.section(':', 1, 1);
        else if ( line.startsWith( "OpenGL version string:" ) )
            m_info[GFX_DRIVER] = line.section(':', 1, 1);
    }

    if (!openGlSupported or m_info[GFX_MODEL].toString().contains("Software Rasterizer"))
        m_info[GFX_3D] = i18n("3D Not Supported");
    else
        m_info[GFX_3D] = i18n("3D Supported");

    pclose( fd );
    return true;
}

void kio_sysinfoProtocol::getArch()
{
    FILE *fd = popen( "arch", "r" );
    if ( !fd ){
        m_info[ARCH] = i18n("Not Available");
    }
        else {
        QTextStream is( fd, QIODevice::ReadOnly );

         while ( !is.atEnd() )
        {
        QString line = is.readLine();
            if (!line.isNull()){
                m_info[ARCH] = line;
            }
        }

    }
    pclose( fd );

}

QString kio_sysinfoProtocol::diskInfo()
{
    QString result;
    if ( fillMediaDevices() )
    {
        for ( QList<DiskInfo>::ConstIterator it = m_devices.constBegin(); it != m_devices.constEnd(); ++it )
        {
            DiskInfo di = ( *it );
            unsigned long long usage,percent,peer;
            QString label = di.label;
            QString mountState = di.mounted ? i18n( "Mounted on %1", di.mountPoint) : i18n( "Not mounted" );
            QString path = di.mounted ? "file://" + di.mountPoint : "";
            QString emblem = di.mounted ? QString("<div style=\"background:url('%1') no-repeat;background-position:bottom right;width:48px;height:48px;\" \\>").arg( icon( "emblem-mounted", 22, true) ) : "";

            QString tooltip = di.model;

            usage = di.total - di.avail;
            peer = di.total / 100;
            peer == 0 ? percent = 0 : percent = usage / peer;
            QString sizeStatus = i18n( "%1 free of %2", formattedUnit( di.avail,0 ), formattedUnit( di.total,0 ) );

            result +=   QString("<tr class=\"media\">"
                                "   <td>"
                                "   <a href=\"%1\" title=\"%2\">"
                                "       <div style=\"background:url('%3') no-repeat;width:48px;height:48px;\">"
                                "       %4"
                                "   </div></a></td>").
                                arg( path ).
                                arg( tooltip+" "+di.deviceNode ).
                                arg( icon( di.iconName, 48, true) ).
                                arg( emblem );

            result +=   QString("   <td>"
                                "       <span class=\"detail\">[ %1 ]<br><span style=\"float:right\">[ %2 ]</span></span>"
                                "       <a href=\"%3\" title=\"%4\">"
                                "       %5<br><span class=\"mediaDf\">%6</span><br></a>"
                                "       <img class=\"diskusage\" src=\"file:%7\" width=\"%8%\">"
                                "   </td>"
                                "   <td></td>"
                                "</tr>").
                                arg( mountState ).
                                arg( di.fsType ).
                                arg( path ).
                                arg( tooltip+" "+di.deviceNode ).
                                arg( label ).
                                arg( sizeStatus ).
                                arg( KStandardDirs::locate( "data", "sysinfo/about/images/progress.png" ) ).
                                arg( percent );
        }
    }
    return result;

}

extern "C" int KDE_EXPORT kdemain(int argc, char **argv)
{
    KComponentData componentData( "kio_sysinfo" );
    ( void ) KGlobal::locale();

    kDebug(1242) << "*** Starting kio_sysinfo ";

    if (argc != 4) {
        kDebug(1242) << "Usage: kio_sysinfo  protocol domain-socket1 domain-socket2";
        exit(-1);
    }

    kio_sysinfoProtocol slave(argv[2], argv[3]);
    slave.dispatchLoop();

    kDebug(1242) << "*** kio_sysinfo Done";
    return 0;
}

bool kio_sysinfoProtocol::fillMediaDevices()
{
    QStringList devices;

    const QList<Solid::Device> &deviceList = Solid::Device::listFromQuery(m_predicate);

    if (deviceList.isEmpty())
    {
        kDebug(1242) << "DEVICE LIST IS EMPTY!";
        return false;
    }

    m_devices.clear();

    foreach(const Solid::Device &device, deviceList)
    {
        if (!device.isValid())
            continue;

        const Solid::StorageAccess *access = device.as<Solid::StorageAccess>();
        const Solid::StorageVolume *volume = device.as<Solid::StorageVolume>();
        const Solid::Block *block = device.as<Solid::Block>();

        DiskInfo di;

        di.id = device.udi();
        if (access)
            di.mountPoint = access->filePath();

        if (volume)
            di.label = volume->label();
        if (di.label.isEmpty())
            di.label = di.mountPoint;
        di.mountable = access != 0;
        if (block)
            di.deviceNode = block->device();
        if (volume)
            di.fsType = volume->fsType();
        di.mounted = access && access->isAccessible();
        di.iconName = device.icon();
        di.model = device.product();
        di.total = di.avail = 0;

        if (volume)
            di.total = volume->size();

        // calc the free/total space
        struct statfs sfs;
        if ( di.mounted && statfs( QFile::encodeName( di.mountPoint ), &sfs ) == 0 )
        {
            di.total = ( unsigned long long )sfs.f_blocks * sfs.f_bsize;
            di.avail = ( unsigned long long )( getuid() ? sfs.f_bavail : sfs.f_bfree ) * sfs.f_bsize;
        }

        m_devices.append( di );
    }

    // this is ugly workaround, should be in HAL but there is no LVM support
    QRegExp rxlvm("^/dev/mapper/\\S*-\\S*");

    const KMountPoint::List mountPoints = KMountPoint::currentMountPoints(KMountPoint::NeedRealDeviceName);

    foreach( KMountPoint::Ptr mountPoint, mountPoints)
    {
        if ( rxlvm.exactMatch( mountPoint->realDeviceName() ) )
        {
            DiskInfo di;

            di.mountPoint = mountPoint->mountPoint();
            di.label = di.mountPoint;
            di.mountable = di.mounted = true;
            di.deviceNode = mountPoint->realDeviceName();
            di.fsType = mountPoint->mountType();
            di.iconName = QString::fromLatin1( "drive-harddisk" );

            di.total = di.avail = 0;

            // calc the free/total space
            struct statfs sfs;
            if ( di.mounted && statfs( QFile::encodeName( di.mountPoint ), &sfs ) == 0 )
            {
                di.total = ( unsigned long long )sfs.f_blocks * sfs.f_bsize;
                di.avail = ( unsigned long long )( getuid() ? sfs.f_bavail : sfs.f_bfree ) * sfs.f_bsize;
            }
            m_devices.append( di );
        }
    }
    return true;
}
