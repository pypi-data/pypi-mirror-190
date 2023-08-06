#!/usr/bin/env python
from distutils.core import setup
setup(name='indic_unified_parser',
    version='1.0.3',
    description='The Unified Parser unifies Indian languages using a common label set and syllable structure. It converts text to a common label set, generates phoneme sequences and improves natural language understanding in Indian languages. The method requires basic language knowledge and can achieve more than 95% accuracy with good lexicons. New Indian language parsers can be easily developed using this unified approach.',
    author='Vikram K V',
    author_email='vikram.kv2001@gmail.com',
    url='https://github.com/vikram-kv/Unified_Parser',
    packages=['indic_unified_parser'],
    package_dir={'indic_unified_parser': 'src/indic_unified_parser'},
    package_data={'indic_unified_parser': ['*.mat']},
    include_package_data=True
)