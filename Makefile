INSTALL=/usr/bin/install -c

prefix=/usr/local/share
instdir=$(DESTDIR)${prefix}/asyserver

all:

install:
	$(INSTALL) -d $(instdir)
	$(INSTALL) -p -m 755 ./*.py $(instdir)
	$(INSTALL) -p -m 644 asyserver.service /usr/lib/systemd/system
	-systemctl daemon-reload

uninstall:
	-systemctl stop asyserver
	-systemctl disable asyserver
	-cd $(instdir) && rm -rf *
	-rmdir $(instdir)
	-rm /usr/lib/systemd/system/asyserver.service
	-systemctl daemon-reload
