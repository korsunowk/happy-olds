from boarding_visit.models import BoardingVisit


def get_list_of_visits(old, excluded):
    """
    The help function for get list of all visits dates ranges of the Old object
    :param old: the Old model object
    :param excluded: the current visit object
    :return: the list of dates
    """
    visits = BoardingVisit.objects.filter(old=old).exclude(pk=excluded.pk)

    return [{'start': vis.start_date, 'end': vis.end_date} for vis in visits]
