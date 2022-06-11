import os
from typing import Any
import json
import datasets
import pandas as pd
import numpy as np
from math import ceil

from collections import OrderedDict
from collections import defaultdict

CCAGT_CLASSES = OrderedDict(
    {
        0: 'BACKGROUND',
        1: 'NUCLEUS',
        2: 'CLUSTER',
        3: 'SATELLITE',
        4: 'NUCLEUS_OUT_OF_FOCUS',
        5: 'OVERLAPPED_NUCLEI',
        6: 'NON_VIABLE_NUCLEUS',
        7: 'LEUKOCYTE_NUCLEUS',
    }
)


_LICENSE = 'CC BY NC 3.0 License'

_CITATION = '''\
@misc{CCAgTDataset,
  doi = {10.17632/WG4BPM33HJ.2},
  url = {https://data.mendeley.com/datasets/wg4bpm33hj/2},
  author =  {Jo{\~{a}}o Gustavo Atkinson Amorim and Andr{\'{e}} Vict{\'{o}}ria Matias and Tainee Bottamedi and Vinícius Sanches and Ane Francyne Costa and Fabiana Botelho De Miranda Onofre and Alexandre Sherlley Casimiro Onofre and Aldo von Wangenheim},
  title = {CCAgT: Images of Cervical Cells with AgNOR Stain Technique},
  publisher = {Mendeley},
  year = {2022},
  copyright = {Attribution-NonCommercial 3.0 Unported}
}
'''

_HOMEPAGE = 'https://data.mendeley.com/datasets/wg4bpm33hj'

_DESCRIPTION = '''\
Images of Cervical Cells with AgNOR Stain Technique - CCAgT dataset Contains 9339 images with resolution of 1600×1200 where each pixel is
0.111µmX0.111µm from 15 different slides stained with AgNOR technique, having at least one label per image. Have more than sixty-three thousand
annotations. The images from patients of Gynecology and Colonoscopy Outpatient Clinic of the Polydoro Ernani de São Thiago University Hospital of
the Universidade Federal de Santa Catarina (HU-UFSC). This research was approved by the UFSC Research Ethics Committee (CEPSH), protocol number
57423616.3.0000.0121. First, all patients involved were informed about the objectives of the study, and those who agreed to participate signed an
informed consent form.
'''

_DATA_URL = 'https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/wg4bpm33hj-2.zip'


def tvt(
    ids: list[int],
    tvt_size: tuple[float, float, float],
    seed: int = 1609,
) -> tuple[set[int], set[int], set[int]]:
    '''From a list of indexes/ids (int) will generate the train-validation-test data.

    Based on `github.com/scikit-learn/scikit-learn/blob/37ac6788c9504ee409b75e5e24ff7d86c90c2ffb/sklearn/model_selection/_split.py#L2321`
    '''
    n_samples = len(ids)

    qtd = {
        'valid': ceil(n_samples * tvt_size[1]),
        'test': ceil(n_samples * tvt_size[2]),
    }
    qtd['train'] = int(n_samples - qtd['valid'] - qtd['test'])

    rng = np.random.RandomState(seed)
    permutatation = rng.permutation(ids)

    out = {
        'train': set(permutatation[:qtd['train']]),
        'valid': set(permutatation[qtd['train']:qtd['train'] + qtd['valid']]),
        'test': set(permutatation[qtd['train'] + qtd['valid']:]),
    }

    return out['train'], out['valid'], out['test']


def annotations_per_image(df: pd.DataFrame) -> pd.DataFrame:
    '''
    based on: https://github.com/johnnv1/CCAgT-utils/blob/54ade78e4ddb2e2ed9507b8a1633940897767cac/CCAgT_utils/describe.py#L152
    '''
    df_describe_images = df.groupby(['image_id', 'category_id']).size().reset_index().rename(columns={0: 'count'})
    df_describe_images = df_describe_images.pivot(columns=['category_id'], index='image_id')
    df_describe_images = df_describe_images.rename(CCAGT_CLASSES, axis=1)
    df_describe_images['qtd_annotations'] = df_describe_images.sum(axis=1)
    df_describe_images = df_describe_images.fillna(0)
    df_describe_images['NORs'] = df_describe_images[
        'count',
        CCAGT_CLASSES[2],
    ] + df_describe_images[
        'count',
        CCAGT_CLASSES[3],
    ]

    return df_describe_images


