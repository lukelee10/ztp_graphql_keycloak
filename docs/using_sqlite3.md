# How to use SQLite3 for development

Just add this to your `settings.py`:

```python
"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```