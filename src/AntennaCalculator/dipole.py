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


class Dipole:
    def __init__(self, args):
        self.args = args

    def half_wave_dipole(self, f):
        return(3e8 / (2 * f))

    def unit_print(self, name, value, unit=None):
        if unit is not None:
            logger.info(f"[*] {name} = {(value * ureg.meter).to(self.args.unit):.2f}")
        else:
            logger.info(f"[*] {name} = {(value * ureg.meter).to_compact():.2f}")

    def half_wave_dipole_calculator(self):
        f = self.args.frequency
        l = self.half_wave_dipole(f)
        self.unit_print("Total Dipole Length", l, self.args.unit)
        self.unit_print("Each Dipole Element Length", l/2, self.args.unit)
        if self.args.variable_return:
            return l





