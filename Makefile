INSTALL=/usr/bin/install -c

prefix=/opt
instdir=$(DESTDIR)${prefix}/asyrunner

install:
	$(INSTALL) -d $(instdir)
	$(INSTALL) -p -m 755 ./*.py $(instdir)
	$(INSTALL) -p -m 644 asyrunner.service /usr/lib/systemd/system
	-systemctl daemon-reload

uninstall:
	-systemctl stop asyrunner.service
	-systemctl disable asyrunner.service
	-cd $(instdir) && rm -rf *
	-rmdir $(instdir)
	-rm /usr/lib/systemd/system/asyrunner.service
	-systemctl daemon-reload