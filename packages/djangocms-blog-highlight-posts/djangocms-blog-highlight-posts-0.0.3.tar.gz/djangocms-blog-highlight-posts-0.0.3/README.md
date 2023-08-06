A djangocms-blog extension allowing to mark some posts as highlight and sort queryset to display them first on the posts list

----

## Install

* Install the package
    ```bash
    python3 -m pip install djangocms-blog-highlight-posts
    ```

* Add it in your `INSTALLED_APPS`:
    ```python

        "djangocms_blog_highlight_posts",
    ```

* Override blog url conf (in project settings):
    ```python

        BLOG_URLCONF = "djangocms_blog_highlight_posts.urls"
    ```

* Run the migration:
    ```sh
    python3 manage.py migrate djangocms_blog_highlight_posts
    ```


