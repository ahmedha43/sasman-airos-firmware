# SASMAN CI compatibility override for the legacy pkg-config host package
include $(TOPDIR)/rules.mk

PKG_NAME:=pkg-config
PKG_VERSION:=0.22

include $(INCLUDE_DIR)/host-build.mk

define Build/Configure
endef

define Build/Compile
endef

define Build/Install
	mkdir -p $(STAGING_DIR_HOST)/bin
	install -m0755 /usr/bin/pkg-config $(STAGING_DIR_HOST)/bin/pkg-config.real
	install -m0755 ./files/pkg-config $(STAGING_DIR_HOST)/bin/pkg-config
endef

define Build/Clean
	rm -f $(STAGING_DIR_HOST)/bin/pkg-config $(STAGING_DIR_HOST)/bin/pkg-config.real
endef

$(eval $(call HostBuild))
