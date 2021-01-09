import datetime
import os
import re
import requests
import hashlib
import shutil
import sys

from slugify import slugify

from notion.client import NotionClient
from PIL import Image

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_USER_ID = os.getenv('NOTION_USER_ID')
NOTION_ROOT_PAGE_ID = os.getenv('NOTION_ROOT_PAGE_ID')

if NOTION_TOKEN is None:
    sys.exit("The NOTION_TOKEN is missing, see the readme on how to set it.")
if NOTION_ROOT_PAGE_ID is None:
    sys.exit(
        "The NOTION_ROOT_PAGE_ID is missing, see the readme on how to set it."
    )

client = NotionClient(token_v2=NOTION_TOKEN)
root_page_id = NOTION_ROOT_PAGE_ID

dest_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'content', 'blog')
)

markdown_pages = {}
regex_meta = re.compile(r'^== *(\w+) *:* (.+) *$')
ignore_root = True


def download_file(file_url, destination_folder, block_id=None):
    if file_url is None:
        print('Input file is wrong')
        return

    if block_id is not None:
        if 'X-Amz-Algorithm' in file_url:
            pass
        elif 'amazonaws' in file_url:
            file_url = (
                'https://www.notion.so/image/'
                + file_url.replace('://', '%3A%2F%2F').replace('/', '%2F')
                + f'?table=block&id={block_id}&userId={NOTION_USER_ID}&cache=v2'
            )
        elif '/images/page-cover' in file_url:
            file_url = (
                'https://www.notion.so/image/https%3A%2F%2Fwww.notion.so'
                + file_url.replace('/', '%2F')
                + f'?table=block&id={block_id}&userId={NOTION_USER_ID}&cache=v2'
            )

    r = requests.get(file_url, stream=True)
    # converts response headers mime type to an extension (may not work with everything)
    ext = r.headers['content-type'].split('/')[-1]

    tmp_file_name = f'tmp.{ext}'
    tmp_file_path = os.path.join(destination_folder, tmp_file_name)

    print(f"-> Downloading {file_url}")

    h = hashlib.sha1()
    # open the file to write as binary - replace 'wb' with 'w' for text files
    with open(tmp_file_path, 'wb') as f:
        # iterate on stream using 1KB packets
        for chunk in r.iter_content(1024):
            f.write(chunk)  # write the file
            h.update(chunk)

    final_file_name = f'{h.hexdigest()}.{ext}'
    final_file_path = os.path.join(destination_folder, final_file_name)

    os.rename(tmp_file_path, final_file_path)

    if ext == 'x-icon':
        img = Image.open(final_file_path)
        final_file_name = final_file_name.replace('x-icon', 'png')
        img.save(os.path.join(destination_folder, final_file_name))
        img.close()
        os.remove(final_file_path)

    return final_file_name


