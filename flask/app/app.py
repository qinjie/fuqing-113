from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.environ['API_HOST']
API_PORT = os.environ['API_PORT']

# Define the base URL of your RESTful API
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def display_pictures():
    # Create a list of image URLs or file paths
    image_urls = [
        'day1.png',
        'day2.png',
        'day3.png',
        # Add more image URLs or file paths here
    ]
    
    return render_template('index.html', image_urls=image_urls)

@app.route('/guest', methods=['GET', 'POST'])
def index_guest():
    guests = []  # Initialize an empty list to store search results

    if request.method == 'POST':
        pattern = request.form['search_pattern']
        # Make a GET request to the API search endpoint
        response = requests.get(f"{API_BASE_URL}/guest/search/{pattern}")
        if response.status_code == 200:
            guests = response.json()['data']

    return render_template('guest_index.html', guests=guests, pattern=request.form.get('search_pattern', ''))

@app.route('/guest/create', methods=['GET', 'POST'])
def create_guest():
    if request.method == 'POST':
        # Create a new guest by making a POST request to the API
        data = {
            'full_name': request.form['full_name'],
            'alt_name': request.form['alt_name'],
            'salute': request.form['salute'],
            'title': request.form['title'],
            'organization': request.form['organization'],
            'country': request.form['country'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'details': request.form['details']
        }
        response = requests.post(f"{API_BASE_URL}/guest", json=data)
        if response.status_code == 201:
            flash('Guest created successfully', 'success')
            return redirect(url_for('index_guest'))
        else:
            flash('Failed to create guest', 'error')

    return render_template('guest_create.html')

@app.route('/guest/view/<int:guest_id>')
def view_guest(guest_id):
    # Retrieve guest details from the API
    response = requests.get(f"{API_BASE_URL}/guest/{guest_id}")
    app.logger.debug(response.json())
    guest = response.json()['data']
    if 'error' in guest:
        flash('Guest not found', 'error')
        return redirect(url_for('index_guest'))

    return render_template('guest_view.html', guest=guest)

@app.route('/guest/hash/<string:hash>')
def view_guest_by_hash(hash):
    # Retrieve guest details from the API
    response = requests.get(f"{API_BASE_URL}/guest/hash/{hash}")
    app.logger.debug(response.json())
    guest = response.json()['data']
    if 'error' in guest:
        flash('Guest not found', 'error')
        return redirect(url_for('index_guest'))

    return render_template('guest_view.html', guest=guest)


@app.route('/guest/edit/<int:guest_id>', methods=['GET', 'POST'])
def edit_guest(guest_id):
    # Retrieve guest details from the API
    response = requests.get(f"{API_BASE_URL}/guest/{guest_id}")
    app.logger.debug(response.json())
    guest = response.json()['data']
    if 'error' in guest:
        flash('Guest not found', 'error')
        return redirect(url_for('index_guest'))

    if request.method == 'POST':
        # Update the guest details by making a PUT request to the API
        data = {
            'id': guest_id,
            'full_name': request.form['full_name'],
            'alt_name': request.form['alt_name'],
            'salute': request.form['salute'],
            'title': request.form['title'],
            'organization': request.form['organization'],
            'country': request.form['country'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'details': request.form['details']
        }
        response = requests.put(f"{API_BASE_URL}/guest/update", json=data)
        app.logger.debug(response.text)
        if response.status_code == 200:
            flash('Guest updated successfully', 'success')
            return redirect(url_for('view_guest', guest_id=guest_id))
        else:
            flash('Failed to update guest', 'error')

    return render_template('guest_edit.html', guest=guest)

@app.route('/guest/delete/<int:guest_id>', methods=['POST'])
def delete_guest(guest_id):
    # Delete the guest by making a DELETE request to the API
    response = requests.delete(f"{API_BASE_URL}/guest/{guest_id}")
    app.logger.debug(response.text)
    if response.status_code == 200:
        flash('Guest deleted successfully', 'success')
    else:
        flash('Failed to delete guest', 'error')

    return redirect(url_for('index_guest'))


if __name__ == '__main__':
    app.run(debug=True)
