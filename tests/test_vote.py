from app import schemas
from jose import jwt
from app.config import settings
import pytest


##TODO test that an user can't vote on his post

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    
    assert res.status_code == 201
    
def test_vote_twice_on_post(authorized_client, test_posts):
    res1 = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    res2 = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    assert res1.status_code == 201
    assert res2.status_code == 409
    
def test_delete_vote(authorized_client, test_posts):
    res1 = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    res2 = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":0})
    
    assert res1.status_code == 201
    assert res2.status_code == 201
    
def test_delete_vote_not_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json= {"post_id": 99999, "dir":0})
    
    assert res.status_code == 404
    
def test_vote_post_not_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json= {"post_id": 99999, "dir":1})
    
    assert res.status_code == 404
    
def test_unauthorized_user_vote_on_post(client, test_posts):
    res = client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    
    assert res.status_code == 401