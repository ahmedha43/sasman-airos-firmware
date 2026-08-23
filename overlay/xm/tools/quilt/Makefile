# SASMAN CI compatibility override for the legacy quilt host package
include $(TOPDIR)/rules.mk

PKG_NAME:=quilt
PKG_VERSION:=0.47
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://download.savannah.gnu.org/releases/$(PKG_NAME)
PKG_MD5SUM:=d33d2442bd34387260b1c1db3e623af0

include $(INCLUDE_DIR)/host-build.mk

define Build/Configure
endef

define Build/Compile
endef

define Build/Install
	mkdir -p $(STAGING_DIR_HOST)/bin
	install -m0755 /usr/bin/quilt $(STAGING_DIR_HOST)/bin/quilt
endef

define Build/Clean
	rm -f $(STAGING_DIR_HOST)/bin/quilt
endef

$(eval $(call HostBuild))
