from flask import Flask, render_template, request, redirect, url_for,jsonify, session
from collections import Counter
import random
import copy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

hands_data_2 = [
    # Pairs
    {"hand": "AA", "equity": 85.2, "ev": 40},
    {"hand": "KK", "equity": 82.4, "ev": 35},
    {"hand": "QQ", "equity": 79.9, "ev": 30},
    {"hand": "JJ", "equity": 77.5, "ev": 25},
    {"hand": "TT", "equity": 75,   "ev": 20},
    {"hand": "99", "equity": 72,   "ev": 15},
    {"hand": "88", "equity": 69.2, "ev": 12},
    {"hand": "77", "equity": 66.2, "ev": 10},
    {"hand": "66", "equity": 63.3, "ev": 8},
    {"hand": "55", "equity": 60.3, "ev": 7},
    {"hand": "44", "equity": 57,   "ev": 6},
    {"hand": "33", "equity": 54,   "ev": 5},
    {"hand": "22", "equity": 50.3, "ev": 4},

    # Suited Hands
    {"hand": "AKs", "equity": 67, "ev": 25},
    {"hand": "AQs", "equity": 66.2, "ev": 20},
    {"hand": "AJs", "equity": 65.4, "ev": 18},
    {"hand": "ATs", "equity": 64.6, "ev": 15},
    {"hand": "A9s", "equity": 63, "ev": 12},
    {"hand": "A8s", "equity": 62.8, "ev": 10},
    {"hand": "A7s", "equity": 61, "ev": 9},
    {"hand": "A6s", "equity": 59.9, "ev": 8},
    {"hand": "A5s", "equity": 59.9, "ev": 7},
    {"hand": "A4s", "equity": 59, "ev": 6},
    {"hand": "A3s", "equity": 58.2, "ev": 5},
    {"hand": "A2s", "equity": 57.4, "ev": 4},

    {"hand": "KQs", "equity": 63.4, "ev": 15},
    {"hand": "KJs", "equity": 62.6, "ev": 12},
    {"hand": "KTs", "equity": 61.8, "ev": 10},
    {"hand": "K9s", "equity": 60, "ev": 8},
    {"hand": "K8s", "equity": 58.3, "ev": 7},
    {"hand": "K7s", "equity": 57.5, "ev": 6},
    {"hand": "K6s", "equity": 56.6, "ev": 5},
    {"hand": "K5s", "equity": 55.8, "ev": 4},
    {"hand": "K4s", "equity": 54.9, "ev": 3},
    {"hand": "K3s", "equity": 54.1, "ev": 2},
    {"hand": "K2s", "equity": 53.2, "ev": 1},

    {"hand": "QJs", "equity": 60.3, "ev": 12},
    {"hand": "QTs", "equity": 59.5, "ev": 10},
    {"hand": "Q9s", "equity": 57.7, "ev": 8},
    {"hand": "Q8s", "equity": 56, "ev": 7},
    {"hand": "Q7s", "equity": 54.3, "ev": 6},
    {"hand": "Q6s", "equity": 53.6, "ev": 5},
    {"hand": "Q5s", "equity": 53, "ev": 4},
    {"hand": "Q4s", "equity": 52.8, "ev": 3},
    {"hand": "Q3s", "equity": 51, "ev": 2},
    {"hand": "Q2s", "equity": 50.2, "ev": 1},

    {"hand": "JTs", "equity": 57.5, "ev": 12},
    {"hand": "J9s", "equity": 55.7, "ev": 10},
    {"hand": "J8s", "equity": 54, "ev": 8},
    {"hand": "J7s", "equity": 52.3, "ev": 7},
    {"hand": "J6s", "equity": 50.6, "ev": 6},
    {"hand": "J5s", "equity": 50, "ev": 5},
    {"hand": "J4s", "equity": 49.1, "ev": 4},
    {"hand": "J3s", "equity": 48.2, "ev": 3},
    {"hand": "J2s", "equity": 47.4, "ev": 2},

    {"hand": "T9s", "equity": 54, "ev": 10},
    {"hand": "T8s", "equity": 52.3, "ev": 9},
    {"hand": "T7s", "equity": 50.6, "ev": 8},
    {"hand": "T6s", "equity": 48.9, "ev": 7},
    {"hand": "T5s", "equity": 47.2, "ev": 6},
    {"hand": "T4s", "equity": 46.5, "ev": 5},
    {"hand": "T3s", "equity": 45.7, "ev": 4},
    {"hand": "T2s", "equity": 44.8, "ev": 3},

    {"hand": "98s", "equity": 50.8, "ev": 5},
    {"hand": "97s", "equity": 49.1, "ev": 4},
    {"hand": "96s", "equity": 47.4, "ev": 3},
    {"hand": "95s", "equity": 45.7, "ev": 2},
    {"hand": "94s", "equity": 43.9, "ev": 1},
    {"hand": "93s", "equity": 43.3, "ev": 0.5},
    {"hand": "92s", "equity": 42.4, "ev": 0},

    {"hand": "87s", "equity": 47.9, "ev": 6},
    {"hand": "86s", "equity": 46.2, "ev": 5},
    {"hand": "85s", "equity": 44.5, "ev": 4},
    {"hand": "84s", "equity": 42.7, "ev": 3},
    {"hand": "83s", "equity": 40.9, "ev": 2},
    {"hand": "82s", "equity": 40.3, "ev": 1},

    {"hand": "76s", "equity": 45.4, "ev": 4},
    {"hand": "75s", "equity": 43.7, "ev": 3},
    {"hand": "74s", "equity": 41.8, "ev": 2},
    {"hand": "73s", "equity": 40, "ev": 1},
    {"hand": "72s", "equity": 38.2, "ev": 0.5},

 

    {"hand": "65s", "equity": 43.1, "ev": 5},
    {"hand": "64s", "equity": 41.3, "ev": 4},
    {"hand": "63s", "equity": 39.5, "ev": 3},
    {"hand": "62s", "equity": 37.7, "ev": 2},


    {"hand": "54s", "equity": 41.5, "ev": 4},
    {"hand": "53s", "equity": 39.7, "ev": 3},
    {"hand": "52s", "equity": 37.8, "ev": 2},
    

    {"hand": "43s", "equity": 38.6, "ev": 3},
    {"hand": "42s", "equity": 36.8, "ev": 2},
                

    {"hand": "32s", "equity": 36, "ev": 1},

    # Unsuited Hands
    {"hand": "AKo", "equity": 65.3, "ev": 25},
    {"hand": "AQo", "equity": 64.4, "ev": 20},
    {"hand": "AJo", "equity": 63.6, "ev": 18},
    {"hand": "ATo", "equity": 62.7, "ev": 15},
    {"hand": "A9o", "equity": 60.8, "ev": 12},
    {"hand": "A8o", "equity": 59.9, "ev": 10},
    {"hand": "A7o", "equity": 58.8, "ev": 9},
    {"hand": "A6o", "equity": 57.7, "ev": 8},
    {"hand": "A5o", "equity": 57.7, "ev": 7},
    {"hand": "A4o", "equity": 56.7, "ev": 6},
    {"hand": "A3o", "equity": 55.8, "ev": 5},
    {"hand": "A2o", "equity": 54.9, "ev": 4},

    {"hand": "KQo", "equity": 61.5, "ev": 15},
    {"hand": "KJo", "equity": 60.6, "ev": 12},
    {"hand": "KTo", "equity": 59.7, "ev": 10},
    {"hand": "K9o", "equity": 57.8, "ev": 8},
    {"hand": "K8o", "equity": 56, "ev": 7},
    {"hand": "K7o", "equity": 55.2, "ev": 6},
    {"hand": "K6o", "equity": 54.2, "ev": 5},
    {"hand": "K5o", "equity": 53.3, "ev": 4},
    {"hand": "K4o", "equity": 52.3, "ev": 3},
    {"hand": "K3o", "equity": 51.4, "ev": 2},
    {"hand": "K2o", "equity": 50.5, "ev": 1},

    {"hand": "QJo", "equity": 58.1, "ev": 12},
    {"hand": "QTo", "equity": 57.3, "ev": 10},
    {"hand": "Q9o", "equity": 55.4, "ev": 8},
    {"hand": "Q8o", "equity": 53.6, "ev": 7},
    {"hand": "Q7o", "equity": 51.8, "ev": 6},
    {"hand": "Q6o", "equity": 51, "ev": 5},
    {"hand": "Q5o", "equity": 50.1, "ev": 4},
    {"hand": "Q4o", "equity": 49.1, "ev": 3},
    {"hand": "Q3o", "equity": 48.2, "ev": 2},
    {"hand": "Q2o", "equity": 47.3, "ev": 1},

    {"hand": "JTo", "equity": 55.2, "ev": 10},
    {"hand": "J9o", "equity": 53.3, "ev": 9},
    {"hand": "J8o", "equity": 51.5, "ev": 8},
    {"hand": "J7o", "equity": 49.7, "ev": 7},
    {"hand": "J6o", "equity": 47.8, "ev": 6},
    {"hand": "J5o", "equity": 47.2, "ev": 5},
    {"hand": "J4o", "equity": 46.2, "ev": 4},
    {"hand": "J3o", "equity": 45.3, "ev": 3},
    {"hand": "J2o", "equity": 44.3, "ev": 2},

    {"hand": "T9o", "equity": 51.5, "ev": 9},
    {"hand": "T8o", "equity": 49.7, "ev": 8},
    {"hand": "T7o", "equity": 47.9, "ev": 7},
    {"hand": "T6o", "equity": 46.1, "ev": 6},
    {"hand": "T5o", "equity": 44.3, "ev": 5},
    {"hand": "T4o", "equity": 43.5, "ev": 4},
    {"hand": "T3o", "equity": 42.6, "ev": 3},
    {"hand": "T2o", "equity": 41.7, "ev": 2},

    {"hand": "98o", "equity": 48.1, "ev": 8},
    {"hand": "97o", "equity": 46.3, "ev": 7},
    {"hand": "96o", "equity": 44.5, "ev": 6},
    {"hand": "95o", "equity": 42.7, "ev": 5},
    {"hand": "94o", "equity": 40.7, "ev": 4},
    {"hand": "93o", "equity": 40, "ev": 3},
    {"hand": "92o", "equity": 39, "ev": 2},

    {"hand": "87o", "equity": 45.1, "ev": 7},
    {"hand": "86o", "equity": 43, "ev": 6},
    {"hand": "85o", "equity": 41.4, "ev": 5},
    {"hand": "84o", "equity": 39.4, "ev": 4},
    {"hand": "83o", "equity": 37.5, "ev": 3},
    {"hand": "82o", "equity": 36.8, "ev": 2},

    {"hand": "76o", "equity": 42.3, "ev": 6},
    {"hand": "75o", "equity": 40.5, "ev": 5},
    {"hand": "74o", "equity": 38.6, "ev": 4},
    {"hand": "73o", "equity": 36.6, "ev": 3},
    {"hand": "72o", "equity": 34.6, "ev": 2},

    {"hand": "65o", "equity": 39.9, "ev": 5},
    {"hand": "64o", "equity": 38, "ev": 4},
    {"hand": "63o", "equity": 36, "ev": 3},
    {"hand": "62o", "equity": 34, "ev": 2},

    {"hand": "54o", "equity": 38.1, "ev": 4},
    {"hand": "53o", "equity": 36.3, "ev": 3},
    {"hand": "52o", "equity": 34.3, "ev": 2},

    {"hand": "43o", "equity": 35.1, "ev": 3},
    {"hand": "42o", "equity": 33.2, "ev": 2},

    {"hand": "32o", "equity": 32.3, "ev": 1},
]


