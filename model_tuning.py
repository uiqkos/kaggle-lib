from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
import time

def search_params(
        model, X, y, random=False,
        param_grid=None, distributions=None,
        fit_args=(), fit_kwargs={}, search_args=(), search_kwargs={}
):
    if random:
        grid_search = RandomizedSearchCV(model, distributions, *search_args, **search_kwargs)
    else:
        grid_search = GridSearchCV(model, param_grid, *search_args, **search_kwargs)

    start_time = time.time()

    grid_search.fit(X, y, *fit_args, **fit_kwargs)

    print(f'Time: {time.time() - start_time} sec')
    print(f'Best estimator: {grid_search.best_estimator_}')
    print(f'Best params: {grid_search.best_params_}')

    return grid_search
