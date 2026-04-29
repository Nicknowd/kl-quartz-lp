"""Script to fix landing.html for local serving via FastAPI."""
import re

with open('templates/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix internal anchor links (from iframe context)
content = content.replace('about:srcdoc#', '#')

# 2. Fix the main form action to our FastAPI endpoint
old_form_action = 'action="https://app.unbouncepreview.com/2779081/variants/272136631/preview?token=5bd8a82c877d925bcdbebde14e598aac84c4e51a7f2fc109429b2c264df907b3&amp;token_time=1777475509"'
content = content.replace(old_form_action, 'action="/submit"')

# 3. Fix WhatsApp form action
old_whats_action = 'action="https://app.unbouncepreview.com/2779081/variants/272136631/POST"'
content = content.replace(old_whats_action, 'action="#"')

# 4. Remove blob CSS references (they won't load locally)
content = re.sub(r'<link type="text/css" rel="stylesheet" href="blob:[^"]+?">', '', content)

# 5. Remove the backdrop div from Unbounce preview
content = content.replace('<div class="backdrop__3tG5Hl"></div>', '')

# 6. Remove the saved from url comment
content = content.replace('<!-- saved from url=(0012)about:srcdoc -->', '')

# 7. Fix the Unbounce form validation endpoint reference
old_form_url = '"url":"https://app.unbouncepreview.com/2779081/variants/272136631/preview?sub_page=form_confirmation&token=5bd8a82c877d925bcdbebde14e598aac84c4e51a7f2fc109429b2c264df907b3&token_time=1777475509"'
content = content.replace(old_form_url, '"url":"/submit"')

# 8. Fix the phone button href  
content = content.replace('href="tel:23124225"', 'href="tel:5123124225"')

# 9. Ensure fonts load from Google Fonts instead of Unbounce CDN
content = content.replace(
    'href="https://fonts.ub-assets.com/css?family=Montserrat:regular,300,700,800,500,900"',
    'href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700;800;900&display=swap"'
)

with open('templates/landing.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! All fixes applied to templates/landing.html")