default_hands_data_0 = [
    {"hand": "AA", "equity":  85.2, "ev": 85.2},
    {"hand": "KK", "equity":  82.4, "ev": 82.4},
    {"hand": "QQ", "equity":  79.9, "ev": 79.9},
    {"hand": "JJ", "equity":  77.5, "ev": 77.5},
    {"hand": "TT", "equity":  75.0, "ev": 75.0},
    {"hand": "99", "equity":  72.0, "ev": 72.0},
    {"hand": "88", "equity":  69.2, "ev": 69.2},
    {"hand": "77", "equity":  66.2, "ev": 66.2},
    {"hand": "66", "equity":  63.3, "ev": 63.3},
    {"hand": "55", "equity":  60.3, "ev": 60.3},
    {"hand": "44", "equity":  57.0, "ev": 57.0},
    {"hand": "33", "equity":  54.0, "ev": 54.0},
    {"hand": "22", "equity":  50.3, "ev": 50.3},
    {"hand": "AKs", "equity": 67.0, "ev": 67.0},
    {"hand": "AQs", "equity": 66.2, "ev": 66.2},
    {"hand": "AJs", "equity": 65.4, "ev": 65.4},
    {"hand": "ATs", "equity": 64.6, "ev": 64.6},
    {"hand": "A9s", "equity": 63.0, "ev": 63.0},
    {"hand": "A8s", "equity": 62.8, "ev": 62.8},
    {"hand": "A7s", "equity": 61.3, "ev": 61.3},
    {"hand": "A6s", "equity": 59.9, "ev": 59.9},
    {"hand": "A5s", "equity": 59.9, "ev": 59.9},
    {"hand": "A4s", "equity": 59.0, "ev": 59.0},
    {"hand": "A3s", "equity": 58.2, "ev": 58.2},
    {"hand": "A2s", "equity": 57.4, "ev": 57.4},
    {"hand": "KQs", "equity": 63.4, "ev": 63.4},
    {"hand": "KJs", "equity": 62.6, "ev": 62.6},
    {"hand": "KTs", "equity": 61.8, "ev": 61.8},
    {"hand": "K9s", "equity": 60.0, "ev": 60.0},
    {"hand": "K8s", "equity": 58.3, "ev": 58.3},
    {"hand": "K7s", "equity": 57.5, "ev": 57.5},
    {"hand": "K6s", "equity": 56.6, "ev": 56.6},
    {"hand": "K5s", "equity": 55.8, "ev": 55.8},
    {"hand": "K4s", "equity": 54.9, "ev": 54.9},
    {"hand": "K3s", "equity": 54.1, "ev": 54.1},
    {"hand": "K2s", "equity": 53.2, "ev": 53.2},
    {"hand": "QJs", "equity": 60.3, "ev": 60.3},
    {"hand": "QTs", "equity": 59.5, "ev": 59.5},
    {"hand": "Q9s", "equity": 57.7, "ev": 57.7},
    {"hand": "Q8s", "equity": 56.0, "ev": 56.0},
    {"hand": "Q7s", "equity": 54.3, "ev": 54.3},
    {"hand": "Q6s", "equity": 53.6, "ev": 53.6},
    {"hand": "Q5s", "equity": 53.0, "ev": 53.0},
    {"hand": "Q4s", "equity": 52.8, "ev": 52.8},
    {"hand": "Q3s", "equity": 51.0, "ev": 51.0},
    {"hand": "Q2s", "equity": 50.2, "ev": 50.2},
    {"hand": "JTs", "equity": 57.5, "ev": 57.5},
    {"hand": "J9s", "equity": 55.7, "ev": 55.7},
    {"hand": "J8s", "equity": 54.0, "ev": 54.0},
    {"hand": "J7s", "equity": 52.3, "ev": 52.3},
    {"hand": "J6s", "equity": 50.6, "ev": 50.6},
    {"hand": "J5s", "equity": 50.0, "ev": 50.0},
    {"hand": "J4s", "equity": 49.1, "ev": 49.1},
    {"hand": "J3s", "equity": 48.2, "ev": 48.2},
    {"hand": "J2s", "equity": 47.4, "ev": 47.4},
    {"hand": "T9s", "equity": 54.0, "ev": 54.0},
    {"hand": "T8s", "equity": 52.3, "ev": 52.3},
    {"hand": "T7s", "equity": 50.6, "ev": 50.6},
    {"hand": "T6s", "equity": 48.9, "ev": 48.9},
    {"hand": "T5s", "equity": 47.2, "ev": 47.2},
    {"hand": "T4s", "equity": 46.5, "ev": 46.5},
    {"hand": "T3s", "equity": 45.7, "ev": 45.7},
    {"hand": "T2s", "equity": 44.8, "ev": 44.8},
    {"hand": "98s", "equity": 50.8, "ev": 50.8},
    {"hand": "97s", "equity": 49.1, "ev": 49.1},
    {"hand": "96s", "equity": 47.4, "ev": 47.4},
    {"hand": "95s", "equity": 45.7, "ev": 45.7},
    {"hand": "94s", "equity": 43.9, "ev": 43.9},
    {"hand": "93s", "equity": 43.3, "ev": 43.3},
    {"hand": "92s", "equity": 42.4, "ev": 42.4},
    {"hand": "87s", "equity": 47.9, "ev": 47.9},
    {"hand": "86s", "equity": 46.2, "ev": 46.2},
    {"hand": "85s", "equity": 44.5, "ev": 44.5},
    {"hand": "84s", "equity": 42.7, "ev": 42.7},
    {"hand": "83s", "equity": 40.9, "ev": 40.9},
    {"hand": "82s", "equity": 40.3, "ev": 40.3},
    {"hand": "76s", "equity": 45.4, "ev": 45.4},
    {"hand": "75s", "equity": 43.7, "ev": 43.7},
    {"hand": "74s", "equity": 41.8, "ev": 41.8},
    {"hand": "73s", "equity": 40.0, "ev": 40.0},
    {"hand": "72s", "equity": 38.2, "ev": 38.2},
    {"hand": "65s", "equity": 43.1, "ev": 43.1},
    {"hand": "64s", "equity": 41.3, "ev": 41.3},
    {"hand": "63s", "equity": 39.5, "ev": 39.5},
    {"hand": "62s", "equity": 37.7, "ev": 37.7},
    {"hand": "54s", "equity": 41.5, "ev": 41.5},
    {"hand": "53s", "equity": 39.7, "ev": 39.7},
    {"hand": "52s", "equity": 37.8, "ev": 37.8},
    {"hand": "43s", "equity": 38.6, "ev": 38.6},
    {"hand": "42s", "equity": 36.8, "ev": 36.8},
    {"hand": "32s", "equity": 36.0, "ev": 36.0},
    {"hand": "AKo", "equity": 65.3, "ev": 65.3},
    {"hand": "AQo", "equity": 64.4, "ev": 64.4},
    {"hand": "AJo", "equity": 63.6, "ev": 63.6},
    {"hand": "ATo", "equity": 62.7, "ev": 62.7},
    {"hand": "A9o", "equity": 60.8, "ev": 60.8},
    {"hand": "A8o", "equity": 59.9, "ev": 59.9},
    {"hand": "A7o", "equity": 58.8, "ev": 58.8},
    {"hand": "A6o", "equity": 57.7, "ev": 57.7},
    {"hand": "A5o", "equity": 57.7, "ev": 57.7},
    {"hand": "A4o", "equity": 56.7, "ev": 56.7},
    {"hand": "A3o", "equity": 55.8, "ev": 55.8},
    {"hand": "A2o", "equity": 54.9, "ev": 54.9},
    {"hand": "KQo", "equity": 61.5, "ev": 61.5},
    {"hand": "KJo", "equity": 60.6, "ev": 60.6},
    {"hand": "KTo", "equity": 59.7, "ev": 59.7},
    {"hand": "K9o", "equity": 57.8, "ev": 57.8},
    {"hand": "K8o", "equity": 56.0, "ev": 56.0},
    {"hand": "K7o", "equity": 55.2, "ev": 55.2},
    {"hand": "K6o", "equity": 54.2, "ev": 54.2},
    {"hand": "K5o", "equity": 53.3, "ev": 53.3},
    {"hand": "K4o", "equity": 52.3, "ev": 52.3},
    {"hand": "K3o", "equity": 51.4, "ev": 51.4},
    {"hand": "K2o", "equity": 50.5, "ev": 50.5},
    {"hand": "QJo", "equity": 58.1, "ev": 58.1},
    {"hand": "QTo", "equity": 57.3, "ev": 57.3},
    {"hand": "Q9o", "equity": 55.4, "ev": 55.4},
    {"hand": "Q8o", "equity": 53.6, "ev": 53.6},
    {"hand": "Q7o", "equity": 51.8, "ev": 51.8},
    {"hand": "Q6o", "equity": 51.0, "ev": 51.0},
    {"hand": "Q5o", "equity": 50.1, "ev": 50.1},
    {"hand": "Q4o", "equity": 49.1, "ev": 49.1},
    {"hand": "Q3o", "equity": 48.2, "ev": 48.2},
    {"hand": "Q2o", "equity": 47.3, "ev": 47.3},
    {"hand": "JTo", "equity": 55.2, "ev": 55.2},
    {"hand": "J9o", "equity": 53.3, "ev": 53.3},
    {"hand": "J8o", "equity": 51.5, "ev": 51.5},
    {"hand": "J7o", "equity": 49.7, "ev": 49.7},
    {"hand": "J6o", "equity": 47.8, "ev": 47.8},
    {"hand": "J5o", "equity": 47.2, "ev": 47.2},
    {"hand": "J4o", "equity": 46.2, "ev": 46.2},
    {"hand": "J3o", "equity": 45.3, "ev": 45.3},
    {"hand": "J2o", "equity": 44.3, "ev": 44.3},
    {"hand": "T9o", "equity": 51.5, "ev": 51.5},
    {"hand": "T8o", "equity": 49.7, "ev": 49.7},
    {"hand": "T7o", "equity": 47.9, "ev": 47.9},
    {"hand": "T6o", "equity": 46.1, "ev": 46.1},
    {"hand": "T5o", "equity": 44.3, "ev": 44.3},
    {"hand": "T4o", "equity": 43.5, "ev": 43.5},
    {"hand": "T3o", "equity": 42.6, "ev": 42.6},
    {"hand": "T2o", "equity": 41.7, "ev": 41.7},
    {"hand": "98o", "equity": 48.1, "ev": 48.1},
    {"hand": "97o", "equity": 46.3, "ev": 46.3},
    {"hand": "96o", "equity": 44.5, "ev": 44.5},
    {"hand": "95o", "equity": 42.7, "ev": 42.7},
    {"hand": "94o", "equity": 40.7, "ev": 40.7},
    {"hand": "93o", "equity": 40.0, "ev": 40.0},
    {"hand": "92o", "equity": 39.0, "ev": 39.0},
    {"hand": "87o", "equity": 45.1, "ev": 45.1},
    {"hand": "86o", "equity": 43.0, "ev": 43.0},
    {"hand": "85o", "equity": 41.4, "ev": 41.4},
    {"hand": "84o", "equity": 39.4, "ev": 39.4},
    {"hand": "83o", "equity": 37.5, "ev": 37.5},
    {"hand": "82o", "equity": 36.8, "ev": 36.8},
    {"hand": "76o", "equity": 42.3, "ev": 42.3},
    {"hand": "75o", "equity": 40.5, "ev": 40.5},
    {"hand": "74o", "equity": 38.6, "ev": 38.6},
    {"hand": "73o", "equity": 36.6, "ev": 36.6},
    {"hand": "72o", "equity": 34.6, "ev": 34.6},
    {"hand": "65o", "equity": 39.9, "ev": 39.9},
    {"hand": "64o", "equity": 38.0, "ev": 38.0},
    {"hand": "63o", "equity": 36.0, "ev": 36.0},
    {"hand": "62o", "equity": 34.0, "ev": 34.0},
    {"hand": "54o", "equity": 38.1, "ev": 38.1},
    {"hand": "53o", "equity": 36.3, "ev": 36.3},
    {"hand": "52o", "equity": 34.3, "ev": 34.3},
    {"hand": "43o", "equity": 35.1, "ev": 35.1},
    {"hand": "42o", "equity": 33.2, "ev": 33.2},
    {"hand": "32o", "equity": 32.3, "ev": 32.3}
]

