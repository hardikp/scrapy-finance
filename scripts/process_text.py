from argparse import ArgumentParser
from glob import glob

import spacy  # Install: pip install spacy && python -m spacy download en

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en')


def create_data_file(source):
    fmt = 'data/{}/*'.format(source)
    print('Reading files from {}...'.format(fmt))
    files = glob(fmt)

    final_text = ''
    count, percentage = 0, 0
    for f in files:
        count += 1
        if count * 100 / len(files) >= 5:
            print("""{}% done...""".format(percentage))
            count = 0
            percentage += 5

        text = open(f).read()
        doc = nlp(text)

        for tok in doc:
            final_text += tok.lower_ + ' '

    f = 'data/{}.txt'.format(source)
    print('Processing done. Writing to {}...'.format(f))
    w = open(f, 'w')
    w.write(final_text)
    w.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='Process individual text files to produce a single .txt file')
    parser.add_argument('source', type=str, help='Source: qplum/wikipedia/investopedia')

    args = parser.parse_args()

    create_data_file(args.source)
