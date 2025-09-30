BLOG POST


Features

Public post list + detail
Authenticated create
Author-only edit/delete
Pagination (optional)
Endpoints (HTML)

GET /post/ → list
GET /post// → detail
GET /post/new/ → create form (login required)
POST /post/new/ → create (login required)
GET /post//edit/ → edit form (author only)
POST /post//edit/ → update (author only)
GET /post//delete/ → confirm delete (author only)
POST /post//delete/ → delete (author only)
Auth

/accounts/login/ (Django auth)
/accounts/logout/
Setup

pip install django
add blog to INSTALLED_APPS
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Django Blog Project
This is a Django-based blog application built as part of the Week 14 capstone project. It allows users to register, create/edit/delete posts, add comments, manage profiles, and use tagging and search features to organize and find content.

Features
User Authentication: Register, log in, log out, and manage profiles with bio and profile pictures.
Posts: Create, edit, delete, and view blog posts (authenticated users only for create/edit/delete).
Comments: Add, edit, delete comments on posts (authenticated users only).
Tagging: Add tags to posts for categorization, with autocomplete support.
Search: Search posts by title, content, or tags.
Tag Filtering: View posts filtered by specific tags.
Setup Instructions (Developers)
Prerequisites
Python 3.9+
Django 4.x
MySQL or SQLite database
Virtual environment recommended
Installation
Clone the repository:
git clone <repository-url>
cd django_blog

Create and activate a virtual environment:python -m venv .venv source .venv/bin/activate # On Windows: .venv\Scripts\activate

Install dependencies:pip install django django-taggit django-taggit-autosuggest

Configure settings.py: Add 'blog', 'taggit', 'taggit_autosuggest' to INSTALLED_APPS. Set up database (e.g., SQLite):DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3', } }

Configure static files:STATIC_URL = '/static/' STATICFILES_DIRS = [BASE_DIR / "static"] STATIC_ROOT = BASE_DIR / "staticfiles"

Run migrations:python manage.py makemigrations python manage.py migrate

Collect static files for tag autocomplete:python manage.py collectstatic

Create a superuser for admin access:python manage.py createsuperuser

Run the development server:python manage.py runserver

Project Structure

blog/models.py: Defines Post, Comment, Profile models, with TaggableManager for tags. blog/forms.py: Includes PostForm with TagField and TagAutoSuggest for tagging. blog/views.py: Contains views for posts, comments, search (SearchView), and tag filtering (TagView). blog/urls.py: Defines URLs like /api/search/, /api/tags/<tag_name>/. blog/templates/blog/: Templates for post list, detail, search results, tag filtering, etc.

Tagging Functionality How It Works

Model: Post.tags uses TaggableManager from django-taggit to manage tags. Storage: Tags are stored in taggit_tag and linked to posts via taggit_taggeditem. Form: PostForm uses TagField with TagAutoSuggest for comma-separated tag input with autocomplete. Display: Tags are shown in post_list.html, post_detail.html, search_results.html, and tag_posts.html with links to /api/tags/<tag_name>/. Filtering: TagView filters posts by tag (e.g., /api/tags/Django/).

Setup

Install django-taggit and django-taggit-autosuggest:pip install django-taggit django-taggit-autosuggest

Add to INSTALLED_APPS:INSTALLED_APPS = [ # ... 'taggit', 'taggit_autosuggest', ]

Run migrations:python manage.py makemigrations python manage.py migrate

Add URL for autocomplete:# blog/urls.py path('taggit_autosuggest/', include('taggit_autosuggest.urls')),

User Instructions

Adding Tags: Go to /api/posts/new/ or /api/posts//edit/ (requires login). In the tags field, type tags (e.g., “Django, Python”) or select suggestions (e.g., type “Dj” to see “Django”). Tags must be at least 2 characters long. Submit the form to save tags with the post.

Viewing Tags: Tags appear on post list (/api/), post detail (/api/posts//), search results (/api/search/), and tag pages (/api/tags/<tag_name>/). Example: “Tags: Django, Python”.

Filtering by Tags: Click a tag (e.g., “Django”) to visit /api/tags/Django/ and see all posts with that tag.

Search Functionality How It Works

View: SearchView uses Q objects to filter posts by title, content, or tags (case-insensitive). URL: /api/search/?q= (e.g., /api/search/?q=Django). Template: search_results.html shows matching posts with linked tags. Search Bar: Located in post_list.html or base.html (site-wide).

Setup

Add search URL:# blog/urls.py path('search/', SearchView.as_view(), name='search'),

Add search bar to templates:

Search
User Instructions

Searching Posts: Use the search bar on the homepage (/api/) or any page (if in base.html). Enter a keyword (e.g., “Django”). Press “Search” to see results at /api/search/?q=Django. Results match the keyword in post title, content, or tags. Example: Searching “Django” shows posts with “Django” in title, content, or tags.

Viewing Results: Results show post titles, authors, dates, content previews, and tags. Click tags to filter further (e.g., /api/tags/Django/). If no results, see “No posts found for ‘’”.

Testing

Tagging: Create a post with tags via /api/posts/new/ (e.g., “Django, Python”). Edit tags at /api/posts//edit/. Verify tags in shell:from blog.models import Post post = Post.objects.get(pk=1) print(post.tags.all()) # E.g., <QuerySet [<Tag: Django>, <Tag: Python>]>

Check tags display and link correctly in templates.

Search: Search for “Django” at /api/search/?q=Django. Verify results include posts with “Django” in title, content, or tags. Test empty or invalid queries.

Admin: Use /admin/taggit/tag/ to view/manage tags.

Troubleshooting

Tags Not Saving: Ensure django-taggit is in INSTALLED_APPS and migrations are applied. Autocomplete Not Working: Check taggit_autosuggest in INSTALLED_APPS, taggit_autosuggest.urls in urls.py, and {{ form.media }} in post_create.html. Search Not Working: Verify Q objects in SearchView and test queries in shell. Broken Links: Ensure path('tags/str:tag_name/', ...) in urls.py and {% url 'tag-posts' tag.name %} in templates.