default_hands_data_1 = [
    {"hand": "AA", "equity":  85.2, "ev": 156},
    {"hand": "KK", "equity":  82.4, "ev": 147},
    {"hand": "QQ", "equity":  79.9, "ev": 140},
    {"hand": "JJ", "equity":  77.5, "ev": 133},
    {"hand": "TT", "equity":  75.0, "ev": 125},
    {"hand": "99", "equity":  72.0, "ev": 116},
    {"hand": "88", "equity":  69.2, "ev": 108},
    {"hand": "77", "equity":  66.2, "ev": 99},
    {"hand": "66", "equity":  63.3, "ev": 90},
    {"hand": "55", "equity":  60.3, "ev": 81},
    {"hand": "44", "equity":  57.0, "ev": 71},
    {"hand": "33", "equity":  54.0, "ev": 62},
    {"hand": "22", "equity":  50.3, "ev": 0.0},  # No value provided
    {"hand": "AKs", "equity": 67.0, "ev": 101},
    {"hand": "AQs", "equity": 66.2, "ev": 99},
    {"hand": "AJs", "equity": 65.4, "ev": 96},
    {"hand": "ATs", "equity": 64.6, "ev": 94},
    {"hand": "A9s", "equity": 63.0, "ev": 89},
    {"hand": "A8s", "equity": 62.8, "ev": 88},
    {"hand": "A7s", "equity": 61.3, "ev": 84},
    {"hand": "A6s", "equity": 59.9, "ev": 80},
    {"hand": "A5s", "equity": 59.9, "ev": 80},
    {"hand": "A4s", "equity": 59.0, "ev": 77},
    {"hand": "A3s", "equity": 58.2, "ev": 75},
    {"hand": "A2s", "equity": 57.4, "ev": 72},
    {"hand": "KQs", "equity": 63.4, "ev": 90},
    {"hand": "KJs", "equity": 62.6, "ev": 88},
    {"hand": "KTs", "equity": 61.8, "ev": 85},
    {"hand": "K9s", "equity": 60.0, "ev": 80},
    {"hand": "K8s", "equity": 58.3, "ev": 75},
    {"hand": "K7s", "equity": 57.5, "ev": 72},
    {"hand": "K6s", "equity": 56.6, "ev": 70},
    {"hand": "K5s", "equity": 55.8, "ev": 67},
    {"hand": "K4s", "equity": 54.9, "ev": 65},
    {"hand": "K3s", "equity": 54.1, "ev": 62},
    {"hand": "K2s", "equity": 53.2, "ev": 60},
    {"hand": "QJs", "equity": 60.3, "ev": 81},
    {"hand": "QTs", "equity": 59.5, "ev": 78},
    {"hand": "Q9s", "equity": 57.7, "ev": 73},
    {"hand": "Q8s", "equity": 56.0, "ev": 68},
    {"hand": "Q7s", "equity": 54.3, "ev": 63},
    {"hand": "Q6s", "equity": 53.6, "ev": 61},
    {"hand": "Q5s", "equity": 53.0, "ev": 0},  # No value provided
    {"hand": "Q4s", "equity": 52.8, "ev": 0},  # No value provided
    {"hand": "Q3s", "equity": 51.0, "ev": 0},  # No value provided
    {"hand": "Q2s", "equity": 50.2, "ev": 0},  # No value provided
    {"hand": "JTs", "equity": 57.5, "ev": 72},
    {"hand": "J9s", "equity": 55.7, "ev": 67},
    {"hand": "J8s", "equity": 54.0, "ev": 62},
    {"hand": "J7s", "equity": 52.3, "ev": 0},  # No value provided
    {"hand": "J6s", "equity": 50.6, "ev": 0},  # No value provided
    {"hand": "J5s", "equity": 50.0, "ev": 0},  # No value provided
    {"hand": "J4s", "equity": 49.1, "ev": 0},  # No value provided
    {"hand": "J3s", "equity": 48.2, "ev": 0},  # No value provided
    {"hand": "J2s", "equity": 47.4, "ev": 0},  # No value provided
    {"hand": "T9s", "equity": 54.0, "ev": 0},  # No value provided
    {"hand": "T8s", "equity": 52.3, "ev": 0},  # No value provided
    {"hand": "T7s", "equity": 50.6, "ev": 0},  # No value provided
    {"hand": "T6s", "equity": 48.9, "ev": 0},  # No value provided
    {"hand": "T5s", "equity": 47.2, "ev": 0},  # No value provided
    {"hand": "T4s", "equity": 46.5, "ev": 0},  # No value provided
    {"hand": "T3s", "equity": 45.7, "ev": 0},  # No value provided
    {"hand": "T2s", "equity": 44.8, "ev": 0},  # No value provided
    {"hand": "98s", "equity": 50.8, "ev": 0},  # No value provided
    {"hand": "97s", "equity": 49.1, "ev": 0},  # No value provided
    {"hand": "96s", "equity": 47.4, "ev": 0},  # No value provided
    {"hand": "95s", "equity": 45.7, "ev": 0},  # No value provided
    {"hand": "94s", "equity": 43.9, "ev": 0},  # No value provided
    {"hand": "93s", "equity": 43.3, "ev": 0},  # No value provided
    {"hand": "92s", "equity": 42.4, "ev": 0},  # No value provided
    {"hand": "87s", "equity": 47.9, "ev": 0},  # No value provided
    {"hand": "86s", "equity": 46.2, "ev": 0},  # No value provided
    {"hand": "85s", "equity": 44.5, "ev": 0},  # No value provided
    {"hand": "84s", "equity": 42.7, "ev": 0},  # No value provided
    {"hand": "83s", "equity": 40.9, "ev": 0},  # No value provided
    {"hand": "82s", "equity": 40.3, "ev": 0},  # No value provided
    {"hand": "76s", "equity": 45.4, "ev": 0},  # No value provided
    {"hand": "75s", "equity": 43.7, "ev": 0},  # No value provided
    {"hand": "74s", "equity": 41.8, "ev": 0},  # No value provided
    {"hand": "73s", "equity": 40.0, "ev": 0},  # No value provided
    {"hand": "72s", "equity": 38.2, "ev": 0},  # No value provided
    {"hand": "65s", "equity": 43.1, "ev": 0},  # No value provided
    {"hand": "64s", "equity": 41.3, "ev": 0},  # No value provided
    {"hand": "63s", "equity": 39.5, "ev": 0},  # No value provided
    {"hand": "62s", "equity": 37.7, "ev": 0},  # No value provided
    {"hand": "54s", "equity": 41.5, "ev": 0},  # No value provided
    {"hand": "53s", "equity": 39.7, "ev": 0},  # No value provided
    {"hand": "52s", "equity": 37.8, "ev": 0},  # No value provided
    {"hand": "43s", "equity": 38.6, "ev": 0},  # No value provided
    {"hand": "42s", "equity": 36.8, "ev": 0},  # No value provided
    {"hand": "32s", "equity": 36.0, "ev": 0},  # No value provided
    {"hand": "AKo", "equity": 65.3, "ev": 0},  # No value provided
    {"hand": "AQo", "equity": 64.4, "ev": 0},  # No value provided
    {"hand": "AJo", "equity": 63.6, "ev": 0},  # No value provided
    {"hand": "ATo", "equity": 62.7, "ev": 0},  # No value provided
    {"hand": "A9o", "equity": 60.8, "ev": 6},
    {"hand": "A8o", "equity": 59.9, "ev": 63},
    {"hand": "A7o", "equity": 58.8, "ev": 66},
    {"hand": "A6o", "equity": 57.7, "ev": 0},  # No value provided
    {"hand": "A5o", "equity": 57.7, "ev": 0},  # No value provided
    {"hand": "A4o", "equity": 56.7, "ev": 0},  # No value provided
    {"hand": "A3o", "equity": 55.8, "ev": 63},
    {"hand": "A2o", "equity": 54.9, "ev": 68},
    {"hand": "KQo", "equity": 61.5, "ev": 70},
    {"hand": "KJo", "equity": 60.6, "ev": 73},
    {"hand": "KTo", "equity": 59.7, "ev": 0.0},  # No value provided
    {"hand": "K9o", "equity": 57.8, "ev": 61},
    {"hand": "K8o", "equity": 56.0, "ev": 66},
    {"hand": "K7o", "equity": 55.2, "ev": 72},
    {"hand": "K6o", "equity": 54.2, "ev": 77},
    {"hand": "K5o", "equity": 53.3, "ev": 79},
    {"hand": "K4o", "equity": 52.3, "ev": 64},
    {"hand": "K3o", "equity": 51.4, "ev": 69},
    {"hand": "K2o", "equity": 50.5, "ev": 75},
    {"hand": "QJo", "equity": 58.1, "ev": 80},
    {"hand": "QTo", "equity": 57.3, "ev": 85},
    {"hand": "Q9o", "equity": 55.4, "ev": 71},
    {"hand": "Q8o", "equity": 53.6, "ev": 76},
    {"hand": "Q7o", "equity": 51.8, "ev": 81},
    {"hand": "Q6o", "equity": 51.0, "ev": 87},
    {"hand": "Q5o", "equity": 50.1, "ev": 76},
    {"hand": "Q4o", "equity": 49.1, "ev": 0},  # No value provided
    {"hand": "Q3o", "equity": 48.2, "ev": 0},  # No value provided
    {"hand": "Q2o", "equity": 47.3, "ev": 0},  # No value provided
    {"hand": "JTo", "equity": 55.2, "ev": 81},
    {"hand": "J9o", "equity": 53.3, "ev": 87},
    {"hand": "J8o", "equity": 51.5, "ev": 84},
    {"hand": "J7o", "equity": 49.7, "ev": 0},  # No value provided
    {"hand": "J6o", "equity": 47.8, "ev": 0},  # No value provided
    {"hand": "J5o", "equity": 47.2, "ev": 0},  # No value provided
    {"hand": "J4o", "equity": 46.2, "ev": 0},  # No value provided
    {"hand": "J3o", "equity": 45.3, "ev": 0},  # No value provided
    {"hand": "J2o", "equity": 44.3, "ev": 0},  # No value provided
    {"hand": "T9o", "equity": 51.5, "ev": 9},
    {"hand": "T8o", "equity": 49.7, "ev": 0},  # No value provided
    {"hand": "T7o", "equity": 47.9, "ev": 0},  # No value provided
    {"hand": "T6o", "equity": 46.1, "ev": 0},  # No value provided
    {"hand": "T5o", "equity": 44.3, "ev": 0},  # No value provided
    {"hand": "T4o", "equity": 43.5, "ev": 0},  # No value provided
    {"hand": "T3o", "equity": 42.6, "ev": 0},  # No value provided
    {"hand": "T2o", "equity": 41.7, "ev": 0},  # No value provided
    {"hand": "98o", "equity": 48.1, "ev": 0},  # No value provided
    {"hand": "97o", "equity": 46.3, "ev": 0},  # No value provided
    {"hand": "96o", "equity": 44.5, "ev": 0},  # No value provided
    {"hand": "95o", "equity": 42.7, "ev": 0},  # No value provided
    {"hand": "94o", "equity": 40.7, "ev": 0},  # No value provided
    {"hand": "93o", "equity": 40.0, "ev": 0},  # No value provided
    {"hand": "92o", "equity": 39.0, "ev": 0},  # No value provided
    {"hand": "87o", "equity": 45.1, "ev": 0},  # No value provided
    {"hand": "86o", "equity": 43.0, "ev": 0},  # No value provided
    {"hand": "85o", "equity": 41.4, "ev": 0},  # No value provided
    {"hand": "84o", "equity": 39.4, "ev": 0},  # No value provided
    {"hand": "83o", "equity": 37.5, "ev": 0},  # No value provided
    {"hand": "82o", "equity": 36.8, "ev": 0},  # No value provided
    {"hand": "76o", "equity": 42.3, "ev": 0},  # No value provided
    {"hand": "75o", "equity": 40.5, "ev": 0},  # No value provided
    {"hand": "74o", "equity": 38.6, "ev": 0},  # No value provided
    {"hand": "73o", "equity": 36.6, "ev": 0},  # No value provided
    {"hand": "72o", "equity": 34.6, "ev": 0},  # No value provided
    {"hand": "65o", "equity": 39.9, "ev": 0},  # No value provided
    {"hand": "64o", "equity": 38.0, "ev": 0},  # No value provided
    {"hand": "63o", "equity": 36.0, "ev": 0},  # No value provided
    {"hand": "62o", "equity": 34.0, "ev": 0},  # No value provided
    {"hand": "54o", "equity": 38.1, "ev": 0},  # No value provided
    {"hand": "53o", "equity": 36.3, "ev": 0},  # No value provided
    {"hand": "52o", "equity": 34.3, "ev": 0},  # No value provided
    {"hand": "43o", "equity": 35.1, "ev": 0},  # No value provided
    {"hand": "42o", "equity": 33.2, "ev": 0},  # No value provided
    {"hand": "32o", "equity": 32.3, "ev": 0},  # No value provided
]
 




