#! /usr/bin/python3

##--------------------------------------------------------------------\
#   AntennaCalculator
#   This is an imported project with several edits to work with 
#       AntennaCAT. The original project can be found at:
#       https://github.com/Dollarhyde/AntennaCalculator
#   Last update: November 1, 2025
##--------------------------------------------------------------------\


import gerberex # pip install pcb-tools-extension
import logging
logger = logging.getLogger(__name__)


class GerberGenerator:
    def __init__(self, args):
        self.args = args    

    def read(self, filename):
        # temporary replacement for pcb-tools-extension python 3 compatibility issue for gerberex.read()
        with open(filename, 'r') as f:
            data = f.read()
        load_gerber = gerberex.loads(data, filename)
        return load_gerber

    def generate_gerber(self, filename):
        base_name = filename.rsplit(".", 1)[0]
        
        # Generate the top layer gerber file
        tl_dxf = self.read(f'{base_name}_top.dxf')
        tl_ctx = gerberex.GerberComposition()
        tl_dxf.draw_mode = tl_dxf.DM_FILL
        tl_ctx.merge(tl_dxf)
        tl_ctx.dump(f'{base_name}_top.gtl')
        logger.info(f"[*] Top layer gerber file generated: {base_name}_top.gtl")
        
        # Generate the substrate gerber file
        s_dxf = self.read(f'{base_name}_substrate.dxf')
        s_ctx = gerberex.GerberComposition()
        s_ctx.merge(s_dxf)
        s_ctx.dump(f'{base_name}_substrate.gml')
        logger.info(f"[*] Substrate gerber file generated: {base_name}_substrate.gml")