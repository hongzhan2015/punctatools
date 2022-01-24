import argparse
import os

from punctatools.lib.quantify import quantify_batch
from punctatools.lib.segment import segment_puncta_batch
from punctatools.lib.utils import load_parameters

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameter-file', type=str, help='json file with parameters', required=True)
    args = parser.parse_args()
    parameter_file = args.parameter_file

    param_keys = [
        'puncta_segm_dir',
        'puncta_stat_dir',
        'cell_stat_dir',
        'puncta_channels',
        'cell_segmentation',
        'minsize_um',
        'maxsize_um',
        'num_sigma',
        'overlap',
        'threshold_detection',
        'threshold_background',
        'global_background',
        'global_background_percentile',
        'background_percentile',
        'threshold_segmentation',
        'segmentation_mode',
        'remove_out_of_cell',
        'maxrad_um',
        'n_jobs',
        'channel_names'
    ]
    param_matches = dict(output_dir='puncta_analysis_dir')
    kwargs = load_parameters(vars(), param_keys, param_matches)
    if kwargs['cell_segmentation']:
        param_matches['input_dir'] = 'cell_segmentation_dir'
    else:
        param_matches['input_dir'] = 'converted_data_dir'
    kwargs = load_parameters(vars(), param_keys, param_matches)

    print('\nThe following are the parameters that will be used:')
    print(kwargs)
    print('\n')

    channel_names = kwargs.pop('channel_names')
    puncta_segm_dir = kwargs.pop('puncta_segm_dir')
    cell_stat_dir = kwargs.pop('cell_stat_dir')
    puncta_stat_dir = kwargs.pop('puncta_stat_dir')

    segm_kwargs = kwargs.copy()
    segm_kwargs['output_dir'] = os.path.join(segm_kwargs['output_dir'], puncta_segm_dir)
    segment_puncta_batch(parallel=True, process_name='Segment puncta', **segm_kwargs)

    print('\n')

    quantify_batch(input_dir=segm_kwargs['output_dir'],
                   output_dir_puncta=os.path.join(kwargs['output_dir'], puncta_stat_dir),
                   output_dir_roi=os.path.join(kwargs['output_dir'], cell_stat_dir),
                   parallel=True, n_jobs=kwargs['n_jobs'],
                   channel_names=channel_names,
                   puncta_channels=kwargs['puncta_channels'],
                   process_name='Quantify puncta')
