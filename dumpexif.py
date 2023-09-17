#! /usr/bin/env python3

import errno
import glob
import json
import mimetypes
import os
import sys

import PIL.Image
import PIL.ExifTags

import pprint   # for debugging

# 検索対象は第一引数、省略時はカレントディレクトリ
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'

# 検索対象がディレクトリでなければエラーを表示して死ぬ
if not os.path.isdir(ROOT):
    print("%s: %s: %s" % (sys.argv[0], ROOT, os.strerror(errno.ENOTDIR)), file=sys.stderr)
    sys.exit(1)

# 検索対象のパスを正規化しておく
ROOT = os.path.normpath(ROOT)

# 検索対象が末尾にスラッシュを持っていなければ付加する
if ROOT[-1] != '/':
    ROOT += '/'

# 再帰的に検索する glob パターンを生成
pattern = ROOT + '**'

# 検索する
find = glob.glob(pattern, recursive=True)

# 検索結果から画像っぽいものを抽出する
images = []
for fname in find:
    mime, _ = mimetypes.guess_type(fname)
    if mime is not None and mime.startswith('image/'):
        images.append(fname)

# 画像ファイル path の Exif 辞書を返す
# そのファイルに Exif 情報が無ければ {} を返す
def getImageExif(path):
    pilImage = PIL.Image.open(path)
    exifDic = pilImage._getexif()
    if exifDic is None:
        return {}
    strDic = {}
    for key, value in exifDic.items():
        strDic[PIL.ExifTags.TAGS.get(key, key)] = str(value)
    return strDic

# 各画像の Exif を辞書形式で列挙する
imgExifs = {}
for image in images:
    imgExifs[image] = getImageExif(image)

# JSON を出力する
print(json.dumps(imgExifs))
