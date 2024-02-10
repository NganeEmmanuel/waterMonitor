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
    if not inputValidator.is_string_valid_numeric_input(s_capacity, s_water_level, s_chlorine, s_ph_level, s_temperature, s_turbidity, s_do, s_conductivity, s_tds,
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
    new_source.capacity = float(s_capacity)
    new_source.status = s_status
    new_source.water_level = float(s_water_level)

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
    new_quality.ph_level = float(s_ph_level) if inputValidator.is_string_valid_numeric_input(s_ph_level) else None
    new_quality.temperature = float(s_temperature) if inputValidator.is_string_valid_numeric_input(s_temperature) else None
    new_quality.turbidity = float(s_turbidity) if inputValidator.is_string_valid_numeric_input(s_turbidity) else None
    new_quality.dissolved_0xygen = float(s_do) if inputValidator.is_string_valid_numeric_input(s_do) else None
    new_quality.conductivity = float(s_conductivity) if inputValidator.is_string_valid_numeric_input(s_conductivity) else None
    new_quality.total_dissolved_solids = float(s_tds) if inputValidator.is_string_valid_numeric_input(s_tds) else None
    new_quality.biochemical_oxygen_demand = float(s_bod) if inputValidator.is_string_valid_numeric_input(s_bod) else None
    new_quality.chemical_oxygen_demand = float(s_cod) if inputValidator.is_string_valid_numeric_input(s_cod) else None
    new_quality.total_suspended_solids = float(s_tss) if inputValidator.is_string_valid_numeric_input(s_tss) else None
    new_quality.chlorine_residual = float(s_chlorine) if inputValidator.is_string_valid_numeric_input(s_chlorine) else None

    # Associate the new quality object with the source
    new_source.quality_readings = new_quality

    # Persist the new source and quality objects to the database
    try:
        crud.add(new_source)
        qualityService.add_quality(new_quality)
        return new_source
    except Exception as e:
        return str(e)
