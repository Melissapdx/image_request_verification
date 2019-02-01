import unittest
import verify_uploaded


class UploadedTest(unittest.TestCase):
    """
    test all functions in verify uploaded
    """

    def setUp(self):
        pass

    def tearDown(self):
        print("teardown module")

    def test_user_input(self):
        self.assertEqual(get_user_input(P92308_ECM_SY_Responsive_Store_Merch_updates_for_09_12_ASSET_09_05_2018),
           "Y:/RWC/Melissa/Projects/Promos/P92308_ECM_SY_Responsive_Store_Merch_updates_for_09_12_ASSET_09_05_2018/final")


if __name__ == '__main__':
    unittest.main()
