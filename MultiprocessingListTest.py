from multiprocessing import Process, Manager
from unittest import TestCase


class MultiprocessingListTest(TestCase):

    def test_normal_list_does_not_share_data_correctly(self):

        normal_list = []
        process = Process(target=self.do_some_work, args=(normal_list, ))

        process.start()
        process.join()

        self.assertEqual(normal_list, [], "Normal list is not shared from Process child to Parent. Then is empty.")

    def test_multiprocessing_list_works_as_expected(self):

        manager = Manager()
        multiprocessing_list = manager.list()
        process = Process(target=self.do_some_work, args=(multiprocessing_list, ))

        process.start()
        process.join()  # Needed to force wait all workers to finish

        self.assertTrue(len(multiprocessing_list) == 100, "All items present, for a single worker should be 100 items")

    def test_multiprocessing_list_works_as_expected_with_multiple_workers(self):

        workers = []
        manager = Manager()
        multiprocessing_list = manager.list()

        for i in range(15):
            workers.append(Process(target=self.do_some_work, args=(multiprocessing_list, )))

        for worker in workers:
            worker.start()
            worker.join()  # Needed to force wait all workers to finish

        self.assertTrue(len(multiprocessing_list) == 1500)

    @staticmethod
    def do_some_work(shared_list: list):
        for i in range(100):
            print(i)
            shared_list.append(i)



