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

1. label image with labelImg. If the images are already classified and cropped, run the `to_xml_for_already_cropped_img.py` tool.
2. split images into `test` and `train`, via `split_images.py` tool.
3. generate csv file `xml_to_csv.py`
4. in `generate_tfrecord.py`, modify `def class_text_to_int(row_label)` accordingly
5.  convert it to `tfrecord` via `generate_tfrecord.py` tool
6. Modify `pipline.config` file
7. Create file named `labelmap.txt` and `labelmap.pbtxt` inside `data/`
