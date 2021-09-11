# kaggle-lib
Kaggle lib for sending predictions to kaggle.com
## Installation
```python setup.py install```
## Example
```python
from kaggle_lib.submission import Submission

s = Submission(
        name='simple_model',
        compete='digit-recognizer',
        work_dir='./submissions',
        create_readme=True,
        description='Simple keras model 8 layers'
    )\
    .save_keras_model(
        model=model,
        save_format='h5',
        file_name='simple',
        save_summary_to_readme=True,
    )\
    .save_predictions(
        predictions=np.argmax(model.predict(test.to_numpy().reshape(-1, 28, 28, 1)), axis=-1),
        columns=['ImageId', 'Label'],
        index=test.index + 1
    )\
    .submit()
```
```
Uploading submission...
kaggle competitions submit -c digit-recognizer -f "./submissions/simple_model - 1631375951.941002/predictions.csv" -m "Simple keras model 8 layers"
100%|██████████| 208k/208k [00:02<00:00, 73.8kB/s]
Successfully submitted to Digit Recognizer
Output:  0
```
```python
s.check_results()
```
```
Description:  Simple keras model 8 layers
Date:  2021-09-11T15:59:38.483Z
Status:  complete
Score:  0.98646
```
```python
s.save_readme()
```
## Example README.md
 ### simple_model - 1631375951.941002
 #### Description
 > Simple keras model 8 layers

```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 14, 14, 24)        624       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 7, 7, 24)          0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 4, 4, 16)          9616      
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 2, 2, 16)          0         
_________________________________________________________________
flatten (Flatten)            (None, 64)                0         
_________________________________________________________________
dense (Dense)                (None, 100)               6500      
_________________________________________________________________
dense_1 (Dense)              (None, 64)                6464      
_________________________________________________________________
dense_2 (Dense)              (None, 10)                650       
=================================================================
Total params: 23,854
Trainable params: 23,854
Non-trainable params: 0
_________________________________________________________________
```

Score: 0.98646

Status: complete

Date: 2021-09-11T15:59:38.483Z

