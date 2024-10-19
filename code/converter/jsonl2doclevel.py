from converter.jsonl2conll import jsonl2conll
from converter.utility import get_structured
from converter.utility import get_tags_structured
from collections import Counter
import pandas as pd

def jsonl2doclevel(file_path,doclevel_mode,relation_mode,debug=False):
    tags = get_tags_structured(get_structured(jsonl2conll(file_path,relation_mode,debug)))
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
    if doclevel_mode == "majority":
        return majority
    elif doclevel_mode == "majority_mix":
        return majority_mix
    elif doclevel_mode == "mix":
        return mix
    elif doclevel_mode == "all":
        df_doclevel = pd.DataFrame({"majority":majority,"majority_mix":majority_mix,"mix":mix})
        return df_doclevel
    else:
        raise ValueError(f"Wrong doclevel_mode. Only 'majority', 'majority_mix', 'mix', or 'all' is allowed.")
