# Data Mining Investigations

Thursday, 17 October 2019

## Prerequisites

 * [Orange DataMining](https://orange.biolab.si/)
 * Python3 with scikit-learn, numpy
 * [Jupyter](https://jupyter.org/)


## Background

### Cybersecurity

Advanced Persistent Threats (or expert cyberattacks) have a [commonly observed](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html) practice: they control the malicious tools from the internet. 

This communication is commonly named [command & control](https://attack.mitre.org/tactics/TA0011/).

Most of the IT systems now have external communication filtering using [web proxies](https://en.wikipedia.org/wiki/Proxy_server) to gather web browsing activity events and to block suspicious or malicious communications.

However the filtering is mostly based on know criterias (values) like internet domain name, internet target ip address, or some know part of the web adress as malicious code.

But expert cyberattacks of course move from the publicly known internet addresses to an unknown one.

Moreover, right now most of the people use internet to perform their jobs (gather information, use cloud services, chat with other people...) so internet browsing events are large volume of data and still growing everyday.

### Machine Learning

[Machine Learning](https://en.wikipedia.org/wiki/Machine_learning) are softwares that process statistical models on a set of data to provide an enriched output. 

It is used in several elements like spam filtering, blog moderation, failure prediction, customer profiling, summaries, aggregation ...

#### Supervised Machine Learning

[Supervised Machine Learning](https://en.wikipedia.org/wiki/Supervised_learning) family of algorithms require to use a training system with a set of tagged data as input to generate a usable model.

Building the training dataset is a complex topic which require to clean, tag, balance data to generate the best machine learning model possible.

Most of the time models generated will provide the tags provided in the training dataset with a level of confidance.

#### Unsupervised Machine Learning 

[Unsupervised Machine Learning](https://en.wikipedia.org/wiki/Unsupervised_learning) family of algorithms don't need to be trained to process the data. 
However the mathematical matrix must represent the meaning of the original data in order that unsupervised machine learning be able to categorise them.

Most of the time the algorithms will provide unnamed and unordered groups of elements (bag of data) as an output. This groups could be 2 or more groups. 

A special case can be found in the case of only 2 groups as output. It is basically one group and data that can not be included in the group. The excluded data are could [outliers](https://medium.com/@mehulved1503/outlier-detection-and-anomaly-detection-with-machine-learning-caa96b34b7f6).


## Warmup Orange DataMining

### Supervised Machine Learning Tutorials 

    [Orange Data Mining Tests Datasets can be found here](https://github.com/biolab/orange3/tree/master/Orange/datasets)

 * Supervised Machine Learning [Random Forest](https://docs.biolab.si//3/visual-programming/widgets/model/randomforest.html)
 * Unsupervised Machine Learning [PCA](https://docs.biolab.si//3/visual-programming/widgets/unsupervised/PCA.html)

### Web proxies logs 

Web proxies logs are tab or comma separeted values.

Raw log example:
```
1462861579^192.168.0.174^http://espaceloisirs.ign.fr/boutique/media/catalog/product/cache/1/small_image/150x/2f57e55fd62616534c2345bc83519ccc/g/v/gvtopo-toulouse_a_velo-max.jpg^Reference^user_786^Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko^http://espaceloisirs.ign.fr/boutique/guides/velo.html?p=2^GET^OBSERVED^200^866
1462864305^192.168.0.182^http://static4.pagesjaunes.fr/media/ugc/sergio_bossi_blagnac_salon_de_coiffure_sergio_bossi_161110870?w=540&h=295&crop=true^Reference^user_743^Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36^http://www.pagesjaunes.fr/pros/55514269^GET^OBSERVED^200^631
1462865976^192.168.0.53^http://france3-regions.francetvinfo.fr/midi-pyrenees/sites/regions_france3/files/styles/asset_list_medium/public/assets/images/2016/05/09/sdk_rugby_toulouse_agen_16h15_-00_00_31_10.jpg?itok=OFBI_YOu^News/Media^user_170^Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko^http://france3-regions.francetvinfo.fr/midi-pyrenees/haute-garonne/toulouse^GET^DENIED^407^1025
```

To be easily processed by Orange DataMining we transformed them into `.tab` files.

Tab File example:
```
TIMESTAMP	BYTES	TYPE	IP_SRC	URL	CATEGORIES	USER	USER_AGENT	REFERRER	METHOD	ACTION	RESULT_CODE	DOMAIN
continuous	continuous	discrete	string	string	string	string	string	string	string	string	string	string
		class	meta	meta	meta	meta	meta	meta	meta	meta	meta	meta
1462861579.0	866.0		192.168.0.174	http://espaceloisirs.ign.fr/boutique/media/catalog/product/cache/1/small_image/150x/2f57e55fd62616534c2345bc83519ccc/g/v/gvtopo-toulouse_a_velo-max.jpg	Reference	user_786	Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko	http://espaceloisirs.ign.fr/boutique/guides/velo.html?p=2	GET	OBSERVED	200	
1462864305.0	631.0		192.168.0.182	http://static4.pagesjaunes.fr/media/ugc/sergio_bossi_blagnac_salon_de_coiffure_sergio_bossi_161110870?w=540&h=295&crop=true	Reference	user_743	Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36	http://www.pagesjaunes.fr/pros/55514269	GET	OBSERVED	200	
1462865976.0	1025.0		192.168.0.53	http://france3-regions.francetvinfo.fr/midi-pyrenees/sites/regions_france3/files/styles/asset_list_medium/public/assets/images/2016/05/09/sdk_rugby_toulouse_agen_16h15_-00_00_31_10.jpg?itok=OFBI_YOu	News/Media	user_170	Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko	http://france3-regions.francetvinfo.fr/midi-pyrenees/haute-garonne/toulouse	GET	DENIED	407	
```

As this dataset comme from a pentest we know what are the communication linked to the cyberattack.

In the [tab files](data) those communications are tagged as `ATTACK`.

## Objective

Explore use of machine learning (supervised and unsupervised) to try to detect the `ATTACK` communications.


## Examples

 * Using Orange Data Mining GUI Workflow [project file here](src/detection_project.ows)
 * Using Orange Data Mining Objects through Python in Jupyter Notebook [project file here](detection_project.ipynb)

## Todo list

 [ ] Comment the source code
 [ ] Provide step by step tutorial for better understanding