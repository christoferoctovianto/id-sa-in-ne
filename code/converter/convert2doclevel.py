from converter.convert_2 import flatten_all
from converter.io import read_jsonl
from converter.utility import get_structured
from converter.utility import get_tags_structured
from collections import Counter
import pandas as pd

def convert2doclevel(file_path):
    tags = get_tags_structured(get_structured(flatten_all(read_jsonl(file_path))))
    majority, majority_mix, mix = [],[],[]
    for tag in tags:
        if tag == []:
            majority.append("NEUTRAL")
            majority_mix.append("NEUTRAL")
            mix.append("NEUTRAL")
        else:
            if Counter(tag)["Exp_Positive"] > Counter(tag)["Exp_Negative"]:
                majority.append("POSITIVE")
                majority_mix.append("POSITIVE")
                if Counter(tag)["Exp_Negative"] == 0:
                    mix.append("POSITIVE")
                else:
                    mix.append("MIXED")
            elif Counter(tag)["Exp_Positive"] < Counter(tag)["Exp_Negative"]:
                majority.append("NEGATIVE")
                majority_mix.append("NEGATIVE")
                if Counter(tag)["Exp_Positive"] == 0:
                    mix.append("NEGATIVE")
                else:
                    mix.append("MIXED")
            else:
                majority.append("NEUTRAL")
                majority_mix.append("MIXED")
                mix.append("MIXED")
    df_doclevel = pd.DataFrame({"majority":majority,"majority_mix":majority_mix,"mix":mix})
    return df_doclevel
