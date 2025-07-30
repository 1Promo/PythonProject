def test_empty_transactions(empty_transactions):
    assert len(empty_transactions) == 0


def test_basic_transactions(basic_transactions):
    assert len(basic_transactions) == 4
    for tx in basic_transactions:
        assert "type" in tx
        assert "from_type" in tx
        assert "to_type" in tx


def test_unknown_type(unknown_type_transactions):
    assert len(unknown_type_transactions) == 1
    tx = unknown_type_transactions[0]
    assert tx["type"] == "unknown"
