import io

from visualizer.utils import csv_parser


def test_auto_read_csv():
    csv_content = "a,b,c\n1,2,3\n4,5,6"
    file_obj = io.StringIO(csv_content)
    df = csv_parser.auto_read_csv(file_obj)
    assert list(df.columns) == ["a", "b", "c"]
    assert df.shape == (2, 3)
