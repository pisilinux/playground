# (tmb) Simple defconfig updater
for arch in x86_64 i386 arm64 arm; do
    for config in defconfig-$arch-*; do
	mv $config .config
	make oldconfig ARCH=$arch
	mv .config $config
    done
done
