#! /usr/bin/python3

##--------------------------------------------------------------------\
#   AntennaCalculator
#   This is an imported project with several edits to work with 
#       AntennaCAT. The original project can be found at:
#       https://github.com/Dollarhyde/AntennaCalculator
#   Last update: November 1, 2025
##--------------------------------------------------------------------\


from os import sep
import ezdxf
import logging
logger = logging.getLogger(__name__)


class DXFGenerator:
    def __init__(self, args):
        self.args = args

    def generate_dxf(self, filename, W, L, x0, y0, Ws=None, separate_layers=None):

        # Initialize drawing
        doc = ezdxf.new('R2000')

        if separate_layers:
            doc1 = ezdxf.new('R2000')
            doc2 = ezdxf.new('R2000')

        # Add new entities to the modelspace:
        msp = doc.modelspace()

        if separate_layers:
            msp1 = doc1.modelspace()
            msp2 = doc2.modelspace()

        # Set up origin and supporting variables
        substrate_origin = 0.0
        originW = substrate_origin + 0.5 * W
        originL = substrate_origin + 0.5 * L

        if self.args.type == "microstrip":
            g = Ws / 3
            W_cut = (W - Ws - g * 2) / 2

        # Draw patch
        if self.args.type == "microstrip":
            points = [(originW, originL), (originW+W, originL), (originW+W, originL+L),
                ((originW+W_cut + Ws + g * 2), originL+L), (originW+W_cut + Ws + g*2, originL+L-x0), (originW+W_cut + Ws + g, originL+L - x0),
                (originW+W_cut + Ws + g, originL+L * 1.5), (originW+W_cut + g, originL+L * 1.5 ), (originW+W_cut + g, originL+L - x0),
                (originW+W_cut, originL+L - x0), (originW + W_cut, originL+L), (originW, originL+L), (originW, originL)]
            msp.add_lwpolyline(points)
            if separate_layers:
                msp1.add_lwpolyline(points)
        elif self.args.type == "probe":
            points = [(originW, originL), (originW+W, originL), (originW+W, originL+L), (originW, originL+L), (originW, originL)]
            msp.add_lwpolyline(points)
            msp.add_circle((originW+W-y0, originL+L-x0), radius=0.0005)
            if separate_layers:
                msp1.add_lwpolyline(points)
                msp1.add_circle((originW+W-y0, originL+L-x0), radius=0.0005)

        # Draw substrate
        substrate_points = [(substrate_origin, substrate_origin), (substrate_origin+2*W, substrate_origin),
        (substrate_origin+2*W, substrate_origin+2*L), (substrate_origin, substrate_origin+2*L), (substrate_origin, substrate_origin)]
        msp.add_lwpolyline(substrate_points)
        if separate_layers:
            msp2.add_lwpolyline(substrate_points)

        # Save DXF file
        doc.saveas(filename)
        if separate_layers:
            doc1.saveas(filename.split(".")[0] + "_top.dxf")
            doc2.saveas(filename.split(".")[0] + "_substrate.dxf")

        # Print message
        logger.info(f"[*] DXF file generated: {filename}")
        if separate_layers:
            base_name = filename.split(".")[0]
            logger.info(f"[*] Top Layer DXF file generated: {base_name}_top.dxf")
            logger.info(f"[*] Substrate DXF file generated: {base_name}_substrate.dxf")