# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_partial_tagger', 'spacy_partial_tagger.layers']

package_data = \
{'': ['*']}

install_requires = \
['partial-tagger>=0.6.0,<0.7.0',
 'spacy-alignments>=0.8.5,<0.9.0',
 'spacy[transformers]>=3.3.1,<4.0.0',
 'thinc>=8.0.15,<9.0.0',
 'torch>=1.11.0,<2.0.0',
 'transformers[ja]>=4.25.1,<5.0.0']

entry_points = \
{'spacy_architectures': ['spacy-partial-tagger.LinearCRFEncoder.v1 = '
                         'spacy_partial_tagger.layers.encoder:build_linear_crf_encoder_v1',
                         'spacy-partial-tagger.MisalignedTok2VecTransformer.v1 '
                         '= '
                         'spacy_partial_tagger.layers.tok2vec_transformer:build_misaligned_tok2vec_transformer',
                         'spacy-partial-tagger.PartialTagger.v1 = '
                         'spacy_partial_tagger.tagger:build_partial_tagger_v1',
                         'spacy-partial-tagger.ViterbiDecoder.v1 = '
                         'spacy_partial_tagger.layers.decoder:build_viterbi_decoder_v1'],
 'spacy_factories': ['partial_ner = '
                     'spacy_partial_tagger.pipeline:make_partial_ner'],
 'spacy_label_indexers': ['spacy-partial-tagger.TransformerLabelIndexer.v1 = '
                          'spacy_partial_tagger.label_indexers:configure_transformer_label_indexer'],
 'thinc_losses': ['spacy-partial-tagger.ExpectedEntityRatioLoss.v1 = '
                  'spacy_partial_tagger.loss:configure_ExpectedEntityRatioLoss']}

setup_kwargs = {
    'name': 'spacy-partial-tagger',
    'version': '0.12.0',
    'description': 'Sequence Tagger for Partially Annotated Dataset in spaCy',
    'long_description': '# spacy-partial-tagger\n\nThis is a library to build a CRF tagger for a partially annotated dataset in spaCy. You can build your own NER tagger only from dictionary. The algorithm of this tagger is based on Effland and Collins. (2021).\n\n## Overview\n\n![The overview of spacy-partial-tagger](https://raw.githubusercontent.com/doccano/spacy-partial-tagger/main/images/overview.png)\n\n## Dataset Preparation\n\nPrepare spaCy binary format file to train your tagger.\nIf you are not familiar with spaCy binary format, see [this page](https://spacy.io/api/data-formats#training).\n\nYou can prepare your own dataset with [spaCy\'s entity ruler](https://spacy.io/usage/rule-based-matching#entityruler) as follows:\n\n```py\nimport spacy\nfrom spacy.tokens import DocBin\n\n\nnlp = spacy.blank("en")\n\npatterns = [{"label": "LOC", "pattern": "Tokyo"}, {"label": "LOC", "pattern": "Japan"}]\nruler = nlp.add_pipe("entity_ruler")\nruler.add_patterns(patterns)\n\ndoc = nlp("Tokyo is the capital of Japan.")\n\ndoc_bin = DocBin()\ndoc_bin.add(doc)\n\n# Replace /path/to/data.spacy with your own path\ndoc_bin.to_disk("/path/to/data.spacy")\n```\n\n## Training\n\nTrain your tagger as follows:\n\n```sh\npython -m spacy train config.cfg --output outputs --paths.train /path/to/train.spacy --paths.dev /path/to/dev.spacy --gpu-id 0\n```\n\nThis library is implemented as [a trainable component](https://spacy.io/usage/layers-architectures#components) in spaCy,\nso you could control the training setting via spaCy\'s configuration system.\nWe provide you the default configuration file [here](https://github.com/tech-sketch/spacy-partial-tagger/blob/main/config.cfg).\nOr you could setup your own. If you are not familiar with spaCy\'s config file format, please check the [documentation](https://spacy.io/usage/training#config).\n\nDon\'t forget to replace `/path/to/train.spacy` and `/path/to/dev.spacy` with your own.\n\n## Evaluation\n\nEvaluate your tagger as follows:\n\n```sh\npython -m spacy evaluate outputs/model-best /path/to/test.spacy --gpu-id 0\n```\n\nDon\'t forget to replace `/path/to/test.spacy` with your own.\n\n## Installation\n\n```sh\npip install spacy-partial-tagger\n```\n\nIf you use M1 Mac, you might have problems installing `fugashi`. In that case, please try `brew install mecab` before the installation.\n\n## References\n\n- Thomas Effland and Michael Collins. 2021. [Partially Supervised Named Entity Recognition via the Expected Entity Ratio Loss](https://aclanthology.org/2021.tacl-1.78/). _Transactions of the Association for Computational Linguistics_, 9:1320–1335.\n',
    'author': 'yasufumi',
    'author_email': 'yasufumi.taniguchi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tech-sketch/spacy-partial-tagger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
