from Database import crud
from model import complaint
from Service import sourceService, loginUser


def submit_complaint(source_name, details):
    if not details.isspace() and details != "":
        source_id = sourceService.get_source_id_by_name(source_name)
        new_complaint = complaint.Complaint()
        new_complaint.source_id = source_id
        new_complaint.user_id = loginUser.login_user.id
        new_complaint.details = details
        crud.add(new_complaint)
        return "success"
    else:
        return "Please add details about the complaint before proceeding"
