from langchain_core.tools import tool

@tool
def create_asana_task(task_name, due_on="today"):
    """
    Creates a task in Asana given the name of the task and when it is due

    Example call:

    create_asana_task("Test Task", "2024-06-24")
    Args:
        task_name (str): The name of the task in Asana
        due_on (str): The date the task is due in the format YYYY-MM-DD. If not given, the current day is used
    Returns:
        str: The API response of adding the task to Asana or an error message if the API call threw an error
    """
    

    print("good")

# @tool
# def create_info_card(name, model_name, type, content):
#     """
#     Creates a infoCard ui element in admin dashboard given the name model_name type content

#     Example call:

#     create_info_card("Manager", "manager", "String", "Text")
#     Args:
#         name (str): user freandly name to dispaly in infoCard ui element
#         model_name (str): The date the task is due in the format YYYY-MM-DD. If not given, the current day is used
#         type (str): mongodb model type entered in node js, valid types - String, Number
#         content (str): valid types -> url, text
#     Returns:
#         str: The API response of adding the task to Asana or an error message if the API call threw an error
#     """
    

#     print("infoCard")