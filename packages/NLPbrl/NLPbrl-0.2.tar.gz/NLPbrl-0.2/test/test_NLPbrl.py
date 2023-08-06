import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from NLPbrl import NLP_


class TestProj(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.nlp = NLP_.NLP()
        self.short_text_en = "simple test of calculate frequency."
        self.freq_short_res_en = [('simple', 1), ('test', 1), ('calculate', 1), ('frequency', 1)]
        self.long_text_en = "The goal of the package is to wrap into a set of R/Python functions a web REST API and offer a package for others to use those functions. The functions offered by the package should also take care of the minimum wrangling necessary to output the data in a viable format (that is, not as a raw binary file, unless a raw binary file is the most appropriate data format). You choose the API and the most appropriate input / output design of your functions. Think carefully of what part of the wrangling is of general interest (i.e., most or all of the users will want to perform it, and thus should be done in the package) and what part is only relevant as an example for the vignette (i.e., is too specific to be of general interest, and thus may just end up in the vignette.)"*20
        self.short_text_cn = "这是一个简单的代码测试代码块，用来测试中文的词频计算"
        self.freq_short_res_cn = [('代码', 2), ('测试', 2), ('一个', 1), ('简单', 1), ('块', 1), ('中文', 1), ('词频', 1), ('计算', 1)]
        self.empty_text = ""
        self.tf_idf_corpus1 = ['This is the first document.',
                        'This document is the second document.',
                        'And this is the third one.',
                        'Is this the first document?',
                        "let's begin our test.",]
        self.tf_idf_text1 = 'This is the test.'
        self.tf_idf_corpus2 = ["The cat sat on my bed",
                                "The dog sat on my knees"]
        self.tf_idf_text2 = "The dog sat on my knees"
        self.simi_text1 = 'I am eating an apple'
        self.simi_text2 = 'She is eating an apple'
        self.rank_short_res_en = [('test', 1.0), ('calculate', 1.0), ('frequency', 1.0)]
        self.rela_text = "FLIR Systems is headquartered in Oregon and produces thermal imaging, night vision, and infrared cameras and sensor systems.  According to the SEC’s order instituting a settled administrative proceeding, FLIR entered into a multi-million dollar contract to provide thermal binoculars to the Saudi government in November 2008.  Timms and Ramahi were the primary sales employees responsible for the contract, and also were involved in negotiations to sell FLIR’s security cameras to the same government officials.  At the time, Timms was the head of FLIR’s Middle East office in Dubai."
        self.cate_text = "Sony Pictures is planning to shoot a good portion of the new \"Ghostbusters\" in Boston as well."
        self.cate_res = [{'label': 'ARTS_AND_ENTERTAINMENT','confidence': 0.06416648,'score': -0.01447566},
                        {'label': 'SPORTS', 'confidence': 0.05782175, 'score': -0.11859164},
                        {'label': 'TRAVEL', 'confidence': 0.05627946, 'score': -0.14562697}]
        
    @classmethod
    def tearDownClass(self):
        print('successful')
        
    def test_cal_frequency(self):
        self.assertEqual(self.nlp.cal_frequency(self.short_text_en),self.freq_short_res_en)
        self.assertEqual(self.nlp.cal_frequency(self.long_text_en)[0][1],self.long_text_en.count('package'))
        self.assertEqual(self.nlp.cal_frequency(self.short_text_cn),self.freq_short_res_cn)
        self.assertEqual(self.nlp.cal_frequency(self.empty_text),False)

    def test_word_viz(self):
        self.assertEqual(self.nlp.word_viz(self.short_text_en, '', 10),True)
        self.assertEqual(self.nlp.word_viz(self.long_text_en, 'test123/', 10),False)
        self.assertEqual(self.nlp.word_viz(self.short_text_cn, '', 10),True)
        self.assertEqual(self.nlp.word_viz(self.empty_text, '', 10),False)

    def test_extra_tfidf(self):
        self.assertAlmostEqual(self.nlp.key_extra_tfidf(self.tf_idf_text1, self.tf_idf_corpus1)['test'],0.2386,2)
        self.assertAlmostEqual(self.nlp.key_extra_tfidf(self.tf_idf_text2, self.tf_idf_corpus2, 'None')['dog'],0.029,2)
        self.assertEqual(self.nlp.key_extra_tfidf(self.empty_text, self.tf_idf_corpus2),False)
        self.assertEqual(self.nlp.key_extra_tfidf(self.empty_text, self.empty_text),False)

    def test_cal_simi(self):
        self.assertAlmostEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'sen','euc'),0.40277734306421165)
        self.assertAlmostEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'word','euc'),1.46,2)
        self.assertAlmostEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'sen','cos'),0.92,2)
        self.assertAlmostEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'word','cos'),0.787,2)
        self.assertAlmostEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,method='jac'),0.429,2)
        self.assertEqual(self.nlp.cal_simi(self.empty_text,self.simi_text2,'sen','euc'),False)
        self.assertEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'a'),False)
        self.assertEqual(self.nlp.cal_simi(self.simi_text1,self.simi_text2,'sen','a'),False)
        
    def test_textRank(self):
        self.assertEqual(self.nlp.cal_textRank(self.short_text_en),self.rank_short_res_en)
        self.assertAlmostEqual(self.nlp.cal_textRank(self.long_text_en, candidate_pos=['NOUN', 'VERB']),False)
        self.assertAlmostEqual(self.nlp.cal_textRank(self.short_text_cn, candidate_pos=['NOUN', 'VERB'])[0][1],1.586,2)
        self.assertEqual(self.nlp.cal_textRank(self.empty_text),False)

    def test_relation_viz(self):
        self.assertEqual(self.nlp.relation_viz(self.rela_text),True)
        self.assertEqual(self.nlp.relation_viz(self.empty_text),False)

    def test_cal_classification(self):
        self.assertEqual(self.nlp.cal_classification(self.cate_text),self.cate_res)
        self.assertEqual(self.nlp.cal_classification(self.cate_text, 100),False)
        self.assertEqual(self.nlp.cal_classification(self.empty_text),False)
