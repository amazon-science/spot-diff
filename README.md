# SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation

Yang Zou, Jongheon Jeong, Latha Pemula, Dongqing Zhang, Onkar Dabeer.

## Table of Contents
* [Data description](#data-description)
* [Data statistics](#data-statistics)
* [Data Download](#data-download)
* [Utility code](#utility-code)
* [Citation](#citation)
* [License](#license)

## Data Description
![](figures/VisA_samples.png)
The VisA dataset contains 12 subsets corresponding to 12 different objects as shown in the above figure. There are 10,821 images with 9,621 normal and 1,200 anomalous samples. Four subsets are different types of printed circuit boards (PCB) with relatively complex structures containing transistors, capacitors, chips, etc. For the case of multiple instances in a view, we collect four subsets: Capsules, Candles, Macaroni1 and Macaroni2. Instances in Capsules and Macaroni2 largely differ in locations and poses. Moreover, we collect four subsets including Cashew, Chewing gum, Fryum and Pipe fryum, where objects are roughly aligned. The anomalous images contain various flaws, including surface defects such as scratches, dents, color spots or crack, and structural defects like misplacement or missing parts. 

## Data Statistics
|   | Object | # normal samples | # anomaly samples  | # anomaly classes |
|---|--------------|----------------|----------|-----------|
| Complex structure | PCB1 | 1,004 | 100 | 4 |
| Complex structure | PCB2 | 1,001 | 100 | 4 |
| Complex structure | PCB3 | 1,006 | 100 | 4 |
| Complex structure| PCB4 | 1,005 | 100 | 7 |
| Multiple instances | Capsules | 602 | 100 | 5 |
| Multiple instances | Candles | 1,000 | 100 | 8 |
| Multiple instances | Macaronis1 | 1,000 | 100 | 7 |
| Multiple instances | Macaronis2 | 1,000 | 100 | 7 |
| Single instance | Cashew | 500 | 100 | 9 |
| Single instance | Chewing gum | 503 | 100 | 6 |
| Single instance | Fryum | 500 | 100 | 8 |
| Single instance | Pipe fryum | 500 | 100 | 6 |

## Data Download

We host the VisA dataset in AWS S3 and you can download it by this URL(https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA.tar). 

## Utility Code
- For each object, all the anomalous and normal samples are stored in Anomaly and Normal subfolders in the downloaded dataset. We use the prepare_data.py(https://github.com/amazon-research/spot-diff/blob/main/prepare_data.py) to group these samples to train and test folders for 1-class, 2-class-highshot, 2-class-fewshot setups. We give a sample command line for reorganizing the downloaded data to 1-class setup as follows.
~~~~
prepare_data.py --split-type 1cls --data-folder ./VisA --save-folder ./VisA_pytorch --split-file ./VisA/split_csv/1cls.csv
~~~~

- To compute classification and segmentation metrics, please refer to metrics.py(https://github.com/amazon-research/spot-diff/blob/main/metrics.py)

## Citation
Please cite the following paper if this dataset helps your project:

```bibtex
@article{zou2022spot,
  title={SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation},
  author={Zou, Yang and Jeong, Jongheon and Pemula, Latha and Zhang, Dongqing and Dabeer, Onkar},
  journal={arXiv preprint arXiv:2207.14315},
  year={2022}
}
```

## License
The data is released under the CC BY 4.0 license.