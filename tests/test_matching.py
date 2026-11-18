import unittest
from app import rank_jobs

class MatchTests(unittest.TestCase):
    def test_ranking_and_missing(self):
        jobs=[{'job_title':'Developer','requirements':'{"required_skills":["Python","SQL","Flask"]}'},
              {'job_title':'Analyst','requirements':'{"required_skills":["SQL"]}'}]
        ranked=rank_jobs(['python','SQL'],jobs)
        self.assertEqual(ranked[0]['job_title'],'Analyst')
        self.assertEqual(ranked[0]['score'],100)
        self.assertEqual(ranked[1]['score'],67)
        self.assertEqual(ranked[1]['missing'],['Flask'])

    def test_empty_requirements_ignored(self):
        self.assertEqual(rank_jobs(['SQL'],[{'job_title':'Empty','requirements':None}]),[])

if __name__=='__main__': unittest.main()
