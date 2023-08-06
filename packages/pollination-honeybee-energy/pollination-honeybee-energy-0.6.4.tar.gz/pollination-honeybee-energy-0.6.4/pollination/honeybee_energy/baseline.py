from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class ModelToBaseline(Function):
    """Convert a Model to be conformant with ASHRAE 90.1 appendix G.

    This includes running all functions to adjust the geometry, constructions,
    lighting, HVAC, SHW, and remove any clearly-defined energy conservation
    measures like daylight controls. Note that all schedules are essentially
    unchanged, meaning that additional post-processing of setpoints may be
    necessary to account for energy conservation strategies like expanded
    comfort ranges, ceiling fans, and personal thermal comfort devices. It may
    also be necessary to adjust electric equipment loads in cases where such
    equipment qualifies as an energy conservation strategy or hot water loads in
    cases where low-flow fixtures are implemented.

    Note that not all versions of ASHRAE 90.1 use this exact definition of a
    baseline model but version 2016 and onward conform to it. It is essentially
    an adjusted version of the 90.1-2004 methods.
    """

    model = Inputs.file(
        description='Honeybee model.', path='model.hbjson',
        extensions=['hbjson', 'json', 'hbpkl', 'pkl']
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
        'to determine the baseline window-to-wall ratio and HVAC system. If the type is '
        'not recognized or is "Unknown", it will be assumed that the building is generic'
        ' NonResidential. The following have specified systems per the standard: '
        'Residential, NonResidential, MidriseApartment, HighriseApartment, LargeOffice, '
        'MediumOffice, SmallOffice, Retail, StripMall, PrimarySchool, SecondarySchool, '
        'SmallHotel, LargeHotel, Hospital, Outpatient, Warehouse, SuperMarket, '
        'FullServiceRestaurant, QuickServiceRestaurant, Laboratory',
        default='Unknown'
    )

    floor_area = Inputs.float(
        description='A number for the floor area of the building that the model '
        'is a part of in m2. If 0, the model floor area will be used.', default=0
    )

    story_count = Inputs.int(
        description='An integer for the number of stories of the building that the '
        'model is a part of. If None, the model stories will be used.', default=0,
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

    @command
    def create_baseline(self):
        return 'honeybee-energy baseline create model.hbjson {{self.climate_zone}} ' \
            '--building-type "{{self.building_type}}" ' \
            '--story-count {{self.story_count}} --floor-area {{self.floor_area}} ' \
            '--lighting-by-{{self.lighting_method}} ' \
            '--output-file baseline_model.hbjson'

    baseline_model = Outputs.file(
        description='Model JSON with its properties edited to conform to ASHRAE '
        '90.1 appendix G.', path='baseline_model.hbjson'
    )
