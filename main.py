
import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown


# create empty dictionary to store our posts
blog_posts = {}

# iterate through each post in our content folder (markdown files)
for markdown_post in os.listdir('content'):
    # set file path
    path = os.path.join('content', markdown_post)

    with open(path, 'r') as file:
        blog_posts[markdown_post] = markdown(file.read(), extras=['metadata'])


# sorts our blog posts in order chronologically
blog_posts = {
    post: blog_posts[post] for post in sorted(blog_posts, key=lambda post: datetime.strptime(blog_posts[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

# create templates to render our md
env = Environment(loader=PackageLoader('main', 'templates'))
home_template = env.get_template('home.html')
post_template = env.get_template('post.html')

posts_metadata = [blog_posts[post].metadata for post in blog_posts]
tags = [post['tags'] for post in posts_metadata]
home_html = home_template.render(posts=posts_metadata, tags=tags)

# write our content as a file
with open('output/home.html', 'w') as file:
    file.write(home_html)

for post in blog_posts:
    post_metadata = blog_posts[post].metadata

    post_data = {
        'content': blog_posts[post],
        'title': post_metadata['title'],
        'date': post_metadata['date']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)

