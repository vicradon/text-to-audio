import json
import re
import nltk
import random
import math
import os

def break_into_sentences(text):
    nltk.download('punkt')
    sentences = nltk.sent_tokenize(text)

    return sentences

def sanitize_references(text):
    reference_pattern = re.compile(r'\[\d+\]')
    sanitized_text = re.sub(reference_pattern, '', text)

    return sanitized_text

def break_into_units(input_val):
  words = input_val.split(" ")
  output = []
  local_start = 0
  local_end = 0

  local_output = []

  for word in words:
    if len(word) + (local_end - local_start) > (600 - len(local_output)):
      output.append(" ".join(local_output))
      local_output = []
      local_start = local_end
    else:
      local_end += len(word)
      local_output.append(word)

  with open('input.json', 'w') as input_json_file:
    json.dump(output,  input_json_file)


input_value = '''
In the realm of computing, endianness refers to the specific arrangement of bytes within a word of digital data, whether stored in computer memory or transmitted through a data communication medium. This concept is elegantly categorized as big-endian (BE) or little-endian (LE), terms introduced by Danny Cohen in a 1980 publication known as an Internet Experiment Note. The term "endian" itself traces its origins back to the writings of 18th-century Anglo-Irish author Jonathan Swift. In his 1726 novel, Gulliver's Travels, Swift skillfully illustrates the division among sects of Lilliputians based on the method they employ to break the shell of a boiled egg – either from the big end or the little end.

In the intricate landscape of computers, information is stored in groups of binary bits with varying sizes. Each group is assigned a numerical address that serves as the computer's means of accessing the data. On contemporary computers, the smallest data group with an address is an eight-bit byte. Larger groups consist of two or more bytes, such as a 32-bit word comprising four bytes. The choice of how a computer numbers individual bytes within a larger group, starting from either end, gives rise to two prevalent types of endianness in digital electronic engineering. The initial selection of endianness in a new design may be somewhat arbitrary, yet subsequent technological revisions maintain consistency with the existing endianness to ensure backward compatibility.

In a big-endian system, the most significant byte of a word resides at the smallest memory address, while the least significant byte finds its place at the largest address. Conversely, a little-endian system stores the least-significant byte at the smallest address. Of these two, big-endian aligns more closely with the left-to-right writing style of English, as digits are compared to bytes. Bi-endianness emerges as a feature supported by numerous computer architectures, allowing for switchable endianness in data and instruction fetches. Other orderings are broadly termed middle-endian or mixed-endian.

Big-endianness prevails in networking protocols, notably within the Internet protocol suite, where it is aptly termed network order, prioritizing the transmission of the most significant byte first. In contrast, little-endianness dominates processor architectures (such as x86, most ARM implementations, and base RISC-V implementations) and their associated memory. File formats may adopt either ordering, with some using a combination or including an indicator specifying the ordering used throughout the file.
'''

async def process_text(text):
  sanitized_text = sanitize_references(text)
  sentences = break_into_sentences(sanitized_text)

  base_path = "/tmp/python-text-to-audio/" + str(math.floor(random.randint(1, 100000)))
  os.makedirs(base_path, exist_ok=True)

  json_file_path = f"{base_path}/input.json"

  with open(json_file_path, 'w') as input_json_file:
    json.dump(sentences,  input_json_file)
  
  return base_path