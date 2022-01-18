import pytest
from app.calculations import BankAccount, InsufficientFunds, add, multiply, divide, substract


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("a,b,result", [
    (3, 2, 5), (7, 1, 8), (12, 4, 16)
])
def test_add(a, b, result):
    assert add(a, b) == result


def test_substract():
    assert substract(5, 3) == 2


def test_multiply():
    assert multiply(5, 3) == 15


def test_divide():
    assert divide(6, 3) == 2


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100


def test_collect_interst(bank_account):
    bank_account.collect_interest()

    assert bank_account.balance == 50*1.1


@pytest.mark.parametrize("deposited,withdraw,expected", [
    (200, 100, 100), 
    (50, 10, 40), 
    (1200, 400, 800),
])
def test_bank_transaction(zero_bank_account: BankAccount, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account: BankAccount):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
    