# Chefify - Your Personal AI Chef 🧑‍🍳

Chefify is a web application that acts as your personal AI chef. Simply input the ingredients you have on hand, select your dietary preferences, and let Chefify generate a delicious recipe tailored to your needs.

## Features

- Generate recipes based on available ingredients
- Support for multiple dietary preferences:
  - Vegetarian
  - Vegan
  - Gluten-free
  - Dairy-free
  - High protein
  - Low carb
  - Keto
  - Paleo
- Beautiful, modern user interface
- Real-time recipe generation
- Mobile-responsive design

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chefify.git
cd chefify
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
chefify/
├── app.py              # Flask application
├── basic.py           # Recipe generation logic
├── requirements.txt   # Python dependencies
├── static/
│   ├── styles.css    # Application styles
│   └── script.js     # Frontend JavaScript
└── templates/
    └── index.html    # Main HTML template
```

## Usage

1. Enter your available ingredients in the text area, separated by commas
2. Select any dietary preferences that apply
3. Click "Generate Recipe" to get your personalized recipe
4. Use the "Clear" button to start over

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

MIT License - feel free to use this project however you'd like! 