def process_block(block, text_prefix=''):
    was_list = False
    text = ''
    metas = []
    number = 1

    for content in block.children:
        # Close the bulleted list.
        if was_list:
            if content.type not in ['bulleted_list', 'numbered_list', 'to_do']:
                text = text + '\n'
                was_list = False
                number = 1

        if content.type == 'header':
            text = text + f'# {content.title}\n\n'
        elif content.type == 'sub_header':
            text = text + f'## {content.title}\n\n'
        elif content.type == 'sub_sub_header':
            text = text + f'### {content.title}\n\n'
        elif content.type == 'code':
            text = text + f'```{content.language}\n{content.title}\n```\n\n'
        elif content.type == 'image':
            block_id = content.id
            image_name = download_file(content.source, dest_path, block_id)
            text = text + text_prefix + f'![{image_name}]({image_name})\n\n'
        elif content.type == 'bulleted_list':
            text = text + text_prefix + f'* {content.title}\n'
            was_list = True
        elif content.type == 'numbered_list':
            text = text + text_prefix + f'{number}. {content.title}\n'
            was_list = True
            number += 1
        elif content.type == 'to_do':
            if content.checked:
                text = text + text_prefix + f'- [X] {content.title}\n'
            else:
                text = text + text_prefix + f'- [ ] {content.title}\n'
            was_list = True
        elif content.type == 'divider':
            text = text + f'---\n'
        elif content.type == 'text':
            matchMeta = regex_meta.match(content.title)
            if matchMeta:
                key = matchMeta.group(1)
                value = matchMeta.group(2)
                metas.append(f"{key}: '{value}'")
            else:
                text = text + text_prefix + f'{content.title}\n\n'
        elif content.type == 'table_of_contents':
            text = text# + 'toc\n'
        elif content.type == 'quote':
            text = text + f'> {content.title}\n'
        elif content.type == 'video':
            text = text + f'`video: {content.source}`\n\n'
        elif content.type == 'page':
            subpage_slug = to_markdown(content.id, ignore=False)
            text = text + f'[{content.title}](/blog/{subpage_slug})\n\n'
        elif content.type == 'bookmark':
            thumbnail = download_file(content.bookmark_cover, dest_path)
            icon = (
                download_file(content.bookmark_icon, dest_path)
                if content.bookmark_icon is not None
                else None
            )
            link = content.link

            text = (
                text
                + f"""
<div class="bookmark">
    <div>
        <div style="display: flex;"><a target="_blank" rel="noopener noreferrer" href="{link}"
                style="display: block; color: inherit; text-decoration: none; flex-grow: 1; min-width: 0px;">
                <div class="" role="button" tabindex="0"
                    style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; width: 100%; display: flex; flex-wrap: wrap-reverse; align-items: stretch; text-align: left; overflow: hidden; border: 1px solid; border-radius: 3px; position: relative; color: inherit; fill: inherit;">
                    <div style="flex: 4 1 180px; padding: 12px 14px 14px; overflow: hidden; text-align: left;">
                        <div
                            style="font-size: 14px; line-height: 20px; color: inherit; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-height: 24px; margin-bottom: 2px;">
                            {content.title}</div>
                        <div style="display: flex; margin-top: 6px;"><img src="{icon}"
                                style="width: 16px; height: 16px; min-width: 16px; margin-right: 6px;">
                            <div
                                style="font-size: 12px; line-height: 16px; color: inherit; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                {link}</div>
                        </div>
                    </div>
                    <div style="flex: 1 1 180px; display: block; position: relative;">
                        <div style="position: absolute; inset: 0px;">
                            <div style="width: 100%; height: 100%;"><img src="{thumbnail}"
                                    style="display: block; object-fit: cover; border-radius: 1px; width: 100%; height: 100%;">
                            </div>
                        </div>
                    </div>
                </div>
            </a></div>
    </div>
</div>\n
"""
            )

        else:
            print("Unsupported type: " + content.type)

        if len(content.children) and content.type != 'page':
            child_text, child_metas = process_block(content, '  ')
            text = text + child_text
            metas = metas + child_metas

    return text, metas


def to_markdown(page_id, ignore):
    page = client.get_block(page_id)
    page_title = page.title
    slug = slugify(page_title)
    text = ''
    metas = []

    # Handle Frontmatter
    metas.append(f"title: '{page_title}'")

    # Download the cover and add it to the frontmatter.
    page_cover_url = page.get("format.page_cover")
    block_id = page.id
    cover_image_name = download_file(page_cover_url, dest_path, block_id)
    metas.append(f"featured: {cover_image_name}")

    text, child_metas = process_block(page)

    metas = metas + child_metas

    if 'date' not in metas:
        date_raw = requests.head(f'https://www.notion.so/{page_id}').headers[
            'last-modified'
        ]
        date = datetime.datetime.strptime(date_raw, "%a, %d %b %Y %H:%M:%S GMT")
        datestring = datetime.datetime.strftime(date, "%Y-%m-%d")
        metas.append(f"date: '{datestring}'")

    if 'description' not in metas:
        description = text[:100].replace('\n', '')
        metas.append(f"description: '{description}'")

    metaText = '---\n' + '\n'.join(metas) + '\n---\n'
    text = metaText + text

    # Save the page data if it is not the root page.
    if not ignore:
        markdown_pages[slug] = text

    return slug


if __name__ == "__main__":
    print(f'-> Cleaning the "{dest_path}" folder')
    try:
        shutil.rmtree(dest_path)
    except:
        pass
    os.mkdir(dest_path)

    to_markdown(root_page_id, ignore=ignore_root)

    for slug, markdown in markdown_pages.items():
        file_name = slug + '.md'
        file_path = os.path.join(dest_path, file_name)

        file = open(file_path, 'w', -1, 'utf-8')
        file.write(markdown)
        file.close()
        print('-> Imported "' + file_name + '"')

    print('Done: imported ' + str(len(markdown_pages)) + ' pages.')
