#!/usr/bin/env python3


import argparse
import sys
import unicodedata
import multiprocessing

import pytorch_pretrained_bert as bert


# This set contains all letter and number characters.
_ALPHANUMERIC_CHAR_SET = set(
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith("L") or
        unicodedata.category(chr(i)).startswith("N")))


_BERT_TOKENIZER: bert.BertTokenizer = None


_HAS_TAG = False
_ADD_TAG = False
_VOCAB_SET = set()


_SUFFIX = {
    'st', 'nd', 'rd', 'th',
    'mm', 'm',
    'ns', 'ms', 's', 'hr', 'h'
}


def parse_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='-')
    p.add_argument('--output', default='-')
    p.add_argument('--bert-name', default='bert-base-cased',
        help='Pretrained bert tokenizer to use, default to "bert-base-cased"')
    p.add_argument('--worker', type=int,
        help='Number of workers, will choose automatically if omitted.')
    p.add_argument('--has-tag', action='store_true',
        help='Whether there is a tag in every line, e.g. TAGun')
    p.add_argument('--add-tag', action='store_true',
        help='Add a dummy tag to every output line')
    return p.parse_args()


def split_number(token):
    x = [token[0]]
    x.extend('##' + c for c in token[1:])
    return x


def split_number_suffix(token, suffix):
    x = [token[0]]
    x.extend('##' + c for c in token[1:suffix])
    x.append('##' + token[suffix:])
    return x


def encode(text):
    if not text:
        return []
    ret = []
    token_start = 0
    # Classify each character in the input string
    is_alnum = [c in _ALPHANUMERIC_CHAR_SET for c in text]
    for pos in range(1, len(text)):
        if is_alnum[pos] != is_alnum[pos - 1]:
            token = text[token_start:pos]
            if token != u" " or token_start == 0:
                ret.extend(split_token(token))
            token_start = pos
    final_token = text[token_start:]
    ret.extend(split_token(final_token))

    return ' '.join(ret)


def tokenize(text):
    if _HAS_TAG:
        space = text.find(' ')
        return text[:space] + ' ' + encode(text[space+1:])
    if _ADD_TAG:
        return '@ ' + encode(text)
    return encode(text)


def split_token(t):
    if t[0] not in _ALPHANUMERIC_CHAR_SET:
        return list(t)

    if t[0].isdigit():
        # Numbers w/ two-letter suffixes 1st, 2nd, etc.
        if len(t) >= 3 and t[-2:] in _SUFFIX and t[:-2].isdigit():
            return split_number_suffix(t, -2)

        # Numbers w/ one-letter suffixes, e.g. 1930s, 500m
        if len(t) >= 2 and t[-1:] in _SUFFIX and t[:-1].isdigit():
            return split_number_suffix(t, -1)

        # Numbers
        if t.isdigit():
            r = split_number(t)
            return r

    ret = []
    start = 0
    cjk = [0x4e00 <= ord(c) <= 0x9fff for c in t]
    for i, c in enumerate(t):
        if cjk[i]:
            if start != i:
                ret.extend(split_token(t[start:i]))
            start = i + 1
            ret.append(c)
            continue
    if start < len(t):
        if start == 0:
            if t in _VOCAB_SET:
                ret.append(t)
            else:
                ret.extend(_BERT_TOKENIZER.tokenize(t))
        else:
            ret.extend(split_token(t[start:]))

    return ret


def create_tokenizer(name):
    never_split = ["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"]
    for i in range(10):
        never_split.append(f'##{i}')
    for s in _SUFFIX:
        never_split.append(f'##{s}')

    lower = name.find('uncased') >= 0 or name == 'bert-base-chinese'

    return bert.BertTokenizer.from_pretrained(name, never_split=never_split,
        do_lower_case=lower)


def main():
    cmdline = parse_cmdline()

    global _HAS_TAG
    _HAS_TAG = cmdline.has_tag
    global _ADD_TAG
    _ADD_TAG = cmdline.add_tag
    global _BERT_TOKENIZER
    _BERT_TOKENIZER = create_tokenizer(cmdline.bert_name)
    global _VOCAB_SET
    _VOCAB_SET = set(x for x, y in _BERT_TOKENIZER.vocab.items())

    if cmdline.input == '-':
        input_file = sys.stdin
    else:
        input_file = open(cmdline.input)
    if cmdline.output == '-':
        output_file = sys.stdout
    else:
        output_file = open(cmdline.output, 'w')

    with input_file, output_file:
        if cmdline.worker != 1:
            pool = multiprocessing.Pool(processes=cmdline.worker)
            buffer = []
            for line in input_file:
                if len(buffer) < 768:
                    buffer.append(line.strip())
                    continue
                for o in pool.map(tokenize, buffer):
                    print(o, file=output_file)
                buffer = []
            else:
                for o in pool.map(tokenize, buffer):
                    print(o, file=output_file)
        else:
            for line in input_file:
                print(tokenize(line.strip()), file=output_file)


if __name__ == '__main__':
    main()
