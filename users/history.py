from .models import History


def form_history(user, result, time_counted, formula):
    hist = History.objects.create(
        user=user,
        result=result,
        time_counted=time_counted,
        formula=formula
    )
    hist.save()


