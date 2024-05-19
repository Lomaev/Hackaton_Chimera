from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)


def select_names(text: str):
    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        if span.type == PER:
            span.normalize(morph_vocab)
            span.extract_fact(names_extractor)

    try:
        return tuple(_.fact.as_dict for _ in doc.spans if _.type == PER)
    except AttributeError:  # Sometimes extract_fact failes, and name not split.
        print('Error while extract_fact for', text)
        ret = []
        for _ in doc.spans:
            if _.type == PER:
                name_parts = _.normal.split()
                if len(name_parts) == 1:
                    ret.append({'first': name_parts[0]})
                else:
                    ret.append({'first': name_parts[0], 'last': name_parts[1]})

        return tuple(ret)