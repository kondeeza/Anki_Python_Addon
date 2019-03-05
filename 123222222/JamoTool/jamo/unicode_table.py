# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super, filter, map, zip)

JAMO_UNICODE = {
    'CHOSEONG': [0x1100, 0x1101, 0x1102, 0x1103, 0x1104, 0x1105,
                 0x1106, 0x1107, 0x1108, 0x1109, 0x110a, 0x110b,
                 0x110c, 0x110d, 0x110e, 0x110f, 0x1110, 0x1111,
                 0x1112],
    'JUNGSEONG' : [0x1161, 0x1162, 0x1163, 0x1164, 0x1165, 0x1166,
                 0x1167, 0x1168, 0x1169, 0x116a, 0x116b, 0x116c,
                 0x116d, 0x116e, 0x116f, 0x1170, 0x1171, 0x1172,
                 0x1173, 0x1174, 0x1175],
    'JONGSEONG' : [0x11a8, 0x11a9, 0x11aa, 0x11ab, 0x11ac, 0x11ad,
                0x11ae, 0x11af, 0x11b0, 0x11b1, 0x11b2, 0x11b3,
                0x11b4, 0x11b5, 0x11b6, 0x11b7, 0x11b8, 0x11b9,
                0x11ba, 0x11bb, 0x11bc, 0x11bd, 0x11be, 0x11bf,
                0x11c0, 0x11c1, 0x11c2]
}

COMPAT_UNICODE = {
    'CHOSEONG': [0x3131, 0x3132, 0x3134, 0x3137, 0x3138, 0x3139,
                 0x3141, 0x3142, 0x3143, 0x3145, 0x3146, 0x3147,
                 0x3148, 0x3149, 0x314a, 0x314b, 0x314c, 0x314d,
                 0x314e],
    'JUNGSEONG' : [0x314f, 0x3150, 0x3151, 0x3152, 0x3153, 0x3154,
                 0x3155, 0x3156, 0x3157, 0x3158, 0x3159, 0x315a,
                 0x315b, 0x315c, 0x315d, 0x315e, 0x315f, 0x3160,
                 0x3161, 0x3162, 0x3163],
    'JONGSEONG' : [0x3131, 0x3132, 0x3133, 0x3134, 0x3135, 0x3136,
                0x3137, 0x3139, 0x313a, 0x313b, 0x313c, 0x313d,
                0x313e, 0x313f, 0x3140, 0x3141, 0x3142, 0x3144,
                0x3145, 0x3146, 0x3147, 0x3148, 0x314a, 0x314b,
                0x314c, 0x314d, 0x314e] # ㄸ, ㅃ, ㅉ 제외 (완성형 한글 불가)
}

HALFWIDTH_UNICODE = {
    'CHOSEONG': [0xffa1, 0xffa2, 0xffa4, 0xffa7, 0xffa8, 0xffa9, 
                 0xffb1, 0xffb2, 0xffb3, 0xffb5, 0xffb6, 0xffb7, 
                 0xffb8, 0xffb9, 0xffba, 0xffbb, 0xffbc, 0xffbd, 
                 0xffbe],
    'JUNGSEONG' : [0xffc2, 0xffc3, 0xffc4, 0xffc5, 0xffc6, 0xffc7,
                 0xffca, 0xffcb, 0xffcc, 0xffcd, 0xffce, 0xffcf,
                 0xffd2, 0xffd3, 0xffd4, 0xffd5, 0xffd6, 0xffd7,
                 0xffda, 0xffdb, 0xffdc],
    'JONGSEONG' : [0xffa1, 0xffa2, 0xffa3, 0xffa4, 0xffa5, 0xffa6,
                0xffa7, 0xffa9, 0xffaa, 0xffab, 0xffac, 0xffad, 
                0xffae, 0xffaf, 0xffb0, 0xffb1, 0xffb2, 0xffb4, 
                0xffb5, 0xffb6, 0xffb7, 0xffb8, 0xffba, 0xffbb, 
                0xffbc, 0xffbd, 0xffbe] # ㄸ, ㅃ, ㅉ 제외 (완성형 한글 불가)
}


JAMO_TO_COMPAT_UNICODE_MAP={}
for _jamo, _compat  in zip(JAMO_UNICODE['CHOSEONG'], COMPAT_UNICODE['CHOSEONG']):
    JAMO_TO_COMPAT_UNICODE_MAP[_jamo]=_compat

for _jamo, _compat  in zip(JAMO_UNICODE['JUNGSEONG'], COMPAT_UNICODE['JUNGSEONG']):
    JAMO_TO_COMPAT_UNICODE_MAP[_jamo]=_compat

for _jamo, _compat  in zip(JAMO_UNICODE['JONGSEONG'], COMPAT_UNICODE['JONGSEONG']):
    JAMO_TO_COMPAT_UNICODE_MAP[_jamo]=_compat


HALFWIDTH_TO_COMPAT_UNICODE_MAP={}
for _jamo, _compat  in zip(HALFWIDTH_UNICODE['CHOSEONG'], COMPAT_UNICODE['CHOSEONG']):
    HALFWIDTH_TO_COMPAT_UNICODE_MAP[_jamo]=_compat

for _jamo, _compat  in zip(HALFWIDTH_UNICODE['JUNGSEONG'], COMPAT_UNICODE['JUNGSEONG']):
    HALFWIDTH_TO_COMPAT_UNICODE_MAP[_jamo]=_compat

for _jamo, _compat  in zip(HALFWIDTH_UNICODE['JONGSEONG'], COMPAT_UNICODE['JONGSEONG']):
    HALFWIDTH_TO_COMPAT_UNICODE_MAP[_jamo]=_compat