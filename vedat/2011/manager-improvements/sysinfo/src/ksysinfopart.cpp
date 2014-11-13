/*  This file is part of the KDE project
    Copyright (C) 2002 Alexander Neundorf <neundorf@kde.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.
*/

#include "ksysinfopart.h"
#include <qstring.h>

#include <qtimer.h>
//Added by qt3to4:
#include <QCustomEvent>
#include <QMouseEvent>
#include <kcomponentdata.h>
#include <kglobal.h>
#include <kdebug.h>
#include <klocale.h>
#include <kstandarddirs.h>
#include <kaboutdata.h>
#include <kdeversion.h>
#include <kmenu.h>
#include <khtmlview.h>
#include <khtml_events.h>
#include <qcursor.h>
#include <kio/netaccess.h>
#include <kfileitem.h>

#include <solid/networking.h>
#include <solid/storageaccess.h>
#include <solid/storagedrive.h>
#include <solid/block.h>
#include <solid/devicenotifier.h>
#include <solid/deviceinterface.h>
#include <solid/device.h>

#include <assert.h>

extern "C"
{
   KDE_EXPORT void* init_libksysinfopart()
   {
      return new KSysinfoPartFactory;
   }
}

KComponentData* KSysinfoPartFactory::s_componentData = 0L;
KAboutData* KSysinfoPartFactory::s_about = 0L;

KSysinfoPartFactory::KSysinfoPartFactory( QObject* parent )
   : KParts::Factory( parent )
{}

KSysinfoPartFactory::~KSysinfoPartFactory()
{
   delete s_componentData;
   s_componentData = 0L;
   delete s_about;
}

KParts::Part* KSysinfoPartFactory::createPartObject( QWidget * parentWidget, QObject *,
                                 const char* /*className*/,const QStringList & )
{
   KSysinfoPart* part = new KSysinfoPart(parentWidget);
   return part;
}

KComponentData* KSysinfoPartFactory::instance()
{
   if( !s_componentData )
   {
      s_about = new KAboutData( "ksysinfopart", 0, ki18n("KSysInfo"), KDE_VERSION_STRING,
                                ki18n( "Embeddable System Information" ), KAboutData::License_GPL );
      s_componentData = new KComponentData( s_about );
   }
   return s_componentData;
}


KSysinfoPart::KSysinfoPart( QWidget * parent )
  : KHTMLPart( parent )
{
   KComponentData * instance = new KComponentData( "ksysinfopart" );
   setComponentData( *instance );

   rescanTimer=new QTimer(this);
   connect(rescanTimer, SIGNAL(timeout()), SLOT(rescan()));
   rescanTimer->setSingleShot(true);
   rescanTimer->start(20000);

   setJScriptEnabled(true);
   setJavaEnabled(false);
   setPluginsEnabled(false);
   setMetaRefreshEnabled(false);

   connect(Solid::DeviceNotifier::instance(), SIGNAL(deviceAdded(const QString &)),
            this, SLOT(deviceAction(const QString &)));
   connect(Solid::DeviceNotifier::instance(), SIGNAL(deviceRemoved(const QString &)),
            this, SLOT(rescan()));
   connect(Solid::Networking::notifier(), SIGNAL(statusChanged(Solid::Networking::Status)),
            this, SLOT(rescan()));
   installEventFilter( this );
}

void KSysinfoPart::slotResult( KJob *job)
{
  KIO::StatJob *sjob = dynamic_cast<KIO::StatJob*>(job);
  if (!job)
    return;

  KFileItemList list;
  list.append(KFileItem(sjob->statResult(), sjob->url()));
  emit browserExtension()->popupMenu(QCursor::pos(), list); //, );
}

void KSysinfoPart::customEvent( QEvent *event )
{
  if ( KParts::Event::test(event, "khtml/Events/MousePressEvent"))
  {
    khtml::MousePressEvent *ev = static_cast<khtml::MousePressEvent *>( event );
    KUrl url(ev->url().string());
    //kDebug(1242) << "URL was : " << url.path();
    if (url.path().startsWith("/") && (ev->qmouseEvent()->button() & Qt::RightButton) )
      {
          KIO::UDSEntry entry;
          KIO::Job *job = KIO::stat(url, KIO::HideProgressInfo);
          //kDebug(1242) << "entered.." << url.path();
          connect( job, SIGNAL( result( KJob * ) ),SLOT( slotResult( KJob * ) ) );
          return;
      }
    else if (ev->qmouseEvent()->button() & Qt::RightButton)
        return;
  }
  KHTMLPart::customEvent(event);
}

void KSysinfoPart::rescan()
{
  openUrl(KUrl("sysinfo:/"));
  rescanTimer->stop();
  rescanTimer->start(20000);
}

void KSysinfoPart::deviceAction(const QString &udi)
{
    Solid::Device device(udi);
    if (!device.isValid())
        return;
    if (device.is<Solid::StorageAccess>() || device.is<Solid::Block>() || device.is<Solid::StorageDrive>())
        rescan();
}

#include "ksysinfopart.moc"

