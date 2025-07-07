import os
import tempfile
import pytest
import sqlite3
from server.repositories.news_repository import NewsRepository

DB_SCHEMA = '''
CREATE TABLE news_articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0,
    is_hidden INTEGER DEFAULT 0,
    published_at TEXT
);
CREATE TABLE article_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    reported_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

@pytest.fixture(scope="function")
def temp_db(monkeypatch):
    # Create a temporary SQLite DB
    db_fd, db_path = tempfile.mkstemp()
    conn = sqlite3.connect(db_path)
    conn.executescript(DB_SCHEMA)
    conn.commit()
    monkeypatch.setattr('server.repositories.base_repository.DB_PATH', db_path)
    yield db_path
    conn.close()
    os.close(db_fd)
    os.remove(db_path)

def test_like_dislike_mutual_exclusive(temp_db):
    repo = NewsRepository()
    # Insert a dummy article
    repo.execute("INSERT INTO news_articles (title, content) VALUES (?, ?)", ("Test Article", "Test Content"))
    article_id = repo.fetchone("SELECT article_id FROM news_articles WHERE title=?", ("Test Article",))[0]
    # Like the article
    repo.increment_like(article_id)
    row = repo.fetchone("SELECT likes, dislikes FROM news_articles WHERE article_id=?", (article_id,))
    assert row[0] == 1 and row[1] == 0
    # Dislike the article (should decrease likes)
    repo.increment_dislike(article_id)
    row = repo.fetchone("SELECT likes, dislikes FROM news_articles WHERE article_id=?", (article_id,))
    assert row[0] == 0 and row[1] == 1
    # Like again (should decrease dislikes)
    repo.increment_like(article_id)
    row = repo.fetchone("SELECT likes, dislikes FROM news_articles WHERE article_id=?", (article_id,))
    assert row[0] == 1 and row[1] == 0

def test_report_and_hide(temp_db):
    repo = NewsRepository()
    repo.execute("INSERT INTO news_articles (title, content) VALUES (?, ?)", ("Report Me", "Content"))
    article_id = repo.fetchone("SELECT article_id FROM news_articles WHERE title=?", ("Report Me",))[0]
    # Report 3 times
    for _ in range(3):
        repo.add_report(article_id)
    row = repo.fetchone("SELECT is_hidden FROM news_articles WHERE article_id=?", (article_id,))
    assert row[0] == 1  # Article should be hidden after 3 reports

def test_delete_article(temp_db):
    repo = NewsRepository()
    repo.execute("INSERT INTO news_articles (title, content) VALUES (?, ?)", ("Delete Me", "Content"))
    article_id = repo.fetchone("SELECT article_id FROM news_articles WHERE title=?", ("Delete Me",))[0]
    repo.delete_article(article_id)
    row = repo.fetchone("SELECT * FROM news_articles WHERE article_id=?", (article_id,))
    assert row is None 