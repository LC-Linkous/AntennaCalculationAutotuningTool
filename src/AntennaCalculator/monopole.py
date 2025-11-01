#! /usr/bin/python3

##--------------------------------------------------------------------\
#   AntennaCalculator
#   This is an imported project with several edits to work with 
#       AntennaCAT. The original project can be found at:
#       https://github.com/Dollarhyde/AntennaCalculator
#   Last update: November 1, 2025
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
        if unit is not None:
            logger.info(f"[*] {name} = {(value * ureg.meter).to(self.args.unit):.2f}")
        else:
            logger.info(f"[*] {name} = {(value * ureg.meter).to_compact():.2f}")

    def quarter_wave_monopole_calculator(self):
        f = self.args.frequency
        l = self.quarter_wave_monopole(f)
        self.unit_print("Quarter Wave Monopole Length", l, self.args.unit)
        if self.args.variable_return:
            return l





