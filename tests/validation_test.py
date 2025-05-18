import pytest

from api.models.schemas.target_schema import TargetCreate
from api.models.schemas.task_schema import TaskCreate
from api.models.schemas.user_schema import UserCreate

def test_task_create_validation():
    task = TaskCreate(name="Valid", deadline=10, is_done=False)
    assert task.name == "Valid"
    assert task.deadline == 10
    assert task.is_done == False

    with pytest.raises(ValueError):
        TaskCreate(name="Valid", deadline=0, is_done=False) #deadline <=0

    with pytest.raises(ValueError):
        TaskCreate(name="", deadline=1, is_done=False) #name != empty

def test_target_create_validation():
    target = TargetCreate(name="Valid", deadline=10, is_done=False)
    assert target.name == "Valid"
    assert target.deadline == 10
    assert target.is_done == False

    with pytest.raises(ValueError):
        TargetCreate(name="", deadline=1, is_done=False) #name != empty
    
    with pytest.raises(ValueError):
        TargetCreate(name="Valid", deadline=0, is_done=False) #deadline <=0

def test_user_create_validation():
    with pytest.raises(ValueError):
        UserCreate(username="", email="", password="") #empty

    with pytest.raises(ValueError):
        UserCreate(username="turtle123", email="turtle@example.com", password="turtle123") #login!=password

    with pytest.raises(ValueError):
        UserCreate(username="turtle", email="turtle", password="turtle123") #email must be email

    with pytest.raises(ValueError):
        UserCreate(username="turtle", email="turtle@example.com", password="turt") #email must be email
    
    user = UserCreate(username="turtle", email="super@yandex.ru", password="danikdanik")
    assert user.username == "turtle" and user.email == "super@yandex.ru" and user.password == "danikdanik" #default

    