from typing import List
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostResponse(**post)

    post_map = map(validate, res.json())
    posts_list = list(post_map)
    posts_list.sort(key=lambda x: x.Post.id)

    assert posts_list[0].Post.id == test_posts[0].id
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/999')
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
                         ("Title 1", "Content 1", True),
                         ("Title 2", "Content 2", False),
                         ("Title 1", "Content 1", True), ])
def test_create_post(authorized_client, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    
def test_create_post_default_published_true(authorized_client):
    res = authorized_client.post("/posts/", json={
        "title": "title",
        "content": "content"
    })

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True


def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={
        "title": "title",
        "content": "content"
    })

    assert res.status_code == 401

def test_unauthorazide_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code ==401
    
    
def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_post_non_exists(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/9999")
    assert res.status_code == 404


def test_delete_other_user_posts(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_posts):
    data = {
        "title" : "updated title",
        "content" : "update content",
        "published" : True
    }
    res =  authorized_client.put(f"/posts/{test_posts[0].id}",json = data)
    updated_post = schemas.Post(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == "updated title"
    
def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title" : "updated title",
        "content" : "update content",
        "published" : True
    }
    res =  authorized_client.put(f"/posts/{test_posts[3].id}",json = data)
    assert res.status_code == 403
    

def test_update_post_not_exists(authorized_client, test_posts):
    data = {
        "title" : "updated title",
        "content" : "update content",
        "published" : True
    }
    res =  authorized_client.put(f"/posts/999999",json = data)
    
    assert res.status_code == 404