def tvt_by_nors(
    df: pd.DataFrame,
    tvt_size: tuple[float, float, float] = (.7, .15, .15),
    **kwargs: Any
) -> tuple[set[int], set[int], set[int]]:
    '''This will split the CCAgT annotations based on the number of NORs
    into each image. With a silly separation, first will split
    between each fold images with one or less NORs, after will split
    images with the amount of NORs is between 2 and 7, and at least will
    split images that have more than 7 NORs.

    based on `https://github.com/johnnv1/CCAgT-utils/blob/54ade78e4ddb2e2ed9507b8a1633940897767cac/CCAgT_utils/split.py#L64`
    '''
    if sum(tvt_size) != 1:
        raise ValueError('The sum of `tvt_size` need to be equals 1!')

    df_describe_imgs = annotations_per_image(df)

    img_ids = {}
    img_ids['low_nors'] = df_describe_imgs.loc[(df_describe_imgs['NORs'] < 2)].index
    img_ids['medium_nors'] = df_describe_imgs[(df_describe_imgs['NORs'] >= 2) * (df_describe_imgs['NORs'] <= 7)].index
    img_ids['high_nors'] = df_describe_imgs[(df_describe_imgs['NORs'] > 7)].index

    train_ids: set[int] = set({})
    valid_ids: set[int] = set({})
    test_ids: set[int] = set({})

    for k, ids in img_ids.items():
        print(f'Splitting {len(ids)} images with {k} quantity...')
        if len(ids) == 0:
            continue
        _train, _valid, _test = tvt(ids, tvt_size, **kwargs)
        print(f'>T: {len(_train)} V: {len(_valid)} T: {len(_test)}')
        train_ids = train_ids.union(_train)
        valid_ids = valid_ids.union(_valid)
        test_ids = test_ids.union(_test)

    return train_ids, valid_ids, test_ids


def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_slide_id(path):
    bn = get_basename(path)
    slide_id = bn.split('_')[0]
    return slide_id


class CCAgTConfig(datasets.BuilderConfig):
    """BuilderConfig for CCAgT."""
    seed = 1609
    tvt_size = (.7, .15, .15)


