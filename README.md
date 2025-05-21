# dailygator
Florida Man Headlines
Daily Gator 🐊
A Progressive Web App that aggregates and displays the wildest "Florida Man" news stories from around the web.

🌴 Overview
Daily Gator automatically collects news stories featuring the infamous "Florida Man" phenomenon, presenting them in a clean, mobile-friendly interface. The app updates hourly to bring you the latest and most outrageous headlines from the Sunshine State.
Features

Live News Feed: Automatically updated collection of Florida Man stories
Offline Access: Full PWA support for reading stories without internet
Bookmark Stories: Save your favorite Florida Man adventures
Mobile-Friendly: Install on your home screen like a native app

Coming Soon

Florida Man Birthday Challenge: Discover what Florida Man did on your birthday
Heat Map: See where the wildest Florida Man stories happen across the state
Florida or Not?: Test your knowledge with our quiz game
Florida Man of the Month: Vote for the most outrageous story
Weather Correlation: See how Florida Man activity correlates with weather patterns

🚀 Installation
As a PWA (Mobile)

Visit the app in your mobile browser
Tap the "Add to Home Screen" button in your browser menu
Daily Gator will be installed like a native app

As a PWA (Desktop)

Visit the app in Chrome, Edge, or another compatible browser
Look for the install icon in the address bar
Click "Install" when prompted

From Source

Clone this repository
Open index.html in your browser
For local development, you may need to use a local server (like python -m http.server)

🔧 Technical Details
Daily Gator is built as a lightweight Progressive Web App with:

No framework dependencies - pure HTML, CSS, and JavaScript
Automated data collection via GitHub Actions
Service worker for offline capabilities
LocalStorage for saved stories
Hosted on GitHub Pages - completely free, no server needed

📊 How It Works

A scheduled GitHub Action runs hourly to scrape Florida news sites
Stories containing "Florida Man" are extracted and saved to a JSON file
The web app fetches this data and displays it in a user-friendly interface
Service workers cache the content for offline viewing

🤝 Contributing
Contributions are welcome! Feel free to:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Development Ideas

Improve the scraper to better identify genuine Florida Man stories
Add more news sources to the scraper
Implement any of the "Coming Soon" features
Improve the UI/UX design

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Inspired by the internet's fascination with Florida Man stories
Built with love for the weird and wonderful state of Florida


Disclaimer: Daily Gator is meant for entertainment purposes only. We love Florida and its wonderfully unique residents. No alligators were harmed in the making of this app.
