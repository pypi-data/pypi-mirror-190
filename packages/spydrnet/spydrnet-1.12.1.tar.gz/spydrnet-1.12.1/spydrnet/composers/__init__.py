import os


def compose(netlist, filename, voters=[], definition_list=[], write_blackbox=True, write_eblif_cname=True, defparam = False, reinsert_space=False):
    """To compose a file into a netlist format"""
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in {".edf", ".edif"}:
        from spydrnet.composers.edif.composer import ComposeEdif
        composer = ComposeEdif()
        if netlist.name is None:
            raise Exception("netlist.name undefined")
        composer.run(netlist, filename)
    elif extension_lower in [".v", ".vh", ".vm"]:
        if reinsert_space:
            from spydrnet.util.reinsert_space import reinserting_space
            reinserting_space(netlist, voters)
        from spydrnet.composers.verilog.composer import Composer
        composer = Composer(definition_list, write_blackbox, defparam)
        composer.run(netlist, file_out=filename)
    elif extension_lower in [".eblif",".blif"]:
        from spydrnet.composers.eblif.eblif_composer import EBLIFComposer
        composer = EBLIFComposer(write_blackbox, write_eblif_cname)
        composer.run(netlist,filename)
        None
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
