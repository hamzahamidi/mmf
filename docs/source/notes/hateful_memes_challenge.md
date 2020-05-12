# Hateful Memes challenge

Hateful Memes challenge is available at [this link](https://www.drivendata.org/competitions/64/hateful-memes).

We provide the baseline pretrained models for this challenge and the configurations used for training the reported baselines. For details check [here](https://github.com/facebookresearch/mmf/tree/master/projects/hateful_memes).

Here we provide a step-by-step tutorial on how to setup your mmf codebase for development, running training and evaluation of your models on hateful memes dataset and generating submission file for the challenge.

## Installation
Install MMF following the [installation docs](https://mmf.readthedocs.io/en/latest/notes/installation.html).

## Preparing the dataset

To acquire the data, register at DrivenData's Hateful Memes Competition and download data from the challenge's [download page](https://www.drivendata.org/competitions/64/hateful-memes/data/). Follow the steps below to convert data into MMF format.

1. Download Images, Train, Dev and Test JSONL to a folder "x".
2. Run `mmf_convert_hm --download_folder=x`

This will automatically save the dataset into MMF's cache data directory and you are ready to launch training.


## Training and Evaluation

We will show how to run training with MMBT model on the train set and then evaluate it on the val set.

### Training
For running training on train set, run the following command:
```
mmf_run config=projects/hateful_memes/configs/mmbt/defaults.yaml model=mmbt dataset=hateful_memes training.run_type=train_val
```
This will train the mmbt model on the dataset and generate the checkpoints and best trained model (mmbt_final.pth) will be stored in the `./save` directory by default.

### Evaluation

Next run evaluation on the validation set:
```
mmf_run config=projects/hateful_memes/configs/mmbt/defaults.yaml model=mmbt dataset=hateful_memes training.run_type=val resume_file=./save/mmbt_final.pth
```
This will give you the performance of your model on the validation set. The metrics are AUROC, ACC, Binary F1 etc.


## Predictions for Challenge

After we trained the model and evaluated on the validation set, we will generate the predictions on the test set. For generating predictions in a csv file for submission, run the following command:

```
mmf_predict config=projects/hateful_memes/configs/mmbt/defaults.yaml model=mmbt dataset=hateful_memes training.run_type=test evaluation.prediction=true evaluation.prediction_file_format=csv
```

This command will output where the generated predictions csv file is stored.

## Submission for Challenge

Next you can upload the generated csv file on DrivenData in the submissions page for Hateful Memes:
```
> Go to the [submission page](https://www.drivendata.org/competitions/64/hateful-memes/submissions/)
> Upload the csv file
> Follow the instructions to check the results

```
[TODO] Fill in more details about submission page.
