#! /usr/bin/python3

##--------------------------------------------------------------------\
#   AntennaCalculator
#   This is an imported project with several edits to work with 
#       AntennaCAT. The original project can be found at:
#       https://github.com/Dollarhyde/AntennaCalculator
#   Last update: October 29, 2025
##--------------------------------------------------------------------\


from pint import UnitRegistry
ureg = UnitRegistry()
import logging
logger = logging.getLogger(__name__)


class Monopole:
    def __init__(self, args):
        self.args = args

    def quarter_wave_monopole(self, f):
        return(3e8 / (4 * f))

    def unit_print(self, name, value, unit=None):
        if unit != None:
            logger.info("[*]", name, "= {:.2f}".format((value*ureg.meter).to(self.args.unit)))
        else:
            logger.info("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

    def quarter_wave_monopole_calculator(self):
        f = self.args.frequency
        l = self.quarter_wave_monopole(f)
        self.unit_print("Quarter Wave Monopole Length", l, self.args.unit)
        if self.args.variable_return:
            return l





