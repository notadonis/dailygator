🐊 Florida Man Headlines — Daily Gator
A Progressive Web App that aggregates and displays the wildest "Florida Man" news stories from around the web.

🌴 Overview
Daily Gator automatically scrapes and showcases the most outrageous "Florida Man" headlines from online sources, updating hourly. Designed as a mobile-first PWA, the app offers a smooth, offline-ready experience with bookmarking and native install capabilities.

🔥 Features
📡 Live News Feed – Hourly-updated stories featuring the infamous Florida Man

📴 Offline Access – Full PWA support lets you browse stories without an internet connection

🔖 Bookmarking – Save your favorite Florida Man escapades

📱 Mobile-First – Install on your home screen like a native app

🧪 Coming Soon
🎂 Florida Man Birthday Challenge – Discover what Florida Man did on your birthday

🗺️ Heat Map – Visualize where the wildest stories originate in Florida

🧐 Florida or Not? – Quiz game to test your weird-news instincts

🏆 Florida Man of the Month – Community voting for the craziest headline

☀️ Weather Correlation – Analyze how heat and humidity affect Florida Man behavior

🚀 Installation
📱 As a PWA (Mobile)
Open the app in your mobile browser

Tap Add to Home Screen in your browser menu

Launch Daily Gator like a native app

💻 As a PWA (Desktop)
Open the app in Chrome, Edge, or any PWA-compatible browser

Click the install icon in the address bar

Follow the prompt to install

🛠️ From Source
bash
Copy
Edit
git clone https://github.com/your-username/daily-gator.git
cd daily-gator
# Open index.html in your browser, or:
python3 -m http.server
🔧 Technical Details
📦 No frameworks – Just vanilla HTML, CSS, and JavaScript

🤖 GitHub Actions – Scheduled scraping every hour

💾 LocalStorage – Client-side storage for bookmarks

📡 Service Worker – Enables full offline support

🚀 Deployed via GitHub Pages – 100% free hosting

📊 How It Works
A GitHub Action runs every hour and scrapes select Florida news sources

Headlines containing “Florida Man” are filtered and saved to a JSON file

The frontend fetches and renders these stories

Service workers ensure the app is usable offline

🤝 Contributing
We welcome contributions!

bash
Copy
Edit
# Fork the repository
# Create your feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "Add amazing feature"

# Push and open a PR
git push origin feature/amazing-feature
🧠 Development Ideas
Improve scraper accuracy and filtering logic

Expand news source coverage

Build "Coming Soon" features

Refine the UI/UX and responsiveness

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgments
Inspired by the internet’s obsession with all things Florida Man

Built with 💚 for the weird and wonderful residents of the Sunshine State

Disclaimer: Daily Gator is for entertainment purposes only. We love Florida—and no gators were harmed in the making of this app.
