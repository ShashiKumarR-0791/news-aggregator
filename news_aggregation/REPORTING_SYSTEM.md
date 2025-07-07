# Enhanced Article Reporting System

## Overview

The enhanced article reporting system provides a robust mechanism for users to report inappropriate content and for administrators to manage reported articles with configurable thresholds and automatic actions.

## Features

###  Configurable Thresholds
- **Hide Threshold**: Articles are automatically hidden when they reach a certain number of reports (default: 3)
- **Remove Threshold**: Articles are permanently removed when they reach a higher number of reports (default: 10)
- **Dynamic Updates**: Admins can update thresholds in real-time

### 🚫 Automatic Actions
- **Automatic Hiding**: Articles are hidden from public view when they reach the hide threshold
- **Automatic Removal**: Articles are permanently deleted when they reach the remove threshold
- **Cascade Cleanup**: When articles are removed, all related data (saved articles, reports) is also cleaned up

### 👥 User Features
- **One Report Per User**: Users can only report an article once
- **Immediate Feedback**: Users receive detailed feedback about their report
- **Status Updates**: Users are informed when articles are hidden or removed

### 🔍 Admin Features
- **Comprehensive Dashboard**: View all reported articles with detailed information
- **Detailed Reports**: See who reported each article and when
- **Flexible Management**: Unhide articles, clear reports, or remove individual reports
- **Threshold Management**: Update hide and remove thresholds dynamically

## Configuration

### Settings (`server/config/settings.py`)

```python
# Article Reporting Configuration
ARTICLE_REPORT_THRESHOLD = 3  # Number of reports before article is hidden
ARTICLE_AUTO_REMOVE_THRESHOLD = 10  # Number of reports before article is permanently removed
ARTICLE_REPORT_ENABLED = True  # Enable/disable article reporting
ARTICLE_AUTO_REMOVE_ENABLED = True  # Enable/disable automatic removal
```

## API Endpoints

### User Endpoints

#### Report Article
```
POST /news/report
Content-Type: application/json
Authorization: Bearer <token>

{
    "article_id": 123
}

Response:
{
    "message": "Article reported successfully. Total reports: 2",
    "report_count": 2,
    "status": "reported"
}
```

### Admin Endpoints

#### Get Reported Articles
```
GET /admin/reported-articles
Authorization: Bearer <admin_token>

Response:
{
    "articles": [
        {
            "article_id": 123,
            "title": "Article Title",
            "source": "News Source",
            "published_at": "2024-01-01T00:00:00",
            "is_hidden": true,
            "report_count": 5,
            "reporting_users": "1,2,3,4,5"
        }
    ],
    "thresholds": {
        "hide_threshold": 3,
        "remove_threshold": 10
    }
}
```

#### Get Article Reports
```
GET /admin/article-reports?article_id=123
Authorization: Bearer <admin_token>

Response:
{
    "reports": [
        {
            "report_id": 1,
            "user_id": 1,
            "reported_at": "2024-01-01T10:00:00",
            "username": "user1"
        }
    ]
}
```

#### Remove Individual Report
```
DELETE /admin/remove-report
Authorization: Bearer <admin_token>

{
    "report_id": 1,
    "user_id": 1
}
```

#### Clear All Reports for Article
```
DELETE /admin/clear-article-reports
Authorization: Bearer <admin_token>

{
    "article_id": 123
}
```

#### Update Thresholds
```
PUT /admin/update-report-thresholds
Authorization: Bearer <admin_token>

{
    "hide_threshold": 2,
    "remove_threshold": 5
}
```

#### Unhide Article
```
POST /admin/unhide-article
Authorization: Bearer <admin_token>

{
    "article_id": 123
}
```

## Database Schema

### Article Reports Table
```sql
CREATE TABLE article_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reported_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(article_id) REFERENCES news_articles(article_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(article_id, user_id)
);
```

### News Articles Table (Enhanced)
```sql
ALTER TABLE news_articles ADD COLUMN is_hidden INTEGER DEFAULT 0;
```

## Usage Examples

### For Users

1. **Report an Article**
   ```python
   from client.api.news_api import report_article_by_id
   
   result = report_article_by_id(article_id)
   # Provides immediate feedback about the report
   ```

### For Administrators

1. **View Reported Articles**
   ```python
   from client.utils.report_article import view_reported_articles
   
   view_reported_articles()
   # Shows comprehensive dashboard with admin actions
   ```

2. **Update Thresholds**
   ```python
   # Via the admin interface or API
   # Changes take effect immediately
   ```

## Security Features

- **Role-based Access**: Only admins can access reporting management
- **Audit Logging**: All actions are logged for security purposes
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: Users can only report an article once

## Monitoring and Logging

The system provides comprehensive logging for:
- Article reports
- Automatic hiding/removal actions
- Admin actions
- Error conditions

Logs include:
- User IDs
- Article IDs
- Timestamps
- Action descriptions
- Error details

## Testing

Use the provided test script to verify functionality:

```bash
python test_reporting_system.py
```

This script tests:
- User reporting functionality
- Admin management features
- Threshold updates
- API responses

## Best Practices

1. **Regular Monitoring**: Check reported articles regularly
2. **Appropriate Thresholds**: Set thresholds based on your community size
3. **Backup Before Removal**: Consider backing up articles before permanent removal
4. **User Education**: Inform users about the reporting system
5. **Transparency**: Be transparent about how reports are handled

## Troubleshooting

### Common Issues

1. **Articles not hiding**: Check if `ARTICLE_REPORT_ENABLED` is True
2. **Reports not counting**: Verify user hasn't already reported the article
3. **Admin access denied**: Ensure user has 'admin' role
4. **Database errors**: Check foreign key constraints and table structure

### Debug Mode

Enable debug logging by setting the logging level to DEBUG in your configuration.

## Future Enhancements

Potential improvements:
- Report categories (spam, inappropriate, fake news, etc.)
- Report reasons and descriptions
- Automated content analysis
- Report analytics and trends
- Email notifications for admins
- Report appeal system 