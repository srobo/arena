# Flag Assembly Guide
all: deploy

flag_assembly_guide:
	mkdir -p flag_assembly_guide

flag_assembly_guide/readme.html: flag_assembly_guide guide/readme/readme.md
	pandoc guide/readme/readme.md -o "flag_assembly_guide/readme.html" --template=guide/readme/template.html

deploy: flag_assembly_guide/readme.html links 
	mkdir -p flag_assembly_guide/photos
	cp guide/readme/photos/* flag_assembly_guide/photos/
	zip flag_assembly_guide.zip -r flag_assembly_guide/
	@echo "WARNING: Files being zipped include .eps files for razorlab, which need to be manually regenerated with the .jsx script in this directory if the .dxf files have been changed."

links: flag_assembly_guide
	mkdir -p flag_assembly_guide/790x380
	cp -ru  sr2015_flag_razorlab_panel1_reva.dxf flag_assembly_guide/790x380/sr2015_flag_razorlab_panel1_reva.dxf
	cp -ru sr2015_flag_razorlab_panel2_reva.dxf flag_assembly_guide/790x380/sr2015_flag_razorlab_panel2_reva.dxf
	mkdir -p flag_assembly_guide/600x400
	cp -ru 600mmx400mm_A.dxf flag_assembly_guide/600x400/600mmx400mm_A.dxf
	cp -ru 600mmx400mm_B_x2.dxf flag_assembly_guide/600x400/600mmx400mm_B_x2.dxf
	mkdir -p flag_assembly_guide/razorlab
	cp -ru sr2015_flag_razorlab_panel1_reva.eps flag_assembly_guide/razorlab/sr2015_flag_razorlab_panel1_reva.eps
	cp -ru sr2015_flag_razorlab_panel2_reva.eps flag_assembly_guide/razorlab/sr2015_flag_razorlab_panel2_reva.eps

clean:
	rm -rf flag_assembly_guide
	rm -rf flag_assembly_guide.zip
