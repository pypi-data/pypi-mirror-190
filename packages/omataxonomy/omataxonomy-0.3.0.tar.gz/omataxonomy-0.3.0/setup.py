# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omataxonomy']

package_data = \
{'': ['*']}

install_requires = \
['ete3>=3.1.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'six>=1.16.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'omataxonomy',
    'version': '0.3.0',
    'description': 'Package to work with combined NCBI and GTDB taxonomy',
    'long_description': '# OMA Taxonomy \n\nomataxonomy is a library based on \n[ete\'s ncbi_taxonomy module](https://etetoolkit.org/docs/latest/tutorial/tutorial_ncbitaxonomy.html) \nthat is used internally for the [OMA project](https://omabrowser.org), but that can also \nbe used in different contexts.\nEssentially, it combines the NCBI Taxonomy and the GTDB taxonomy (including all their genome as subspecies). \nFor GTDB we generate stable taxon ids by hashing the scientific names. \n\nomataxonomy stores the data in a sqlite database under `${HOME}/.config/omataxonomy/` \nand therefor uses little resources when being used as not all the data will be loaded into memory.\n\n## Install\n\nOMA Taxonomy can be installed directly from pip:\n\n    pip install omataxonomy\n\n## Usage\n\n    from omataxonomy import Taxonomy\n    tax = Taxonomy()\n    print(tax.get_name_lineage([\'RS_GCF_006228565.1\', \'GB_GCA_001515945.1\', "f__Leptotrichiaceae", "Homo sapiens", "Gallus"]))\n\n{\'f__Leptotrichiaceae\': [\'root\', \'d__Bacteria\', \'p__Fusobacteriota\', \'o__Fusobacteriales\', \'f__Leptotrichiaceae\'], \'Gallus\': [\'root\', \'cellular organisms\', \'Eukaryota\', \'Opisthokonta\', \'Metazoa\', \'Eumetazoa\', \'Bilateria\', \'Deuterostomia\', \'Chordata\', \'Craniata\', \'Vertebrata\', \'Gnathostomata\', \'Teleostomi\', \'Euteleostomi\', \'Sarcopterygii\', \'Dipnotetrapodomorpha\', \'Tetrapoda\', \'Amniota\', \'Sauropsida\', \'Sauria\', \'Archelosauria\', \'Archosauria\', \'Dinosauria\', \'Saurischia\', \'Theropoda\', \'Coelurosauria\', \'Aves\', \'Neognathae\', \'Galloanserae\', \'Galliformes\', \'Phasianidae\', \'Phasianinae\', \'Gallus\'], \'GB_GCA_001515945.1\': [\'root\', \'d__Bacteria\', \'p__Firmicutes_B\', \'c__Moorellia\', \'o__Desulfitibacterales\', \'s__Desulfitibacter sp001515945\', \'GB_GCA_001515945.1\'], \'Homo sapiens\': [\'root\', \'cellular organisms\', \'Eukaryota\', \'Opisthokonta\', \'Metazoa\', \'Eumetazoa\', \'Bilateria\', \'Deuterostomia\', \'Chordata\', \'Craniata\', \'Vertebrata\', \'Gnathostomata\', \'Teleostomi\', \'Euteleostomi\', \'Sarcopterygii\', \'Dipnotetrapodomorpha\', \'Tetrapoda\', \'Amniota\', \'Mammalia\', \'Theria\', \'Eutheria\', \'Boreoeutheria\', \'Euarchontoglires\', \'Primates\', \'Haplorrhini\', \'Simiiformes\', \'Catarrhini\', \'Hominoidea\', \'Hominidae\', \'Homininae\', \'Homo\', \'Homo sapiens\'], \'RS_GCF_006228565.1\': [\'root\', \'d__Bacteria\', \'p__Firmicutes_B\', \'c__Moorellia\', \'o__Moorellales\', \'f__Moorellaceae\', \'g__Moorella\', \'s__Moorella thermoacetica\', \'RS_GCF_006228565.1\']}\n',
    'author': 'Adrian Altenhoff',
    'author_email': 'adrian.altenhoff@inf.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
