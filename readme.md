## folder structure

```
├── export_tflite_graph_tf2.py
├── generate_tfrecord.py
├── model_main_tf2.py
├── split_images.py
├── xml_to_csv.py
│
├── data
│   ├── labelmap.pbtxt
│   ├── test.record
│   ├── test_labels.csv
│   ├── train.record
│   └── train_labels.csv
│
├── images
│      ├── test
│      │     │__ ...jpg
│      │
│      ├── train
│            │__ ...jpg
│
│
├── models
│
│
├── pre-trained-models
```

# Protocols

1. keep the image and xml file name the name inside train and test. (e.g. `hello.jpg, hello.xml ...`).
2. If training models in local system, switch pyenv to 3.8 and use `tensorflow` conda environment (personal note).

# Process

1. label image with labelImg. If relabeling needed, use `re_annotate_xml.py`

2. split images into `test`, `train` and `validation`, via `train_val_test_split.py` tool.

3. generate csv file `xml_to_csv.py`

4. create `labelmap.txt` inside `data` folder.
format:

```
label_a
label_b
...
```

5. convert it to `tfrecord` via `generate_tfrecord.py` tool

```
python generate_tfrecord.py --csv_input=data/train_labels.csv --labelmap=data/labelmap.txt --image_dir=images/train --output_path=data/train.tfrecord

python generate_tfrecord.py --csv_input=data/validation_labels.csv --labelmap=data/labelmap.txt --image_dir=images/validation --output_path=data/val.tfrecord
```

6. Modify `pre-trained-models/.../pipline.config` file via `python python_scripts/modify_pipline_config.py` script.

### To modify:

```
num_classes, batch_size, data_augmentation_options, num_steps,
fine_tune_checkpoint, fine_tune_checkpoint_type ...
```


# Training

1. Start training model with this command:
```
python model_main_tf2.py \
    --pipeline_config_path=models/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/pipeline.config \
    --model_dir=models/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8 \
    --alsologtostderr \
    --num_train_steps=30000 \
    --sample_1_of_n_eval_examples=1
```

2. See the model training performance and statistics here:

```
tensorboard --logdir 'models/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/train'
```
