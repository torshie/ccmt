#!/usr/bin/env python3

import argparse
import tarfile
import os.path
import shutil


def parse_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument('--source', default='en', choices=('en', 'zh'),
        help='Source language, default to "en"')
    p.add_argument('--target', default='zh', choices=('zh', 'en'),
        help='Target language, default to "zh"')
    p.add_argument('--no-tag', action='store_true',
        help='Do not create a dataset tag on the target sentences, '
             'NOT recommended')
    p.add_argument('--keep-tmp', action='store_true',
        help='Keep extracted temporary files.')
    return p.parse_args()


def main():
    cmdline = parse_cmdline()

    config = [
        {
            'package': 'training-parallel-nc-v13.tgz',
            'files': [
                ['training-parallel-nc-v13/news-commentary-v13.zh-en.en',
                 'training-parallel-nc-v13/news-commentary-v13.zh-en.zh']
            ],
            'dataset': 'nc'
        },
        {
            'package': 'UNv1.0.en-zh.tar.gz',
            'files': [
                ['en-zh/UNv1.0.en-zh.en',
                 'en-zh/UNv1.0.en-zh.zh']
            ],
            'dataset': 'un'
        },
        {
            'package': 'ccmt.tar.gz',
            'files': [
                ["cwmt/casia2015/casia2015_en.txt",
                 "cwmt/casia2015/casia2015_ch.txt"],
                ["cwmt/casict2015/casict2015_en.txt",
                 "cwmt/casict2015/casict2015_ch.txt"],
                ["cwmt/neu2017/NEU_en.txt", "cwmt/neu2017/NEU_cn.txt"],
                ["cwmt/datum2015/datum_en.txt", "cwmt/datum2015/datum_ch.txt"],
                *[
                    [
                        f"cwmt/datum2017/Book{i}_en.txt",
                        f"cwmt/datum2017/Book{i}_cn.txt"
                    ]
                    for i in range(1, 21)
                ]
            ],
            'dataset': 'ccmt'
        }
    ]

    my_dir = os.path.dirname(os.path.abspath(__file__))
    extract_dir = f'{my_dir}/../data/train/x'
    os.makedirs(extract_dir, exist_ok=True)

    for cfg in config:
        package = my_dir + '/../data/' + cfg['package']
        with tarfile.open(package, mode='r:gz') as tar:
            tar.extractall(extract_dir)

        for en_file, zh_file in cfg['files']:
            if cmdline.source == 'en':
                src_file = open(extract_dir + '/' + en_file, 'rb')
                tgt_file = open(extract_dir + '/' + zh_file, 'rb')
            else:
                src_file = open(extract_dir + '/' + zh_file, 'rb')
                tgt_file = open(extract_dir + '/' + en_file, 'rb')

            with open(extract_dir + '/train.src', 'ab') as src_output, \
                    open(extract_dir + '/train.tgt', 'ab') as tgt_output:
                content = src_file.read()
                src_output.write(content)
                src_file.close()

                if cmdline.no_tag:
                    content = tgt_file.read()
                    tgt_output.write(content)
                else:
                    tag = b'TAG' + cfg['dataset'].encode('UTF-8')
                    for line in tgt_file:
                        tgt_output.write(tag + b' ')
                        tgt_output.write(line)
                tgt_file.close()

    if not cmdline.keep_tmp:
        shutil.rmtree(extract_dir + '/cwmt')
        shutil.rmtree(extract_dir + '/en-zh')
        shutil.rmtree(extract_dir + '/training-parallel-nc-v13')


if __name__ == '__main__':
    main()
