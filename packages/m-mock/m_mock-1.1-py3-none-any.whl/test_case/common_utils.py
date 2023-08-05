from src.m_mock import m_mock


def execute(params):
    print(f'm_mock.m_mock("{params}"):{m_mock.mocker(params)}')


def execute_ran(params):
    print(f'm_mock.m_mock("{params}"):{m_mock.mocker(params)}')