default_hands_data_2 = [
    {"hand": "AA", "equity":  85.2, "ev": 85.2},
    {"hand": "KK", "equity":  82.4, "ev": 82.4},
    {"hand": "QQ", "equity":  79.9, "ev": 79.9},
    {"hand": "JJ", "equity":  77.5, "ev": 77.5},
    {"hand": "TT", "equity":  75.0, "ev": 75.0},
    {"hand": "99", "equity":  72.0, "ev": 72.0},
    {"hand": "88", "equity":  69.2, "ev": 69.2},
    {"hand": "77", "equity":  66.2, "ev": 66.2},
    {"hand": "66", "equity":  63.3, "ev": 63.3},
    {"hand": "55", "equity":  60.3, "ev": 60.3},
    {"hand": "44", "equity":  57.0, "ev": 57.0},
    {"hand": "33", "equity":  54.0, "ev": 54.0},
    {"hand": "22", "equity":  50.3, "ev": 00.0},
    {"hand": "AKs", "equity": 67.0, "ev": 67.0},
    {"hand": "AQs", "equity": 66.2, "ev": 66.2},
    {"hand": "AJs", "equity": 65.4, "ev": 65.4},
    {"hand": "ATs", "equity": 64.6, "ev": 64.6},
    {"hand": "A9s", "equity": 63.0, "ev": 63.0},
    {"hand": "A8s", "equity": 62.8, "ev": 62.8},
    {"hand": "A7s", "equity": 61.3, "ev": 61.3},
    {"hand": "A6s", "equity": 59.9, "ev": 59.9},
    {"hand": "A5s", "equity": 59.9, "ev": 59.9},
    {"hand": "A4s", "equity": 59.0, "ev": 59.0},
    {"hand": "A3s", "equity": 58.2, "ev": 58.2},
    {"hand": "A2s", "equity": 57.4, "ev": 57.4},
    {"hand": "KQs", "equity": 63.4, "ev": 63.4},
    {"hand": "KJs", "equity": 62.6, "ev": 62.6},
    {"hand": "KTs", "equity": 61.8, "ev": 61.8},
    {"hand": "K9s", "equity": 60.0, "ev": 60.0},
    {"hand": "K8s", "equity": 58.3, "ev": 58.3},
    {"hand": "K7s", "equity": 57.5, "ev": 57.5},
    {"hand": "K6s", "equity": 56.6, "ev": 56.6},
    {"hand": "K5s", "equity": 55.8, "ev": 55.8},
    {"hand": "K4s", "equity": 54.9, "ev": 54.9},
    {"hand": "K3s", "equity": 54.1, "ev": 54.1},
    {"hand": "K2s", "equity": 53.2, "ev": 53.2},
    {"hand": "QJs", "equity": 60.3, "ev": 60.3},
    {"hand": "QTs", "equity": 59.5, "ev": 59.5},
    {"hand": "Q9s", "equity": 57.7, "ev": 57.7},
    {"hand": "Q8s", "equity": 56.0, "ev": 56.0},
    {"hand": "Q7s", "equity": 54.3, "ev": 54.3},
    {"hand": "Q6s", "equity": 53.6, "ev": 53.6},
    {"hand": "Q5s", "equity": 53.0, "ev": 00.0},
    {"hand": "Q4s", "equity": 52.8, "ev": 52.8},
    {"hand": "Q3s", "equity": 51.0, "ev": 00.0},
    {"hand": "Q2s", "equity": 50.2, "ev": 00.0},
    {"hand": "JTs", "equity": 57.5, "ev": 57.5},
    {"hand": "J9s", "equity": 55.7, "ev": 55.7},
    {"hand": "J8s", "equity": 54.0, "ev": 54.0},
    {"hand": "J7s", "equity": 52.3, "ev": 00.0},
    {"hand": "J6s", "equity": 50.6, "ev": 00.0},
    {"hand": "J5s", "equity": 50.0, "ev": 00.0},
    {"hand": "J4s", "equity": 49.1, "ev": 49.1},
    {"hand": "J3s", "equity": 48.2, "ev": 00.0},
    {"hand": "J2s", "equity": 47.4, "ev": 00.0},
    {"hand": "T9s", "equity": 54.0, "ev": 54.0},
    {"hand": "T8s", "equity": 52.3, "ev": 00.0},
    {"hand": "T7s", "equity": 50.6, "ev": 00.0},
    {"hand": "T6s", "equity": 48.9, "ev": 00.0},
    {"hand": "T5s", "equity": 47.2, "ev": 00.0},
    {"hand": "T4s", "equity": 46.5, "ev": 46.5},
    {"hand": "T3s", "equity": 45.7, "ev": 45.7},
    {"hand": "T2s", "equity": 44.8, "ev": 44.8},
    {"hand": "98s", "equity": 50.8, "ev": 50.8},
    {"hand": "97s", "equity": 49.1, "ev": 49.1},
    {"hand": "96s", "equity": 47.4, "ev": 47.4},
    {"hand": "95s", "equity": 45.7, "ev": 45.7},
    {"hand": "94s", "equity": 43.9, "ev": 43.9},
    {"hand": "93s", "equity": 43.3, "ev": 43.3},
    {"hand": "92s", "equity": 42.4, "ev": 42.4},
    {"hand": "87s", "equity": 47.9, "ev": 00.0},
    {"hand": "86s", "equity": 46.2, "ev": 46.2},
    {"hand": "85s", "equity": 44.5, "ev": 44.5},
    {"hand": "84s", "equity": 42.7, "ev": 42.7},
    {"hand": "83s", "equity": 40.9, "ev": 40.9},
    {"hand": "82s", "equity": 40.3, "ev": 40.3},
    {"hand": "76s", "equity": 45.4, "ev": 45.4},
    {"hand": "75s", "equity": 43.7, "ev": 43.7},
    {"hand": "74s", "equity": 41.8, "ev": 41.8},
    {"hand": "73s", "equity": 40.0, "ev": 40.0},
    {"hand": "72s", "equity": 38.2, "ev": 38.2},
    {"hand": "65s", "equity": 43.1, "ev": 43.1},
    {"hand": "64s", "equity": 41.3, "ev": 41.3},
    {"hand": "63s", "equity": 39.5, "ev": 39.5},
    {"hand": "62s", "equity": 37.7, "ev": 37.7},
    {"hand": "54s", "equity": 41.5, "ev": 41.5},
    {"hand": "53s", "equity": 39.7, "ev": 39.7},
    {"hand": "52s", "equity": 37.8, "ev": 37.8},
    {"hand": "43s", "equity": 38.6, "ev": 38.6},
    {"hand": "42s", "equity": 36.8, "ev": 36.8},
    {"hand": "32s", "equity": 36.0, "ev": 36.0},
    {"hand": "AKo", "equity": 65.3, "ev": 65.3},
    {"hand": "AQo", "equity": 64.4, "ev": 64.4},
    {"hand": "AJo", "equity": 63.6, "ev": 63.6},
    {"hand": "ATo", "equity": 62.7, "ev": 62.7},
    {"hand": "A9o", "equity": 60.8, "ev": 60.8},
    {"hand": "A8o", "equity": 59.9, "ev": 59.9},
    {"hand": "A7o", "equity": 58.8, "ev": 58.8},
    {"hand": "A6o", "equity": 57.7, "ev": 57.7},
    {"hand": "A5o", "equity": 57.7, "ev": 57.7},
    {"hand": "A4o", "equity": 56.7, "ev": 56.7},
    {"hand": "A3o", "equity": 55.8, "ev": 55.8},
    {"hand": "A2o", "equity": 54.9, "ev": 54.9},
    {"hand": "KQo", "equity": 61.5, "ev": 61.5},
    {"hand": "KJo", "equity": 60.6, "ev": 60.6},
    {"hand": "KTo", "equity": 59.7, "ev": 59.7},
    {"hand": "K9o", "equity": 57.8, "ev": 57.8},
    {"hand": "K8o", "equity": 56.0, "ev": 56.0},
    {"hand": "K7o", "equity": 55.2, "ev": 00.0},
    {"hand": "K6o", "equity": 54.2, "ev": 00.0},
    {"hand": "K5o", "equity": 53.3, "ev": 00.0},
    {"hand": "K4o", "equity": 52.3, "ev": 52.3},
    {"hand": "K3o", "equity": 51.4, "ev": 00.0},
    {"hand": "K2o", "equity": 50.5, "ev": 00.0},
    {"hand": "QJo", "equity": 58.1, "ev": 58.1},
    {"hand": "QTo", "equity": 57.3, "ev": 57.3},
    {"hand": "Q9o", "equity": 55.4, "ev": 55.4},
    {"hand": "Q8o", "equity": 53.6, "ev": 53.6},
    {"hand": "Q7o", "equity": 51.8, "ev": 00.0},
    {"hand": "Q6o", "equity": 51.0, "ev": 00.0},
    {"hand": "Q5o", "equity": 50.1, "ev": 00.0},
    {"hand": "Q4o", "equity": 49.1, "ev": 49.1},
    {"hand": "Q3o", "equity": 48.2, "ev": 00.0},
    {"hand": "Q2o", "equity": 47.3, "ev": 00.0},
    {"hand": "JTo", "equity": 55.2, "ev": 55.2},
    {"hand": "J9o", "equity": 53.3, "ev": 53.3},
    {"hand": "J8o", "equity": 51.5, "ev": 00.0},
    {"hand": "J7o", "equity": 49.7, "ev": 00.0},
    {"hand": "J6o", "equity": 47.8, "ev": 00.0},
    {"hand": "J5o", "equity": 47.2, "ev": 00.0},
    {"hand": "J4o", "equity": 46.2, "ev": 46.2},
    {"hand": "J3o", "equity": 45.3, "ev": 45.3},
    {"hand": "J2o", "equity": 44.3, "ev": 44.3},
    {"hand": "T9o", "equity": 51.5, "ev": 51.5},
    {"hand": "T8o", "equity": 49.7, "ev": 00.0},
    {"hand": "T7o", "equity": 47.9, "ev": 00.0},
    {"hand": "T6o", "equity": 46.1, "ev": 46.1},
    {"hand": "T5o", "equity": 44.3, "ev": 44.3},
    {"hand": "T4o", "equity": 43.5, "ev": 43.5},
    {"hand": "T3o", "equity": 42.6, "ev": 42.6},
    {"hand": "T2o", "equity": 41.7, "ev": 41.7},
    {"hand": "98o", "equity": 48.1, "ev": 48.1},
    {"hand": "97o", "equity": 46.3, "ev": 46.3},
    {"hand": "96o", "equity": 44.5, "ev": 44.5},
    {"hand": "95o", "equity": 42.7, "ev": 42.7},
    {"hand": "94o", "equity": 40.7, "ev": 40.7},
    {"hand": "93o", "equity": 40.0, "ev": 40.0},
    {"hand": "92o", "equity": 39.0, "ev": 39.0},
    {"hand": "87o", "equity": 45.1, "ev": 45.1},
    {"hand": "86o", "equity": 43.0, "ev": 43.0},
    {"hand": "85o", "equity": 41.4, "ev": 41.4},
    {"hand": "84o", "equity": 39.4, "ev": 39.4},
    {"hand": "83o", "equity": 37.5, "ev": 37.5},
    {"hand": "82o", "equity": 36.8, "ev": 36.8},
    {"hand": "76o", "equity": 42.3, "ev": 42.3},
    {"hand": "75o", "equity": 40.5, "ev": 40.5},
    {"hand": "74o", "equity": 38.6, "ev": 38.6},
    {"hand": "73o", "equity": 36.6, "ev": 36.6},
    {"hand": "72o", "equity": 34.6, "ev": 34.6},
    {"hand": "65o", "equity": 39.9, "ev": 39.9},
    {"hand": "64o", "equity": 38.0, "ev": 38.0},
    {"hand": "63o", "equity": 36.0, "ev": 36.0},
    {"hand": "62o", "equity": 34.0, "ev": 34.0},
    {"hand": "54o", "equity": 38.1, "ev": 38.1},
    {"hand": "53o", "equity": 36.3, "ev": 36.3},
    {"hand": "52o", "equity": 34.3, "ev": 34.3},
    {"hand": "43o", "equity": 35.1, "ev": 35.1},
    {"hand": "42o", "equity": 33.2, "ev": 33.2},
    {"hand": "32o", "equity": 32.3, "ev": 32.3}
]


