# MessengerStats - Facebook Messenger Counter
A python script that counts your messages along with other statistics on Facebook Messenger.

This project was inspired by https://github.com/KMChris/messenger-counter.

## Installation
Clone the repository:
```bash
git clone https://github.com/lengvietcuong/messenger-stats.git
```
Install requirements using
```bash
pip install -r requirements.txt
```

## How to download your Facebook Messenger data
1. Go to https://accountscenter.facebook.com/info_and_permissions/dyi.
2. Click `Download or transfer information` → `Specific types of information`.
3. Click `Messages` → `Next` → `Download to device`.
4. Click `Date range`, select `All time`, then `Save`.
5. Click `Format`, select `JSON`, then `Save`.
6. Click `Media quality`, select `Low`, then `Save` (to reduce file sizes for images and videos).
7. Click `Create files`. You will be notified when they are available for download.

**Note**: Facebook recently introduced end-to-end encryption for Messenger, and only messages sent before this change can be downloaded.

## Usage
1. Move your downloaded data files to the `data` folder in the project directory (no need to unzip)
2. Run `main.py` and enjoy!

## Sample Output
```
👤 donaldtrump

💬 messages
╒══════════════╤════════╕
│ Total        │ 70,225 │
├──────────────┼────────┤
│ Donald Trump │ 37,188 │
├──────────────┼────────┤
│ Việt Cường   │ 33,037 │
╘══════════════╧════════╛

ℹ️ chars
╒══════════════╤═══════════╕
│ Total        │ 1,748,745 │
├──────────────┼───────────┤
│ Việt Cường   │   907,822 │
├──────────────┼───────────┤
│ Donald Trump │   840,923 │
╘══════════════╧═══════════╛

😍 reactions
╒══════════════╤═══════╕
│ Total        │ 2,754 │
├──────────────┼───────┤
│ Donald Trump │ 1,919 │
├──────────────┼───────┤
│ Việt Cường   │   835 │
╘══════════════╧═══════╛

🌠 stickers
╒══════════════╤═════╕
│ Total        │ 126 │
├──────────────┼─────┤
│ Việt Cường   │ 110 │
├──────────────┼─────┤
│ Donald Trump │  16 │
╘══════════════╧═════╛

🖼️ photos
╒══════════════╤═══════╕
│ Total        │ 3,981 │
├──────────────┼───────┤
│ Việt Cường   │ 2,096 │
├──────────────┼───────┤
│ Donald Trump │ 1,885 │
╘══════════════╧═══════╛

📹 videos
╒══════════════╤════╕
│ Total        │ 86 │
├──────────────┼────┤
│ Việt Cường   │ 44 │
├──────────────┼────┤
│ Donald Trump │ 42 │
╘══════════════╧════╛

📁 files
╒══════════════╤════╕
│ Total        │ 24 │
├──────────────┼────┤
│ Việt Cường   │ 14 │
├──────────────┼────┤
│ Donald Trump │ 10 │
╘══════════════╧════╛

🔗 shares
╒══════════════╤═════╕
│ Total        │ 436 │
├──────────────┼─────┤
│ Donald Trump │ 242 │
├──────────────┼─────┤
│ Việt Cường   │ 194 │
╘══════════════╧═════╛

📱 calls
╒══════════════╤════╕
│ Total        │ 41 │
├──────────────┼────┤
│ Donald Trump │ 29 │
├──────────────┼────┤
│ Việt Cường   │ 12 │
╘══════════════╧════╛
```