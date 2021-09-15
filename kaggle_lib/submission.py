import datetime
import io
import json
import re

from kaggle import KaggleApi
import time
import pandas as pd
import os
import webbrowser
import pickle


class Readme:
    def __init__(
        self,
        name,
        description=None,
        score=None,
        status=None,
        model_summary=None
    ):
        self.description = description
        self.model_summary = model_summary
        self.name = name
        self.score = score
        self.status = status
        self.date = datetime.datetime.now()

    def markdown(self):
        return self.__str__()

    def __str__(self):
        return re.sub(r'[\t ]+', ' ', f'''
            ### {self.name}
            #### Description
            > {self.description}\n\n''') \
               + ('' if self.model_summary is None else f'```\n{self.model_summary}```\n\n') \
               + ('' if self.score is None else f'Score: {self.score}\n\n') \
               + ('' if self.status is None else f'Status: {self.status}\n\n') \
               + f'Date: { self.date if isinstance(self.date, str) else self.date.strftime("%Y-%m-%d %H:%M:%S") }\n\n'


class Submission:
    def __init__(self, compete, name, work_dir, description=None, create_readme=False):
        self.id = str(time.time())
        self.compete = compete
        self.name = f'{name} - {self.id}'
        self.description = description

        if work_dir[-1] == '/':
            self.new_folder_path = work_dir + self.name
        else:
            self.new_folder_path = work_dir + '/' + self.name

        self.kaggle_api = KaggleApi()
        self.kaggle_api.authenticate()

        if not os.path.exists(self.new_folder_path):
            os.mkdir(self.new_folder_path)

        self.readme = Readme(self.name, self.description) if create_readme else None

    def save_model(self, model, file_name=None):
        if file_name is None:
            file_name = str(model).replace('\\', '')

        with open(f'{self.new_folder_path}/{file_name}.pickle', 'wb') as pickle_file:
            pickle.dump(model, pickle_file)

    def save_keras_model(
        self,
        model,
        file_name=None,
        save_format='pickle',
        save_summary_to_readme=True,
        *args,
        **kwargs
    ):
        from tensorflow.keras import Model

        if not isinstance(model, Model):
            raise Exception(f'Model should be instance of keras.Model')

        if file_name is None:
            file_name = str(model).replace('\\', '')

        if save_summary_to_readme:
            summary = io.StringIO()
            model.summary(print_fn=lambda s: print(s, file=summary))

            if self.readme is None:
                raise Exception("'create_readme' should be True")

            self.readme.model_summary = summary.getvalue()

        if save_format == 'pickle':
            with open(f'{self.new_folder_path}/{file_name}.pickle', 'wb') as pickle_file:
                pickle.dump(model, pickle_file)

        elif save_format == 'config':
            with open(f'{self.new_folder_path}/{file_name}.json', 'w') as config_file:
                json.dump(model.get_config(), config_file)

        elif save_format == 'h5':
            model.save(f'{self.new_folder_path}/{file_name}', *args, **kwargs)

        else:
            raise Exception('Undefined save_format')

        return self

    def save_predictions(self, predictions, columns, index, file_name='predictions.csv'):
        pd.DataFrame(dict(zip(columns, [index, predictions]))) \
            .to_csv(f'{self.new_folder_path}/{file_name}', index=False)

        return self

    def open_in_browser(self):
        webbrowser.open(f'https://www.kaggle.com/c/{self.compete}/submissions', new=2)

        return self

    def submit(self, predictions_file_name='predictions.csv'):
        print('Uploading submission...')
        command = f'kaggle competitions submit -c {self.compete} -f "{self.new_folder_path}/{predictions_file_name}" -m "{self.description}"'
        print(command)
        output = os.system(command)
        print('Output: ', output)

        return self

    def check_results(self, timeout=5):
        time.sleep(timeout)
        last_submission = self.kaggle_api.competitions_submissions_list(self.compete)[0]

        if self.readme is not None:
            self.readme.score = last_submission['publicScore']
            self.readme.date = last_submission['date']
            self.readme.status = last_submission['status']

        print('Description: ', last_submission['description'])
        print('Date: ', last_submission['date'])
        print('Status: ', last_submission['status'])
        print('Score: ', last_submission['publicScore'])

        return self

    def save_readme(self):
        readme_file = open(f'{self.new_folder_path}/README.md', 'w')
        readme_file.write(self.readme.markdown())

        return self
