from model import source, quality
from Service import userService, qualityService, inputValidator
from Database import crud


def add_source(s_name, s_location, s_type, s_capacity, s_status, s_water_level, s_moderator_1, s_moderator_2,
               s_moderator_3,
               s_chlorine, s_ph_level, s_temperature, s_turbidity, s_do, s_conductivity, s_tds, s_bod, s_cod, s_tss):
    # Check if compulsory fields are not empty/blank (s_name, s_location, s_type, s_capacity, s_status,
    # s_water_level, s_moderator_1)
    if any(not field.strip() for field in
           (s_name, s_location, s_type, s_capacity, s_status, s_water_level, s_moderator_1)):
        return "Please fill in all required fields"

    # Check if fields contain valid input type (double or integer)
    if not inputValidator.is_valid_numeric_input(s_chlorine, s_ph_level, s_temperature, s_turbidity, s_do, s_conductivity, s_tds,
                                  s_bod, s_cod, s_tss):
        return "Invalid input for numeric fields"

    # Get user from the database by their name using userService.get_user_by_name(s_moderator_1)
    moderator_1_user = userService.get_user_by_name(s_moderator_1)
    if moderator_1_user is None:
        return "Moderator 1 user does not exist"

    # Create a new source object and add all the data in the required fields
    new_source = source.Source()
    new_source.name = s_name
    new_source.location = s_location
    new_source.type = s_type
    new_source.capacity = s_capacity
    new_source.status = s_status
    new_source.water_level = s_water_level

    # Create a comma-separated string of approver IDs
    approver_ids = str(moderator_1_user.id)
    if s_moderator_2:
        moderator_2_user = userService.get_user_by_name(s_moderator_2)
        if moderator_2_user:
            approver_ids += f",{moderator_2_user.id}"
    if s_moderator_3:
        moderator_3_user = userService.get_user_by_name(s_moderator_3)
        if moderator_3_user:
            approver_ids += f",{moderator_3_user.id}"

    new_source.approvers = approver_ids

    # Create a quality object and populate it with the provided data
    new_quality = quality.Quality()
    new_quality.ph_level = s_ph_level
    new_quality.temperature = s_temperature
    new_quality.turbidity = s_turbidity
    new_quality.dissolved_0xygen = s_do
    new_quality.conductivity = s_conductivity
    new_quality.total_dissolved_solids = s_tds
    new_quality.biochemical_oxygen_demand = s_bod
    new_quality.chemical_oxygen_demand = s_cod
    new_quality.total_suspended_solids = s_tss
    new_quality.chlorine_residual = s_chlorine

    # Associate the new quality object with the source
    new_source.quality_readings = [new_quality]

    # Persist the new source and quality objects to the database
    try:
        crud.add(new_source)
        qualityService.add_quality(new_quality)
        return new_source
    except Exception as e:
        return str(e)