default_hands_data_3 = [
    {"hand": "AA", "equity":  85.2, "ev": 156.00},
    {"hand": "KK", "equity":  82.4, "ev": 147.00},
    {"hand": "QQ", "equity":  79.9, "ev": 140.00},
    {"hand": "JJ", "equity":  77.5, "ev": 133.00},
    {"hand": "TT", "equity":  75.0, "ev": 125.00},
    {"hand": "99", "equity":  72.0, "ev": 116.00},
    {"hand": "88", "equity":  69.2, "ev": 108.00},
    {"hand": "77", "equity":  66.2, "ev": 99.00},
    {"hand": "66", "equity":  63.3, "ev": 90.00},
    {"hand": "55", "equity":  60.3, "ev": 81.00},
    {"hand": "44", "equity":  57.0, "ev": 71.00},
    {"hand": "33", "equity":  54.0, "ev": 62.00},
    {"hand": "22", "equity":  50.3, "ev": 00.00},  # No value provided
    {"hand": "AKs", "equity": 67.0, "ev": 101.00},
    {"hand": "AQs", "equity": 66.2, "ev": 99.00},
    {"hand": "AJs", "equity": 65.4, "ev": 96.00},
    {"hand": "ATs", "equity": 64.6, "ev": 94.00},
    {"hand": "A9s", "equity": 63.0, "ev": 89.00},
    {"hand": "A8s", "equity": 62.8, "ev": 88.00},
    {"hand": "A7s", "equity": 61.3, "ev": 84.00},
    {"hand": "A6s", "equity": 59.9, "ev": 80.00},
    {"hand": "A5s", "equity": 59.9, "ev": 80.00},
    {"hand": "A4s", "equity": 59.0, "ev": 77.00},
    {"hand": "A3s", "equity": 58.2, "ev": 75.00},
    {"hand": "A2s", "equity": 57.4, "ev": 72.00},
    {"hand": "KQs", "equity": 63.4, "ev": 90.00},
    {"hand": "KJs", "equity": 62.6, "ev": 88.00},
    {"hand": "KTs", "equity": 61.8, "ev": 85.00},
    {"hand": "K9s", "equity": 60.0, "ev": 80.00},
    {"hand": "K8s", "equity": 58.3, "ev": 75.00},
    {"hand": "K7s", "equity": 57.5, "ev": 72.00},
    {"hand": "K6s", "equity": 56.6, "ev": 70.00},
    {"hand": "K5s", "equity": 55.8, "ev": 67.00},
    {"hand": "K4s", "equity": 54.9, "ev": 65.00},
    {"hand": "K3s", "equity": 54.1, "ev": 62.00},
    {"hand": "K2s", "equity": 53.2, "ev": 60.00},
    {"hand": "QJs", "equity": 60.3, "ev": 81.00},
    {"hand": "QTs", "equity": 59.5, "ev": 78.00},
    {"hand": "Q9s", "equity": 57.7, "ev": 73.00},
    {"hand": "Q8s", "equity": 56.0, "ev": 68.00},
    {"hand": "Q7s", "equity": 54.3, "ev": 63.00},
    {"hand": "Q6s", "equity": 53.6, "ev": 61.00},
    {"hand": "Q5s", "equity": 53.0, "ev": 00.00},  # No value provided
    {"hand": "Q4s", "equity": 52.8, "ev": 58.28},
    {"hand": "Q3s", "equity": 51.0, "ev": 00.00},  # No value provided
    {"hand": "Q2s", "equity": 50.2, "ev": 00.00},  # No value provided
    {"hand": "JTs", "equity": 57.5, "ev": 72.00},
    {"hand": "J9s", "equity": 55.7, "ev": 67.00},
    {"hand": "J8s", "equity": 54.0, "ev": 62.00},
    {"hand": "J7s", "equity": 52.3, "ev": 00.00},  # No value provided
    {"hand": "J6s", "equity": 50.6, "ev": 00.00},  # No value provided
    {"hand": "J5s", "equity": 50.0, "ev": 00.00},  # No value provided
    {"hand": "J4s", "equity": 49.1, "ev": 57.80},
    {"hand": "J3s", "equity": 48.2, "ev": 00.00},  # No value provided
    {"hand": "J2s", "equity": 47.4, "ev": 00.00},  # No value provided
    {"hand": "T9s", "equity": 54.0, "ev": 62.00},
    {"hand": "T8s", "equity": 52.3, "ev": 00.00},  # No value provided
    {"hand": "T7s", "equity": 50.6, "ev": 00.00},  # No value provided
    {"hand": "T6s", "equity": 48.9, "ev": 00.00},  # No value provided
    {"hand": "T5s", "equity": 47.2, "ev": 00.00},  # No value provided
    {"hand": "T4s", "equity": 46.5, "ev": 60.00},
    {"hand": "T3s", "equity": 45.7, "ev": 63.00},
    {"hand": "T2s", "equity": 44.8, "ev": 66.00},
    {"hand": "98s", "equity": 50.8, "ev": 68.23},
    {"hand": "97s", "equity": 49.1, "ev": 68.55},
    {"hand": "96s", "equity": 47.4, "ev": 68.12},
    {"hand": "95s", "equity": 45.7, "ev": 62.99},
    {"hand": "94s", "equity": 43.9, "ev": 68.00},
    {"hand": "93s", "equity": 43.3, "ev": 69.99},
    {"hand": "92s", "equity": 42.4, "ev": 73.00},
    {"hand": "87s", "equity": 47.9, "ev": 00.00},  # No value provided
    {"hand": "86s", "equity": 46.2, "ev": 61.00},
    {"hand": "85s", "equity": 44.5, "ev": 66.00},
    {"hand": "84s", "equity": 42.7, "ev": 72.00},
    {"hand": "83s", "equity": 40.9, "ev": 77.00},
    {"hand": "82s", "equity": 40.3, "ev": 79.00},
    {"hand": "76s", "equity": 45.4, "ev": 64.00},
    {"hand": "75s", "equity": 43.7, "ev": 69.00},
    {"hand": "74s", "equity": 41.8, "ev": 75.00},
    {"hand": "73s", "equity": 40.0, "ev": 80.00},
    {"hand": "72s", "equity": 38.2, "ev": 85.00},
    {"hand": "65s", "equity": 43.1, "ev": 71.00},
    {"hand": "64s", "equity": 41.3, "ev": 76.00},
    {"hand": "63s", "equity": 39.5, "ev": 81.00},
    {"hand": "62s", "equity": 37.7, "ev": 87.00},
    {"hand": "54s", "equity": 41.5, "ev": 76.00},
    {"hand": "53s", "equity": 39.7, "ev": 81.00},
    {"hand": "52s", "equity": 37.8, "ev": 87.00},
    {"hand": "43s", "equity": 38.6, "ev": 84.00},
    {"hand": "42s", "equity": 36.8, "ev": 90.00},
    {"hand": "32s", "equity": 36.0, "ev": 92.00},
    {"hand": "AKo", "equity": 65.3, "ev": 96.00},
    {"hand": "AQo", "equity": 64.4, "ev": 93.00},
    {"hand": "AJo", "equity": 63.6, "ev": 91.00},
    {"hand": "ATo", "equity": 62.7, "ev": 88.00},
    {"hand": "A9o", "equity": 60.8, "ev": 82.00},
    {"hand": "A8o", "equity": 59.9, "ev": 80.00},
    {"hand": "A7o", "equity": 58.8, "ev": 76.00},
    {"hand": "A6o", "equity": 57.7, "ev": 73.00},
    {"hand": "A5o", "equity": 57.7, "ev": 73.00},
    {"hand": "A4o", "equity": 56.7, "ev": 70.00},
    {"hand": "A3o", "equity": 55.8, "ev": 67.00},
    {"hand": "A2o", "equity": 54.9, "ev": 65.00},
    {"hand": "KQo", "equity": 61.5, "ev": 84.00},
    {"hand": "KJo", "equity": 60.6, "ev": 82.00},
    {"hand": "KTo", "equity": 59.7, "ev": 79.00},
    {"hand": "K9o", "equity": 57.8, "ev": 73.00},
    {"hand": "K8o", "equity": 56.0, "ev": 68.00},
    {"hand": "K7o", "equity": 55.2, "ev": 00.00},
    {"hand": "K6o", "equity": 54.2, "ev": 00.00},
    {"hand": "K5o", "equity": 53.3, "ev": 00.00},
    {"hand": "K4o", "equity": 52.3, "ev": 57.90},
    {"hand": "K3o", "equity": 51.4, "ev": 00.00},
    {"hand": "K2o", "equity": 50.5, "ev": 00.00},
    {"hand": "QJo", "equity": 58.1, "ev": 74.00},
    {"hand": "QTo", "equity": 57.3, "ev": 72.00},
    {"hand": "Q9o", "equity": 55.4, "ev": 66.00},
    {"hand": "Q8o", "equity": 53.6, "ev": 61.00},
    {"hand": "Q7o", "equity": 51.8, "ev": 00.00},
    {"hand": "Q6o", "equity": 51.0, "ev": 00.00},
    {"hand": "Q5o", "equity": 50.1, "ev": 00.00},
    {"hand": "Q4o", "equity": 49.1, "ev": 53.00},
    {"hand": "Q3o", "equity": 48.2, "ev": 00.00},
    {"hand": "Q2o", "equity": 47.3, "ev": 00.00},
    {"hand": "JTo", "equity": 55.2, "ev": 66.00},
    {"hand": "J9o", "equity": 53.3, "ev": 00.00},
    {"hand": "J8o", "equity": 51.5, "ev": 00.00},  # No value provided
    {"hand": "J7o", "equity": 49.7, "ev": 00.00},
    {"hand": "J6o", "equity": 47.8, "ev": 00.00},
    {"hand": "J5o", "equity": 47.2, "ev": 00.00},
    {"hand": "J4o", "equity": 46.2, "ev": 61.00},
    {"hand": "J3o", "equity": 45.3, "ev": 64.00},
    {"hand": "J2o", "equity": 44.3, "ev": 67.00},
    {"hand": "T9o", "equity": 51.5, "ev": 00.00},  # No value provided
    {"hand": "T8o", "equity": 49.7, "ev": 00.00},  # No value provided
    {"hand": "T7o", "equity": 47.9, "ev": 00.00},  # No value provided
    {"hand": "T6o", "equity": 46.1, "ev": 62.00},
    {"hand": "T5o", "equity": 44.3, "ev": 67.00},
    {"hand": "T4o", "equity": 43.5, "ev": 69.00},
    {"hand": "T3o", "equity": 42.6, "ev": 72.00},
    {"hand": "T2o", "equity": 41.7, "ev": 75.00},
    {"hand": "98o", "equity": 48.1, "ev": 67.50},
    {"hand": "97o", "equity": 46.3, "ev": 61.00},
    {"hand": "96o", "equity": 44.5, "ev": 66.00},
    {"hand": "95o", "equity": 42.7, "ev": 72.00},
    {"hand": "94o", "equity": 40.7, "ev": 78.00},
    {"hand": "93o", "equity": 40.0, "ev": 80.00},
    {"hand": "92o", "equity": 39.0, "ev": 83.00},
    {"hand": "87o", "equity": 45.1, "ev": 65.00},
    {"hand": "86o", "equity": 43.0, "ev": 71.00},
    {"hand": "85o", "equity": 41.4, "ev": 76.00},
    {"hand": "84o", "equity": 39.4, "ev": 82.00},
    {"hand": "83o", "equity": 37.5, "ev": 88.00},
    {"hand": "82o", "equity": 36.8, "ev": 90.00},
    {"hand": "76o", "equity": 42.3, "ev": 73.00},
    {"hand": "75o", "equity": 40.5, "ev": 78.00},
    {"hand": "74o", "equity": 38.6, "ev": 84.00},
    {"hand": "73o", "equity": 36.6, "ev": 90.00},
    {"hand": "72o", "equity": 34.6, "ev": 96.00},
    {"hand": "65o", "equity": 39.9, "ev": 80.00},
    {"hand": "64o", "equity": 38.0, "ev": 86.00},
    {"hand": "63o", "equity": 36.0, "ev": 92.00},
    {"hand": "62o", "equity": 34.0, "ev": 98.00},
    {"hand": "54o", "equity": 38.1, "ev": 86.00},
    {"hand": "53o", "equity": 36.3, "ev": 91.00},
    {"hand": "52o", "equity": 34.3, "ev": 97.00},
    {"hand": "43o", "equity": 35.1, "ev": 95.00},
    {"hand": "42o", "equity": 33.2, "ev": 100.00}, 
    {"hand": "32o", "equity": 32.3, "ev": 400.00}
]



