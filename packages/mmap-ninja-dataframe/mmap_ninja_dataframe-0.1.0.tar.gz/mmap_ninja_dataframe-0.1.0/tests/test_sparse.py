from dnn_cool_synthetic_dataset.base import create_dataset

from mmap_ninja_dataframe.sparse import SparseDataFrameMmap


def test_sparse_creation(tmp_path):
    dicts = create_dataset(10_000)
    sparse_mmap = SparseDataFrameMmap.from_list_of_dicts(
        out_dir=tmp_path / 'sparse',
        dicts=dicts
    )
    assert len(sparse_mmap) == 10_000
    assert sparse_mmap[0].keys() == dicts[0].keys()


def test_sparse_creation_from_a_generator(tmp_path):
    dicts = create_dataset(10_000)
    sparse_mmap: SparseDataFrameMmap = SparseDataFrameMmap.from_generator(
        out_dir=tmp_path / 'sparse',
        sample_generator=dicts,
        batch_size=64,
        verbose=True
    )
    assert len(sparse_mmap) == 10_000
    assert sparse_mmap[0].keys() == dicts[0].keys()
    assert sparse_mmap[-1].keys() == dicts[-1].keys()

    sparse_mmap.append(dicts[5])
    assert sparse_mmap[-1].keys() == dicts[5].keys()
    assert '_positions' not in sparse_mmap.get_columns()
