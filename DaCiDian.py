#!/usr/bin/env python

# This script processes DaCiDian
# FROM:
# 	layer-1 mapping: DaCiDian/word_to_pinyin.txt
# 	layer-2 mapping: DaCiDian/pinyin_to_phone.txt
# TO: 
# 	lexicon.txt

import sys

syllable_to_phones={}

word_to_syllable_file  = sys.argv[1]  # layer-1 mapping
syllable_to_phone_file = sys.argv[2]  # layer-2 mapping

for l in open(syllable_to_phone_file):  # "ZHENG	zh eng"
	cols = l.strip().split('\t')
	assert(len(cols) == 2)
	syllable = cols[0]
	phones   = cols[1].split()
	syllable_to_phones[syllable] = phones

def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

ss = 0
for l in open(word_to_syllable_file): # "15	YI_1 WU_3;YAO_1 WU_3"
	cols = l.strip().split('\t')
	assert(len(cols) == 2)
	word  = cols[0]
	prons = cols[1].split(';')
	for pron in prons:
		phone_seq = []
		for syllable in pron.split():
			base,tone = syllable.split('_')
                        #if is_contain_chinese(base):
                        #if sum(str(j) in base for j in range(10)) > 0:
                        if tone not in [str(i) for i in range(5)]:
                            base = (base+tone).upper()        
			if base in syllable_to_phones:    
                            phones = [phn for phn in syllable_to_phones[base]]
			    phones[-1] = phones[-1]+'_'+tone
			    phone_seq.extend(phones)
                        else:
                            pass
                            #print syllable                 
                if len(phone_seq) > 0:
                    ss += 1
                    sys.stdout.write(word + '\t' + ' '.join(phone_seq) + '\n')