default_hands_data = [
    {"hand": "AA", "equity":  85.2, "ev": 85.2},
    {"hand": "KK", "equity":  82.4, "ev": 82.4},
    {"hand": "QQ", "equity":  79.9, "ev": 79.9},
    {"hand": "JJ", "equity":  77.5, "ev": 77.5},
    {"hand": "TT", "equity":  75.0, "ev": 75.0},
    {"hand": "99", "equity":  72.0, "ev": 72.0},
    {"hand": "88", "equity":  69.2, "ev": 69.2},
    {"hand": "77", "equity":  66.2, "ev": 66.2},
    {"hand": "66", "equity":  63.3, "ev": 63.3},
    {"hand": "55", "equity":  60.3, "ev": 60.3},
    {"hand": "44", "equity":  57.0, "ev": 57.0},
    {"hand": "33", "equity":  54.0, "ev": 54.0},
    {"hand": "22", "equity":  50.3, "ev": 50.3},
    {"hand": "AKs", "equity": 67.0, "ev": 67.0},
    {"hand": "AQs", "equity": 66.2, "ev": 66.2},
    {"hand": "AJs", "equity": 65.4, "ev": 65.4},
    {"hand": "ATs", "equity": 64.6, "ev": 64.6},
    {"hand": "A9s", "equity": 63.0, "ev": 63.0},
    {"hand": "A8s", "equity": 62.8, "ev": 62.8},
    {"hand": "A7s", "equity": 61.3, "ev": 61.3},
    {"hand": "A6s", "equity": 59.9, "ev": 59.9},
    {"hand": "A5s", "equity": 59.9, "ev": 59.9},
    {"hand": "A4s", "equity": 59.0, "ev": 59.0},
    {"hand": "A3s", "equity": 58.2, "ev": 58.2},
    {"hand": "A2s", "equity": 57.4, "ev": 57.4},
    {"hand": "KQs", "equity": 63.4, "ev": 63.4},
    {"hand": "KJs", "equity": 62.6, "ev": 62.6},
    {"hand": "KTs", "equity": 61.8, "ev": 61.8},
    {"hand": "K9s", "equity": 60.0, "ev": 60.0},
    {"hand": "K8s", "equity": 58.3, "ev": 58.3},
    {"hand": "K7s", "equity": 57.5, "ev": 57.5},
    {"hand": "K6s", "equity": 56.6, "ev": 56.6},
    {"hand": "K5s", "equity": 55.8, "ev": 55.8},
    {"hand": "K4s", "equity": 54.9, "ev": 54.9},
    {"hand": "K3s", "equity": 54.1, "ev": 54.1},
    {"hand": "K2s", "equity": 53.2, "ev": 53.2},
    {"hand": "QJs", "equity": 60.3, "ev": 60.3},
    {"hand": "QTs", "equity": 59.5, "ev": 59.5},
    {"hand": "Q9s", "equity": 57.7, "ev": 57.7},
    {"hand": "Q8s", "equity": 56.0, "ev": 56.0},
    {"hand": "Q7s", "equity": 54.3, "ev": 54.3},
    {"hand": "Q6s", "equity": 53.6, "ev": 53.6},
    {"hand": "Q5s", "equity": 53.0, "ev": 53.0},
    {"hand": "Q4s", "equity": 52.8, "ev": 52.8},
    {"hand": "Q3s", "equity": 51.0, "ev": 51.0},
    {"hand": "Q2s", "equity": 50.2, "ev": 50.2},
    {"hand": "JTs", "equity": 57.5, "ev": 57.5},
    {"hand": "J9s", "equity": 55.7, "ev": 55.7},
    {"hand": "J8s", "equity": 54.0, "ev": 54.0},
    {"hand": "J7s", "equity": 52.3, "ev": 52.3},
    {"hand": "J6s", "equity": 50.6, "ev": 50.6},
    {"hand": "J5s", "equity": 50.0, "ev": 50.0},
    {"hand": "J4s", "equity": 49.1, "ev": 49.1},
    {"hand": "J3s", "equity": 48.2, "ev": 48.2},
    {"hand": "J2s", "equity": 47.4, "ev": 47.4},
    {"hand": "T9s", "equity": 54.0, "ev": 54.0},
    {"hand": "T8s", "equity": 52.3, "ev": 52.3},
    {"hand": "T7s", "equity": 50.6, "ev": 50.6},
    {"hand": "T6s", "equity": 48.9, "ev": 48.9},
    {"hand": "T5s", "equity": 47.2, "ev": 47.2},
    {"hand": "T4s", "equity": 46.5, "ev": 46.5},
    {"hand": "T3s", "equity": 45.7, "ev": 45.7},
    {"hand": "T2s", "equity": 44.8, "ev": 44.8},
    {"hand": "98s", "equity": 50.8, "ev": 50.8},
    {"hand": "97s", "equity": 49.1, "ev": 49.1},
    {"hand": "96s", "equity": 47.4, "ev": 47.4},
    {"hand": "95s", "equity": 45.7, "ev": 45.7},
    {"hand": "94s", "equity": 43.9, "ev": 43.9},
    {"hand": "93s", "equity": 43.3, "ev": 43.3},
    {"hand": "92s", "equity": 42.4, "ev": 42.4},
    {"hand": "87s", "equity": 47.9, "ev": 47.9},
    {"hand": "86s", "equity": 46.2, "ev": 46.2},
    {"hand": "85s", "equity": 44.5, "ev": 44.5},
    {"hand": "84s", "equity": 42.7, "ev": 42.7},
    {"hand": "83s", "equity": 40.9, "ev": 40.9},
    {"hand": "82s", "equity": 40.3, "ev": 40.3},
    {"hand": "76s", "equity": 45.4, "ev": 45.4},
    {"hand": "75s", "equity": 43.7, "ev": 43.7},
    {"hand": "74s", "equity": 41.8, "ev": 41.8},
    {"hand": "73s", "equity": 40.0, "ev": 40.0},
    {"hand": "72s", "equity": 38.2, "ev": 38.2},
    {"hand": "65s", "equity": 43.1, "ev": 43.1},
    {"hand": "64s", "equity": 41.3, "ev": 41.3},
    {"hand": "63s", "equity": 39.5, "ev": 39.5},
    {"hand": "62s", "equity": 37.7, "ev": 37.7},
    {"hand": "54s", "equity": 41.5, "ev": 41.5},
    {"hand": "53s", "equity": 39.7, "ev": 39.7},
    {"hand": "52s", "equity": 37.8, "ev": 37.8},
    {"hand": "43s", "equity": 38.6, "ev": 38.6},
    {"hand": "42s", "equity": 36.8, "ev": 36.8},
    {"hand": "32s", "equity": 36.0, "ev": 36.0},
    {"hand": "AKo", "equity": 65.3, "ev": 65.3},
    {"hand": "AQo", "equity": 64.4, "ev": 64.4},
    {"hand": "AJo", "equity": 63.6, "ev": 63.6},
    {"hand": "ATo", "equity": 62.7, "ev": 62.7},
    {"hand": "A9o", "equity": 60.8, "ev": 60.8},
    {"hand": "A8o", "equity": 59.9, "ev": 59.9},
    {"hand": "A7o", "equity": 58.8, "ev": 58.8},
    {"hand": "A6o", "equity": 57.7, "ev": 57.7},
    {"hand": "A5o", "equity": 57.7, "ev": 57.7},
    {"hand": "A4o", "equity": 56.7, "ev": 56.7},
    {"hand": "A3o", "equity": 55.8, "ev": 55.8},
    {"hand": "A2o", "equity": 54.9, "ev": 54.9},
    {"hand": "KQo", "equity": 61.5, "ev": 61.5},
    {"hand": "KJo", "equity": 60.6, "ev": 60.6},
    {"hand": "KTo", "equity": 59.7, "ev": 59.7},
    {"hand": "K9o", "equity": 57.8, "ev": 57.8},
    {"hand": "K8o", "equity": 56.0, "ev": 56.0},
    {"hand": "K7o", "equity": 55.2, "ev": 55.2},
    {"hand": "K6o", "equity": 54.2, "ev": 54.2},
    {"hand": "K5o", "equity": 53.3, "ev": 53.3},
    {"hand": "K4o", "equity": 52.3, "ev": 52.3},
    {"hand": "K3o", "equity": 51.4, "ev": 51.4},
    {"hand": "K2o", "equity": 50.5, "ev": 50.5},
    {"hand": "QJo", "equity": 58.1, "ev": 58.1},
    {"hand": "QTo", "equity": 57.3, "ev": 57.3},
    {"hand": "Q9o", "equity": 55.4, "ev": 55.4},
    {"hand": "Q8o", "equity": 53.6, "ev": 53.6},
    {"hand": "Q7o", "equity": 51.8, "ev": 51.8},
    {"hand": "Q6o", "equity": 51.0, "ev": 51.0},
    {"hand": "Q5o", "equity": 50.1, "ev": 50.1},
    {"hand": "Q4o", "equity": 49.1, "ev": 49.1},
    {"hand": "Q3o", "equity": 48.2, "ev": 48.2},
    {"hand": "Q2o", "equity": 47.3, "ev": 47.3},
    {"hand": "JTo", "equity": 55.2, "ev": 55.2},
    {"hand": "J9o", "equity": 53.3, "ev": 53.3},
    {"hand": "J8o", "equity": 51.5, "ev": 51.5},
    {"hand": "J7o", "equity": 49.7, "ev": 49.7},
    {"hand": "J6o", "equity": 47.8, "ev": 47.8},
    {"hand": "J5o", "equity": 47.2, "ev": 47.2},
    {"hand": "J4o", "equity": 46.2, "ev": 46.2},
    {"hand": "J3o", "equity": 45.3, "ev": 45.3},
    {"hand": "J2o", "equity": 44.3, "ev": 44.3},
    {"hand": "T9o", "equity": 51.5, "ev": 51.5},
    {"hand": "T8o", "equity": 49.7, "ev": 49.7},
    {"hand": "T7o", "equity": 47.9, "ev": 47.9},
    {"hand": "T6o", "equity": 46.1, "ev": 46.1},
    {"hand": "T5o", "equity": 44.3, "ev": 44.3},
    {"hand": "T4o", "equity": 43.5, "ev": 43.5},
    {"hand": "T3o", "equity": 42.6, "ev": 42.6},
    {"hand": "T2o", "equity": 41.7, "ev": 41.7},
    {"hand": "98o", "equity": 48.1, "ev": 48.1},
    {"hand": "97o", "equity": 46.3, "ev": 46.3},
    {"hand": "96o", "equity": 44.5, "ev": 44.5},
    {"hand": "95o", "equity": 42.7, "ev": 42.7},
    {"hand": "94o", "equity": 40.7, "ev": 40.7},
    {"hand": "93o", "equity": 40.0, "ev": 40.0},
    {"hand": "92o", "equity": 39.0, "ev": 39.0},
    {"hand": "87o", "equity": 45.1, "ev": 45.1},
    {"hand": "86o", "equity": 43.0, "ev": 43.0},
    {"hand": "85o", "equity": 41.4, "ev": 41.4},
    {"hand": "84o", "equity": 39.4, "ev": 39.4},
    {"hand": "83o", "equity": 37.5, "ev": 37.5},
    {"hand": "82o", "equity": 36.8, "ev": 36.8},
    {"hand": "76o", "equity": 42.3, "ev": 42.3},
    {"hand": "75o", "equity": 40.5, "ev": 40.5},
    {"hand": "74o", "equity": 38.6, "ev": 38.6},
    {"hand": "73o", "equity": 36.6, "ev": 36.6},
    {"hand": "72o", "equity": 34.6, "ev": 34.6},
    {"hand": "65o", "equity": 39.9, "ev": 39.9},
    {"hand": "64o", "equity": 38.0, "ev": 38.0},
    {"hand": "63o", "equity": 36.0, "ev": 36.0},
    {"hand": "62o", "equity": 34.0, "ev": 34.0},
    {"hand": "54o", "equity": 38.1, "ev": 38.1},
    {"hand": "53o", "equity": 36.3, "ev": 36.3},
    {"hand": "52o", "equity": 34.3, "ev": 34.3},
    {"hand": "43o", "equity": 35.1, "ev": 35.1},
    {"hand": "42o", "equity": 33.2, "ev": 33.2},
    {"hand": "32o", "equity": 32.3, "ev": 32.3}
]

