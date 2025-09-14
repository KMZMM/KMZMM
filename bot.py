import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import json
import aiohttp
import asyncio
import threading

# ----------------- Bot Setup -----------------
BOT_TOKEN = "8011361961:AAGNU9RCAq3pcUDmKljgGnm7VXsta4P6dDY"

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# ----------------- API Config -----------------
HEADERS = {
    "user-agent": "Dart/3.7 (dart:io)",
    "accept-encoding": "gzip",
    "content-type": "application/json",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZWJjNDUzZS00ZTU5LTRiOGEtYjk0Ny0xMWUwNjUyN2NhZDUiLCJqdGkiOiI0NzdhMzUyYWMwOGVhYWNiMDNiNTNmYzhkY2FmMTQ4YmQ2MWMwNTZhMDcwY2Y2MzJmMWFhYzI5OTQ5MWNjMDE5YzIyZDk3YTQwNGFiOTE2YiIsImlhdCI6MTc1NzQ5OTIxNy40NjQwOTYsIm5iZiI6MTc1NzQ5OTIxNy40NjQxMDQsImV4cCI6MTc4OTAzNTIxNy40NTEyMjEsInN1YiI6IjE3MDkiLCJzY29wZXMiOltdfQ.fHLgsxcD-zvdxWF0tvlW2zZzrQvXTGrcrKkBf1_HkyWYEoKE_Vu13_nVt9BUJQhgeJyN5vj-9rPnWIJmOfjFDaxJODxHuQ3xxHvKi80GBDz7MypXRfMaH0QYcVYGYCnoesL0oOMOuya55NNWF2R5wqlxS7n5CjHHwqbgiV0HQ3qqZn1ifZasLDiS8dufflDDrQoCHj_gHOSg8IHgWQEprrBh-jgH83KdtZkhM7JdXudKF4K_JZycD9u7sCtMRbWqRYCqMiwWD91n2A8dpPgzChsMVB3nLBtCnsI-hRVptq9phunfDK13GtvPiKPTVwnLTWH5TpXgqqTPeYXGdbodbETsIo9AC6f02lWuczXOW2kjKHKXcOxAQnEN4J7unvnuI5Gm_zmbebTzmbOwH2HuanYsEJlmw7cUh52mek2DWBQFXSqg_iKt5DaiCSL8eM20fVDH3PNpgHhadolGgL0msSvdUscSUbLnpU2ekVJZcQwviLM0IkKXih7cPIXgQV2EuUUN09bR4mQvb7H2S3TFXwzs6QUpDv8F10vn0VBsFx9rRqkdT_y7b45XB8XcCYvCCEVkDa6rrx_W343xNQ4HLboVVQkn-wEKMXaNzpoKcdmOrU3sbT169ybt_U-nqAs_YY1MC-o1GknSBeU6nrWUjIb2cIyee8oGu_fkLdTB-gk"  # Replace with your token or GitHub secret
}

# ----------------- API Config -----------------
SEARCH_URL = "https://msubyoteshin.net/movie"
HEADERS = {
    "user-agent": "Dart/3.5 (dart:io)",
    "accept": "application/json",
    "access-code": ".:MfgYz?a!=W=HZP<ew('[-<thaimm2d",
    "accept-encoding": "gzip",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNlZjJjMjZhMzM3NmFhYWI4YTJiZDciLCJpc19iYW5uZWQiOmZhbHNlLCJzaG93X2FkdWx0Ijp0cnVlLCJwcmVtaXVtX2V4cGlyZV9kYXRlIjoiMjAyNi0wMS0wOFQxMjo0MTozOS4yODlaIiwibGFzdF9vbmxpbmVfZGF0ZSI6IjIwMjUtMDktMTBUMTM6MTQ6MjYuNTgwWiIsImF1dG9faW5jX2RhdGUiOjAsImRldmljZV9saW1pdCI6MiwicG9pbnQiOjEsInVzZXJfbmFtZSI6IktNWk1NIiwicGFzc3dvcmQiOiIkMmEkMTAkTjYxL0F6WTIxWmJjNUQ1OVp0YzN5T3NUdkhlczJ4SFQ1d2lyM1JtdkxEMi9mcURmZy5BZDIiLCJjcmVhdGVkQXQiOiIyMDI1LTA2LTAzVDEzOjA0OjAyLjgwNloiLCJ1cGRhdGVkQXQiOiIyMDI1LTA5LTEwVDEzOjE0OjI2Ljk5NVoiLCJfX3YiOjAsImlhdCI6MTc1NzUzNTY4OX0.GGhwLfZ-9-FjOtLI9kzSRf2zMFxKWJVpdNl8tAiEIl4",
    "host": "msubyoteshin.net",
    "content-type": "application/json"
}

# ----------------- API Functions -----------------

# ----------------- Async API Functions -----------------
import aiohttp
from bs4 import BeautifulSoup  # Make sure you have this installed via pip install beautifulsoup4
import aiohttp
import asyncio
import base64
import json

