
pkgname=calamares
pkgver=1.0.1
pkgrel=2
pkgdesc='Distribution-independent installer framework'
arch=('x86_64')
url='https://github.com/calamares/calamares'
license=('LGPL')
depends=('qt5-svg' 'kconfig' 'ki18n' 'kcoreaddons' 'solid' 'yaml-cpp'
         'parted' 'libatasmart' 'udisks2' 'polkit-qt5' 'boost-libs'
         'rsync')
makedepends=('extra-cmake-modules' 'git' 'qt5-tools')
source=("git://github.com/rshipp/calamares"
#source=("calamares.tar.xz"
        'displaymanagers.conf'
        'locale.conf'
        'prepare.conf'
        'settings.conf'
        'packages.conf'
        'unpackfs.conf'
        'launch-calamares.sh'
        'installer.svg'
        'calamares.desktop')
#        'GreetingPage.diff'
#        'CalamaresStyle.diff'
#        'UEFI.diff'
#        'JobQueue.diff'
#        'along_UEFI.diff')
md5sums=('SKIP'
         '0364830e843823dff80b18509ea4042e'
         'c05b2dda2e0a8a57cf25cc89913a1f4f'
         '76cf16c8e4347d369330ed64ff28083b'
         '97973937b364dde58aafbf937330316e'
         'c98260c476e1a9eee8f03b01714c8099'
         'f8e10a9fa0324f68650a646769339da9'
         '2437e44479a54376ad9244d120369f6c'
         'f005a6e10b8e0425e04207920b6231b7'
         '31a21df45f1f6a9fb0aaf0d5418895f2')

prepare () {
  cd ${srcdir}/${pkgname}
  
  git submodule init
  git submodule update
  sed -i 's|Ext4|Xfs|' ${srcdir}/${pkgname}/src/modules/partition/tests/PartitionJobTests.cpp
  sed -i 's|Ext4|Xfs|' ${srcdir}/${pkgname}/src/modules/partition/gui/EraseDiskPage.cpp
  sed -i 's|Ext4|Xfs|' ${srcdir}/${pkgname}/src/modules/partition/gui/ReplacePage.cpp
  #patch -p1 -i ${srcdir}/GreetingPage.diff
  #patch -p1 -i ${srcdir}/CalamaresStyle.diff
  #patch -p1 -i ${srcdir}/UEFI.diff
  #patch -p1 -i ${srcdir}/JobQueue.diff
  #patch -p1 -i ${srcdir}/along_UEFI.diff
}

build() {
  mkdir -p build
  
  cd build
  
  cmake ../${pkgname} \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DWITH_PARTITIONMANAGER=1 \
    -DCMAKE_INSTALL_LIBDIR=lib 
  make
}

package() {
  cd build 
  make DESTDIR="${pkgdir}" install
  
  rm -rf "${pkgdir}/usr/share/calamares/settings.conf"
  install -D -m644 "${srcdir}/settings.conf" "${pkgdir}/usr/share/calamares/settings.conf"
  install -D -m644 "${srcdir}/displaymanagers.conf" "${pkgdir}/etc/calamares/modules/displaymanagers.conf"
  install -D -m644 "${srcdir}/locale.conf" "${pkgdir}/etc/calamares/modules/locale.conf"
  install -D -m644 "${srcdir}/prepare.conf" "${pkgdir}/etc/calamares/modules/prepare.conf"
  install -D -m644 "${srcdir}/unpackfs.conf" "${pkgdir}/etc/calamares/modules/unpackfs.conf"
  install -D -m644 "${srcdir}/packages.conf" "${pkgdir}/etc/calamares/modules/packages.conf"
  
  sed 's|linux312|linux|' -i "${pkgdir}/usr/share/calamares/modules/initcpio.conf"
  
  install -Dm755 "${srcdir}/launch-calamares.sh" "${pkgdir}/usr/bin/launch-calamares.sh"
  install -Dm644 "$srcdir/$pkgname.desktop" "$pkgdir/usr/share/applications/$pkgname.desktop"
  install -Dm644 "${srcdir}/installer.svg" "${pkgdir}/usr/share/pixmaps/installer.svg"
}