def determine_opponents_range(opponent_bet, total_pot, hands_data):
    opponent_range = []
    advertised_equity = opponent_bet / (opponent_bet + total_pot)
    for hand in hands_data:
        if hand['equity'] >= advertised_equity * 100:
            opponent_range.append(hand['hand'])
    return opponent_range
    
@app.route('/ev_hand/<hand_name>')
def ev_hand_detail(hand_name):
    hand = get_hand_data2(hand_name)
    if hand:
        original_ev = hand['ev'] / 100

        # Retrieve pot size and bet size from session
        pot_size = session.get('pot_size', 0)
        bet_size = session.get('bet_size', 0)

        total_pot = pot_size + bet_size
        pot_odds = (bet_size / total_pot) * 100 if total_pot > 0 else 0

        # Set default values if not present in session
        opponent_pot_size = session.get('opponent_pot_size', 0)
        opponent_bet_size = session.get('opponent_bet_size', 0)

        # Calculate advertised pot odds for opponent's bet
        total_opponent_pot = opponent_pot_size + opponent_bet_size
        opponent_pot_odds = (opponent_bet_size / total_opponent_pot) * 100 if total_opponent_pot > 0 else 0
        

        # Calculate EV
        ev_value = ((hand['equity']/100) * pot_size) - ((1 - (hand['equity']/100)) * bet_size)
        
        # Calculate total equity = Total Equity = (FE*HE)+HE
        #= (((100 - (hand.equity / 100)) * hand.equity) + hand.equity)
        total_equity = ( ( (1 -  (hand['equity']/100)  )  * (hand['equity']/100)) + (hand['equity'])/100)
        
        
        # Calculate equity realizations  realization = EV / (Equity * Pot)
        opponent_equity_realization = ev_value/(total_equity*total_opponent_pot)   #   (original_ev / (((100- (hand['equity']/100)) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (total_opponent_pot)   ##  (original_ev / (((100 - hand['equity']) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (total_opponent_pot)
        your_equity_realization =  ev_value/(total_equity*total_pot) ## (original_ev / (((100- (hand['equity']/100)) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (total_pot) ## #(original_ev / (((100 - hand['equity']) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (total_pot)
        diff_yours_vs_opponent = your_equity_realization - opponent_equity_realization
        diff_opponent_vs_yours = opponent_equity_realization - your_equity_realization
        


        return render_template('ev_hand_detail.html',
                               hand=hand,
                               original_ev=original_ev,
                               pot_odds=pot_odds,
                               opponent_pot_odds=opponent_pot_odds,
                               your_pot_size=pot_size,
                               your_bet_size=bet_size,
                               opponent_pot_size=opponent_pot_size,
                               opponent_bet_size=opponent_bet_size,
                               opponent_equity_realization=round(opponent_equity_realization, 2),
                               your_equity_realization=round(your_equity_realization, 2),
                               diff_yours_vs_opponent=round(diff_yours_vs_opponent, 2),
                               total_equity=round(total_equity, 2),
                               ev_value=round(ev_value, 2),
                               diff_opponent_vs_yours = round(diff_opponent_vs_yours, 2)
                               )
    else:
        return "Hand not found", 404

@app.route('/ev_hand_table', methods=['GET', 'POST'])
def ev_hand_table():
    global hands_data_2
    advertised_pot_odds = None
    pot_odds_percentage = None
    opponent_range = None
    opponent_range_hands = None
    opponent_range_formatted = ""
    opponent_range_equity = ""
    opponent_counter_range_ev = ""
    combined_range_ev_formatted = ""
    complement_combined_range_ev = ""

    # Set default values if not present in session
    if 'pot_size' not in session:
        session['pot_size'] = 6
    if 'bet_size' not in session:
        session['bet_size'] = 12
    if 'opponent_pot_size' not in session:
        session['opponent_pot_size'] = session['pot_size'] + session['bet_size']
    if 'opponent_bet_size' not in session:
        session['opponent_bet_size'] = 18
    if 'factor' not in session:
        session['factor'] = 1.75
    if 'reraise_factor' not in session:
        session['reraise_factor'] = .5

    pot_size = session['pot_size']
    bet_size = session['bet_size']
    opponent_pot_size = session['opponent_pot_size']
    opponent_bet_size = session['opponent_bet_size']
    factor = session['factor']
    reraise_factor = session['reraise_factor']

    if request.method == 'POST':
        if 'reset_ev' in request.form:
            hands_data_2 = copy.deepcopy(default_hands_data)
            # Reset to default values
            session['pot_size'] = 6
            session['bet_size'] = 12
            session['opponent_pot_size'] = session['pot_size'] + session['bet_size']
            session['opponent_bet_size'] = session['opponent_pot_size']
            session['factor'] = 1.75
            session['reraise_factor'] = .5
        else:
            pot_size = float(request.form.get('pot_size', pot_size))
            factor = float(request.form.get('factor', factor))
            reraise_factor = float(request.form.get('reraise_factor', reraise_factor))

            # Update bet_size based on the equation
            bet_size = round(pot_size * (((pot_size * factor) / pot_size) ** (1/3)), 0)
            # Update opponent_pot_size and opponent_bet_size based on the equations
            opponent_pot_size = round(pot_size + bet_size, 2)
            opponent_bet_size = round(opponent_pot_size * (((pot_size * reraise_factor) / opponent_pot_size) ** (1/3)), 0)

            session['pot_size'] = pot_size
            session['bet_size'] = bet_size
            session['factor'] = factor
            session['reraise_factor'] = reraise_factor
            session['opponent_pot_size'] = opponent_pot_size
            session['opponent_bet_size'] = opponent_bet_size
            
            if 'update_ev' in request.form:
                for hand in hands_data_2:
                    equity = hand['equity']
                    win_percentage = equity / 100
                    loss_percentage = 1 - win_percentage
                    ev_value = (win_percentage * pot_size) - (loss_percentage * bet_size)
                    hand['ev'] = round(ev_value * 100)  # Multiply by 100 for color coding 

            elif 'calculate_opp_pot_odds' in request.form:
                opponent_bet = float(request.form.get('opponent_bet', opponent_bet_size))
                session['opponent_bet_size'] = opponent_bet
                session['opponent_pot_size'] = pot_size + bet_size

                total_pot = pot_size + opponent_bet
                advertised_pot_odds = total_pot / opponent_bet
                pot_odds_percentage = (1 / advertised_pot_odds) * 100

                opponent_range = determine_opponents_range(opponent_bet, pot_size, hands_data_2)
                opponent_range_hands = {hand: hands_data_2[i]['ev'] for i, hand in enumerate(opponent_range)}
                opponent_range_formatted = ', '.join([f"{hand}:{hands_data_2[i]['ev']/100:.2f}" for i, hand in enumerate(opponent_range)])
                opponent_range_equity = ', '.join([f"{hand}:{hands_data_2[i]['equity']/100:.2f}" for i, hand in enumerate(opponent_range)])
                counter_range_hands_ev = calculate_counter_range_ev(hands_data_2, opponent_range)
                opponent_counter_range_ev = ', '.join([f"{hand}:{ev:.2f}" for hand, ev in counter_range_hands_ev.items()])
                combined_range_ev = merge_ranges(opponent_range_hands, counter_range_hands_ev)
                combined_range_ev_formatted = ', '.join([f"{hand}:{ev:.2f}" for hand, ev in combined_range_ev.items()])
                complement_combined_range_ev = calculate_complement_combined_range(combined_range_ev)

    return render_template('ev_hand_table.html',
                           hands=hands_data_2,
                           advertised_pot_odds=advertised_pot_odds,
                           pot_odds_percentage=pot_odds_percentage,
                           opponent_range=opponent_range_formatted,
                           opponent_range_equity=opponent_range_equity,
                           opponent_counter_range_ev=opponent_counter_range_ev,
                           combined_range_ev=combined_range_ev_formatted,
                           complement_combined_range_ev=complement_combined_range_ev,
                           opponent_range_hands=opponent_range_hands,
                           factor=factor,
                           pot_size=pot_size,
                           bet_size=bet_size,
                           reraise_factor=reraise_factor,
                           opponent_pot_size=opponent_pot_size,
                           opponent_bet_size=opponent_bet_size)

    
    
