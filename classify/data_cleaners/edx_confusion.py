from abstract_data_cleaner import DataCleaner
import dc_util
from edx import Edx


class EdxConfusion(Edx):
    def __init__(self,
                 binary=False,
                 collapse_numbers=False,
                 latex=True,
                 extract_noun_phrases=False,
                 first_sentence_weight=1):
        super(EdxConfusion, self).__init__(binary, collapse_numbers, latex,
                                           extract_noun_phrases,
                                           first_sentence_weight)
        self.name = 'EdxConfusion ' + self.name


    def labels(self):
        if self.binary:
            return ['not-confused', 'confused']
        else:
            return ['knowledgeable', 'neutral', 'confused']


    def process_doc(self, document):
        return super(EdxConfusion, self).process_doc(document)


    # The first entry in each record is the document;
    # the sixth entry in each record is the confusion likert score.
    def process_records(self, records):
        return [(self.process_doc(record[0]),
                dc_util.compress_likert(int(float(record[5])), self.binary, 4))
                for record in records]
