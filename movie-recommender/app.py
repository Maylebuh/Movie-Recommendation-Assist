from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Movie database with tags for genre, actors, and mood
movies = [
    {"title": "The Shawshank Redemption", "genres": ["drama"], "actors": ["Morgan Freeman", "Tim Robbins"], "mood": ["thoughtful", "hopeful"]},
    {"title": "The Dark Knight", "genres": ["action", "crime", "drama"], "actors": ["Christian Bale", "Heath Ledger"], "mood": ["intense", "exciting"]},
    {"title": "Pulp Fiction", "genres": ["crime", "drama"], "actors": ["John Travolta", "Uma Thurman"], "mood": ["quirky", "exciting"]},
    {"title": "Forrest Gump", "genres": ["drama", "romance"], "actors": ["Tom Hanks", "Robin Wright"], "mood": ["heartwarming", "hopeful"]},
    {"title": "Inception", "genres": ["action", "sci-fi", "thriller"], "actors": ["Leonardo DiCaprio", "Tom Hardy"], "mood": ["mind-bending", "exciting"]},
    {"title": "The Matrix", "genres": ["action", "sci-fi"], "actors": ["Keanu Reeves", "Laurence Fishburne"], "mood": ["mind-bending", "exciting"]},
    {"title": "Goodfellas", "genres": ["crime", "drama"], "actors": ["Robert De Niro", "Joe Pesci"], "mood": ["intense", "gritty"]},
    {"title": "The Godfather", "genres": ["crime", "drama"], "actors": ["Marlon Brando", "Al Pacino"], "mood": ["intense", "dramatic"]},
    {"title": "The Avengers", "genres": ["action", "adventure", "sci-fi"], "actors": ["Robert Downey Jr.", "Chris Evans"], "mood": ["exciting", "fun"]},
    {"title": "Toy Story", "genres": ["animation", "adventure", "comedy"], "actors": ["Tom Hanks", "Tim Allen"], "mood": ["happy", "heartwarming"]},
    {"title": "Up", "genres": ["animation", "adventure", "comedy"], "actors": ["Ed Asner"], "mood": ["heartwarming", "emotional"]},
    {"title": "La La Land", "genres": ["drama", "music", "romance"], "actors": ["Ryan Gosling", "Emma Stone"], "mood": ["romantic", "nostalgic"]},
    {"title": "The Hangover", "genres": ["comedy"], "actors": ["Bradley Cooper", "Zach Galifianakis"], "mood": ["funny", "wild"]},
    {"title": "Interstellar", "genres": ["adventure", "drama", "sci-fi"], "actors": ["Matthew McConaughey", "Anne Hathaway"], "mood": ["thoughtful", "epic"]},
    {"title": "The Notebook", "genres": ["drama", "romance"], "actors": ["Ryan Gosling", "Rachel McAdams"], "mood": ["romantic", "emotional"]},
    {"title": "Mad Max: Fury Road", "genres": ["action", "adventure", "sci-fi"], "actors": ["Tom Hardy", "Charlize Theron"], "mood": ["intense", "exciting"]},
    {"title": "Inside Out", "genres": ["animation", "adventure", "comedy"], "actors": ["Amy Poehler", "Bill Hader"], "mood": ["thoughtful", "heartwarming"]},
    {"title": "The Wolf of Wall Street", "genres": ["biography", "crime", "drama"], "actors": ["Leonardo DiCaprio", "Jonah Hill"], "mood": ["wild", "exciting"]},
    {"title": "Guardians of the Galaxy", "genres": ["action", "adventure", "comedy"], "actors": ["Chris Pratt", "Zoe Saldana"], "mood": ["fun", "exciting"]},
    {"title": "The Silence of the Lambs", "genres": ["crime", "drama", "thriller"], "actors": ["Jodie Foster", "Anthony Hopkins"], "mood": ["suspenseful", "intense"]}
]

# Common keywords for matching
genres = ["action", "comedy", "drama", "romance", "sci-fi", "thriller", "crime", "adventure", "animation", "horror", "fantasy"]
moods = ["happy", "excited", "relaxed", "adventurous", "thoughtful", "romantic", "funny", "intense", "mind-bending", "heartwarming"]
actors_list = ["Leonardo DiCaprio", "Tom Hanks", "Morgan Freeman", "Meryl Streep", "Robert De Niro", "Brad Pitt", "Julia Roberts", "Denzel Washington", "Emma Stone", "Ryan Gosling"]