def calculate_counter_range_ev(hands_data, opponent_range):
    counter_range = {}
    for hand in hands_data:
        if hand['hand'] not in opponent_range:
            counter_range[hand['hand']] = 1 - (hand['ev'] / 100)  # Using 1 - EV for counter range
    return counter_range

def merge_ranges(opponent_range, counter_range):
    combined_range = {**opponent_range, **counter_range}
    return combined_range

def calculate_complement_combined_range(combined_range):
    complement_range = {}
    for hand, ev in combined_range.items():
        if ev > 1:
            complement_range[hand] = 1 - (ev / 100)
        else:
            complement_range[hand] = ev - 1
    return ', '.join([f"{hand}:{ev:.2f}" for hand, ev in complement_range.items()])


def merge_ranges(opponent_range, counter_range):
    combined_range = {**opponent_range, **counter_range}
    return combined_range

def calculate_complement_combined_range(combined_range):
    complement_range = {}
    for hand, ev in combined_range.items():
        if ev > 1:
            complement_range[hand] = 1 - (ev / 100)
        else:
            complement_range[hand] =  1-ev
    return ', '.join([f"{hand}:{ev:.2f}" for hand, ev in complement_range.items()])


def get_hand_data2(hand_name):
    for hand in hands_data_2:
        if hand["hand"] == hand_name:
            return hand
    return None


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
#def determine_opponents_range(opponent_bet, total_pot, hands_data):
#    opponent_range = []
#    advertised_equity = opponent_bet / (opponent_bet + total_pot)
#    for hand in hands_data:
#        if hand['equity'] >= advertised_equity * 100:
#            opponent_range.append(hand['hand'])
#    return opponent_range
#    
#@app.route('/ev_hand/<hand_name>')
#def ev_hand_detail(hand_name):
#    hand = get_hand_data2(hand_name)
#    if hand:
#        original_ev = hand['ev'] / 100
#
#        # Retrieve pot size and bet size from session
#        pot_size = session.get('pot_size', 0)
#        bet_size = session.get('bet_size', 0)
#
#        total_pot = pot_size + bet_size
#        pot_odds = (bet_size / total_pot) * 100 if total_pot > 0 else 0
#
#        # Set default values if not present in session
#        opponent_pot_size = session.get('opponent_pot_size', 0)
#        opponent_bet_size = session.get('opponent_bet_size', 0)
#
#        # Calculate advertised pot odds for opponent's bet
#        total_opponent_pot = opponent_pot_size + opponent_bet_size
#        opponent_pot_odds = (opponent_bet_size / total_opponent_pot) * 100 if total_opponent_pot > 0 else 0
#        
#
#        # Calculate equity realizations
#        opponent_equity_realization = (original_ev * 100 / (((100 - hand['equity']) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (opponent_pot_size + opponent_bet_size)
#        your_equity_realization = (original_ev * 100 / (((100 - hand['equity']) * (hand['equity'] / 100)) + (hand['equity'] / 100))) * (pot_size + bet_size)
#        diff_yours_vs_opponent = your_equity_realization - opponent_equity_realization
#        #diff_opponent_vs_yours = opponent_equity_realization * your_equity_realization
#        
#        # Calculate total equity
#        total_equity = (((100 - hand['equity']) * (hand['equity'] / 100)) + (hand['equity'] / 100))
#        
#        
#        # Calculate EV
#        ev_value = ((hand['equity']/100) * pot_size) - ((1 - (hand['equity']/100)) * bet_size)
#
#        return render_template('ev_hand_detail.html',
#                               hand=hand,
#                               original_ev=original_ev,
#                               pot_odds=pot_odds,
#                               opponent_pot_odds=opponent_pot_odds,
#                               your_pot_size=pot_size,
#                               your_bet_size=bet_size,
#                               opponent_pot_size=opponent_pot_size,
#                               opponent_bet_size=opponent_bet_size,
#                               opponent_equity_realization=round(opponent_equity_realization, 2),
#                               your_equity_realization=round(your_equity_realization, 2),
#                               diff_yours_vs_opponent=round(diff_yours_vs_opponent, 2),
#                               total_equity=round(total_equity, 2),
#                               ev_value=round(ev_value, 2)
#                               #diff_opponent_vs_yours = round(diff_opponent_vs_yours, 2)
#                               )
#    else:
#        return "Hand not found", 404
#
#
#
#@app.route('/ev_hand_table', methods=['GET', 'POST'])
#def ev_hand_table():
#    global hands_data_2
#    advertised_pot_odds = None
#    pot_odds_percentage = None
#    opponent_range = None
#    opponent_range_hands = None
#    opponent_range_formatted = ""
#    opponent_range_equity = ""
#    opponent_counter_range_equity = ""
#    opponent_counter_range_ev = ""
#    combined_range_ev_formatted = ""
#    complement_combined_range_ev = ""
#
#    # Set default values if not present in session
#    if 'pot_size' not in session:
#        session['pot_size'] = 2
#    if 'bet_size' not in session:
#        session['bet_size'] = 1
#    if 'opponent_pot_size' not in session:
#        session['opponent_pot_size'] = session['pot_size'] + session['bet_size']
#    if 'opponent_bet_size' not in session:
#        session['opponent_bet_size'] = 3
#
#    pot_size = session['pot_size']
#    bet_size = session['bet_size']
#    opponent_pot_size = session['opponent_pot_size']
#    opponent_bet_size = session['opponent_bet_size']
#
#    if request.method == 'POST':
#        pot_size = float(request.form.get('pot_size', 3))
#        bet_size = float(request.form.get('bet_size', 1))
#        session['pot_size'] = pot_size
#        session['bet_size'] = bet_size
#
#        if 'reset_ev' in request.form:
#            hands_data_2 = copy.deepcopy(default_hands_data)
#            # Reset to default values
#            session['pot_size'] = 2
#            session['bet_size'] =  1 #round(session['pot_size']*((140/session['pot_size'] )**(1/3)),0)#round(session['pot_size']*(((pot_size*5)/pot_size)**(1/3)),0)
#            session['opponent_pot_size'] = session['pot_size'] + session['bet_size'] 
#            session['opponent_bet_size'] =   session['opponent_pot_size'] #round((session['opponent_pot_size']*((140/session['pot_size'] )**1/3)),0)
#            
#        elif 'update_ev' in request.form:
#            for hand in hands_data_2:
#                equity = hand['equity']
#                win_percentage = equity / 100
#                loss_percentage = 1 - win_percentage
#                ev_value = (win_percentage * pot_size) - (loss_percentage * bet_size)
#                hand['ev'] = round(ev_value * 100)  # Multiply by 100 for color coding
#
#        elif 'calculate_opp_pot_odds' in request.form:
#            opponent_bet = float(request.form.get('opponent_bet', 5))
#            session['opponent_bet_size'] = opponent_bet
#            session['opponent_pot_size'] = pot_size + bet_size  # Use the current values directly
#
#            # Calculate advertised pot odds
#            total_pot = pot_size + opponent_bet
#            advertised_pot_odds = total_pot / opponent_bet
#            pot_odds_percentage = (1 / advertised_pot_odds) * 100
#            # Determine opponent's range based on equity
#            opponent_range = determine_opponents_range(opponent_bet, pot_size, hands_data_2)
#            # Create a dictionary for the opponent's range hands for color coding
#            opponent_range_hands = {hand: hands_data_2[i]['ev'] for i, hand in enumerate(opponent_range)}
#            # Format opponent's range with EV values
#            opponent_range_formatted = ', '.join([f"{hand}:{hands_data_2[i]['ev']/100:.2f}" for i, hand in enumerate(opponent_range)])
#            # Format opponent's range with equity values
#            opponent_range_equity = ', '.join([f"{hand}:{hands_data_2[i]['equity']/100:.2f}" for i, hand in enumerate(opponent_range)])
#            # Calculate counter range based on hands that are not in the opponent's range
#            counter_range_hands_ev = calculate_counter_range_ev(hands_data_2, opponent_range)
#            opponent_counter_range_ev = ', '.join([f"{hand}:{ev:.2f}" for hand, ev in counter_range_hands_ev.items()])
#            # Combine opponent's range and counter range
#            combined_range_ev = merge_ranges(opponent_range_hands, counter_range_hands_ev)
#            combined_range_ev_formatted = ', '.join([f"{hand}:{ev:.2f}" for hand, ev in combined_range_ev.items()])
#            # Calculate the complement of the combined range
#            complement_combined_range_ev = calculate_complement_combined_range(combined_range_ev)
#
#    return render_template('ev_hand_table.html', 
#                           hands=hands_data_2, 
#                           advertised_pot_odds=advertised_pot_odds, 
#                           pot_odds_percentage=pot_odds_percentage, 
#                           opponent_range=opponent_range_formatted, 
#                           opponent_range_equity=opponent_range_equity, 
#                           opponent_counter_range_equity=opponent_counter_range_equity, 
#                           opponent_counter_range_ev=opponent_counter_range_ev, 
#                           combined_range_ev=combined_range_ev_formatted, 
#                           complement_combined_range_ev=complement_combined_range_ev, 
#                           opponent_range_hands=opponent_range_hands, 
#                           pot_size= 2,#session['pot_size'],  # Ensure correct value passed
#                           bet_size= 1,#session['bet_size'],  # Ensure correct value passed
#                           opponent_pot_size= 3,#session['opponent_pot_size'],  # Ensure correct value passed
#                           opponent_bet_size=2)#session['opponent_bet_size'])  # Ensure correct value passed
#
#
#
#
#
#def calculate_counter_range_ev(hands_data, opponent_range):
#    counter_range = {}
#    for hand in hands_data:
#        if hand['hand'] not in opponent_range:
#            counter_range[hand['hand']] = 1 - (hand['ev'] / 100)  # Using 1 - EV for counter range
#    return counter_range
#
#def merge_ranges(opponent_range, counter_range):
#    combined_range = {**opponent_range, **counter_range}
#    return combined_range
#
#def calculate_complement_combined_range(combined_range):
#    complement_range = {}
#    for hand, ev in combined_range.items():
#        if ev > 1:
#            complement_range[hand] = 1 - (ev / 100)
#        else:
#            complement_range[hand] = ev - 1
#    return ', '.join([f"{hand}:{ev:.2f}" for hand, ev in complement_range.items()])
#
#
#def merge_ranges(opponent_range, counter_range):
#    combined_range = {**opponent_range, **counter_range}
#    return combined_range
#
#def calculate_complement_combined_range(combined_range):
#    complement_range = {}
#    for hand, ev in combined_range.items():
#        if ev > 1:
#            complement_range[hand] = 1 - (ev / 100)
#        else:
#            complement_range[hand] =  1-ev
#    return ', '.join([f"{hand}:{ev:.2f}" for hand, ev in complement_range.items()])
#
#
#def get_hand_data2(hand_name):
#    for hand in hands_data_2:
#        if hand["hand"] == hand_name:
#            return hand
#    return None