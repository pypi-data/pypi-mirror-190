from pollination_dsl.dag import Inputs, task, Outputs, GroupedDAG
from dataclasses import dataclass
from typing import Dict, List
from pollination.honeybee_energy.simulate import SimulateModel
from pollination.honeybee_energy.result import EnergyUseIntensity


# input/output alias
from pollination.alias.inputs.model import hbjson_model_input
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.outputs.eui import parse_eui_results


@dataclass
class AppendixGPerformanceEntryPoint(GroupedDAG):
    """Appendix G Performance entry point."""

    # inputs
    model = Inputs.file(
        description='An energy Model as either a HBJSON or HBPkl file.',
        extensions=['hbjson', 'json', 'hbpkl', 'pkl'],
        alias=hbjson_model_input
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the annual energy simulation.',
        extensions=['epw']
    )

    ddy = Inputs.file(
        description='A DDY file with design days to be used for the initial '
        'sizing calculation.', extensions=['ddy'],
        alias=ddy_input
    )

    climate_zone = Inputs.str(
        description='Text indicating the ASHRAE climate zone. This can be a single '
        'integer (in which case it is interpreted as A) or it can include the '
        'A, B, or C qualifier (eg. 3C).',
        spec={
            'type': 'string',
            'enum': [
                '0', '1', '2', '3', '4', '5', '6', '7', '8',
                '0A', '1A', '2A', '3A', '4A', '5A', '6A',
                '0B', '1B', '2B', '3B', '4B', '5B', '6B',
                '3C', '4C', '5C'
            ]
        }
    )

    building_type = Inputs.str(
        description='Text for the building type that the Model represents. This is used '
        'to determine the baseline window-to-wall ratio and HVAC system. The '
        'following have specified systems per the standard: '
        'Residential, NonResidential, MidriseApartment, HighriseApartment, LargeOffice, '
        'MediumOffice, SmallOffice, Retail, StripMall, PrimarySchool, SecondarySchool, '
        'SmallHotel, LargeHotel, Hospital, Outpatient, Warehouse, SuperMarket, '
        'FullServiceRestaurant, QuickServiceRestaurant, Laboratory, Courthouse',
        spec={
            'type': 'string',
            'enum': [
                'Residential', 'NonResidential',
                'MidriseApartment', 'HighriseApartment',
                'LargeOffice', 'MediumOffice', 'SmallOffice',
                'Retail', 'StripMall',
                'PrimarySchool', 'SecondarySchool',
                'SmallHotel', 'LargeHotel',
                'Hospital', 'Outpatient',
                'Warehouse', 'SuperMarket',
                'FullServiceRestaurant', 'QuickServiceRestaurant',
                'Laboratory', 'Courthouse'
            ]
        }
    )

    energy_costs = Inputs.str(
        description='A string of energy cost parameters to customize the cost '
        'assumptions used to calculate the Performance Cost Index (PCI). Note that '
        'not all of the energy sources need to be specified for this input to be valid. '
        'For example, if the input model contains no district heating or cooling, '
        'something like the following would be acceptable: --electricity-cost 0.24 '
        '--natural-gas-cost 0.08',
        default='--electricity-cost 0.15 --natural-gas-cost 0.06 '
        '--district-cooling-cost 0.04 --district-heating-cost 0.08'
    )

    electricity_emissions = Inputs.float(
        description='A number for the electric grid carbon emissions'
        'in kg CO2 per MWh. For locations in the USA, this can be obtained '
        'from he honeybee_energy.result.emissions future_electricity_emissions '
        'method. For locations outside of the USA where specific data is unavailable, '
        'the following rules of thumb may be used as a guide. (Default: 400).\n'
        '800 kg/MWh - for an inefficient coal or oil-dominated grid\n'
        '400 kg/MWh - for the US (energy mixed) grid around 2020\n'
        '100-200 kg/MWh - for grids with majority renewable/nuclear composition\n'
        '0-100 kg/MWh - for grids with nuclear or renewables and storage', default=400
    )

    floor_area = Inputs.float(
        description='A number for the floor area of the building that the model '
        'is a part of in m2. Setting this value is useful when the input model '
        'represents a portion of the full building so it is necessary to explicitly '
        'specify the full floor area to ensure the correct baseline HVAC system is '
        'selected. If unspecified or 0, the model floor area will be used.', default=0
    )

    story_count = Inputs.int(
        description='An integer for the number of stories of the building that the '
        'model is a part of. Setting this value is useful when the input model '
        'represents a portion of the full building so it is necessary to explicitly '
        'specify the total story count to ensure the correct baseline HVAC system is '
        'selected. If unspecified or 0, the model stories will be used.', default=0,
        spec={'type': 'integer', 'minimum': 0}
    )

    lighting_method = Inputs.str(
        description='A switch to note whether the building-type should be used to '
        'assign the baseline lighting power density, which will use the same value '
        'for all Rooms in the model, or a space-by-space method should be used. '
        'To use the space-by-space method, the model should either be built '
        'with the programs that ship with Ladybug Tools in honeybee-energy-standards '
        'or the baseline_watts_per_area should be correctly '
        'assigned for all Rooms.', default='space',
        spec={'type': 'string', 'enum': ['space', 'building']}
    )

    # tasks
    @task(template=SimulateModel)
    def run_proposed_simulation(
        self, model=model, epw=epw, ddy=ddy
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.hbjson, 'to': 'proposed_model.hbjson'},
            {'from': SimulateModel()._outputs.result_folder, 'to': 'proposed_run'}
        ]

    @task(template=EnergyUseIntensity, needs=[run_proposed_simulation])
    def compute_eui(
        self, result_folder=run_proposed_simulation._outputs.result_folder
    ) -> List[Dict]:
        return [
            {'from': EnergyUseIntensity()._outputs.eui_json,
             'to': 'proposed_eui.json'}
        ]

    # outputs
    proposed_eui = Outputs.file(
        source='proposed_eui.json', description='A JSON containing energy use intensity '
        'information across the proposed model. Values are kWh/m2.',
        alias=parse_eui_results
    )

    proposed_sql = Outputs.file(
        source='proposed_run/eplusout.sql',
        description='The result SQL file output by the proposed simulation.'
    )
