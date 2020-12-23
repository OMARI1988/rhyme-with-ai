import copy

import streamlit as st
from rhyme_with_ai.rhyme import query_rhyme_words
from rhyme_with_ai.rhyme_generator import RhymeGenerator
from rhyme_with_ai.utils import color_new_words, sanitize
from transformers import BertTokenizer, TFBertForMaskedLM

DEFAULT_QUERY = "Thomas ans Simon are in town"
N_RHYMES = 7
ITER_FACTOR = 5


LANGUAGE = st.sidebar.radio("Language",["english","dutch"],0)
if LANGUAGE == "english":
    MODEL_PATH = "./data/bert-large-cased-whole-word-masking"
elif LANGUAGE == "dutch":
    MODEL_PATH = "./data/wietsedv/bert-base-dutch-cased"
else:
    raise NotImplementedError(f"Unsupported language ({LANGUAGE}) expected 'english' or 'dutch'.")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    st.markdown(
        "<sup> Cool AI DJ </sup>",
        unsafe_allow_html=True,
    )
    st.title("Rhyme with AI")
    LANGUAGE = 'english'
    query = get_query()
    print('>>>>>>',query)
    if not query:
        query = DEFAULT_QUERY
    rhyme_words_options = query_rhyme_words(query, n_rhymes=N_RHYMES,language=LANGUAGE)
    print(rhyme_words_options)
    if rhyme_words_options:
        start_rhyming(query, rhyme_words_options)
    else:
        st.write("No rhyme words found")


def get_query():
    return str(input('Write your first sentence and press ENTER to rhyme:   ')) 
    # q = sanitize(
    #     st.text_input("Write your first line and press ENTER to rhyme:", DEFAULT_QUERY)
    # )
    # if not q:
    #     return DEFAULT_QUERY
    # return q


def start_rhyming(query, rhyme_words_options):
    st.markdown("## My Suggestions:")

    progress_bar = st.progress(0)
    status_text = st.empty()
    max_iter = len(query.split()) * ITER_FACTOR
    print('>>>max_iter',max_iter)
    
    rhyme_words = rhyme_words_options[:N_RHYMES]
    print('>>>rhyme_words',rhyme_words)

    print('>>>loading the BERTs')
    model, tokenizer = load_model(MODEL_PATH)
    
    print('>>>start generating')
    sentence_generator = RhymeGenerator(model, tokenizer)
    sentence_generator.start(query, rhyme_words)

    current_sentences = [" " for _ in range(N_RHYMES)]
    for i in range(max_iter):
        previous_sentences = copy.deepcopy(current_sentences)
        current_sentences = sentence_generator.mutate()
        display_output(status_text, query, current_sentences, previous_sentences, i)
        # progress_bar.progress(i / (max_iter - 1))
    print()
    # st.balloons()


@st.cache(allow_output_mutation=True)
def load_model(model_path):
    return (
        TFBertForMaskedLM.from_pretrained(model_path),
        BertTokenizer.from_pretrained(model_path),
    )


def display_output(status_text, query, current_sentences, previous_sentences, i):
    # print_sentences = []
    # for new, old in zip(current_sentences, previous_sentences):
    #     for n,o in zip(new.split(' '), old.split(' ')):
    #         print(n,o)
    #     # print(new, old)
    #     formatted = color_new_words(new, old)
    #     after_comma = "<li>" + formatted.split(",")[1][:-2] + "</li>"
    #     print_sentences.append(after_comma)
    # status_text.markdown(
    #     query + ",<br>" + "".join(print_sentences), unsafe_allow_html=True
    # )
    # print(+ "Warning: No active frommets remain. Continue?" + )

    print()
    print('==----------------------------- iteration num:',i,' ----==')
    A = [bcolors.WARNING + query + bcolors.ENDC] + [i.split(', ')[1] for i in current_sentences]
    print('\n'.join(A))


if __name__ == "__main__":
    main()
