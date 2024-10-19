import re
from converter.io import read_jsonl

def flatten(data,relation_mode,debug):
  output_text = []
  beg_index = 0
  end_index = 0
  text = data["text"]
  # No relation mode
  if relation_mode == "no_relation":
    all_labels = sorted(data["label"])
  elif relation_mode == "with_relation":
    label_list = []
    for i in data["entities"]:
      set_label = []
      set_label.append(i.get("start_offset"))
      set_label.append(i.get("end_offset"))
      set_label.append(i.get("label"))
      label_list.append(set_label)
    all_labels = sorted(label_list)
  else:
    raise ValueError("Wrong relation_mode. Only 'no_relation' or 'with_relation' is allowed.")

  for ind in range(len(all_labels)):
    next_label = all_labels[ind]
    output_text += [(label_word, "O") for label_word in re.findall(r"[\w']+|[.,!?;]",text[end_index:next_label[0]].strip())]

    label = next_label
    beg_index = label[0]
    if beg_index !=0:
      try:
        if debug == True:
          print("We correcting the beg_index")
          print(f'Origin beg_index is {beg_index}')
        if text[beg_index-1].isalnum():
          i = -1
          while(text[beg_index+i].isalnum() and (beg_index+i)!=0):
              i = i-1
          beg_index = beg_index+i+1
          if debug == True:
            print(f'New beg_index is {beg_index}')
          if beg_index == 1:
            beg_index = 0
            if debug == True:
              print(f'New beg_index after re-correction is {beg_index}')
          output_text = output_text[:-1]
      except:
        pass
    end_index = label[1]
    try:
      if (text[end_index-1] != " " or text[end_index-1] == "") and text[end_index].isalnum():
        if debug == True:
          print("We correcting the end_index")
          print(f'Origin end_index is {end_index}')
          print(f'len(text) is {len(text)}')
        i = 1
        try:
          while(text[end_index+i].isalnum()):
              i = i+1
        except:
          pass
        end_index = end_index+i
        if debug == True:
          print(f'New end_index is {end_index}')
    except:
      pass
    try:
      if text[end_index] == "'":
        if debug == True:
          print("We re-correcting the end_index to handle apostrophe (')")
          print(f'Origin end_index is {end_index}')
          print(f'len(text) is {len(text)}')
        i = 1
        try:
          while(text[end_index+i].isalnum()):
              i = i+1
        except:
          pass
        end_index = end_index+i
        if debug == True:
          print(f"New end_index after handling apostrophe (') is {end_index}")
    except:
      pass
    label_text = text[beg_index:end_index]
    output_text += [(label_word, "B-" + label[2]) if not i else (label_word, "I-" + label[2]) for i, label_word in enumerate(re.findall(r"[\w']+|[.,!?;]",label_text.strip()))]

  output_text += [(label_word, "O") for label_word in re.findall(r"[\w']+|[.,!?;]",text[end_index:].strip())]
  return output_text

def flatten_all(datas,relation_mode,debug,):
  return [flatten(data,relation_mode,debug) for data in datas]

def jsonl2conll(file_path,relation_mode,debug=False):
  return flatten_all(read_jsonl(file_path),relation_mode,debug)