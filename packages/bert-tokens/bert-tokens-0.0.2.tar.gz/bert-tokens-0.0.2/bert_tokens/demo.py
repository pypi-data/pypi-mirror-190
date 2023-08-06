# Show cases

from bert_tokenizer import Tokenizer
from convert_word_span import convert_word_span

dict_path = "vocab/vocab_chinese.txt"
delete_cls_sep = True
tokenizer = Tokenizer(dict_path, do_lower_case=True)
#tokens = tokenizer.tokenize("翻译Je pense a vous tout le temps")
tokens =  tokenizer.tokenize("播放MYLOVE")
print(tokens)

print(convert_word_span("播放MYLOVE", [2, 8], tokenizer, delete_cls_sep))