# ----------------- Async API Functions with SSL Decryption -----------------
async def search_movies(keyword, page=1):
    """Search movies using the new API endpoint with SSL decryption"""
    try:
        params = {
            "page": page,
            "limit": 20,
            "sort": "desc", 
            "search": keyword,
            "adult": "false"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(SEARCH_URL, headers=HEADERS, params=params, timeout=10) as response:
                response.raise_for_status()
                
                # Get the response as text (it's base64 encoded encrypted data)
                encrypted_base64 = await response.text()
                
                # Decrypt the base64 encoded data
                encrypted_data = base64.b64decode(encrypted_base64.strip())
                decrypted_data = decrypt_openssl_data(encrypted_data)
                decrypted_response = json.loads(decrypted_data.decode('utf-8'))
                
                # Return the decrypted list of movies
                return decrypted_response.get("data", [])
                
    except Exception as e:
        print(f"Error searching movies: {e}")
        return []
    
async def fetch_movie_sources(movie_id):
    """Return full movie specification with SSL decryption"""
    try:
        source_url = f"https://msubyoteshin.net/movie/{movie_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(source_url, headers=HEADERS, timeout=10) as response:
                response.raise_for_status()
                
                # Get the response as text (it's base64 encoded encrypted data)
                encrypted_base64 = await response.text()
                
                # Decrypt the base64 encoded data
                encrypted_data = base64.b64decode(encrypted_base64.strip())
                decrypted_data = decrypt_openssl_data(encrypted_data)
                
                # Handle encoding issues when decoding
                try:
                    response_data = json.loads(decrypted_data.decode('utf-8'))
                except UnicodeDecodeError:
                    # Try alternative encoding if UTF-8 fails
                    response_data = json.loads(decrypted_data.decode('latin-1'))
                
                # Extract the actual movie data from the response
                if response_data.get("status") and "data" in response_data:
                    movie_data = response_data["data"]
                    
                    # Safe printing - avoid Unicode issues
                    try:
                        title = movie_data.get('title', 'Unknown')
                        print(f"Successfully fetched: {title}")
                        print(f"Sources count: {len(movie_data.get('sources', []))}")
                    except UnicodeEncodeError:
                        print("Successfully fetched movie (title contains special characters)")
                        print(f"Sources count: {len(movie_data.get('sources', []))}")
                    
                    return movie_data
                else:
                    print(f"Invalid response format, status: {response_data.get('status')}")
                    return None
                
    except Exception as e:
        # Safe error message handling
        error_msg = f"Error fetching movie data: {str(e)}"
        try:
            print(error_msg)
        except UnicodeEncodeError:
            print("Error fetching movie data (encoding issue in error message)")
        return None

# ----------------- Telegram Handlers -----------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Welcome! Send me a movie name, and I will search it for you with direct play links.")

import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Create a thread pool for async operations
executor = ThreadPoolExecutor(max_workers=5)

def run_async_in_thread(async_func, *args):
    """Run async function in a thread and return the result"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(async_func(*args))
    finally:
        loop.close()
import urllib.parse
def generate_video_url(file_name):
    """Generate video URL from file name using the API with SSL decryption"""
    try:
        generate_url = "https://msubyoteshin.net/source/generate"
        payload = {
            "type": "movies",
            "file_name": file_name
        }
        
        print(f"Generating URL for: {file_name}")
        response = requests.post(generate_url, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        
        # Get the encrypted response
        encrypted_base64 = response.text
        print(f"Encrypted response length: {len(encrypted_base64)}")
        
        # Decrypt the base64 encoded data
        encrypted_data = base64.b64decode(encrypted_base64.strip())
        decrypted_data = decrypt_openssl_data(encrypted_data)
        
        # Parse the decrypted JSON
        try:
            response_data = json.loads(decrypted_data.decode('utf-8'))
        except UnicodeDecodeError:
            response_data = json.loads(decrypted_data.decode('latin-1'))
        
        print(f"Decrypted response: {response_data}")
        
        if response_data.get("status") and "data" in response_data:
            generated_url = response_data["data"]
            print(f"Generated URL: {generated_url}")
            return generated_url
        else:
            print(f"Failed to generate URL for {file_name}: {response_data}")
            return None
            
    except Exception as e:
        print(f"Error generating URL for {file_name}: {e}")
        return None

def process_search(message, keyword):
    """Process the search with sync bot methods but async HTTP requests in threads"""
    # Inform user that search is in progress
    msg = bot.send_message(message.chat.id, f"Searching for '{keyword}'...")

    all_movies = []
    page = 1
    MAX_PAGES = 10

    # Search through all pages (async HTTP calls in threads)
    while page <= MAX_PAGES:
        # Run async search_movies in a thread
        movies = run_async_in_thread(search_movies, keyword, page)
        if not movies:
            break
        all_movies.extend(movies)
        page += 1
        # Update progress every page
        bot.edit_message_text(f"Searching... Found {len(all_movies)} movies so far", 
                             chat_id=message.chat.id, message_id=msg.message_id)

    if not all_movies:
        bot.edit_message_text("No movies found.", chat_id=message.chat.id, message_id=msg.message_id)
        return

    bot.edit_message_text(f"Found {len(all_movies)} movies across {page-1} pages. Sending results...", 
                         chat_id=message.chat.id, message_id=msg.message_id)

    # Send movie info with "Watch" buttons
    for movie in all_movies:
        movie_id = movie.get("_id")
        name = movie.get("title")
        poster = movie.get("poster")
        description = movie.get("overview", "No description available.")
        release_year = movie.get("release_year", "")
        rating = movie.get("rating", "")
        
        # Run async fetch_movie_sources in a thread - get full movie data
        movie_data = run_async_in_thread(fetch_movie_sources, movie_id)

        if not movie_data:
            sources = []
        else:
            # Extract sources and updated info from detailed movie data
            sources = movie_data.get("sources", [])
            # Use detailed information if available
            name = movie_data.get("title", name)
            description = movie_data.get("overview", description)
            poster = movie_data.get("poster", poster)
            release_year = movie_data.get("release_year", release_year)
            rating = movie_data.get("rating", rating)

        # Handle encoding issues and limit description length
        try:
            max_desc_length = 800
            safe_description = description
            if len(description) > max_desc_length:
                safe_description = description[:max_desc_length] + "..."
        except UnicodeEncodeError:
            safe_description = "Description contains special characters"

        # Format the caption
        caption = f"<b>{name} ({release_year})</b>\n\n"
        if rating:
            caption += f"⭐ Rating: {rating}/100\n\n"
        caption += f"{safe_description}"
        caption += f"\n\n-<b>botByYeHtut</b>-"

        if len(caption) > 1024:
            excess = len(caption) - 1024
            caption = caption[:-excess-3] + "..." + caption[-3:]

        # Create inline keyboard for multiple sources
        markup = InlineKeyboardMarkup()
        unique_resolutions = set()
        
        if sources:
            for src in sources:
                if src.get("url"):
                    resolution = src.get("resolution", "Unknown")
                    # Clean up resolution text
                    if ":" in resolution:
                        resolution = resolution.split(":")[-1].strip()
                    
                    # Make resolution unique
                    base_resolution = resolution
                    counter = 1
                    while resolution in unique_resolutions:
                        resolution = f"{base_resolution} ({counter})"
                        counter += 1
                    unique_resolutions.add(resolution)
                    
                    video_url = src['url']
                    
                    # Check if URL is a direct link or needs generation
                    if video_url.startswith(('http://', 'https://')):
                        # Direct URL - use as is (single URL encoding)
                        final_url = f"https://kmzmm.github.io/KMZMM/player.html?video={video_url}"
                    else:
                        # File name - generate URL first
                        generated_url = generate_video_url(video_url)
                        if generated_url:
                            # Direct URL - use as is (single URL encoding)
                            final_url = f"https://kmzmm.github.io/KMZMM/player.html?video={generated_url}"
                        else:
                            # Fallback: try to construct URL from filename
                            final_url = f"https://kmzmm.github.io/KMZMM/player.html?video=https://msubyoteshin.net/{urllib.parse.quote(video_url)}"
                    
                    markup.add(
                        InlineKeyboardButton(
                            f"🎬 {resolution}",
                            url=final_url
                        )
                    )
        else:
            markup.add(InlineKeyboardButton("❌ No sources available", callback_data="no_sources"))

        try:
            if poster:
                full_poster_url = f"https://msubyoteshin.net{poster}" if poster.startswith('/') else poster
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=full_poster_url,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=caption,
                    parse_mode="HTML",
                    reply_markup=markup
                )
        except Exception as e:
            print(f"Error sending movie {name}: {e}")
            bot.send_message(
                chat_id=message.chat.id,
                text=caption,
                parse_mode="HTML",
                reply_markup=markup
            )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    keyword = message.text.strip()
    if not keyword:
        bot.send_message(message.chat.id, "Please provide a movie name.")
        return

    # Start the search in a separate thread
    thread = threading.Thread(target=process_search, args=(message, keyword))
    thread.start()

def EVP_BytesToKey(password: bytes, salt: bytes, key_len: int, iv_len: int):
    d = b''
    key_iv = b''
    while len(key_iv) < key_len + iv_len:
        d = hashlib.md5(d + password + salt).digest()
        key_iv += d
    return key_iv[:key_len], key_iv[key_len:key_len+iv_len]

def decrypt_openssl_data(encrypted_data: bytes) -> bytes:
    """
    Decrypt OpenSSL salted data using static key 'MSuB_2p0iNt0'
    """
    password = 'MSuB_2p0iNt0'
    
    # Check for Salted__ header
    if encrypted_data[:8] != b'Salted__':
        raise ValueError('Input is not OpenSSL salted format')
    
    salt = encrypted_data[8:16]
    ciphertext = encrypted_data[16:]
    
    # Derive key & iv
    key, iv = EVP_BytesToKey(password.encode('utf-8'), salt, 32, 16)
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plain
       

# ----------------- Run Bot -----------------

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True, timeout=10)
