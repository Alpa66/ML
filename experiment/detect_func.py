# import dill


def detect(time, metric_name):
    filepath = 'results.pkl'
    dill.load_session(filepath)
    res = results[metric_name]
    nres = pd.DataFrame(res.resid)
    ind = nres.index
    full_time_range = ind[-1] - ind[0]
    time_obj = datetime.datetime.strptime(time, '%y-%m-%d %H:%M:%S')
    while time_obj > ind[-1]:
        time_obj = time_obj - full_time_range
    while time_obj < ind[0]:
        time_obj = time_obj + full_time_range
    if nres.loc[time_obj] > th:
        return 'yes'
    else:
        return 'no'