class CCAgT(datasets.GeneratorBasedBuilder):
    """Images of Cervical Cells with AgNOR Stain Technique (CCAgT) dataset"""
    VERSION = datasets.Version('2.0.0')

    BUILDER_CONFIG_CLASS = CCAgTConfig
    BUILDER_CONFIGS = [
        CCAgTConfig(name='semantic_segmentation', version=VERSION, description='The scene semantic segmentation variant.'),
        CCAgTConfig(name='object_detection', version=VERSION, description='The instance segmentation variant.'),
    ]

    DEFAULT_CONFIG_NAME = 'semantic_segmentation'

    def _info(self):
        assert len(CCAGT_CLASSES) == 8

        if self.config.name == 'semantic_segmentation':
            features = datasets.Features(
                {
                    'image': datasets.Image(),
                    'annotation': datasets.Image(),
                }
            )
        elif self.config.name == 'object_detection':
            features = datasets.Features(
                {
                    'image': datasets.Image(),
                    'digits': datasets.Sequence(
                        {
                            'bbox': datasets.Sequence(datasets.Value('int32'), length=4),
                            'label': datasets.ClassLabel(num_classes=len(CCAGT_CLASSES)),
                        }
                    ),
                }
            )
        else:
            raise NotImplementedError

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _download_and_extract_all(self, dl_manager):

        def extracted_by_slide(paths):
            return {get_slide_id(path): dl_manager.extract(path) for path in paths}

        data_dir = dl_manager.download_and_extract(_DATA_URL)
        base_dir_name = os.listdir(data_dir)[0]
        base_path = os.path.join(data_dir, base_dir_name)

        print('Extracting images...')
        self.images_base_dir = os.path.join(base_path, 'images')
        images_to_extract = [os.path.join(self.images_base_dir, fn) for fn in os.listdir(self.images_base_dir) if fn.endswith('.zip')]
        self.images_extracted = extracted_by_slide(images_to_extract)

        if self.config.name == 'semantic_segmentation':
            print('Extracting masks...')
            self.masks_base_dir = os.path.join(base_path, 'masks')
            masks_to_extract = [os.path.join(self.masks_base_dir, fn) for fn in os.listdir(self.masks_base_dir) if fn.endswith('.zip')]
            self.masks_extracted = extracted_by_slide(masks_to_extract)
        elif self.config.name == 'object_detection':
            print('Reading COCO OD file...')
            ccagt_OD_COCO_path = os.path.join(base_path, 'CCAgT_COCO_OD.json')
            with open(ccagt_OD_COCO_path, 'r') as json_file:
                coco_OD = json.load(json_file)

            self._imageid_to_coco_OD_annotations = defaultdict(list)
            for annotations in coco_OD['annotations']:
                self._imageid_to_coco_OD_annotations[annotations['image_id']].append(annotations)

        print('Loading dataset info...')
        ccagt_raw_path = os.path.join(base_path, 'CCAgT.parquet.gzip')
        self._ccagt_info = pd.read_parquet(ccagt_raw_path, columns=['image_name', 'category_id', 'image_id', 'slide_id'])
        self._bn_to_imageid = pd.Series(self._ccagt_info['image_id'].values, index=self._ccagt_info['image_name']).to_dict()

    def _split_generators(self, dl_manager):
        '''Returns SplitGenerators.'''
        def build_path(basename, tp='images'):
            slide = basename.split('_')[0]
            if tp == 'images':
                dir_path = self.images_extracted[slide]
                ext = '.jpg'
            else:
                dir_path = self.masks_extracted[slide]
                ext = '.png'

            return os.path.join(dir_path, slide, basename + ext)

        def images_and_masks(basenames):
            for bn in basenames:
                yield build_path(bn), build_path(bn, 'masks')

        def images_and_boxes(basenames):
            for bn in basenames:
                image_id = self._bn_to_imageid[bn]
                annotations = [{'bbox': annotation['bbox'],
                                'label': annotation['category_id']}
                               for annotation in self._imageid_to_coco_OD_annotations[image_id]]

                yield build_path(bn), annotations

        self._download_and_extract_all(dl_manager)

        print('Splitting dataset based on the NORs quantity by image...')
        train_ids, valid_ids, test_ids = tvt_by_nors(self._ccagt_info, tvt_size=self.config.tvt_size, seed=self.config.seed)
        train_bn_images = self._ccagt_info.loc[self._ccagt_info['image_id'].isin(train_ids), 'image_name'].unique()
        valid_bn_images = self._ccagt_info.loc[self._ccagt_info['image_id'].isin(valid_ids), 'image_name'].unique()
        test_bn_images = self._ccagt_info.loc[self._ccagt_info['image_id'].isin(test_ids), 'image_name'].unique()

        if self.config.name == 'semantic_segmentation':
            train_data = images_and_masks(train_bn_images)
            valid_data = images_and_masks(valid_bn_images)
            test_data = images_and_masks(test_bn_images)
        elif self.config.name == 'object_detection':
            train_data = images_and_boxes(train_bn_images)
            valid_data = images_and_boxes(valid_bn_images)
            test_data = images_and_boxes(test_bn_images)
        else:
            NotImplementedError

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={'data': train_data},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={'data': test_data},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={'data': valid_data},
            ),
        ]

    def _generate_examples(self, data):
        if self.config.name == 'semantic_segmentation':
            for img_path, msk_path in data:
                img_basename = get_basename(img_path)
                image_id = self._bn_to_imageid[img_basename]
                yield image_id, {'image': {'path': img_path, 'bytes': None},
                                 'annotation': {'path': msk_path, 'bytes': None}}
        elif self.config.name == 'object_detection':
            for img_path, annotations in data:
                img_basename = get_basename(img_path)
                image_id = self._bn_to_imageid[img_basename]
                yield image_id, {'image': {'path': img_path, 'bytes': None},
                                 'digits': annotations}
        else:
            NotImplementedError
