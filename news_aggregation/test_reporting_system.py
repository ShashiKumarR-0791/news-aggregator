#!/usr/bin/env python3
"""
Test script for the enhanced article reporting system
This script demonstrates the new features:
- Configurable thresholds
- Automatic hiding and removal
- Detailed admin controls
- Better user feedback
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_login(username, password):
    """Login and get session token"""
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("token")
        else:
            print(f" Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f" Login error: {e}")
        return None

def get_headers(token):
    """Get headers with authentication token"""
    return {"Authorization": f"Bearer {token}"}

def test_report_article(article_id, token):
    """Test reporting an article"""
    try:
        headers = get_headers(token)
        response = requests.post(f"{BASE_URL}/news/report", 
                               json={"article_id": article_id}, 
                               headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f" Article {article_id} reported successfully")
            print(f"   Message: {result.get('message')}")
            print(f"   Report count: {result.get('report_count')}")
            print(f"   Status: {result.get('status', 'reported')}")
            return result
        else:
            print(f" Failed to report article: {response.json()}")
            return None
    except Exception as e:
        print(f" Error reporting article: {e}")
        return None

def test_get_reported_articles(token):
    """Test getting reported articles (admin only)"""
    try:
        headers = get_headers(token)
        response = requests.get(f"{BASE_URL}/admin/reported-articles", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            thresholds = data.get("thresholds", {})
            
            print(f"\n📊 Reported Articles (Admin View)")
            print(f" Thresholds: Hide at {thresholds.get('hide_threshold')}, Remove at {thresholds.get('remove_threshold')}")
            print(f" Found {len(articles)} reported articles")
            
            for article in articles:
                print(f"\n🆔 Article ID: {article['article_id']}")
                print(f"📰 Title: {article['title'][:60]}...")
                print(f"📊 Reports: {article['report_count']}")
                print(f"🚫 Hidden: {bool(article['is_hidden'])}")
            
            return articles
        else:
            print(f" Failed to get reported articles: {response.json()}")
            return []
    except Exception as e:
        print(f" Error getting reported articles: {e}")
        return []

def test_get_article_reports(article_id, token):
    """Test getting detailed reports for an article (admin only)"""
    try:
        headers = get_headers(token)
        response = requests.get(f"{BASE_URL}/admin/article-reports", 
                              params={"article_id": article_id}, 
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            reports = data.get("reports", [])
            
            print(f"\n Detailed Reports for Article {article_id}")
            print(f"📊 Found {len(reports)} reports")
            
            for report in reports:
                print(f"   🆔 Report ID: {report['report_id']}")
                username = report.get("username", f"User {report['user_id']}")
                print(f"   👤 User: {username}")
                print(f"    Reported: {report['reported_at']}")
            
            return reports
        else:
            print(f" Failed to get article reports: {response.json()}")
            return []
    except Exception as e:
        print(f" Error getting article reports: {e}")
        return []


def test_update_thresholds(token):
    """Test updating report thresholds (admin only)"""
    try:
        headers = get_headers(token)
        new_thresholds = {
            "hide_threshold": 2,
            "remove_threshold": 5
        }
        
        response = requests.put(f"{BASE_URL}/admin/update-report-thresholds", 
                              json=new_thresholds, 
                              headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f" Thresholds updated successfully")
            print(f"   Message: {result.get('message')}")
            print(f"   New thresholds: {result.get('current_thresholds')}")
            return True
        else:
            print(f" Failed to update thresholds: {response.json()}")
            return False
    except Exception as e:
        print(f" Error updating thresholds: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Enhanced Article Reporting System")
    print("=" * 50)
    
    # Test with admin user
    print("\n1. Testing with admin user...")
    admin_token = test_login("admin", "admin123")
    if not admin_token:
        print(" Cannot proceed without admin login")
        return
    
    # Test updating thresholds
    print("\n2. Testing threshold updates...")
    test_update_thresholds(admin_token)
    
    # Test getting reported articles
    print("\n3. Testing reported articles view...")
    reported_articles = test_get_reported_articles(admin_token)
    
    # Test detailed reports if there are any reported articles
    if reported_articles:
        article_id = reported_articles[0]['article_id']
        print(f"\n4. Testing detailed reports for article {article_id}...")
        test_get_article_reports(article_id, admin_token)
    
    # Test with regular user
    print("\n5. Testing with regular user...")
    user_token = test_login("user", "user123")
    if user_token:
        # Test reporting an article (you'll need to provide a valid article ID)
        test_article_id = 1  # Change this to a valid article ID
        print(f"\n6. Testing article reporting for article {test_article_id}...")
        test_report_article(test_article_id, user_token)
    
    print("\n Testing completed!")

if __name__ == "__main__":
    main() 