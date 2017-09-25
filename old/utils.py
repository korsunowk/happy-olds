from old.models import Old


def full_name_check(old_name):
    """
    The help function for check the unique full_name of a Old model
    :param old_name: the dict with first/last name of the Old object
    :return: True if free, False if already exists
    """
    return not Old.objects.filter(**old_name).exists()
