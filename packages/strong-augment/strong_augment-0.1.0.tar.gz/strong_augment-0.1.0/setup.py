# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strong_augment']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'opencv-python-headless>=4.7,<5.0', 'pillow>=9,<10', 'tqdm']

setup_kwargs = {
    'name': 'strong-augment',
    'version': '0.1.0',
    'description': "Augment like there's no tomorrow: Consistently performing neural networks",
    'long_description': '# Augment like there\'s no tomorrow: Consistently performing neural networks for medical imaging [[`arXiv`]](https://arxiv.org/abs/2206.15274)\n\nThis repository contains implementations for `StrongAugment` and creating\n**_distribution-shifted_** datasets.\n\n## Installation\n\n```bash\npip3 install strong-augment\n```\n\n## Training with strong augmentation.\n\nTo train your neural networks with strong augmentatiom simply include `StrongAugment` to your image transformation pipeline!\n\n```python\nimport torchvision.transforms as T\nfrom strong_augment import StrongAugment\n\ntrnsf = T.Compose(\n    T.RandomResizedCrop(224),\n    T.RandomVerticalFlip(0.5),\n    T.RandomHorizontalFlip(0.5),\n    StrongAugment(operations=[2, 3, 4], probabilities=[0.5, 0.3, 0.2]), # Just one line!\n    T.ToTensor(),\n    T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.2, 0.2, 0.2])\n    T.RandomErase(0.2)\n)\n```\n## Creating shifted datasets.\n\nFunction `shift_dataset` can be used create the distribution-shifted datasets for shifted evaluation.\n\n```python\nfrom functools import partial\nimport torchvision.transforms.functional as F\nfrom strong_augment import shift_dataset\n\n# Let\'s define the distribution shift function.\nshift_fn = partial(F.adjust_gamma, gamma=0.2)\n\n# Now we can shift the dataset!\nshift_dataset(\n    paths=paths_to_dataset_images,\n    output_dir="/data/shifted_datasets/gamma_02",\n    function=shift_fn,\n    num_workers=20,\n)\n```\n\n    Processing images |##########| 100000/100000 [00:49<00:00]\n\n## Citation\n\nIf you use `StrongAugment` or **_shifted evaluation_**, please cite us!\n\n```bibtex\n@paper{strong_augment2022,\n    title = {Augment like there\'s no tomorrow: Consistently performing neural networks for medical imaging},\n    author = {Pohjonen, Joona and Stürenberg, Carolin and Föhr, Atte and Randen-Brady, Reija and Luomala, Lassi and Lohi, Jouni and Pitkänen, Esa and Rannikko, Antti and Mirtti, Tuomas},\n    url = {https://arxiv.org/abs/2206.15274},\n    publisher = {arXiv},\n    year = {2022},\n}\n```\n',
    'author': 'jopo666',
    'author_email': 'jopo@birdlover.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