class MovieRecommendationAssistant:
    def __init__(self):
        self.conversation_state = "start"
        self.user_preferences = {"genres": [], "actors": [], "mood": []}
    
    def extract_keywords(self, input_text, keyword_list):
        """Extract relevant keywords from user input"""
        matches = []
        for keyword in keyword_list:
            if keyword in input_text.lower():
                matches.append(keyword)
        return matches if matches else ["any"]
    
    def extract_actors(self, input_text):
        """Extract actor names from user input"""
        if "no preference" in input_text.lower() or "any" in input_text.lower() or "don't care" in input_text.lower():
            return ["any"]
        
        matches = []
        for actor in actors_list:
            if actor.lower() in input_text.lower():
                matches.append(actor)
        return matches if matches else ["any"]
    
    def get_recommendations(self, preferences):
        """Get movie recommendations based on user preferences"""
        scored_movies = []
        
        for movie in movies:
            score = 0
            
            # Score based on genre match
            if preferences["genres"][0] != "any":
                for genre in preferences["genres"]:
                    if genre in movie["genres"]:
                        score += 3
            
            # Score based on actor match
            if preferences["actors"][0] != "any":
                for actor in preferences["actors"]:
                    if actor in movie["actors"]:
                        score += 2
            
            # Score based on mood match
            if preferences["mood"][0] != "any":
                for mood in preferences["mood"]:
                    if mood in movie["mood"]:
                        score += 1
            
            # Only consider movies with at least one match
            if score > 0:
                scored_movies.append((movie, score))
        
        # Sort by score and return top 3
        scored_movies.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, score in scored_movies[:3]]
    
    def process_message(self, message):
        """Process user message and return bot response"""
        if self.conversation_state == "start":
            self.conversation_state = "ask_genre"
            return "🎬 Welcome to the Movie Recommendation Assistant! I'll help you find the perfect movie based on your preferences. What genre are you in the mood for? (action, comedy, drama, romance, sci-fi, thriller, crime, adventure, animation)"
        
        elif self.conversation_state == "ask_genre":
            self.user_preferences["genres"] = self.extract_keywords(message, genres)
            self.conversation_state = "ask_actors"
            return "Great choice! Any favorite actors you'd like to see? (You can name specific actors or say 'no preference')"
        
        elif self.conversation_state == "ask_actors":
            self.user_preferences["actors"] = self.extract_actors(message)
            self.conversation_state = "ask_mood"
            return "Nice! How are you feeling today? (happy, excited, relaxed, adventurous, thoughtful, romantic, funny, intense)"
        
        elif self.conversation_state == "ask_mood":
            self.user_preferences["mood"] = self.extract_keywords(message, moods)
            self.conversation_state = "show_results"
            
            recommendations = self.get_recommendations(self.user_preferences)
            
            if not recommendations:
                return "I couldn't find any movies matching your preferences. 😢 Maybe try being less specific with your choices?"
            
            result = "Based on your preferences, I recommend these movies:\n\n"
            for i, movie in enumerate(recommendations, 1):
                result += f"{i}. {movie['title']}\n"
                result += f"   Genres: {', '.join(movie['genres'])}\n"
                result += f"   Stars: {', '.join(movie['actors'])}\n"
                result += f"   Mood: {', '.join(movie['mood'])}\n\n"
            
            result += "Enjoy your movie night! 🍿 Would you like to start over?"
            return result
        
        elif self.conversation_state == "show_results":
            if "yes" in message.lower() or "sure" in message.lower() or "ok" in message.lower():
                self.conversation_state = "start"
                self.user_preferences = {"genres": [], "actors": [], "mood": []}
                return "Great! Let's find another movie. What genre are you in the mood for?"
            else:
                return "Thanks for using the Movie Recommendation Assistant! Goodbye! 👋"

# Initialize the assistant
assistant = MovieRecommendationAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    bot_response = assistant.process_message(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)