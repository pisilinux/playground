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


#ifndef KSYSINFOPART_H
#define KSYSINFOPART_H

#include <kparts/factory.h>
#include <kparts/part.h>
#include <kparts/browserextension.h>
#include <khtml_part.h>
#include <kio/job.h>
#include <kio/jobclasses.h>
#include <kdirnotify.h>

#include <q3cstring.h>
//Added by qt3to4:
#include <QCustomEvent>

class KComponentData;
class KAboutData;

/**
 * Sysinfo Page Viewer
 * \todo: Why is it needed? Why is KHTML alone not possible?
 */
class KSysinfoPartFactory: public KParts::Factory
{
   Q_OBJECT
   public:
      KSysinfoPartFactory( QObject * parent = 0 );
      virtual ~KSysinfoPartFactory();

      virtual KParts::Part* createPartObject( QWidget * parentWidget,
                                QObject* parent, const char * classname,
                                const QStringList &args);

      static KComponentData * instance();

   private:
      static KComponentData * s_componentData;
      static KAboutData * s_about;

};

class KSysinfoPart : public KHTMLPart
{
   Q_OBJECT
   public:
      KSysinfoPart( QWidget * parent );

   protected slots:
      void rescan();
      void deviceAction( const QString &udi );
      void slotResult( KJob *job );

   protected:
      KComponentData *m_instance;
      QTimer *rescanTimer;

      void customEvent( QEvent *event );
};

#endif

