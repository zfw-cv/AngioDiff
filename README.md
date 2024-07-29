## Paper

This repository provides the official PyTorch implementation of our model in the following papers:

**[******](***)** <br/> 
[Zhifeng Wang](***), [Renjiao Yi](https://renjiaoyi.github.io/), [Xin Wen](***), [Chenyang Zhu](http://www.zhuchenyang.net/), [Kai Xu](https://kevinkaixu.net/), [Kunlun He](https://scholar.google.com/citations?user=31wT3skAAAAJ&hl=en) <br/>


![Image of The Proposed method](figs/network.png)

## Abstract

*******

## Environment

We could ensure that the code is available in such environment.

  * OS : Ubuntu 18.04
  * Python >= 3.8
  * PyTorch >= 1.13.0


## Dataset

In this paper, we used the **[XCAD dataset](https://www.dropbox.com/scl/fi/mvstwdgxo0hfk678x94d4/XCAD.zip?rlkey=qdztml0gzfzoc0t5d16k71u76&e=1&dl=0)**  and the **[ARCADE dataset](https://zenodo.org/records/10390295)** for training. In the Blood vessel simulation part, we used the **[RPCA-UNet dataset](https://github.com/Binjie-Qin/RPCA-UNet)**.

## Train

```
python main.py -p train -c config/train.json
```

## Test

```
python main.py -p test -c config/test.json
```


<!-- ## Citation
If you use this code or use our pre-trained weights for your research, please cite our papers:

```
``` -->


```
