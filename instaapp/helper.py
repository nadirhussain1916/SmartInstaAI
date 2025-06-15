from playwright.sync_api import sync_playwright
from threading import Thread
from .models import Instagram_User,InstagramPost
import requests
import datetime
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async
from django.core.management import call_command

def check_instagram_credentials(username, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Headless = True for no browser UI
            context = browser.new_context()
            page = context.new_page()

            # 1. Go to Instagram login page
            page.goto("https://www.instagram.com/accounts/login/")
            page.wait_for_timeout(3000)

            # 2. Fill login credentials
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # 3. Click login button
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            error_div_selector = 'div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x11gldyt.xyorhqc.x11hdunq.x2b8uid'

            if page.locator(error_div_selector).is_visible():
                error_text = page.locator(error_div_selector).inner_text()
                if 'incorrect' in error_text.lower():
                    return {"status": "error", "message": "Sorry, your password was incorrect. Please double-check your password."}
                else:
                    return {"status": "error", "message": error_text}
                        # ✅ Launch background thread (doesn't block response)

            # If no error div is visible, assume login success
            return {"status": "success", "message": "Login successful"}
            
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
        

def fetch_instagram_data(username,password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Headless = True for no browser UI
            context = browser.new_context()
            page = context.new_page()

            # 1. Go to Instagram login page
            page.goto("https://www.instagram.com/accounts/login/")
            page.wait_for_timeout(3000)

            # 2. Fill login credentials
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # 3. Click login button
            page.click('button[type="submit"]')
            page.wait_for_timeout(6000)

            # Wait for login to complete (check for redirect or profile icon)
            page.wait_for_timeout(7000)

            # Step 2: Go to target user profile
            page.goto(f"https://www.instagram.com/{username}/")
            # container = page.locator('div.x1iyjqo2.xh8yej3')
            # # 2. Find all child divs inside this container
            # child_divs = container.locator('div')

            # # 3. Loop through them and click those that contain a span with the desired text
            # count = child_divs.count()

            # for i in range(count):
            #     div = child_divs.nth(i)
            #     try:
            #         # Check if this div contains the target span
            #         span = div.locator('span.x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft')
            #         if span.is_visible() and span.inner_text().strip().lower() == 'profile':
            #             div.click()
            #             break  # click only the first matching one, or remove break to click all
            #     except:
            #         continue
                
            # Step 2: Go to target user profile
            page.wait_for_selector('header.xrvj5dj', timeout=10000)

            # Step 3: Get profile image from inside specific section
            try:
                profile_section = page.locator('section.x6s0dn4')
                profile_img = profile_section.locator('button[title="Change profile photo"] img').first.get_attribute("src")
            except:
                profile_img = "Not found"

            # Step 4: Get posts, followers, following counts
            try:
                stats_section = page.locator('section.xc3tme8 ul li')
                post_count = stats_section.nth(0).inner_text().split()[0]
                followers = stats_section.nth(1).inner_text().split()[0]
                following = stats_section.nth(2).inner_text().split()[0]
            except:
                post_count = followers = following = "N/A"

            # Step 5: Get full name from specific section
            try:
                full_name_section = page.locator('section.xc3tme8.x1vnunu7')
                full_name = full_name_section.locator('h1, h2, span').first.inner_text()
            except:
                full_name = "Not found"
            
                # Step 6: Click post section to reveal posts
            try:
                outer_div = page.locator('div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl').first
                inner_clickable = outer_div.locator('div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x78zum5.x124el2t.x1q0q8m5.x1co6499.x17zd0t2').first
                click_target = inner_clickable.locator('div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x6s0dn4.x78zum5.x1r8uery.x1iyjqo2.xs83m0k.xl56j7k').first
                click_target.click()
                page.wait_for_timeout(2000)
            except Exception as e:
                print(f"Click post section failed: {e}")

            # Step 7: Extract post links
            post_links = []
            try:
                post_grid = page.locator('div.xg7h5cd.x1n2onr6')
                posts = post_grid.locator('div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x14z9mp.xzj7kzq.xbipx2v.x1j53mea')
                count = posts.count()
                for i in range(count):
                    href = posts.nth(i).locator('a').get_attribute("href")
                    if href:
                        post_links.append("https://www.instagram.com" + href)
            except Exception as e:
                print(f"Fetching post links failed: {e}")
            browser.close
            return {
                "status": "success",
                "full_name": full_name,
                "profile_image": profile_img,
                "post_count": post_count,
                "followers": followers,
                "following": following,
                "post_links": post_links,
            }

    except Exception as e:
        print(f"❌ Error saving IG data: {e}")

def save_user_and_posts(username,password, full_name, followers, post_count, profile_img, post_links):
    user_obj, created = Instagram_User.objects.get_or_create(username=username)
    user_obj.full_name = full_name
    user_obj.followers = followers
    user_obj.posts = post_count
    user_obj.password = password

    if profile_img:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        img_response = requests.get(profile_img)
        if img_response.status_code == 200:
            file_name = f"{username}_profile_{timestamp}.jpg"
            user_obj.profile_pic.save(file_name, ContentFile(img_response.content), save=False)

    user_obj.save()

    InstagramPost.objects.filter(user=user_obj).delete()
    InstagramPost.objects.bulk_create([
        InstagramPost(user=user_obj, post_url=link) for link in post_links
    ])
    print(f"\n✅ IG data saved for: {username}")
